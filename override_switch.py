# Helper class and instance from ComfyUI-LogicUtils/autonode.py
# to mimic their generic type handling
class AllTrue(str):
    def __init__(self, representation=None) -> None:
        self.repr = representation
        pass
    def __ne__(self, __value: object) -> bool:
        return False
    def __instancecheck__(self, instance):
        return True
    def __subclasscheck__(self, subclass):
        return True
    def __bool__(self):
        return True
    def __str__(self):
        return self.repr or "*"
    def __jsonencode__(self):
        return self.repr or "*"
    def __repr__(self) -> str:
        return self.repr or "*"
    def __eq__(self, __value: object) -> bool:
        return True
anytype = AllTrue("*")

class OverrideSwitch:
    """
    A node that switches between two inputs based on a boolean condition.
    - Uses custom 'anytype' for generic typing for broad compatibility.
    - Inputs 'condition', 'true_input', and 'false_input' are optional.
    - A 'Default_Input' widget (True/False) determines which input (true_input or false_input respectively)
      is used if the 'condition' input is not provided.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            # Add widget to control default behavior when condition is missing
            "required": {
                 "Default_Input": ("BOOLEAN", {"default": False}), # Changed default to False
            },
            "optional": {
                "condition": (anytype, {}), # Optional condition
                "true_input": (anytype, {}), # Input if condition is True
                "false_input": (anytype, {}), # Input if condition is False
            }
        }
    
    # RETURN_TYPES still uses anytype
    RETURN_TYPES = (anytype,)
    RETURN_NAMES = ("output",)
    FUNCTION = "switch"
    CATEGORY = "logic"

    # Adjust logic for the new default behavior control
    def switch(self, Default_Input, condition=None, true_input=None, false_input=None): # Renamed parameter
        # If condition is not provided or None, use the Default_Input setting
        if condition is None:
            if Default_Input: # Use renamed parameter
                # Defaulting to true_input (return None if true_input is missing)
                return (true_input,)
            else:
                # Defaulting to false_input (return None if false_input is missing)
                return (false_input,)
        
        # --- Condition is provided (True or False), proceed with normal logic --- 
            
        # If true_input is missing and condition is True, use false_input
        if condition and true_input is None:
             # If false_input is also None, output actual None
            return (false_input if false_input is not None else None,)
            
        # If false_input is missing and condition is False, return None (as per original Goals.md#3)
        if not condition and false_input is None:
             return (None,)
            
        # Normal switch behavior (inputs are present or handled above)
        selected_output = true_input if condition else false_input
        return (selected_output,)

# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "OverrideSwitch": OverrideSwitch
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "OverrideSwitch": "Override Switch"
} 