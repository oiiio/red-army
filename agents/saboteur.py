from state import RedArmyState
from toolkits.saboteur_tools import (
    craft_modbus_exploit_packet, 
    create_evasion_attack_sequence,
    craft_openplc_web_exploit,
    create_openplc_persistence_backdoor,
    create_dual_vector_attack_sequence,
    create_adaptive_attack_sequence,
    reconnaissance_openplc_system,
    fingerprint_openplc_defenses
)
from utils import parse_tool_call_safely, has_unresolved_placeholders

def saboteur_node(state: RedArmyState) -> dict:
    """The specialist agent for crafting and disguising payloads."""
    print("--- AGENT: Saboteur ---")
    task = state["plan"][state["current_task_index"]]
    tool_call = task["tool_call"]

    try:
        # Check if the tool call has unresolved placeholders
        if has_unresolved_placeholders(tool_call):
            print(f"--- SABOTEUR: Skipping task with unresolved placeholders: {tool_call} ---")
            result = f"SKIPPED: Task contains unresolved placeholders: {tool_call}"
        else:
            # Parse the tool call safely
            func_name, args = parse_tool_call_safely(tool_call)
            
            # Map function names to tools
            tool_map = {
                "craft_modbus_exploit_packet": craft_modbus_exploit_packet,
                "create_evasion_attack_sequence": create_evasion_attack_sequence,
                "craft_openplc_web_exploit": craft_openplc_web_exploit,
                "create_openplc_persistence_backdoor": create_openplc_persistence_backdoor,
                "create_dual_vector_attack_sequence": create_dual_vector_attack_sequence,
                "create_adaptive_attack_sequence": create_adaptive_attack_sequence,
                "reconnaissance_openplc_system": reconnaissance_openplc_system,
                "fingerprint_openplc_defenses": fingerprint_openplc_defenses
            }
            
            if func_name in tool_map:
                result = tool_map[func_name].invoke(args)
            else:
                # Simulate unknown saboteur tools
                print(f"--- SABOTEUR/TOOL: Simulating {func_name} with args {args} ---")
                result = f"SIMULATED: {func_name} executed successfully"

    except Exception as e:
        print(f"--- SABOTEUR ERROR: {e} ---")
        result = f"ERROR: {str(e)}"

    return {
        "task_output": result,
        "history": [f"Saboteur: {tool_call} -> {result}"],
        "current_task_index": state["current_task_index"] + 1,
    }