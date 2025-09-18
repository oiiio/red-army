# toolkits/infiltrator_tools.py

from dotenv import load_dotenv
import nmap
import subprocess
import json
import os
from langchain_core.tools import tool
from shared_tools import analyze_document

# This module contains the toolkit for the Infiltrator Agent.
# Note: analyze_document is imported from shared_tools for consistency across agents

@tool
def discover_docker_networks() -> str:
    """
    Discovers Docker networks and their associated containers for red teaming.
    Specifically looks for networks with PLCs and SCADA systems.
    
    Returns:
        A string detailing discovered Docker networks and their subnets.
    """
    print("--- INFILTRATOR/TOOL: Discovering Docker networks... ---")
    try:
        # Get Docker networks
        result = subprocess.run(['docker', 'network', 'ls', '--format', 'json'], 
                              capture_output=True, text=True, check=True)
        
        networks = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                networks.append(json.loads(line))
        
        # Filter for relevant networks (exclude default ones)
        relevant_networks = [n for n in networks if n['Name'] not in ['bridge', 'host', 'none']]
        
        network_info = []
        for network in relevant_networks:
            # Get detailed network info
            inspect_result = subprocess.run(['docker', 'network', 'inspect', network['Name']], 
                                          capture_output=True, text=True, check=True)
            network_details = json.loads(inspect_result.stdout)[0]
            
            # Extract subnet and containers
            subnet = "Unknown"
            if network_details.get('IPAM', {}).get('Config'):
                subnet = network_details['IPAM']['Config'][0].get('Subnet', 'Unknown')
            
            containers = list(network_details.get('Containers', {}).keys())
            container_names = [network_details['Containers'][c]['Name'] for c in containers]
            
            network_info.append(f"Network: {network['Name']} | Subnet: {subnet} | Containers: {container_names}")
        
        if not network_info:
            return "No relevant Docker networks found for targeting."
        
        return f"Docker networks discovered:\n" + "\n".join(network_info)
        
    except subprocess.CalledProcessError as e:
        return f"Error discovering Docker networks: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

@tool
def scan_docker_network_for_targets() -> str:
    """
    Automatically discovers and scans Docker networks for PLC and SCADA targets.
    Focuses on the local red teaming simulation environment.
    
    Returns:
        A string detailing discovered targets with their IP addresses and open ports.
    """
    print("--- INFILTRATOR/TOOL: Scanning Docker networks for targets... ---")
    try:
        # First discover the networks
        discovery_result = discover_docker_networks.invoke({})
        print(f"Network discovery: {discovery_result}")
        
        # For red teaming simulation, we need to scan both internal Docker IPs and host-exposed ports
        results = ["=== DOCKER TARGET SCAN RESULTS ===\n"]
        results.append("NETWORK TOPOLOGY:")
        results.append(discovery_result)
        results.append("\nTARGET ANALYSIS:")
        
        # Check for exposed services on localhost (host-mapped ports)
        print("Scanning host-exposed services...")
        host_scan = scan_network_for_plcs.invoke({"subnet": "127.0.0.1/32"})
        results.append("Host-exposed services:")
        results.append(host_scan)
        
        # Try to get container details for intelligence gathering
        try:
            container_result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                                            capture_output=True, text=True, check=True)
            
            results.append("\nCONTAINER INTELLIGENCE:")
            for line in container_result.stdout.strip().split('\n'):
                if line.strip():
                    container = json.loads(line)
                    if any(keyword in container['Names'].lower() or keyword in container['Image'].lower() 
                          for keyword in ['plc', 'scada', 'modbus', 'openplc']):
                        results.append(f"  TARGET: {container['Names']}")
                        results.append(f"    Image: {container['Image']}")
                        results.append(f"    Ports: {container['Ports']}")
                        results.append(f"    Status: {container['Status']}")
        
        except subprocess.CalledProcessError:
            results.append("Could not gather detailed container intelligence")
        
        # Add tactical recommendations
        results.append("\nTACTICAL ASSESSMENT:")
        results.append("- OpenPLC Runtime detected on localhost:8080 and localhost:502")
        results.append("- Recommendation: Attack via localhost interface (host-exposed ports)")
        results.append("- Modbus protocol available on port 502 for PLC manipulation")
        results.append("- Web interface on port 8080 for configuration access")
        results.append("- Stealth consideration: Anomaly detector present in network")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"Error scanning Docker networks: {e}"

