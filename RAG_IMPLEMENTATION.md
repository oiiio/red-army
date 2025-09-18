# RAG Implementation for Infiltrator Agent

## Overview

The infiltrator agent now includes a powerful `analyze_document` tool that uses Retrieval-Augmented Generation (RAG) to analyze the `RED_TEAM_ATTACK_GUIDE.md` document and provide accurate, context-aware answers to queries.

## Features

### 1. **RAG Pipeline**
- **Document Loading**: Uses `TextLoader` to load the attack guide
- **Text Chunking**: Splits content using `MarkdownHeaderTextSplitter` and `RecursiveCharacterTextSplitter`
- **Embeddings**: Utilizes Google's `models/embedding-001` for vector representation
- **Vector Storage**: Stores embeddings in a FAISS database for efficient retrieval
- **LLM Integration**: Uses Gemini Pro for generating context-aware responses

### 2. **Fallback System**
- **Graceful Degradation**: If RAG dependencies are unavailable, falls back to text-based search
- **Keyword Matching**: Searches document sections based on query terms
- **Reliable Operation**: Always provides some level of document analysis

## Installation

Install the required dependencies:

```bash
pip install langchain langchain-community langchain-google-genai faiss-cpu markdown
```

Set up your Google API key:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

## Usage

### In Agent Code

The infiltrator agent can now handle `analyze_document` tool calls:

```python
# Example tool call in mission plan
{
    "task": "Find maintenance override information",
    "tool_call": "analyze_document(query='What are the Modbus commands for maintenance override?')",
    "agent": "infiltrator"
}
```

### Direct Usage

```python
from toolkits.infiltrator_tools import analyze_document

result = analyze_document.invoke({
    "query": "What PLC model is used in the system?"
})
print(result)
```

## Example Queries

The tool can answer various types of questions about the attack guide:

- **Technical Details**: "What is the maintenance override register address?"
- **Commands**: "What are the Modbus commands for emergency bypass?"
- **Tactics**: "What are the highest stealth level attack methods?"
- **Detection**: "How can attacks be detected by blue teams?"
- **Scenarios**: "What is the recommended stealth bypass scenario?"

## Implementation Details

### RAG Components

1. **Document Ingestion**:
   - Loads `RED_TEAM_ATTACK_GUIDE.md` using TextLoader
   - Splits by markdown headers (H1-H4) for logical sections
   - Further chunks using RecursiveCharacterTextSplitter (1000 chars, 200 overlap)

2. **Vector Database**:
   - Uses FAISS for local vector storage
   - Stores embeddings from Google's embedding model
   - Enables similarity search for relevant chunks

3. **Query Processing**:
   - Retrieves top 4 most relevant document chunks
   - Combines chunks with query in structured prompt
   - Generates response using Gemini Pro

### Fallback System

When RAG is unavailable:
- Performs simple text search across document sections
- Matches query terms to section content
- Returns most relevant sections with basic formatting

## Testing

Test the implementation using the provided test scripts:

```bash
# Test RAG functionality
python test_rag.py

# Test infiltrator agent integration
python test_infiltrator_rag.py
```

## Benefits

1. **Accuracy**: Retrieves specific, relevant information rather than guessing
2. **Context-Aware**: Provides detailed technical answers based on document content
3. **Reliable**: Fallback ensures functionality even without full RAG setup
4. **Efficient**: Vector search enables fast retrieval from large documents
5. **Extensible**: Can easily be adapted to analyze other documents

## Files Modified

- `toolkits/infiltrator_tools.py`: Added RAG implementation and analyze_document tool
- `agents/infiltrator.py`: Added support for analyze_document tool calls
- `test_rag.py`: Test script for RAG functionality  
- `test_infiltrator_rag.py`: Test script for agent integration

## Performance Notes

- **First Query**: Slower due to vector database initialization
- **Subsequent Queries**: Fast retrieval from in-memory FAISS index
- **Memory Usage**: Moderate due to document embeddings storage
- **Fallback**: Lightweight text search with minimal overhead

The RAG implementation transforms the infiltrator agent from making educated guesses to providing accurate, document-based intelligence for red team operations.