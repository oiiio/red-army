# toolkits/chronicler_tools.py

import subprocess
import re
from datetime import datetime, timedelta
from langchain_core.tools import tool

# This module contains the toolkit for the Chronicler Agent.

@tool
def analyze_gridguardian_logs(attack_start_time: str | None = None, attack_duration_minutes: int = 60) -> str:
    """
    Analyzes the GridGuardian AI's logs to determine if an attack was detected.
    It connects to the running Docker container to read recent log entries and
    correlates anomaly detection timestamps with the attack timeframe.

    Args:
        attack_start_time: ISO format timestamp of when attack started (e.g., "2025-09-17T18:50:00")
        attack_duration_minutes: Duration of the attack in minutes to check for anomalies

    Returns:
        A string summarizing the analysis: 'FAILURE' if relevant alerts are found,
        'SUCCESS' if no relevant alerts are found during the attack window.
    """
    print("--- CHRONICLER/TOOL: Analyzing GridGuardian logs... ---")

    # --- CONFIGURATION REQUIRED ---
    # Update these variables to match your GridGuardian Docker container setup.
    container_name = "anomaly_detector"  # <-- CHANGE THIS
    log_path = "/usr/src/app/logs/anomaly_detector.log"       # <-- CHANGE THIS
    # --- END CONFIGURATION ---

    try:
        # Read more log lines to capture full anomaly reports (they can be long)
        command = ['docker', 'exec', container_name, 'tail', '-n', '200', log_path]
        result = subprocess.run(
            command,
            capture_output=True, text=True, check=True
        )
        log_output = result.stdout
        print(f"--- CHRONICLER: Fetched {len(log_output.splitlines())} log lines")

        # Parse the logs for anomaly detection reports
        anomaly_reports = _parse_anomaly_reports(log_output)
        
        if not anomaly_reports:
            return "Analysis: SUCCESS. No anomaly detection reports found in recent logs."

        # If attack timeframe is provided, check for correlation
        if attack_start_time:
            relevant_anomalies = _check_anomaly_correlation(
                anomaly_reports, attack_start_time, attack_duration_minutes
            )
            
            if relevant_anomalies:
                return f"Analysis: FAILURE. GridGuardian detected {len(relevant_anomalies)} anomaly report(s) that correlate with the attack timeframe. The attack was likely detected."
            else:
                return "Analysis: SUCCESS. While anomaly reports exist, none correlate with the specified attack timeframe."
        else:
            # Fallback to simple detection check
            recent_anomalies = [report for report in anomaly_reports if _is_recent_report(report)]
            if recent_anomalies:
                return f"Analysis: FAILURE. GridGuardian shows {len(recent_anomalies)} recent anomaly report(s). The attack was likely detected."
            else:
                return "Analysis: SUCCESS. No recent anomaly reports found."

    except FileNotFoundError:
        return "Analysis Error: 'docker' command not found. Is Docker installed and in your system's PATH?"
    except subprocess.CalledProcessError as e:
        return (f"Analysis Error: Could not access logs in container '{container_name}'. "
                f"Is the container name correct and running? Error: {e.stderr}")


def _parse_anomaly_reports(log_output: str) -> list:
    """
    Parses the log output to extract anomaly detection reports.
    
    Returns:
        List of dictionaries containing report metadata and anomaly timestamps.
    """
    reports = []
    lines = log_output.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Look for anomaly detection start markers
        if "🚨 ANOMALY DETECTED!" in line:
            # Extract the report timestamp (when the anomaly detector ran)
            report_time_match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            report_timestamp = report_time_match.group(1) if report_time_match else None
            
            # Collect all anomaly timestamps in this report
            anomaly_timestamps = []
            i += 1
            
            # Continue reading until we find the end marker or another report starts
            while i < len(lines) and "📋 END ANOMALY REPORT" not in lines[i]:
                anomaly_match = re.search(r'⚡ (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+):', lines[i])
                if anomaly_match:
                    anomaly_timestamps.append(anomaly_match.group(1))
                i += 1
            
            if anomaly_timestamps:
                reports.append({
                    'report_timestamp': report_timestamp,
                    'anomaly_timestamps': anomaly_timestamps,
                    'anomaly_count': len(anomaly_timestamps)
                })
        
        i += 1
    
    return reports


def _check_anomaly_correlation(reports: list, attack_start_time: str, duration_minutes: int) -> list:
    """
    Checks if any anomalies in the reports correlate with the attack timeframe.
    
    Returns:
        List of reports that contain anomalies within the attack window.
    """
    try:
        # Parse attack timeframe
        attack_start = datetime.fromisoformat(attack_start_time.replace('T', ' '))
        attack_end = attack_start + timedelta(minutes=duration_minutes)
        
        relevant_reports = []
        
        for report in reports:
            # Check if any anomaly timestamps fall within the attack window
            for anomaly_time_str in report['anomaly_timestamps']:
                try:
                    # Parse anomaly timestamp (may have microseconds)
                    anomaly_time = datetime.strptime(anomaly_time_str[:19], '%Y-%m-%d %H:%M:%S')
                    
                    if attack_start <= anomaly_time <= attack_end:
                        relevant_reports.append(report)
                        break  # Found one anomaly in window, no need to check others in this report
                except ValueError:
                    continue  # Skip malformed timestamps
        
        return relevant_reports
        
    except Exception as e:
        print(f"--- CHRONICLER: Error correlating timestamps: {e}")
        return []


def _is_recent_report(report: dict, minutes_threshold: int = 30) -> bool:
    """
    Checks if a report was generated recently (within threshold minutes).
    """
    if not report['report_timestamp']:
        return False
        
    try:
        report_time = datetime.strptime(report['report_timestamp'], '%Y-%m-%d %H:%M:%S')
        time_diff = datetime.now() - report_time
        return time_diff.total_seconds() / 60 <= minutes_threshold
    except ValueError:
        return False