#!/usr/bin/env python3
"""
Test script for the reporter.py agent node
"""

import sys
import os
sys.path.append(os.getcwd())

from agents.reporter import reporting_node
from state import RedArmyState

def test_reporting_node():
    """Test the reporting node with sample RedArmyState data"""
    print("🧪 Testing Reporter Node...")
    
    # Create a sample RedArmyState with realistic mission data
    sample_state: RedArmyState = {
        "objective": "Penetration test of industrial SCADA network to evaluate security posture",
        "plan": [
            {"description": "Network reconnaissance", "tool_call": "scan_network_for_plcs"},
            {"description": "Exploit PLC vulnerabilities", "tool_call": "craft_modbus_exploit_packet"},
            {"description": "Analyze detection logs", "tool_call": "analyze_gridguardian_logs"}
        ],
        "current_task_index": 3,  # All tasks completed
        "task_output": "Final task completed successfully",
        "feedback": "MIXED SUCCESS: Successfully exploited PLC but some attacks were detected by monitoring systems. Network security shows both vulnerabilities and effective detection capabilities.",
        "history": [
            "Commander: Initialized mission with 3-phase attack plan",
            "Infiltrator: scan_network_for_plcs -> Found 2 PLCs at 192.168.1.100 and 192.168.1.101",
            "Saboteur: craft_modbus_exploit_packet -> Created stealthy Modbus payload targeting function code 16",
            "Executioner: execute_plc_attack -> Successfully sent malicious commands to PLC, safety systems bypassed",
            "Chronicler: analyze_gridguardian_logs -> FAILURE detected - 3 anomaly alerts generated during attack window"
        ],
        "revision_number": 1
    }
    
    print("Sample state data:")
    print(f"Objective: {sample_state['objective']}")
    print(f"Tasks completed: {sample_state['current_task_index']}/{len(sample_state['plan'])}")
    print(f"History entries: {len(sample_state['history'])}")
    print(f"Final feedback: {sample_state['feedback'][:60]}...")
    
    try:
        print("\n" + "="*60)
        print("TESTING reporting_node function...")
        print("="*60)
        
        # Execute the reporting node
        result = reporting_node(sample_state)
        
        print("\n📋 REPORTING NODE RESULT:")
        print(f"Task Output Length: {len(result['task_output'])} characters")
        print(f"Feedback: {result['feedback']}")
        print(f"History Update: {result['history'][0] if result['history'] else 'None'}")
        print(f"Current Task Index: {result['current_task_index']}")
        
        # Verify the result contains expected elements
        if "MISSION AFTER-ACTION REPORT" in result['task_output']:
            print("\n✅ Report contains proper header structure")
        else:
            print("\n❌ Missing expected report header")
            
        if "Mission Objective" in result['task_output'] and "Key Findings" in result['task_output']:
            print("✅ Report contains required sections")
        else:
            print("❌ Missing required report sections")
        
        print("\n✅ Testing completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reporting_node()