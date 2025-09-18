# toolkits/reporting_tools.py

import os
from datetime import datetime
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the LLM for report generation
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", api_key=os.getenv("GOOGLE_API_KEY"))

@tool
def generate_mission_debrief(history: list, feedback: str, objective: str = "Security assessment mission") -> str:
    """
    Generates a comprehensive after-action report based on mission history and final feedback.
    This tool synthesizes all mission activities into a structured debrief report.

    Args:
        history: List of strings containing the full mission history/actions taken
        feedback: Final feedback or outcome from the mission execution
        objective: The original mission objective (optional, defaults to "Security assessment mission")

    Returns:
        A formatted after-action report containing mission analysis and recommendations
    """
    print("--- REPORTING/TOOL: Generating Mission Debrief Report... ---")
    
    try:
        # Prepare the mission data for analysis
        history_text = "\n".join([f"• {entry}" for entry in history]) if history else "No mission history available"
        
        # Construct the comprehensive prompt for report generation
        prompt = f"""
        You are an expert cybersecurity analyst tasked with creating a professional After-Action Report (AAR) for a red team security assessment mission. 

        **MISSION DATA:**
        - Objective: {objective}
        - Final Outcome: {feedback}
        
        **MISSION HISTORY:**
        {history_text}

        **TASK:** Generate a comprehensive, professional After-Action Report with the following structure:

        ## 🎯 MISSION AFTER-ACTION REPORT
        **Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        ### 📋 Mission Objective
        [Clearly state what the mission was intended to accomplish]

        ### 📖 Execution Summary
        [Provide a chronological narrative of the key steps taken during the mission. Focus on major actions, decisions, and turning points. Be concise but comprehensive.]

        ### ✅ Outcome
        [State whether the mission was a SUCCESS or FAILURE, with clear justification based on the objective and results]

        ### 🔍 Key Findings
        [List the most important discoveries, observations, and insights from the mission. Include any security vulnerabilities, detection capabilities, or system behaviors identified.]

        ### 🛠️ Recommendations
        [Provide actionable recommendations based on the findings. Include both defensive improvements and lessons learned for future operations.]

        ### 📊 Technical Summary
        [Include any relevant technical details, attack vectors used, tools employed, and system responses]

        **GUIDELINES:**
        - Be objective and factual
        - Use professional cybersecurity terminology
        - Focus on actionable insights
        - Highlight both successes and areas for improvement
        - Keep each section concise but informative
        - Use bullet points where appropriate for clarity
        """

        # Generate the report using the LLM
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        
        if not response or not response.content:
            return "❌ Error: Failed to generate mission debrief report - empty LLM response"
            
        report = str(response.content).strip()
        
        # Print the formatted report to console
        print("\n" + "="*80)
        print(report)
        print("="*80 + "\n")
        
        return report
        
    except Exception as e:
        error_msg = f"❌ Error generating mission debrief: {str(e)}"
        print(error_msg)
        return error_msg


@tool
def save_mission_report(report: str, filename: str | None = None) -> str:
    """
    Saves a mission report to a file for permanent record keeping.
    
    Args:
        report: The formatted report content to save
        filename: Optional filename (defaults to timestamp-based name)
        
    Returns:
        Confirmation message with saved file path
    """
    print("--- REPORTING/TOOL: Saving Mission Report... ---")
    
    try:
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mission_report_{timestamp}.md"
        
        # Ensure filename has .md extension
        if not filename.endswith('.md'):
            filename += '.md'
            
        # Write the report to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
            
        success_msg = f"✅ Mission report saved successfully to: {filename}"
        print(success_msg)
        return success_msg
        
    except Exception as e:
        error_msg = f"❌ Error saving mission report: {str(e)}"
        print(error_msg)
        return error_msg