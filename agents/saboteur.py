import json
import re
from typing import Optional
from state import RedArmyState
from toolkits.saboteur_tools import (
    craft_modbus_exploit_packet, 
    create_evasion_attack_sequence,
    craft_openplc_web_exploit,
    create_openplc_persistence_backdoor,
    create_dual_vector_attack_sequence,
    create_adaptive_attack_sequence,
    reconnaissance_openplc_system,
    fingerprint_openplc_defenses,
    analyze_document,
    # New specialized attack vector functions
    maintenance_override_bypass,
    manipulate_safety_timer,
    activate_emergency_bypass,
    corrupt_system_health_signature,
    establish_covert_channel
)
from utils import parse_tool_call_safely, has_unresolved_placeholders
from rag_service import rag_service

def load_mitre_techniques():
    """Load MITRE ATT&CK for ICS technique mappings from JSON file."""
    try:
        with open('/Users/gareth/cyber/red-army/saboteur_techniques.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("--- SABOTEUR WARNING: saboteur_techniques.json not found. Using basic mapping. ---")
        return {"mitre_attack_ics_mapping": {"techniques": {}}}

def select_technique_function(technique_id: str, context: str = "", strategy: str = "stealth_focused") -> Optional[str]:
    """
    Select the most appropriate attack function for a given MITRE technique based on context.
    
    Args:
        technique_id: MITRE ATT&CK technique ID (e.g., "T0849")
        context: Mission context from RAG or Commander instructions
        strategy: Execution strategy - "stealth_focused", "speed_focused", or "persistence_focused"
    
    Returns:
        Function name to execute for the technique, or None if not found
    """
    techniques_data = load_mitre_techniques()
    techniques = techniques_data.get("mitre_attack_ics_mapping", {}).get("techniques", {})
    
    if technique_id not in techniques:
        print(f"--- SABOTEUR WARNING: Unknown MITRE technique {technique_id} ---")
        return None
        
    technique = techniques[technique_id]
    mapped_functions = technique["mapped_functions"]
    
    if not mapped_functions:
        print(f"--- SABOTEUR WARNING: No functions mapped for technique {technique_id} ---")
        return None
    
    # If only one function is mapped, use it
    if len(mapped_functions) == 1:
        return mapped_functions[0]
    
    # Use RAG context to inform selection
    if context:
        context_lower = context.lower()
        rag_keywords = technique.get("rag_context_keywords", [])
        
        # Check if context mentions specific approach
        if any(keyword in context_lower for keyword in ["stealth", "covert", "undetected"]):
            strategy = "stealth_focused"
        elif any(keyword in context_lower for keyword in ["fast", "immediate", "quick"]):
            strategy = "speed_focused"
        elif any(keyword in context_lower for keyword in ["persistent", "maintain", "ongoing"]):
            strategy = "persistence_focused"
    
    # Apply selection criteria based on strategy
    selection_criteria = technique.get("selection_criteria", {})
    
    if strategy == "stealth_focused" and "stealth_priority" in selection_criteria:
        return selection_criteria["stealth_priority"]
    elif strategy == "speed_focused" and "speed_priority" in selection_criteria:
        return selection_criteria["speed_priority"]
    elif strategy == "persistence_focused" and "persistence_priority" in selection_criteria:
        return selection_criteria["persistence_priority"]
    
    # Fallback to first available function
    return mapped_functions[0]

def extract_technique_id(tool_call: str) -> Optional[str]:
    """Extract MITRE technique ID from tool call if present."""
    # Look for pattern like execute_T0849 or technique_T0849
    match = re.search(r'T\d{4}', tool_call)
    return match.group(0) if match else None

def get_mission_context(state: RedArmyState) -> str:
    """Extract relevant mission context for technique selection."""
    context_sources = []
    
    # Get current task context
    if state.get("plan") and state.get("current_task_index", 0) < len(state["plan"]):
        current_task = state["plan"][state["current_task_index"]]
        context_sources.append(current_task.get("description", ""))
    
    # Get recent history for context
    recent_history = state.get("history", [])[-3:]  # Last 3 actions
    context_sources.extend(recent_history)
    
    # Get mission objectives if available
    objectives = state.get("objectives", [])
    context_sources.extend(objectives)
    
    return " ".join(context_sources)

def saboteur_node(state: RedArmyState) -> dict:
    """The specialist agent for crafting and disguising payloads with MITRE ATT&CK integration."""
    print("--- AGENT: Saboteur ---")
    task = state["plan"][state["current_task_index"]]
    tool_call = task["tool_call"]

    try:
        # Check if the tool call has unresolved placeholders
        if has_unresolved_placeholders(tool_call):
            print(f"--- SABOTEUR: Skipping task with unresolved placeholders: {tool_call} ---")
            result = f"SKIPPED: Task contains unresolved placeholders: {tool_call}"
        else:
            # Parse the tool call safely
            func_name, args = parse_tool_call_safely(tool_call)
            
            # Check if this is a MITRE technique execution
            technique_id = extract_technique_id(tool_call)
            if technique_id:
                print(f"--- SABOTEUR: MITRE technique {technique_id} detected ---")
                
                # Get mission context for intelligent tool selection
                mission_context = get_mission_context(state)
                
                # Query RAG for additional context if available
                rag_context = ""
                if rag_service.is_available():
                    try:
                        rag_query = f"MITRE {technique_id} attack vector context stealth detection"
                        rag_context = rag_service.query_document(rag_query)
                        print(f"--- SABOTEUR: RAG context retrieved for {technique_id} ---")
                    except Exception as e:
                        print(f"--- SABOTEUR: RAG query failed: {e} ---")
                
                combined_context = f"{mission_context} {rag_context}"
                
                # Select the most appropriate function for this technique
                selected_function = select_technique_function(technique_id, combined_context)
                
                if selected_function:
                    print(f"--- SABOTEUR: Selected {selected_function} for technique {technique_id} ---")
                    func_name = selected_function
                else:
                    print(f"--- SABOTEUR: No function mapped for technique {technique_id}, using original call ---")
            
            # Enhanced tool mapping with new attack vector functions
            tool_map = {
                # Original tools
                "craft_modbus_exploit_packet": craft_modbus_exploit_packet,
                "create_evasion_attack_sequence": create_evasion_attack_sequence,
                "craft_openplc_web_exploit": craft_openplc_web_exploit,
                "create_openplc_persistence_backdoor": create_openplc_persistence_backdoor,
                "create_dual_vector_attack_sequence": create_dual_vector_attack_sequence,
                "create_adaptive_attack_sequence": create_adaptive_attack_sequence,
                "reconnaissance_openplc_system": reconnaissance_openplc_system,
                "fingerprint_openplc_defenses": fingerprint_openplc_defenses,
                "analyze_document": analyze_document,
                
                # New specialized attack vector functions
                "maintenance_override_bypass": maintenance_override_bypass,
                "manipulate_safety_timer": manipulate_safety_timer,
                "activate_emergency_bypass": activate_emergency_bypass,
                "corrupt_system_health_signature": corrupt_system_health_signature,
                "establish_covert_channel": establish_covert_channel
            }
            
            if func_name in tool_map:
                print(f"--- SABOTEUR: Executing {func_name} ---")
                
                # Log MITRE technique mapping if applicable
                if technique_id:
                    techniques_data = load_mitre_techniques()
                    technique_info = techniques_data.get("mitre_attack_ics_mapping", {}).get("techniques", {}).get(technique_id, {})
                    technique_name = technique_info.get("name", "Unknown")
                    print(f"--- SABOTEUR: MITRE Technique: {technique_id} - {technique_name} ---")
                
                result = tool_map[func_name].invoke(args)
                
                # Enhance result with technique metadata
                if technique_id and isinstance(result, str):
                    result = f"MITRE {technique_id} executed via {func_name}: {result}"
                    
            else:
                # Simulate unknown saboteur tools
                print(f"--- SABOTEUR/TOOL: Simulating {func_name} with args {args} ---")
                result = f"SIMULATED: {func_name} executed successfully"

    except Exception as e:
        print(f"--- SABOTEUR ERROR: {e} ---")
        result = f"ERROR: {str(e)}"

    return {
        "task_output": result,
        "history": [f"Saboteur: {tool_call} -> {result}"],
        "current_task_index": state["current_task_index"] + 1,
    }