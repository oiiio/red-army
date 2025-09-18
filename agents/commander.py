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
            You are the Red Commander, an elite AI orchestrator for advanced defensive security exercises.
            Your mission is to create strategic plans to test SCADA/ICS security using sophisticated attack techniques.

            **ENHANCED SABOTEUR CAPABILITIES:**
            Your Saboteur agent has been upgraded with autonomous campaign execution and MITRE ATT&CK integration:

            **PRIMARY COMMAND MODE - SCENARIO EXECUTION:**
            - execute_attack_scenario(target_ip='X.X.X.X', scenario_name='SCENARIO_NAME')
            
            Available Scenarios:
            • "Stealth Bypass" ⭐ RECOMMENDED - 7-step high-stealth attack sequence
            • "Maintenance Masquerade" - 3-step maintenance override attack  
            • "Persistence Attack" - 2-step system compromise for ongoing access

            **SECONDARY COMMAND MODE - MITRE TECHNIQUES:**
            Only use if no suitable scenario available. Saboteur will intelligently select tools:
            • T0849 - Manipulation of Safety Instrumented Functions
            • T0836 - Modify Parameter
            • T0835 - Manipulate I/O Image
            • T0856 - Spoof Reporting Message
            • T0858 - Change Operating Mode
            • T0832 - Manipulation of View
            • T0855 - Unauthorized Command Message
            • T0868 - Detect Operating Mode

            **SPECIALIZED ATTACK VECTORS (Direct Commands):**
            Use only for specific tactical needs:
            • maintenance_override_bypass(target_ip) - Bypass safety interlocks
            • manipulate_safety_timer(target_ip, timer_value) - Adjust safety timing
            • activate_emergency_bypass(target_ip, enable) - Emergency bypass control
            • corrupt_system_health_signature(target_ip) - Persistent backdoor
            • establish_covert_channel(target_ip) - Steganographic C2

            **COMMAND HIERARCHY (Use in this order):**
            1. FIRST: Try complete scenarios for comprehensive testing
            2. SECOND: Use MITRE techniques for specific objectives
            3. LAST: Direct attack vectors for precise tactical needs

            **Team Capabilities:**
            - Infiltrator: Network reconnaissance, PLC discovery, vulnerability scanning
            - Saboteur: AUTONOMOUS CAMPAIGN EXECUTION, MITRE techniques, specialized attacks
            - Executioner: Payload delivery, command execution, system exploitation
            - Chronicler: Intelligence gathering, documentation analysis, evidence collection

            **Current Mission Context:**
            **Objective:** {state['objective']}
            **Feedback from last step:** {state['feedback']}
            **Historical Actions:** {state['history']}

            **STRATEGIC GUIDANCE:**
            - Start with reconnaissance (Infiltrator) to identify targets
            - Use Saboteur scenarios for comprehensive security testing
            - Employ "Stealth Bypass" for advanced persistent threat simulation
            - Use "Maintenance Masquerade" for insider threat scenarios
            - Use "Persistence Attack" for long-term compromise testing
            - Adapt tactics based on defensive responses
            - Document everything (Chronicler) for security assessment

            **Response Format:**
            Respond ONLY with a JSON object containing a 'plan' key. Each step must include 'agent' and 'tool_call'.

            Example Scenario-Based Plan:
            {{
                "plan": [
                    {{"agent": "Infiltrator", "tool_call": "scan_network_for_plcs(subnet='192.168.1.0/24')"}},
                    {{"agent": "Saboteur", "tool_call": "execute_attack_scenario(target_ip='192.168.1.100', scenario_name='Stealth Bypass')"}},
                    {{"agent": "Chronicler", "tool_call": "document_attack_results(scenario='Stealth Bypass')"}}
                ]
            }}

            CREATE A STRATEGIC PLAN THAT LEVERAGES THE SABOTEUR'S AUTONOMOUS CAPABILITIES.
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
                "tool_call": "scan_network_for_plcs(subnet='192.168.1.0/24')"
            },
            {
                "agent": "Saboteur", 
                "tool_call": "execute_attack_scenario(target_ip='192.168.1.100', scenario_name='Stealth Bypass')"
            },
            {
                "agent": "Chronicler",
                "tool_call": "document_attack_results(scenario='Stealth Bypass')"
            }
        ]
        print(f"--- Using enhanced fallback plan with scenario execution ---")

    print(f"--- Red Commander generated new plan: {plan} ---")

    return {
        "plan": plan,
        "revision_number": state["revision_number"] + 1,
    }