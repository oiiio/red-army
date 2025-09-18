#!/usr/bin/env python3
"""
Test script to verify that all agents can access the centralized RAG service
through the analyze_document tool.
"""

import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_agent_rag_access():
    """Test that all agents can access the centralized RAG service."""
    
    print("Testing Centralized RAG Service Access Across All Agents")
    print("=" * 65)
    
    # Test agents and their tool imports
    agent_tests = [
        {
            "name": "Infiltrator",
            "import_path": "toolkits.infiltrator_tools",
            "query": "What network reconnaissance tools are mentioned?"
        },
        {
            "name": "Saboteur", 
            "import_path": "toolkits.saboteur_tools",
            "query": "What are the recommended attack vectors for stealth?"
        },
        {
            "name": "Executioner",
            "import_path": "toolkits.executioner_tools", 
            "query": "What Modbus commands should be executed for emergency bypass?"
        },
        {
            "name": "Chronicler",
            "import_path": "toolkits.chronicler_tools",
            "query": "What indicators should be monitored for attack detection?"
        },
        {
            "name": "Shared Tools",
            "import_path": "shared_tools",
            "query": "What is the primary objective of the attack guide?"
        }
    ]
    
    for i, test in enumerate(agent_tests, 1):
        print(f"\n{i}. Testing {test['name']} Agent RAG Access")
        print(f"   Query: '{test['query']}'")
        print("-" * 65)
        
        try:
            # Dynamic import of the analyze_document tool
            module = __import__(test['import_path'], fromlist=['analyze_document'])
            analyze_document = getattr(module, 'analyze_document')
            
            # Test the tool
            result = analyze_document.invoke({"query": test['query']})
            
            # Print a summary (truncated for readability)
            result_summary = result[:300] + "..." if len(result) > 300 else result
            print(f"✅ SUCCESS: {test['name']} can access RAG service")
            print(f"Result preview: {result_summary}")
            
        except ImportError as e:
            print(f"❌ IMPORT ERROR: {test['name']} - {e}")
        except AttributeError as e:
            print(f"❌ ATTRIBUTE ERROR: {test['name']} - analyze_document not found")
        except Exception as e:
            print(f"❌ RUNTIME ERROR: {test['name']} - {e}")
        
        print("-" * 65)

def test_rag_service_directly():
    """Test the RAG service directly."""
    print("\n" + "=" * 40)
    print("Testing RAG Service Directly")
    print("=" * 40)
    
    try:
        from rag_service import rag_service
        
        print(f"RAG Service Available: {rag_service.is_available()}")
        
        if rag_service.is_available():
            result = rag_service.query_document("What is the target PLC system?")
            print(f"Direct RAG Query Result: {result[:200]}...")
        else:
            print("RAG service not available, testing fallback...")
            result = rag_service.query_document("What is the target PLC system?")
            print(f"Fallback Query Result: {result[:200]}...")
            
    except Exception as e:
        print(f"Error testing RAG service directly: {e}")

if __name__ == "__main__":
    test_rag_service_directly()
    test_agent_rag_access()