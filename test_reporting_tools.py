#!/usr/bin/env python3
"""
Test script for the reporting_tools.py toolkit
"""

import sys
import os
sys.path.append(os.getcwd())

from toolkits.reporting_tools import generate_mission_debrief, save_mission_report

def test_reporting_tools():
    """Test the mission debrief generation with sample data"""
    print("🧪 Testing Mission Debrief Tool...")
    
    # Sample mission data that might come from a RedArmyState
    sample_history = [
        "Commander initialized mission with objective: Test SCADA system security",
        "Infiltrator scanned target network and identified PLC at 192.168.1.100",
        "Saboteur executed modbus_anomaly_injection attack vector",
        "Executioner attempted direct manipulation of safety systems", 
        "Chronicler detected anomaly alerts in GridGuardian logs",
        "Mission completed with mixed results"
    ]
    
    sample_feedback = "PARTIAL SUCCESS - Attack vectors were executed successfully but some were detected by monitoring systems. Demonstrates both vulnerabilities and effective monitoring capabilities."
    
    sample_objective = "Evaluate SCADA system security posture and monitoring effectiveness"
    
    print("Sample mission data:")
    print(f"Objective: {sample_objective}")
    print(f"History entries: {len(sample_history)}")
    print(f"Final feedback: {sample_feedback[:50]}...")
    
    try:
        # Test the main debrief generation tool
        print("\n" + "="*60)
        print("TESTING generate_mission_debrief tool...")
        print("="*60)
        
        report = generate_mission_debrief.invoke({
            "history": sample_history,
            "feedback": sample_feedback,
            "objective": sample_objective
        })
        
        # Test the save functionality
        print("\n" + "="*60)
        print("TESTING save_mission_report tool...")
        print("="*60)
        
        save_result = save_mission_report.invoke({
            "report": report, 
            "filename": "test_mission_report.md"
        })
        print(save_result)
        
        print("\n✅ Testing completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reporting_tools()