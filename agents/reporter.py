from state import RedArmyState
from toolkits.reporting_tools import generate_mission_debrief, save_mission_report

def reporting_node(state: RedArmyState) -> dict:
    """
    The final reporting agent that generates comprehensive mission debriefing reports.
    This node synthesizes the entire mission history and outcomes into a structured after-action report.
    """
    print("--- AGENT: Reporter ---")
    print("--- Generating Final Mission Debrief ---")

    try:
        # Extract mission data from state
        mission_history = state.get("history", [])
        mission_feedback = state.get("feedback", "Mission completed")
        mission_objective = state.get("objective", "Security assessment mission")
        
        print(f"--- REPORTER: Processing {len(mission_history)} history entries ---")
        print(f"--- REPORTER: Mission objective: {mission_objective} ---")
        print(f"--- REPORTER: Final feedback: {mission_feedback[:100]}{'...' if len(mission_feedback) > 100 else ''} ---")
        
        # Generate the comprehensive mission debrief
        mission_report = generate_mission_debrief.invoke({
            "history": mission_history,
            "feedback": mission_feedback,
            "objective": mission_objective
        })
        
        # Optionally save the report to file (uncomment if permanent storage is needed)
        # save_result = save_mission_report.invoke({
        #     "report": mission_report,
        #     "filename": None  # Will auto-generate timestamp-based filename
        # })
        # print(f"--- REPORTER: {save_result} ---")
        
        print("--- REPORTER: Mission debrief completed successfully ---")
        
        # Return the final state with the mission report
        return {
            "task_output": mission_report,
            "feedback": "MISSION DEBRIEF COMPLETED: Final after-action report generated successfully",
            "history": [f"Reporter: Generated comprehensive mission debrief report ({len(mission_report)} characters)"],
            "current_task_index": state.get("current_task_index", 0) + 1,
        }
        
    except Exception as e:
        error_msg = f"ERROR generating mission debrief: {str(e)}"
        print(f"--- REPORTER ERROR: {error_msg} ---")
        
        return {
            "task_output": error_msg,
            "feedback": f"MISSION DEBRIEF FAILED: {error_msg}",
            "history": [f"Reporter: Failed to generate mission debrief - {error_msg}"],
            "current_task_index": state.get("current_task_index", 0) + 1,
        }