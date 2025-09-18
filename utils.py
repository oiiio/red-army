"""
Utility functions for the Red Army system.
"""
import re
import ast

def parse_tool_call_safely(tool_call: str) -> tuple[str, dict]:
    """
    Safely parse a tool call string into function name and arguments.
    
    Args:
        tool_call: String like "function_name(arg1='value1', arg2='value2')"
        
    Returns:
        tuple: (function_name, args_dict)
        
    Raises:
        ValueError: If the tool call cannot be parsed or has invalid arguments
    """
    # Extract function name and arguments
    if '(' not in tool_call or not tool_call.endswith(')'):
        raise ValueError(f"Invalid tool call format: {tool_call}")
    
    func_name = tool_call.split('(', 1)[0].strip()
    args_str = tool_call.split('(', 1)[1][:-1].strip()
    
    # If no arguments, return empty dict
    if not args_str:
        return func_name, {}
    
    # Check for placeholder values (anything in angle brackets)
    if re.search(r'<[^>]+>', args_str):
        raise ValueError(f"Tool call contains unresolved placeholders: {tool_call}")
    
    # Try to parse arguments safely
    try:
        # Build a safe dictionary string and evaluate it
        # This handles quoted strings and basic values
        args_dict = {}
        
        # Simple regex-based parsing for basic cases
        # Matches patterns like arg='value' or arg="value" or arg=123
        arg_pattern = r"(\w+)\s*=\s*(?:'([^']*)'|\"([^\"]*)\"|(\w+))"
        matches = re.findall(arg_pattern, args_str)
        
        for match in matches:
            key = match[0]
            # Use whichever capture group has content
            value = match[1] or match[2] or match[3]
            
            # Try to convert numeric values
            if value.isdigit():
                value = int(value)
            elif value.replace('.', '').isdigit():
                value = float(value)
            
            args_dict[key] = value
        
        return func_name, args_dict
        
    except Exception as e:
        raise ValueError(f"Failed to parse tool call arguments in '{tool_call}': {e}")

def has_unresolved_placeholders(tool_call: str) -> bool:
    """Check if a tool call has unresolved placeholder values like <placeholder>."""
    return bool(re.search(r'<[^>]+>', tool_call))