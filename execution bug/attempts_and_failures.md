# Execution Bug - Attempts and Failures

## The Original Problem
When running the `Flux2_Master_02.03.26_Updating_03.json` workflow:
1. First run: The workflow throws a `TypeError: Got unsupported ScalarType BFloat16` originating from the `DepthAnythingPreprocessor`.
2. Second run: The workflow runs successfully without any changes.

The crash always occurs in a node that comes directly after the custom `OverrideSwitch` node.

## Attempt 1: Restricting the `condition` input type
**Assumption:** The error could be caused by a tensor being plugged into the `condition` socket, bypassing python truthiness or acting unexpectedly.
**Action:** Changed `condition` from `anytype` to `("BOOLEAN", {"forceInput": True})`.
**Result:** This was meant to ensure only booleans were processed as conditions. However, it didn't solve the underlying crash related to `BFloat16` and the second run still worked.

## Attempt 2: Forcing upstream node evaluation by changing `optional` inputs to `required`
**Assumption:** ComfyUI uses lazy evaluation. Since `true_input` and `false_input` were marked as `optional` in `INPUT_TYPES`, I assumed ComfyUI evaluated the `OverrideSwitch` *before* the upstream nodes connected to those sockets finished generating data. This would mean `None` was passed into `DepthAnything`, causing a crash on run 1. Then on run 2, the cached data was valid.
**Action:** Moved `true_input` and `false_input` from the `optional` block to the `required` block.
**Result:** **Failed.** This broke workflow validation entirely. ComfyUI blocked execution with errors like `Required input is missing: true_input` because in some states, not all sockets actually have connections until runtime. This change was immediately reverted.

## Attempt 3: Intercepting and converting `bfloat16` tensors to `float32`
**Assumption:** The `OverrideSwitch` was passing a `bfloat16` image tensor flawlessly (because of `anytype`), but the downstream `DepthAnything` node was crashing because `numpy` doesn't natively support `bfloat16`. I assumed converting the tensor to `float32` *inside* the `OverrideSwitch` before outputting would solve the preprocessor crash.
**Action:** Added `import torch` and type-checking logic at the end of the `switch` function:
```python
if isinstance(selected_output, torch.Tensor) and selected_output.dtype == torch.bfloat16:
    selected_output = selected_output.to(torch.float32)
```
**Result:** **Failed.** ComfyUI didn't crash with the `BFloat16` error, but it also didn't run. The logic failed to catch the tensor because ComfyUI often wraps images in batches (lists or tuples).

## Attempt 4: Recursive checking of tuples/lists for `bfloat16` conversion
**Assumption:** Since ComfyUI wraps images in tuples or lists, I assumed iterating through the wrapper and converting the `bfloat16` tensors inside it, then reconstructing the list/tuple would work.
**Action:** Expanded the type-checking logic to iterate through lists/tuples, convert tensors, and reconstruct the output container using dynamic typing and later explicit `tuple(new_output)`.
**Result:** **Failed.** The node silently crashed ComfyUI's execution phase before a stack trace could even be generated. This indicates that intercepting and rebuilding ComfyUI's internal data structures dynamically in this custom node causes catastrophic execution breaks. As a result, the workflow broke on *both* the first and second runs.

## Conclusion and Current State
- Intervening in the data payload's type or structure inside a node meant purely for generic routing (`anytype`) is highly unsafe and breaks ComfyUI.
- Forcing execution order via `required` inputs breaks workflows where connections are conditionally populated.
- All experimental changes have been reverted. The file `override_switch.py` is back to its original state. 
- The root cause is likely related to how ComfyUI caches/passes latent/image tensors generated in `bfloat16` by Flux models, but attempting to resolve this *inside* the `OverrideSwitch` node creates worse side effects.