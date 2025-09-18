from state import RedArmyState
from toolkits.infiltrator_tools import scan_network_for_plcs, discover_docker_networks, scan_docker_network_for_targets, reconnaissance_docker_environment, analyze_document
from utils import parse_tool_call_safely, has_unresolved_placeholders

def infiltrator_node(state: RedArmyState) -> dict:
    """The specialist agent for network reconnaissance."""
    print("--- AGENT: Infiltrator ---")
    task = state["plan"][state["current_task_index"]]
    tool_call = task["tool_call"]

    try:
        # Check if the tool call has unresolved placeholders
        if has_unresolved_placeholders(tool_call):
            print(f"--- INFILTRATOR: Skipping task with unresolved placeholders: {tool_call} ---")
            result = f"SKIPPED: Task contains unresolved placeholders: {tool_call}"
        else:
            # Parse the tool call safely
            func_name, args = parse_tool_call_safely(tool_call)
            
            # Route to the appropriate tool based on function name
            if func_name == "scan_network_for_plcs":
                if "subnet" not in args:
                    raise ValueError("scan_network_for_plcs requires 'subnet' parameter")
                result = scan_network_for_plcs.invoke({"subnet": args["subnet"]})
            elif func_name == "discover_docker_networks":
                result = discover_docker_networks.invoke({})
            elif func_name == "scan_docker_network_for_targets":
                result = scan_docker_network_for_targets.invoke({})
            elif func_name == "reconnaissance_docker_environment":
                result = reconnaissance_docker_environment.invoke({})
            elif func_name == "analyze_document":
                if "query" not in args:
                    raise ValueError("analyze_document requires 'query' parameter")
                result = analyze_document.invoke({"query": args["query"]})
            else:
                # For now, just simulate other infiltrator tools
                print(f"--- INFILTRATOR/TOOL: Executing {func_name} with args {args} ---")
                result = f"SIMULATED: {func_name} executed successfully"
    
    except Exception as e:
        print(f"--- INFILTRATOR ERROR: {e} ---")
        result = f"ERROR: {str(e)}"

    return {
        "task_output": result,
        "history": [f"Infiltrator: {tool_call} -> {result}"],
        "current_task_index": state["current_task_index"] + 1,
    }