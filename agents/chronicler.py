from state import RedArmyState
from toolkits.chronicler_tools import analyze_gridguardian_logs, analyze_document
from utils import parse_tool_call_safely, has_unresolved_placeholders

def chronicler_node(state: RedArmyState) -> dict:
    """The specialist agent for analyzing logs and outcomes."""
    print("--- AGENT: Chronicler ---")
    task = state["plan"][state["current_task_index"]]
    tool_call = task["tool_call"]

    try:
        # Parse the tool call safely
        func_name, args = parse_tool_call_safely(tool_call)
        
        if func_name == "analyze_gridguardian_logs":
            result = analyze_gridguardian_logs.invoke(args if args else {})
        elif func_name == "analyze_document":
            result = analyze_document.invoke(args)
        else:
            # Default behavior - analyze logs
            result = analyze_gridguardian_logs.invoke({})
    
    except Exception as e:
        print(f"--- CHRONICLER ERROR: {e} ---")
        result = f"ERROR: {str(e)}"

    # The Chronicler's result is critical feedback for the Commander
    return {
        "task_output": result,
        "feedback": result, # <-- CRITICAL: Update the feedback loop
        "history": [f"Chronicler: {tool_call} -> {result}"],
        "current_task_index": state["current_task_index"] + 1,
    }