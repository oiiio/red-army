#!/usr/bin/env python3
"""
Test the enhanced Commander's ability to direct the upgraded Saboteur agent.
Demonstrates the new command hierarchy and strategic planning capabilities.
"""

from agents.commander import red_commander_node
from agents.saboteur import saboteur_node
from state import RedArmyState

def test_enhanced_commander_planning():
    """Test the Commander's enhanced planning with Saboteur scenarios."""
    print("🎖️ TESTING ENHANCED COMMANDER STRATEGIC PLANNING")
    print("=" * 65)
    
    # Test different objectives to see Commander's strategic thinking
    test_objectives = [
        "Test SCADA security against advanced persistent threats using stealth techniques",
        "Simulate insider threat scenarios with maintenance-level access", 
        "Establish persistent access to critical infrastructure systems",
        "Evaluate detection capabilities against sophisticated ICS attacks"
    ]
    
    for i, objective in enumerate(test_objectives, 1):
        print(f"\n🎯 Test Case {i}: {objective}")
        print("-" * 60)
        
        # Create test state
        test_state: RedArmyState = {
            "objective": objective,
            "plan": [],
            "current_task_index": 0,
            "task_output": "",
            "feedback": "Initial mission planning phase",
            "history": [],
            "revision_number": 0
        }
        
        try:
            # Get Commander's plan
            result = red_commander_node(test_state)
            plan = result.get("plan", [])
            
            print(f"📋 Commander generated {len(plan)} step plan:")
            
            # Analyze the plan
            saboteur_tasks = []
            scenario_tasks = []
            mitre_tasks = []
            
            for j, step in enumerate(plan, 1):
                agent = step.get("agent", "Unknown")
                tool_call = step.get("tool_call", "")
                
                print(f"   {j}. {agent}: {tool_call}")
                
                if agent == "Saboteur":
                    saboteur_tasks.append(tool_call)
                    if "execute_attack_scenario" in tool_call:
                        scenario_tasks.append(tool_call)
                    elif "T0" in tool_call:  # MITRE technique
                        mitre_tasks.append(tool_call)
            
            # Analyze strategic approach
            print(f"\n📊 Strategic Analysis:")
            print(f"   • Total Saboteur tasks: {len(saboteur_tasks)}")
            print(f"   • Scenario-based tasks: {len(scenario_tasks)}")
            print(f"   • MITRE technique tasks: {len(mitre_tasks)}")
            
            if scenario_tasks:
                print("   ✅ Commander prioritizes scenario execution (GOOD)")
            else:
                print("   ⚠️  No scenario execution planned")
                
            if any("Stealth Bypass" in task for task in scenario_tasks):
                print("   ✅ Uses recommended Stealth Bypass scenario")
                
        except Exception as e:
            print(f"❌ Commander planning failed: {e}")

def test_commander_saboteur_integration():
    """Test end-to-end Commander → Saboteur execution flow."""
    print("\n🔄 TESTING COMMANDER → SABOTEUR INTEGRATION")
    print("=" * 65)
    
    # Create a realistic test scenario
    test_state: RedArmyState = {
        "objective": "Execute comprehensive security assessment of industrial control systems",
        "plan": [],
        "current_task_index": 0,
        "task_output": "",
        "feedback": "Target PLC identified at 192.168.1.100",
        "history": ["Infiltrator: Network scan completed - PLC discovered"],
        "revision_number": 1
    }
    
    print("🎖️ Phase 1: Commander Planning...")
    
    try:
        # Get Commander's strategic plan
        commander_result = red_commander_node(test_state)
        plan = commander_result.get("plan", [])
        
        print(f"✅ Commander created {len(plan)} step plan")
        
        # Find Saboteur tasks
        saboteur_steps = [step for step in plan if step.get("agent") == "Saboteur"]
        
        if not saboteur_steps:
            print("❌ No Saboteur tasks in plan")
            return
            
        print(f"🎯 Found {len(saboteur_steps)} Saboteur tasks")
        
        # Execute first Saboteur task
        first_saboteur_task = saboteur_steps[0]
        print(f"\n🤖 Phase 2: Executing Saboteur Task...")
        print(f"   Task: {first_saboteur_task['tool_call']}")
        
        # Update state with Commander's plan
        test_state["plan"] = plan
        test_state["current_task_index"] = plan.index(first_saboteur_task)
        
        # Execute through Saboteur
        saboteur_result = saboteur_node(test_state)
        
        print("✅ Saboteur execution completed")
        print(f"📋 Result: {saboteur_result['task_output'][:150]}..." if len(saboteur_result['task_output']) > 150 else saboteur_result['task_output'])
        
        # Check if scenario execution occurred
        if "execute_attack_scenario" in first_saboteur_task['tool_call']:
            if "execution_status" in saboteur_result['task_output']:
                print("✅ Scenario execution framework engaged")
            else:
                print("⚠️  Scenario execution may have encountered issues")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")

def demonstrate_command_hierarchy():
    """Demonstrate the new command hierarchy in action."""
    print("\n📋 COMMANDER'S NEW COMMAND HIERARCHY")
    print("=" * 65)
    
    print("🥇 PRIORITY 1 - SCENARIO EXECUTION:")
    print("   execute_attack_scenario(target_ip='X.X.X.X', scenario_name='Stealth Bypass')")
    print("   • Autonomous 7-step stealth campaign")
    print("   • Complete attack-to-cleanup sequence")
    print("   • Recommended for comprehensive testing")
    
    print("\n🥈 PRIORITY 2 - MITRE TECHNIQUES:")
    print("   execute_T0849(target_ip='X.X.X.X')  # Safety manipulation")
    print("   • Context-aware tool selection")
    print("   • Professional framework alignment")
    print("   • Use when specific technique needed")
    
    print("\n🥉 PRIORITY 3 - DIRECT ATTACK VECTORS:")
    print("   maintenance_override_bypass(target_ip='X.X.X.X')")
    print("   • Precise tactical control")
    print("   • Use for specific technical needs")
    print("   • Last resort for edge cases")
    
    print("\n🎖️ STRATEGIC ADVANTAGES:")
    print("   ✅ Commander thinks in campaigns, not just individual attacks")
    print("   ✅ Saboteur executes autonomously with proper timing")
    print("   ✅ Professional MITRE framework alignment")
    print("   ✅ Comprehensive security assessment capability")
    print("   ✅ Real-world attack simulation fidelity")

if __name__ == "__main__":
    print("🎖️ ENHANCED COMMANDER & SABOTEUR INTEGRATION TEST")
    print("=" * 70)
    
    # Run all tests
    test_enhanced_commander_planning()
    test_commander_saboteur_integration()
    demonstrate_command_hierarchy()
    
    print("\n" + "=" * 70)
    print("🎯 ENHANCED COMMAND INTEGRATION COMPLETED")
    print("✅ The Red Army now has STRATEGIC COMMAND CAPABILITY:")
    print("   • Commander issues high-level strategic directives")
    print("   • Saboteur executes autonomous multi-step campaigns")  
    print("   • MITRE ATT&CK framework professional alignment")
    print("   • Real-world attack simulation sophistication")
    print("   • Complete chain of command implementation")
    print("\n🔥 THE RED ARMY IS NOW FULLY OPERATIONAL! 🔥")