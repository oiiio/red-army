#!/usr/bin/env python3
"""
Test script for the RAG implementation in the analyze_document tool.
"""

import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from toolkits.infiltrator_tools import analyze_document

def test_analyze_document():
    """Test the analyze_document tool with various queries."""
    
    print("Testing RAG implementation for analyze_document tool")
    print("=" * 50)
    
    # Test queries
    test_queries = [
        "What PLC model is used in the system?",
        "What are the Modbus commands for maintenance override?", 
        "How can I bypass safety systems stealthily?",
        "What is the maintenance override register address?",
        "What are the recommended stealth attack scenarios?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 40)
        
        try:
            result = analyze_document.invoke({"query": query})
            print(f"Result:\n{result}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    # Check if GOOGLE_API_KEY is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY environment variable is not set!")
        print("The RAG system requires this to function properly.")
        print()
    
    test_analyze_document()