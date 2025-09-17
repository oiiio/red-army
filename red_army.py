from langgraph.graph import StateGraph, END
from state import RedArmyState
from agents.commander import red_commander_node
from agents.executor import tool_executor_node

# --- Define the Graph's Logic ---

def should_continue(state: RedArmyState) -> str:
    """
    This is the conditional edge that decides the next step.
    It's the core of the adaptive logic.
    """
    print("--- ORCHESTRATOR: Evaluating next step... ---")
    
    # Check if the plan is finished.
    if state["current_task_index"] >= len(state["plan"]):
        print("--- ORCHESTRATOR: Plan complete. ---")
        
        # If the last action failed (based on Chronicler's feedback),
        # loop back to the commander to replan.
        if "FAILURE" in state["feedback"]:
            print("--- ORCHESTRATOR: Mission failed. Returning to Red Commander for replanning. ---")
            return "replan"
        else:
            print("--- ORCHESTRATOR: Mission successful. Ending operation. ---")
            return "end"
    else:
        # If the plan is not finished, continue to the next task.
        print("--- ORCHESTRATOR: Plan has more steps. Continuing to Tool Executor. ---")
        return "continue"

# --- Build the Graph ---

# 1. Initialize the StateGraph with our RedArmyState
workflow = StateGraph(RedArmyState)

# 2. Add the nodes to the graph. These are our agents.
workflow.add_node("commander", red_commander_node)
workflow.add_node("executor", tool_executor_node)

# 3. Set the entry point. The Red Commander always starts the mission.
workflow.set_entry_point("commander")

# 4. Add the edges that define the flow.
workflow.add_edge("commander", "executor")

# 5. Add the conditional edge for the adaptive loop.
workflow.add_conditional_edges(
    "executor",
    should_continue,
    {
        "continue": "executor", # If plan continues, loop back to the executor
        "replan": "commander",   # If plan fails, go back to the commander
        "end": END               # If plan succeeds, end the graph
    }
)

# 6. Compile the graph into a runnable application.
app = workflow.compile()
print("--- Red Army Workflow Graph Compiled Successfully ---")

# --- Run the Mission ---

if __name__ == "__main__":
    print("\n--- INITIATING RED ARMY DEFENSIVE EXERCISE ---")
    
    # Define the initial state for the mission.
    initial_state = {
        "objective": "Test the GridGuardian's defenses. First, attempt a direct attack on the substation PLC. If detected, adapt the plan to use a stealthy, model-evasion technique to achieve the same goal (open the circuit breaker).",
        "plan": [],
        "current_task_index": 0,
        "task_output": "",
        "feedback": "Mission has not started yet. Proceed with the initial plan.",
        "history": [],
        "revision_number": 0,
    }

    # The 'stream' method executes the graph and returns all intermediate steps.
    for event in app.stream(initial_state, {"recursion_limit": 25}):
        # The key of the dictionary is the name of the node that just ran.
        node_that_ran = list(event.keys())[0]
        # The value is the state *after* that node ran.
        state_after_node = list(event.values())[0]
        
        print(f"\n--- Turn Complete: {node_that_ran} ---")
        print("Updated State:")
        # Pretty print the feedback and task output for clarity
        print(f"  - Feedback: {state_after_node.get('feedback')}")
        print(f"  - Last Task Output: {state_after_node.get('task_output')}")
        print("-" * 40)

    print("--- RED ARMY MISSION COMPLETE ---")