@tool 
def reconnaissance_docker_environment() -> str:
    """
    Performs comprehensive reconnaissance of the Docker environment for red teaming.
    This is the primary infiltration tool for Docker-based SCADA simulations.
    
    Returns:
        A detailed intelligence report of the target environment.
    """
    print("--- INFILTRATOR/TOOL: Performing comprehensive Docker environment reconnaissance... ---")
    
    try:
        intelligence_report = ["=== DOCKER ENVIRONMENT RECONNAISSANCE REPORT ===\n"]
        
        # Phase 1: Container Discovery
        print("Phase 1: Discovering running containers...")
        container_result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'], 
                                        capture_output=True, text=True, check=True)
        intelligence_report.append("RUNNING CONTAINERS:")
        intelligence_report.append(container_result.stdout)
        intelligence_report.append("")
        
        # Phase 2: Network Discovery
        print("Phase 2: Discovering Docker networks...")
        network_discovery = discover_docker_networks.invoke({})
        intelligence_report.append("NETWORK TOPOLOGY:")
        intelligence_report.append(network_discovery)
        intelligence_report.append("")
        
        # Phase 3: Target Scanning
        print("Phase 3: Scanning for SCADA/PLC targets...")
        target_scan = scan_docker_network_for_targets.invoke({})
        intelligence_report.append("TARGET ANALYSIS:")
        intelligence_report.append(target_scan)
        intelligence_report.append("")
        
        # Phase 4: Tactical Assessment
        intelligence_report.append("TACTICAL ASSESSMENT:")
        intelligence_report.append("- Primary Target: OpenPLC Runtime (likely at 172.19.0.3:8080/502)")
        intelligence_report.append("- Secondary Targets: SCADA HMI and Dashboard systems")
        intelligence_report.append("- Network: gridguard_dtt_control_network (172.19.0.0/16)")
        intelligence_report.append("- Recommended Attack Vector: Modbus protocol exploitation via port 502")
        intelligence_report.append("- Stealth Consideration: Anomaly detector present - use evasive techniques")
        
        return "\n".join(intelligence_report)
        
    except Exception as e:
        return f"Reconnaissance failed: {e}"

@tool
def scan_network_for_plcs(subnet: str) -> str:
    """
    Scans the specified network subnet for devices with Modbus port 502 and OpenPLC port 8080 open.
    This is optimized for red teaming Docker-based SCADA simulations.

    Args:
        subnet: The network subnet to scan in CIDR notation (e.g., '172.19.0.0/16').

    Returns:
        A string detailing the findings, including IP addresses and open ports for potential targets.
    """
    print(f"--- INFILTRATOR/TOOL: Scanning network {subnet} for SCADA/PLC targets... ---")
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        return "Nmap not found. Please ensure nmap is installed and in your system's PATH."

    # For Docker networks, be more efficient by scanning smaller ranges or specific hosts
    # If it's a /16 network, focus on the common Docker range where containers typically reside
    # For localhost, scan directly
    if subnet == "127.0.0.1/32" or subnet == "localhost":
        target_range = "localhost"
        print(f"Scanning localhost for exposed Docker services...")
    elif "/16" in subnet:
        base_ip = subnet.split("/")[0].rsplit(".", 1)[0]  # e.g., "172.19.0" from "172.19.0.0/16"
        target_range = f"{base_ip}.1-20"  # Extended range to catch typical Docker container IPs
        print(f"Optimizing scan for Docker network - targeting: {target_range}")
    else:
        target_range = subnet

    # Scan for both Modbus (502) and OpenPLC web interface (8080) ports
    # Also include common SCADA ports for comprehensive reconnaissance
    target_ports = "502,8080,5001,80"
    scan_results = nm.scan(hosts=target_range, arguments=f'-p {target_ports} --open -T4 --host-timeout 10s')

    targets_found = {}
    if 'scan' in scan_results:
        for host in scan_results['scan']:
            host_ports = []
            if 'tcp' in scan_results['scan'][host]:
                tcp_ports = scan_results['scan'][host]['tcp']
                for port in tcp_ports:
                    if tcp_ports[port]['state'] == 'open':
                        service = tcp_ports[port].get('name', 'unknown')
                        host_ports.append(f"{port}/{service}")
                
                if host_ports:
                    targets_found[host] = host_ports

    if not targets_found:
        return f"Scan complete. No SCADA/PLC targets found on network {subnet} (scanned range: {target_range})."

    # Format results for red team intelligence
    results = [f"Network reconnaissance complete for {subnet}:"]
    for host, ports in targets_found.items():
        port_info = ", ".join(ports)
        target_type = "CRITICAL TARGET" if any("502" in p or "8080" in p for p in ports) else "Secondary Target"
        results.append(f"  {target_type}: {host} | Open ports: {port_info}")
        
        # Add tactical intelligence
        if any("502" in p for p in ports):
            results.append(f"    ↳ Modbus interface detected - PLC access possible")
        if any("8080" in p for p in ports):
            results.append(f"    ↳ Web interface detected - likely OpenPLC runtime")

    return "\n".join(results)