# red-army
Quick conceptualization of agent team meant for red teaming SCADA systems with defensive monitors ("agents"). Uses LLMS, RAG, MITRE ATT&CK mapping, 

There are probably terrible race conditions related to how we are handling states

Technically this could be done simply with a commander and executor langgraph nodes, but we take a dedicated agent node + router approach for the sake of demonstration

FAISS seems approriate for text vectorstore

9/18 saboteur now uses MITRE ICS techniques mapped to our attack functions, uses the FAISS store for contextual selection criteria

