#!/usr/bin/env python3
"""
Test script to simulate the infiltrator agent using the analyze_document tool.
"""

import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from state import RedArmyState
from agents.infiltrator import infiltrator_node
from utils import parse_tool_call_safely

def test_infiltrator_analyze_document():
    """Test the infiltrator agent with analyze_document tasks."""
    
    print("Testing Infiltrator Agent with analyze_document tool")
    print("=" * 60)
    
    # Create test tasks for the infiltrator agent
    test_tasks = [
        {
            "task": "Analyze the attack guide to find PLC information",
            "tool_call": "analyze_document(query='What PLC model is used in the system?')",
            "agent": "infiltrator"
        },
        {
            "task": "Find maintenance override commands", 
            "tool_call": "analyze_document(query='What are the Modbus commands for maintenance override?')",
            "agent": "infiltrator"
        },
        {
            "task": "Identify stealth attack methods",
            "tool_call": "analyze_document(query='What are the highest stealth level attack methods?')",
            "agent": "infiltrator"
        }
    ]
    
    for i, task in enumerate(test_tasks):
        print(f"\n{i+1}. Testing task: {task['task']}")
        print(f"   Tool call: {task['tool_call']}")
        print("-" * 60)
        
        # Create a minimal state for testing
        state = {
            "objective": "Test analyze_document functionality",
            "plan": test_tasks,
            "current_task_index": i,
            "task_output": "",
            "feedback": "",
            "history": [],
            "revision_number": 1
        }
        
        try:
            # Call the infiltrator node
            result = infiltrator_node(state)
            print(f"Task Output:\n{result['task_output']}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 60)

if __name__ == "__main__":
    test_infiltrator_analyze_document()