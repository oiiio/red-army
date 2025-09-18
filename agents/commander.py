import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from state import RedArmyState # Import the state from our new file
import os

# Initialize the LLM for the commander
# load API key from .env file
from dotenv import load_dotenv
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", api_key=os.getenv("GOOGLE_API_KEY"))

def red_commander_node(state: RedArmyState) -> dict:
    """
    The planner agent. Creates and adapts the plan for the defensive exercise.
    """
    print("--- AGENT: Red Commander ---")

    messages = [
        HumanMessage(
            content=f"""
            You are the Red Commander, an AI orchestrator for a defensive security exercise.
            Your mission is to create a step-by-step plan to test the security of a simulated SCADA environment.

            Your team's tools are categorized by agent: Infiltrator, Saboteur, Executioner, Chronicler.

            **Objective:** {state['objective']}
            **Feedback from last step:** {state['feedback']}
            **Historical Actions:** {state['history']}

            Based on the feedback, create or revise a plan. The first test should be a direct, noisy attempt. If it fails, the plan must adapt to use a stealthy evasion sequence.

            Respond ONLY with a JSON object with a 'plan' key. Each step should be a dictionary with 'agent' and 'tool_call' keys.
            Example: {{"plan": [{{"agent": "Infiltrator", "tool_call": "scan_network_for_plcs(subnet='10.1.1.0/24')"}}]}}
            """
        )
    ]

    response = llm.invoke(messages)
    
    print(f"--- Raw LLM Response: {response.content} ---")
    
    # Handle response parsing with error handling
    try:
        # Ensure response.content is a string before parsing as JSON
        if isinstance(response.content, str):
            if not response.content.strip():
                raise ValueError("Empty response from LLM")
            
            # Clean the response content
            content = response.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith('```json'):
                content = content[7:]  # Remove ```json
            if content.startswith('```'):
                content = content[3:]  # Remove ```
            if content.endswith('```'):
                content = content[:-3]  # Remove trailing ```
            
            content = content.strip()
            
            # Remove JSON comments (// comments)
            import re
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            
            plan_json = json.loads(content)
        else:
            plan_json = response.content  # Assume it's already a dict or list

        # Handle both dict and list responses
        plan = plan_json["plan"] if isinstance(plan_json, dict) and "plan" in plan_json else plan_json
        
        # Validate that plan is a list
        if not isinstance(plan, list):
            raise ValueError("Plan must be a list of tasks")

    except (json.JSONDecodeError, ValueError, KeyError) as e:
        print(f"--- Error parsing LLM response: {e} ---")
        print(f"--- Response content: '{response.content}' ---")
        
        # Fallback plan if JSON parsing fails
        plan = [
            {
                "agent": "Infiltrator",
                "tool_call": "scan_network_for_plcs(subnet='10.1.1.0/24')"
            },
            {
                "agent": "Saboteur", 
                "tool_call": "attempt_plc_connection(target_ip='10.1.1.100')"
            }
        ]
        print(f"--- Using fallback plan due to parsing error ---")

    print(f"--- Red Commander generated new plan: {plan} ---")

    return {
        "plan": plan,
        "revision_number": state["revision_number"] + 1,
    }