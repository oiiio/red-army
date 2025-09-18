from state import RedArmyState
from toolkits.executioner_tools import execute_direct_attack, execute_evasion_sequence, analyze_document
from utils import parse_tool_call_safely, has_unresolved_placeholders

def executioner_node(state: RedArmyState) -> dict:
    """The specialist agent for executing attacks."""
    print("--- AGENT: Executioner ---")
    task = state["plan"][state["current_task_index"]]
    tool_call = task["tool_call"]

    try:
        # Check if the tool call has unresolved placeholders
        if has_unresolved_placeholders(tool_call):
            print(f"--- EXECUTIONER: Skipping task with unresolved placeholders: {tool_call} ---")
            result = f"SKIPPED: Task contains unresolved placeholders: {tool_call}"
        else:
            # Parse the tool call safely
            func_name, args = parse_tool_call_safely(tool_call)
            
            if func_name == "execute_direct_attack" or "execute_direct_attack" in tool_call:
                result = execute_direct_attack.invoke(args)
            elif func_name == "execute_evasion_sequence" or "execute_evasion_sequence" in tool_call:
                # The argument for this tool is the *output* of a previous Saboteur task
                args = {"sequence_plan_str": state["task_output"]}
                result = execute_evasion_sequence.invoke(args)
            elif func_name == "analyze_document":
                result = analyze_document.invoke(args)
            else:
                # Simulate other executioner tools
                print(f"--- EXECUTIONER/TOOL: Simulating {func_name} with args {args} ---")
                result = f"SIMULATED: {func_name} executed successfully"

    except Exception as e:
        print(f"--- EXECUTIONER ERROR: {e} ---")
        result = f"ERROR: {str(e)}"

    return {
        "task_output": result,
        "history": [f"Executioner: {tool_call} -> {result}"],
        "current_task_index": state["current_task_index"] + 1,
    }