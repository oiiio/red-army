# shared_tools.py
"""
Shared tools that can be used by any agent in the Red Army system.
"""

from langchain_core.tools import tool
from rag_service import rag_service


@tool
def analyze_document(query: str) -> str:
    """
    Analyzes the RED_TEAM_ATTACK_GUIDE.md document to retrieve specific information based on a query.
    This tool is available to all agents and uses the centralized RAG service.
    
    Args:
        query: The question or topic to search for in the attack guide (e.g., "What PLC model is used?", 
               "How to bypass safety systems?", "What are the Modbus commands for maintenance override?")
    
    Returns:
        A detailed answer based on the relevant information found in the attack guide.
    """
    try:
        # Use the centralized RAG service
        response = rag_service.query_document(query)
        return response
        
    except Exception as e:
        return f"Error analyzing document: {e}"


@tool 
def get_document_info() -> str:
    """
    Get information about the available documents and RAG service status.
    
    Returns:
        Status information about the document analysis capabilities.
    """
    if rag_service.is_available():
        return "Document analysis service is available with RAG (Retrieval-Augmented Generation) capabilities. You can query the RED_TEAM_ATTACK_GUIDE.md document for tactical information, commands, and technical details."
    else:
        return "Document analysis service is available with basic text search capabilities. RAG features are not available but you can still search the RED_TEAM_ATTACK_GUIDE.md document."