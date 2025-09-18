#!/usr/bin/env python3
"""
Debug script to see exactly what's being parsed
"""

import sys
import os
sys.path.append(os.getcwd())

import re

def debug_parse_tool_call_safely(tool_call: str):
    """Debug version to see what's happening"""
    
    func_name = tool_call.split('(', 1)[0].strip()
    args_str = tool_call.split('(', 1)[1][:-1].strip()
    
    print(f"Function: {func_name}")
    print(f"Args string: '{args_str}'")
    
    # Simple regex-based parsing for basic cases
    arg_pattern = r"(\w+)\s*=\s*(?:'([^']*)'|\"([^\"]*)\"|([^\s,)]+))"
    matches = re.findall(arg_pattern, args_str)
    
    print(f"Regex matches: {matches}")
    
    args_dict = {}
    for match in matches:
        key = match[0]
        # Use whichever capture group has content
        value = match[1] or match[2] or match[3]
        print(f"  Key: '{key}', Raw value: '{value}'")
        
        # Try to convert numeric values
        if value.isdigit():
            print(f"    Converting to int: {int(value)}")
            value = int(value)
        elif '.' in value:
            print(f"    Has dot, count: {value.count('.')}")
            if value.count('.') == 1:
                parts = value.split('.')
                print(f"    Parts: {parts}")
                if len(parts) == 2 and all(part.isdigit() for part in parts):
                    print(f"    Converting to float: {float(value)}")
                    value = float(value)
        
        args_dict[key] = value
        
    return func_name, args_dict

if __name__ == "__main__":
    test_case = "function_with_number(count=42, rate=3.14)"
    print(f"Testing: {test_case}")
    func_name, args = debug_parse_tool_call_safely(test_case)
    print(f"Result: {func_name}, {args}")