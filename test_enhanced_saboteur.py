#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced Saboteur agent capabilities.
Shows MITRE ATT&CK technique mapping and context-aware tool selection.
"""

import json
from agents.saboteur import (
    load_mitre_techniques, 
    select_technique_function, 
    extract_technique_id,
    saboteur_node
)
from toolkits.saboteur_tools import (
    maintenance_override_bypass,
    manipulate_safety_timer,
    activate_emergency_bypass,
    corrupt_system_health_signature,
    establish_covert_channel
)
from state import RedArmyState

def test_attack_vector_functions():
    """Test the 5 new attack vector functions directly."""
    print("🧰 TESTING ATTACK VECTOR TOOLKIT")
    print("=" * 50)
    
    target_ip = "192.168.1.100"
    
    # Test each attack vector function
    attack_functions = [
        ("maintenance_override_bypass", maintenance_override_bypass, {"target_ip": target_ip}),
        ("manipulate_safety_timer", manipulate_safety_timer, {"target_ip": target_ip, "timer_value": 75}),
        ("activate_emergency_bypass", activate_emergency_bypass, {"target_ip": target_ip, "enable": True}),
        ("corrupt_system_health_signature", corrupt_system_health_signature, {"target_ip": target_ip}),
        ("establish_covert_channel", establish_covert_channel, {"target_ip": target_ip, "enable_debug": True, "monitor_channel": True})
    ]
    
    for func_name, func, args in attack_functions:
        print(f"\n🔴 Testing {func_name}")
        print("-" * 30)
        try:
            result = func.invoke(args)
            print(f"✅ SUCCESS: Function executed")
            
            # Parse and display key information from result
            if "attack_vector" in result:
                print(f"   Vector: {func_name}")
                if "detection_risk" in result:
                    print(f"   Detection Risk: Extracted from result")
                if "stealth_level" in result:
                    print(f"   Stealth Level: Extracted from result")
                    
        except Exception as e:
            print(f"❌ ERROR: {e}")

def test_mitre_technique_mapping():
    """Test MITRE ATT&CK technique mapping functionality."""
    print("\n🗺️  TESTING MITRE ATT&CK MAPPING")
    print("=" * 50)
    
    # Load the techniques data
    techniques_data = load_mitre_techniques()
    techniques = techniques_data.get("mitre_attack_ics_mapping", {}).get("techniques", {})
    
    print(f"📋 Loaded {len(techniques)} MITRE techniques")
    
    # Test technique selection for different contexts
    test_cases = [
        ("T0849", "Need to disable safety systems stealthily", "stealth_focused"),
        ("T0849", "Emergency situation - need immediate access", "speed_focused"),
        ("T0855", "Establish ongoing access to the system", "persistence_focused"),
        ("T0835", "Manipulate I/O covertly", "stealth_focused")
    ]
    
    for technique_id, context, strategy in test_cases:
        print(f"\n🎯 Testing {technique_id}")
        print(f"   Context: {context}")
        print(f"   Strategy: {strategy}")
        
        selected_function = select_technique_function(technique_id, context, strategy)
        
        if selected_function:
            print(f"   ✅ Selected: {selected_function}")
        else:
            print(f"   ❌ No function selected")

def test_technique_id_extraction():
    """Test extraction of technique IDs from tool calls."""
    print("\n🔍 TESTING TECHNIQUE ID EXTRACTION")
    print("=" * 50)
    
    test_calls = [
        "execute_T0849(target='192.168.1.100')",
        "technique_T0855_maintenance_override",
        "T0836_parameter_manipulation", 
        "regular_function_call()",
        "craft_T0832_view_manipulation_attack"
    ]
    
    for call in test_calls:
        technique_id = extract_technique_id(call)
        print(f"📞 Call: {call}")
        print(f"   🆔 Extracted: {technique_id if technique_id else 'None'}")

def test_enhanced_saboteur_execution():
    """Test the enhanced saboteur node with MITRE technique execution."""
    print("\n🤖 TESTING ENHANCED SABOTEUR EXECUTION")
    print("=" * 50)
    
    # Create a test state with MITRE technique tasks
    test_state: RedArmyState = {
        "objective": "Test MITRE technique execution",
        "plan": [
            {
                "tool_call": "execute_T0849(target_ip='192.168.1.100')",
                "description": "Disable safety systems using MITRE T0849 technique"
            },
            {
                "tool_call": "maintenance_override_bypass(target_ip='192.168.1.100')",
                "description": "Direct maintenance override attack"
            }
        ],
        "current_task_index": 0,
        "task_output": "",
        "feedback": "",
        "history": [],
        "revision_number": 0
    }
    
    # Test execution of MITRE technique
    print("🎯 Executing MITRE technique task...")
    try:
        result = saboteur_node(test_state)
        print("✅ MITRE technique execution completed")
        print(f"   Output: {result['task_output'][:100]}..." if len(result['task_output']) > 100 else f"   Output: {result['task_output']}")
    except Exception as e:
        print(f"❌ Execution error: {e}")
    
    # Test regular function execution
    test_state["current_task_index"] = 1
    print("\n🔧 Executing direct function call...")
    try:
        result = saboteur_node(test_state)
        print("✅ Direct function execution completed") 
        print(f"   Output: {result['task_output'][:100]}..." if len(result['task_output']) > 100 else f"   Output: {result['task_output']}")
    except Exception as e:
        print(f"❌ Execution error: {e}")

def display_technique_summary():
    """Display a summary of available techniques and their mappings."""
    print("\n📊 SABOTEUR TECHNIQUE SUMMARY")
    print("=" * 50)
    
    techniques_data = load_mitre_techniques()
    techniques = techniques_data.get("mitre_attack_ics_mapping", {}).get("techniques", {})
    function_metadata = techniques_data.get("function_metadata", {})
    
    for technique_id, technique in techniques.items():
        print(f"\n🆔 {technique_id}: {technique['name']}")
        print(f"   📝 {technique['description']}")
        print(f"   🛠️  Mapped Functions: {', '.join(technique['mapped_functions'])}")
        
        # Show function details
        for func_name in technique['mapped_functions']:
            if func_name in function_metadata:
                metadata = function_metadata[func_name]
                print(f"      • {func_name}: {metadata['stealth_level']} stealth, {metadata['detection_risk']} risk")

if __name__ == "__main__":
    print("🔴 RED ARMY - ENHANCED SABOTEUR TEST SUITE")
    print("=" * 60)
    
    # Run all tests
    test_attack_vector_functions()
    test_mitre_technique_mapping()
    test_technique_id_extraction()
    test_enhanced_saboteur_execution()
    display_technique_summary()
    
    print("\n" + "=" * 60)
    print("🎯 SABOTEUR ENHANCEMENT TESTING COMPLETED")
    print("✅ The Saboteur agent now has:")
    print("   • 5 specialized attack vector functions")  
    print("   • MITRE ATT&CK for ICS technique mapping")
    print("   • Context-aware tool selection")
    print("   • RAG-enhanced intelligence")
    print("   • Sophisticated tactical decision making")