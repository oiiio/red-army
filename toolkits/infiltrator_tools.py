# toolkits/infiltrator_tools.py

import nmap
from langchain_core.tools import tool

# This module contains the toolkit for the Infiltrator Agent.

@tool
def scan_network_for_plcs(subnet: str) -> str:
    """
    Scans the specified network subnet for devices with Modbus port 502 open.
    This is used to identify potential PLC targets for the operation.

    Args:
        subnet: The network subnet to scan in CIDR notation (e.g., '192.168.1.0/24').

    Returns:
        A string detailing the findings, including a list of IP addresses for potential PLCs.
    """
    print(f"--- INFILTRATOR/TOOL: Scanning network {subnet} for PLCs... ---")
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        return "Nmap not found. Please ensure nmap is installed and in your system's PATH."

    # The '-p 502' argument specifically targets the Modbus protocol port.
    # '--open' ensures we only see hosts where the port is confirmed to be open.
    scan_results = nm.scan(hosts=subnet, arguments='-p 502 --open')

    hosts_found = []
    if 'scan' in scan_results:
        for host in scan_results['scan']:
            if 'tcp' in scan_results['scan'][host] and 502 in scan_results['scan'][host]['tcp']:
                hosts_found.append(host)

    if not hosts_found:
        return "Scan complete. No PLCs found on the network with port 502 open."

    return f"Scan complete. Found potential PLCs at the following IP addresses: {hosts_found}"