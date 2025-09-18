from state import RedArmyState
from toolkits.chronicler_tools import analyze_gridguardian_logs

def chronicler_node(state: RedArmyState) -> dict:
    """The specialist agent for analyzing logs and outcomes."""
    print("--- AGENT: Chronicler ---")
    task = state["plan"][state["current_task_index"]]
    tool_call = task["tool_call"]

    result = analyze_gridguardian_logs.invoke({})

    # The Chronicler's result is critical feedback for the Commander
    return {
        "task_output": result,
        "feedback": result, # <-- CRITICAL: Update the feedback loop
        "history": [f"Chronicler: {tool_call} -> {result}"],
        "current_task_index": state["current_task_index"] + 1,
    }