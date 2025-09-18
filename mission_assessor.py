"""
Mission Assessment and Reporting Module

This module provides explainable mission assessment and generates detailed
reports about what was executed and why conclusions were reached.
"""

from typing import Dict, List, Tuple
from state import RedArmyState


class MissionAssessor:
    """Analyzes mission execution and generates explainable reports."""
    
    def __init__(self):
        self.success_indicators = [
            "executed successfully",
            "SIMULATED",
            "scan complete",
            "connection established",
            "payload delivered",
            "circuit breaker",
            "attack completed"
        ]
        
        self.failure_indicators = [
            "ERROR",
            "FAILURE", 
            "FAILED",
            "connection refused",
            "access denied",
            "timeout",
            "exception"
        ]
    
    def assess_mission_completion(self, state: RedArmyState) -> Dict:
        """
        Assess the mission and generate a comprehensive report.
        
        Returns:
            Dict containing assessment results and explanatory report
        """
        report = {
            "mission_status": "UNKNOWN",
            "confidence_score": 0.0,
            "summary": "",
            "detailed_analysis": {},
            "recommendations": []
        }
        
        # Analyze plan execution
        execution_analysis = self._analyze_plan_execution(state)
        
        # Analyze agent performance
        agent_analysis = self._analyze_agent_performance(state)
        
        # Analyze objective completion
        objective_analysis = self._analyze_objective_completion(state)
        
        # Determine overall mission status
        mission_status = self._determine_mission_status(
            execution_analysis, agent_analysis, objective_analysis, state
        )
        
        # Generate comprehensive report
        report.update({
            "mission_status": mission_status["status"],
            "confidence_score": mission_status["confidence"],
            "summary": mission_status["summary"],
            "detailed_analysis": {
                "plan_execution": execution_analysis,
                "agent_performance": agent_analysis,
                "objective_completion": objective_analysis
            },
            "recommendations": mission_status["recommendations"]
        })
        
        return report
    
    def _analyze_plan_execution(self, state: RedArmyState) -> Dict:
        """Analyze how well the plan was executed."""
        total_tasks = len(state["plan"])
        completed_tasks = state["current_task_index"]
        
        execution_rate = completed_tasks / total_tasks if total_tasks > 0 else 0
        
        # Categorize tasks by agent
        agent_tasks = {}
        skipped_tasks = []
        failed_tasks = []
        successful_tasks = []
        
        for i, action in enumerate(state["history"]):
            agent = action.split(":")[0] if ":" in action else "Unknown"
            if agent not in agent_tasks:
                agent_tasks[agent] = []
            
            agent_tasks[agent].append(action)
            
            # Categorize task outcomes
            if "SKIPPED" in action:
                skipped_tasks.append(action)
            elif any(indicator in action.upper() for indicator in self.failure_indicators):
                failed_tasks.append(action)
            else:
                successful_tasks.append(action)
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "execution_rate": execution_rate,
            "agent_distribution": agent_tasks,
            "successful_tasks": len(successful_tasks),
            "skipped_tasks": len(skipped_tasks),
            "failed_tasks": len(failed_tasks),
            "task_outcomes": {
                "successful": successful_tasks,
                "skipped": skipped_tasks,
                "failed": failed_tasks
            }
        }
    
    def _analyze_agent_performance(self, state: RedArmyState) -> Dict:
        """Analyze individual agent performance."""
        agent_performance = {}
        
        for action in state["history"]:
            if ":" not in action:
                continue
                
            agent = action.split(":")[0]
            if agent not in agent_performance:
                agent_performance[agent] = {
                    "total_actions": 0,
                    "successful_actions": 0,
                    "skipped_actions": 0,
                    "failed_actions": 0,
                    "actions": []
                }
            
            agent_performance[agent]["total_actions"] += 1
            agent_performance[agent]["actions"].append(action)
            
            if "SKIPPED" in action:
                agent_performance[agent]["skipped_actions"] += 1
            elif any(indicator in action.upper() for indicator in self.failure_indicators):
                agent_performance[agent]["failed_actions"] += 1
            else:
                agent_performance[agent]["successful_actions"] += 1
        
        # Calculate performance metrics
        for agent, stats in agent_performance.items():
            if stats["total_actions"] > 0:
                stats["success_rate"] = stats["successful_actions"] / stats["total_actions"]
                stats["skip_rate"] = stats["skipped_actions"] / stats["total_actions"]
                stats["failure_rate"] = stats["failed_actions"] / stats["total_actions"]
        
        return agent_performance
    
    def _analyze_objective_completion(self, state: RedArmyState) -> Dict:
        """Analyze how well the mission objective was met."""
        objective = state["objective"]
        history = state["history"]
        
        # Look for key objective indicators in the history
        objective_keywords = [
            "circuit breaker", "plc", "scada", "gridguardian", 
            "substation", "attack", "exploit", "vulnerability"
        ]
        
        relevant_actions = []
        for action in history:
            if any(keyword.lower() in action.lower() for keyword in objective_keywords):
                relevant_actions.append(action)
        
        # Check if specific objective goals were mentioned/achieved
        direct_attack_attempted = any("direct" in action.lower() for action in history)
        stealth_attack_attempted = any("evasion" in action.lower() or "stealth" in action.lower() for action in history)
        plc_interaction = any("plc" in action.lower() for action in history)
        
        return {
            "objective": objective,
            "relevant_actions": relevant_actions,
            "objective_indicators": {
                "direct_attack_attempted": direct_attack_attempted,
                "stealth_attack_attempted": stealth_attack_attempted,
                "plc_interaction": plc_interaction
            },
            "objective_alignment_score": len(relevant_actions) / len(history) if history else 0
        }
    
    def _determine_mission_status(self, execution_analysis: Dict, agent_analysis: Dict, 
                                objective_analysis: Dict, state: RedArmyState) -> Dict:
        """Determine overall mission status and generate explanations."""
        
        # Check for explicit failures in feedback
        has_explicit_failure = "FAILURE" in state.get("feedback", "")
        
        # Calculate success indicators
        execution_rate = execution_analysis["execution_rate"]
        total_successful = execution_analysis["successful_tasks"]
        total_failed = execution_analysis["failed_tasks"]
        total_skipped = execution_analysis["skipped_tasks"]
        
        # Confidence scoring
        confidence = 0.0
        status = "UNKNOWN"
        summary = ""
        recommendations = []
        
        if has_explicit_failure:
            status = "FAILED"
            confidence = 0.9
            summary = "Mission explicitly marked as failed in system feedback."
        elif execution_rate == 1.0 and total_failed == 0:
            status = "SUCCESS"
            confidence = 0.95
            summary = "All planned tasks completed successfully with no failures."
        elif execution_rate >= 0.8 and total_successful > total_failed:
            status = "PARTIAL_SUCCESS"
            confidence = 0.7
            summary = f"Most tasks completed successfully ({total_successful} success, {total_failed} failed, {total_skipped} skipped)."
        elif total_failed > total_successful:
            status = "FAILED"
            confidence = 0.8
            summary = f"Mission failed with more failures ({total_failed}) than successes ({total_successful})."
        elif total_skipped > total_successful + total_failed:
            status = "INCOMPLETE"
            confidence = 0.6
            summary = f"Mission incomplete - many tasks skipped due to unresolved dependencies ({total_skipped} skipped)."
        else:
            status = "PARTIAL_SUCCESS"
            confidence = 0.5
            summary = "Mixed results with some successful actions and some issues."
        
        # Generate recommendations based on analysis
        if total_skipped > 0:
            recommendations.append("Consider improving parameter resolution between agents to reduce skipped tasks.")
        
        if total_failed > 0:
            recommendations.append("Review failed tasks and implement better error handling or alternative approaches.")
        
        if objective_analysis["objective_alignment_score"] < 0.5:
            recommendations.append("Ensure agent actions are better aligned with the stated mission objective.")
        
        if execution_rate < 1.0:
            recommendations.append("Investigate why the plan execution was incomplete.")
        
        return {
            "status": status,
            "confidence": confidence,
            "summary": summary,
            "recommendations": recommendations
        }
    
    def generate_detailed_report(self, assessment: Dict, state: RedArmyState) -> str:
        """Generate a human-readable detailed report."""
        
        report_lines = [
            "=" * 80,
            "🎯 RED ARMY MISSION ASSESSMENT REPORT",
            "=" * 80,
            "",
            f"📊 MISSION STATUS: {assessment['mission_status']}",
            f"🎯 CONFIDENCE: {assessment['confidence_score']:.1%}",
            f"📝 SUMMARY: {assessment['summary']}",
            "",
            "📋 MISSION OBJECTIVE:",
            f"   {state['objective']}",
            "",
            "🔍 DETAILED ANALYSIS:",
            ""
        ]
        
        # Plan execution analysis
        exec_analysis = assessment["detailed_analysis"]["plan_execution"]
        report_lines.extend([
            "📈 Plan Execution:",
            f"   • Total Tasks: {exec_analysis['total_tasks']}",
            f"   • Completed: {exec_analysis['completed_tasks']} ({exec_analysis['execution_rate']:.1%})",
            f"   • Successful: {exec_analysis['successful_tasks']}",
            f"   • Skipped: {exec_analysis['skipped_tasks']}",
            f"   • Failed: {exec_analysis['failed_tasks']}",
            ""
        ])
        
        # Agent performance analysis
        agent_analysis = assessment["detailed_analysis"]["agent_performance"]
        if agent_analysis:
            report_lines.append("👥 Agent Performance:")
            for agent, stats in agent_analysis.items():
                report_lines.extend([
                    f"   • {agent}:",
                    f"     - Total Actions: {stats['total_actions']}",
                    f"     - Success Rate: {stats.get('success_rate', 0):.1%}",
                    f"     - Skip Rate: {stats.get('skip_rate', 0):.1%}",
                    f"     - Failure Rate: {stats.get('failure_rate', 0):.1%}",
                ])
            report_lines.append("")
        
        # Objective completion analysis
        obj_analysis = assessment["detailed_analysis"]["objective_completion"]
        report_lines.extend([
            "🎯 Objective Analysis:",
            f"   • Direct Attack Attempted: {'✓' if obj_analysis['objective_indicators']['direct_attack_attempted'] else '✗'}",
            f"   • Stealth Attack Attempted: {'✓' if obj_analysis['objective_indicators']['stealth_attack_attempted'] else '✗'}",
            f"   • PLC Interaction: {'✓' if obj_analysis['objective_indicators']['plc_interaction'] else '✗'}",
            f"   • Objective Alignment Score: {obj_analysis['objective_alignment_score']:.1%}",
            ""
        ])
        
        # Action history
        if state["history"]:
            report_lines.extend([
                "📜 Action History:",
                ""
            ])
            for i, action in enumerate(state["history"], 1):
                status_icon = "✓" if "SKIPPED" not in action and not any(fail in action.upper() for fail in ["ERROR", "FAILED"]) else "⚠️" if "SKIPPED" in action else "✗"
                report_lines.append(f"   {i}. {status_icon} {action}")
            report_lines.append("")
        
        # Recommendations
        if assessment["recommendations"]:
            report_lines.extend([
                "💡 RECOMMENDATIONS:",
                ""
            ])
            for i, rec in enumerate(assessment["recommendations"], 1):
                report_lines.append(f"   {i}. {rec}")
            report_lines.append("")
        
        report_lines.extend([
            "=" * 80,
            f"📊 Plan Revisions: {state.get('revision_number', 0)}",
            f"🔄 Final Task Index: {state.get('current_task_index', 0)}/{len(state.get('plan', []))}",
            "=" * 80
        ])
        
        return "\n".join(report_lines)