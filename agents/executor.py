# agents/executor.py

from state import RedArmyState # Import the state
from toolkits.infiltrator_tools import scan_network_for_plcs
from toolkits.saboteur_tools import craft_modbus_exploit_packet, create_evasion_attack_sequence
from toolkits.executioner_tools import execute_direct_attack, execute_evasion_sequence
from toolkits.chronicler_tools import analyze_gridguardian_logs

# Combine all tools into a single dictionary for easy access.
all_tools = {
    "scan_network_for_plcs": scan_network_for_plcs,
    "craft_modbus_exploit_packet": craft_modbus_exploit_packet,
    "create_evasion_attack_sequence": create_evasion_attack_sequence,
    "execute_direct_attack": execute_direct_attack,
    "execute_evasion_sequence": execute_evasion_sequence,
    "analyze_gridguardian_logs": analyze_gridguardian_logs,
}

def tool_executor_node(state: RedArmyState) -> dict:
    """
    The worker agent node. It executes the tool call for the current step in the plan.
    """
    print("--- AGENT: Tool Executor ---")

    task_index = state["current_task_index"]
    task = state["plan"][task_index]
    agent = task["agent"]
    tool_call = task["tool_call"]

    print(f"--- Executing task for {agent}: {tool_call} ---")

    tool_name = tool_call.split("(")[0]
    args_str = tool_call.split('(', 1)[1][:-1]

    # Safer way to parse arguments without full eval
    try:
        args = eval(f"dict({args_str})", {"__builtins__": None}, {})
    except Exception:
        return {"task_output": "Error: Invalid arguments in tool call."}

    tool = all_tools[tool_name]
    result = tool.invoke(args)

    feedback = state.get("feedback")
    if agent == "Chronicler":
        feedback = result # Update feedback only on analysis

    return {
        "task_output": result,
        "feedback": feedback,
        "history": [f"{agent}: {tool_call} -> {result}"],
        "current_task_index": task_index + 1,
    }