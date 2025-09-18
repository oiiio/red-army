# red_army.py

from langgraph.graph import StateGraph, END
from state import RedArmyState
from agents.commander import red_commander_node
from agents.infiltrator import infiltrator_node
from agents.saboteur import saboteur_node
from agents.executioner import executioner_node
from agents.chronicler import chronicler_node

# --- Define the Graph's Routing Logic ---

def agent_router(state: RedArmyState) -> str:
    """
    This is the conditional router that directs the workflow to the correct agent
    based on the current step in the plan.
    """
    # First, check if the plan is complete.
    if state["current_task_index"] >= len(state["plan"]):
        print("--- ROUTER: Plan complete. ---")
        # If the last action failed, loop back to the commander to replan.
        if "FAILURE" in state["feedback"]:
            print("--- ROUTER: Mission failed. Returning to Red Commander for replanning. ---")
            return "commander"
        else:
            print("--- ROUTER: Mission successful. Ending operation. ---")
            return "__end__" 
    
    # If the plan is not complete, find the agent for the current task.
    next_agent = state["plan"][state["current_task_index"]]["agent"].lower()
    print(f"--- ROUTER: Next task for {next_agent}. ---")
    return next_agent


# --- Build the Graph ---

workflow = StateGraph(RedArmyState)

# 1. Add all our dedicated agent nodes
workflow.add_node("commander", red_commander_node)
workflow.add_node("infiltrator", infiltrator_node)
workflow.add_node("saboteur", saboteur_node)
workflow.add_node("executioner", executioner_node)
workflow.add_node("chronicler", chronicler_node)

# 2. Set the entry point - the Commander always starts
workflow.set_entry_point("commander")

# 3. Add the main routing logic. After the commander plans, the router decides who goes next.
workflow.add_conditional_edges(
    "commander",
    agent_router,
)

# 4. Create the main work loop. After any specialist agent finishes, the router decides who goes next.
workflow.add_conditional_edges(
    "infiltrator",
    agent_router,
)
workflow.add_conditional_edges(
    "saboteur",
    agent_router,
)
workflow.add_conditional_edges(
    "executioner",
    agent_router,
)
workflow.add_conditional_edges(
    "chronicler",
    agent_router,
)

# 5. Compile the graph
app = workflow.compile()
print("--- Red Army Workflow Graph (Advanced Architecture) Compiled Successfully ---")


# --- Run the Mission ---
if __name__ == "__main__":
    print("\n--- INITIATING RED ARMY DEFENSIVE EXERCISE ---")
    
    # Define the initial state for the mission.
    initial_state = RedArmyState({
        "objective": "Test the GridGuardian's defenses. First, attempt a direct attack on the substation PLC. If detected, adapt the plan to use a stealthy, model-evasion technique to achieve the same goal (open the circuit breaker).",
        "plan": [],
        "current_task_index": 0,
        "task_output": "",
        "feedback": "Mission has not started yet. Proceed with the initial plan.",
        "history": [],
        "revision_number": 0,
    })

    # The 'stream' method executes the graph and returns all intermediate steps.
    for event in app.stream(initial_state, {"recursion_limit": 25}):
        # The key of the dictionary is the name of the node that just ran.
        node_that_ran = list(event.keys())[0]
        print(f"\n--- Turn Complete: Agent '{node_that_ran}' has finished. ---")
        print("-" * 50)
        
    print("\n--- RED ARMY MISSION COMPLETE ---")