from typing import TypedDict, Annotated, List
import operator

class RedArmyState(TypedDict):
    """
    Represents the state of the Red Army multi-agent system.
    This is the shared memory that all agents will read from and write to.
    """
    objective: str
    plan: List[dict]
    current_task_index: int
    task_output: str
    feedback: str
    history: Annotated[List[str], operator.add]
    revision_number: int