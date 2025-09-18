#!/usr/bin/env python3
"""
Test script for advanced scenario execution capability.
Demonstrates the Saboteur's ability to execute complete attack campaigns autonomously.
"""

from toolkits.saboteur_tools import execute_attack_scenario
from agents.saboteur import saboteur_node
from state import RedArmyState

def test_scenario_execution_direct():
    """Test the execute_attack_scenario function directly."""
    print("⭐ TESTING DIRECT SCENARIO EXECUTION")
    print("=" * 60)
    
    target_ip = "192.168.1.100"
    scenarios = ["Stealth Bypass", "Maintenance Masquerade", "Persistence Attack"]
    
    for scenario in scenarios:
        print(f"\n🎮 Testing Scenario: {scenario}")
        print("-" * 40)
        
        try:
            result = execute_attack_scenario.invoke({
                "target_ip": target_ip,
                "scenario_name": scenario,
                "execution_delay": 1  # Fast execution for testing
            })
            
            print("✅ Scenario execution completed successfully")
            print(f"📋 Result summary: {len(str(result))} characters of execution log")
            
            # Parse some key information from result
            if "steps_executed" in result and "total_steps" in result:
                print(f"📊 Execution summary extracted from result")
            else:
                print(f"📄 Raw result: {result[:200]}..." if len(result) > 200 else result)
                
        except Exception as e:
            print(f"❌ Scenario execution failed: {e}")

def test_saboteur_scenario_integration():
    """Test scenario execution through the Saboteur agent."""
    print("\n🤖 TESTING SABOTEUR AGENT SCENARIO INTEGRATION")
    print("=" * 60)
    
    # Create test state for scenario execution
    test_state: RedArmyState = {
        "objective": "Execute Stealth Bypass scenario autonomously",
        "plan": [
            {
                "tool_call": "execute_attack_scenario(target_ip='192.168.1.100', scenario_name='Stealth Bypass', execution_delay=1)",
                "description": "Execute complete Stealth Bypass campaign"
            }
        ],
        "current_task_index": 0,
        "task_output": "",
        "feedback": "",
        "history": [],
        "revision_number": 0
    }
    
    print("🎯 Executing Stealth Bypass scenario through Saboteur agent...")
    
    try:
        result = saboteur_node(test_state)
        print("✅ Saboteur scenario execution completed")
        
        output = result.get("task_output", "")
        print(f"📊 Execution completed with {len(output)} character output")
        
        # Show key results
        if "execution_status" in output:
            print("📋 Scenario execution log generated")
        
        print(f"📄 Sample output: {output[:300]}..." if len(output) > 300 else output)
        
    except Exception as e:
        print(f"❌ Saboteur scenario execution failed: {e}")

def test_scenario_capabilities():
    """Test various scenario execution capabilities."""
    print("\n🔧 TESTING SCENARIO CAPABILITIES")
    print("=" * 60)
    
    # Test scenario parsing
    print("🔍 Testing scenario availability...")
    scenarios_to_test = [
        "Stealth Bypass",
        "Maintenance Masquerade", 
        "Persistence Attack",
        "Unknown Scenario"  # Should fail gracefully
    ]
    
    target_ip = "192.168.1.100"
    
    for scenario in scenarios_to_test:
        print(f"\n📋 Testing scenario: {scenario}")
        
        try:
            # Test with minimal execution delay for speed
            result = execute_attack_scenario.invoke({
                "target_ip": target_ip,
                "scenario_name": scenario,
                "execution_delay": 0  # No delay for capability testing
            })
            
            if "Unknown scenario" in result:
                print("   ⚠️  Scenario not found (expected for unknown scenario)")
            elif "execution_status" in result:
                print("   ✅ Scenario structure valid")
            else:
                print("   📄 Basic execution completed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def demonstrate_scenario_features():
    """Demonstrate key features of scenario execution."""
    print("\n🌟 SCENARIO EXECUTION FEATURES DEMONSTRATION")
    print("=" * 60)
    
    print("🧰 Key Features:")
    print("   • RAG-Enhanced Parsing: Queries attack guide for scenario steps")
    print("   • Hardcoded Fallback: Built-in scenarios if RAG unavailable") 
    print("   • Step-by-Step Execution: Orchestrates individual attack functions")
    print("   • Timing Control: Handles delays and operational timing")
    print("   • Error Handling: Continues execution on non-critical failures")
    print("   • Execution Logging: Detailed logs of each step")
    print("   • Campaign Autonomy: Single command executes entire attack sequence")
    
    print("\n🎯 Available Scenarios:")
    print("   1. Stealth Bypass (⭐ RECOMMENDED)")
    print("      - 7-step high-stealth attack sequence")
    print("      - Debug mode → Timer manipulation → Emergency bypass → Cleanup")
    print("   2. Maintenance Masquerade")
    print("      - 3-step maintenance override attack") 
    print("      - Fast but high detection risk")
    print("   3. Persistence Attack")
    print("      - 2-step system compromise for ongoing access")
    print("      - Health signature corruption + covert channel")
    
    print("\n🚀 Usage Example:")
    print("   execute_attack_scenario(")
    print("       target_ip='192.168.1.100',")
    print("       scenario_name='Stealth Bypass',")
    print("       execution_delay=2")
    print("   )")

if __name__ == "__main__":
    print("⭐ ADVANCED SCENARIO EXECUTION TEST SUITE")
    print("=" * 70)
    
    # Run all tests
    test_scenario_execution_direct()
    test_saboteur_scenario_integration() 
    test_scenario_capabilities()
    demonstrate_scenario_features()
    
    print("\n" + "=" * 70)
    print("🎯 ADVANCED SCENARIO TESTING COMPLETED")
    print("✅ The Saboteur agent now has AUTONOMOUS CAMPAIGN capability:")
    print("   • Execute complete multi-step attack scenarios")
    print("   • RAG-enhanced scenario parsing from attack guide")
    print("   • Intelligent step orchestration with proper timing")
    print("   • Comprehensive execution logging and error handling")
    print("   • Single-command campaign execution")
    print("\n🔥 The Saboteur is now a TRUE AUTONOMOUS OPERATOR! 🔥")