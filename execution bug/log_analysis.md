## Update based on Full Logs

After reviewing the complete logs provided:

### Why the node "silently failed" during our fixes:
The logs revealed this error during workflow validation:
`Return type mismatch between linked nodes: condition, received_type(BOOL) mismatch input_type(BOOLEAN)`
When I changed the `condition` input from `anytype` to strict `BOOLEAN`, ComfyUI's validator rejected the graph because the upstream node outputs `BOOL` (ComfyUI is very pedantic about type string names). This caused the workflow to silently abort before execution even began. **This confirms that changing `anytype` to a strict type in this generic switch is dangerous and causes validation blocks.**

### Why the original workflow crashes on Run 1 but succeeds on Run 2:
The log proves that the crash happens deep inside the HuggingFace `transformers` library (`depth_estimation.py`), specifically when it tries to convert a `bfloat16` tensor to a NumPy array. NumPy does not support `bfloat16`. 

**The False Assumption:** 
We originally assumed the switch was outputting `None` or "null" on the first run. This is **false**. If the switch outputted `None`, the `DepthAnything` preprocessor would have crashed immediately when trying to read the image's dimensions, long before it reached the neural network pipeline. 

**The Real Cause:**
The switch is successfully passing a valid image tensor. However, the ComfyUI environment (likely due to loading the FLUX model) has set the PyTorch default precision to `bfloat16`. `DepthAnything` processes the image and attempts to output its depth map in `bfloat16`, which instantly crashes NumPy.

**Why does it work on the second run?**
ComfyUI's node execution order and environment state shifts. By the time the second run occurs, the environment's default tensor type has likely been reset to `float32` by another node that finished executing at the end of the first run (or ComfyUI pulls a cached `float32` version of the tensor). This allows `DepthAnything` to process the image in standard precision without crashing.

**Conclusion:**
The `OverrideSwitch` is completely innocent. It routes exactly what it receives. The bug is entirely a precision handling issue between the FLUX workflow environment and the `DepthAnything` preprocessor. Any attempt to intercept and fix this inside the `OverrideSwitch`'s code is outside the scope of a generic routing node and leads to structural execution crashes (as seen in our tuple-conversion attempt).