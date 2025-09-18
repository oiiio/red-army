#!/usr/bin/env python3
"""
Test script to verify the fixed tool call parsing
"""

import sys
import os
sys.path.append(os.getcwd())

from utils import parse_tool_call_safely

def test_tool_call_parsing():
    """Test the parsing of tool calls with various argument types"""
    print("🧪 Testing Tool Call Parsing Fix...")
    
    test_cases = [
        # The problematic case that was failing
        "execute_attack_scenario(target_ip='192.168.1.100', scenario_name='Stealth Bypass')",
        
        # Other test cases to ensure we didn't break anything
        "scan_network_for_plcs(subnet='192.168.1.0/24')",
        "craft_modbus_exploit_packet(function_code=16, data='test')",
        "analyze_gridguardian_logs(attack_start_time='2025-09-18T18:50:00', attack_duration_minutes=60)",
        "simple_function()",
        "function_with_number(count=42, rate=3.14)",
    ]
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case}")
        
        try:
            func_name, args = parse_tool_call_safely(test_case)
            print(f"✅ SUCCESS:")
            print(f"   Function: {func_name}")
            print(f"   Args: {args}")
            
            # Verify specific expectations for the problematic case
            if "target_ip" in args:
                if isinstance(args["target_ip"], str) and args["target_ip"] == "192.168.1.100":
                    print("   ✅ IP address correctly parsed as string")
                else:
                    print(f"   ❌ IP address parsing issue: got {args['target_ip']} ({type(args['target_ip'])})")
                    
        except Exception as e:
            print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    test_tool_call_parsing()