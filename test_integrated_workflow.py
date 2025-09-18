#!/usr/bin/env python3
"""
Test script to verify the integrated reporting workflow
"""

import sys
import os
sys.path.append(os.getcwd())

def test_routing_logic():
    """Test the agent router with a completed mission state"""
    print("🧪 Testing Integrated Reporting Workflow...")
    
    # Import here to avoid loading issues
    from red_army import agent_router
    from state import RedArmyState
    
    # Create a completed mission state
    completed_state: RedArmyState = {
        "objective": "Test mission for routing verification",
        "plan": [
            {"agent": "infiltrator", "description": "Scan network", "tool_call": "scan_network_for_plcs"},
            {"agent": "saboteur", "description": "Create exploit", "tool_call": "craft_modbus_exploit_packet"}
        ],
        "current_task_index": 2,  # Plan is complete (index >= len(plan))
        "task_output": "Mission completed successfully",
        "feedback": "SUCCESS: All objectives achieved",
        "history": [
            "Commander: Created 2-task plan",
            "Infiltrator: Found target PLCs", 
            "Saboteur: Crafted exploit successfully"
        ],
        "revision_number": 1
    }
    
    # Test the router logic
    print(f"Mission plan has {len(completed_state['plan'])} tasks")
    print(f"Current task index: {completed_state['current_task_index']}")
    print(f"Mission feedback: {completed_state['feedback']}")
    
    try:
        print("\n" + "="*60)
        print("TESTING agent_router with completed mission...")
        print("="*60)
        
        next_node = agent_router(completed_state)
        
        print(f"\n📋 ROUTER RESULT: {next_node}")
        
        if next_node == "reporter":
            print("✅ SUCCESS: Router correctly directs to reporting node")
        else:
            print(f"❌ FAILURE: Expected 'reporter', got '{next_node}'")
            
        print("\n✅ Routing test completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_routing_logic()