# ComfyUI Override Switch

A custom node for ComfyUI that provides a switch with override behavior. This node allows you to switch between two inputs based on a boolean condition, with graceful handling of missing inputs.

## Features

- Optional boolean condition input (defaults to False if not provided)
- Handles missing inputs gracefully
- Works with any input type
- Clear and intuitive interface

## Installation

1. Navigate to your ComfyUI's `custom_nodes` directory
2. Clone this repository:
```bash
git clone https://github.com/SpaceWarpStudio/ComfyUI-OverrideSwitch.git
```
3. Install the node:
```bash
cd ComfyUI-OverrideSwitch
pip install -e .
```

## Usage

The node has three optional inputs:
- `condition`: Boolean input that determines which input to use
- `true_input`: Input to use when condition is True
- `false_input`: Input to use when condition is False

Default behaviors:
- If condition is not provided or None: defaults to False
- If true_input is missing and condition is True: uses false_input
- If false_input is missing and condition is False: returns None
- If both inputs are missing: returns None

## License

This project is licensed under the [MIT License](LICENSE).