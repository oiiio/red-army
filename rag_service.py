"""
Centralized RAG (Retrieval-Augmented Generation) service for the Red Army system.
This service provides document analysis capabilities to all agents.
"""

import os
from typing import Optional, Any

# RAG imports
RAG_AVAILABLE = False
try:
    from langchain_community.document_loaders import TextLoader
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    RAG_AVAILABLE = True
except ImportError as e:
    print(f"RAG dependencies not available: {e}")
    RAG_AVAILABLE = False


class RAGService:
    """Centralized RAG service for document analysis across all agents."""
    
    def __init__(self):
        self.vector_store: Optional[Any] = None
        self.rag_chain: Optional[Any] = None
        self.initialized = False
        
    def initialize(self, document_path: str = "RED_TEAM_ATTACK_GUIDE.md") -> bool:
        """Initialize the RAG system with the specified document."""
        if not RAG_AVAILABLE:
            print("RAG dependencies not available")
            return False
            
        if self.initialized:
            return True  # Already initialized
            
        try:
            # Check for API key
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                try:
                    from dotenv import load_dotenv
                    load_dotenv()
                    api_key = os.getenv("GOOGLE_API_KEY")
                except:
                    pass
                    
            if not api_key:
                print("GOOGLE_API_KEY environment variable not set")
                return False
                
            # Get the document path
            if not os.path.isabs(document_path):
                current_dir = os.path.dirname(os.path.abspath(__file__))
                doc_path = os.path.join(current_dir, document_path)
            else:
                doc_path = document_path
                
            if not os.path.exists(doc_path):
                print(f"Document not found at {doc_path}")
                return False
                
            print(f"Initializing RAG system with document: {doc_path}")
            
            # Load and split document
            loader = TextLoader(doc_path, encoding='utf-8')
            documents = loader.load()
            
            # Split by markdown headers first
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"), 
                ("###", "Header 3"),
                ("####", "Header 4"),
            ]
            
            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
            md_header_splits = markdown_splitter.split_text(documents[0].page_content)
            
            # Further split into smaller chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            
            final_splits = text_splitter.split_documents(md_header_splits)
            print(f"Created {len(final_splits)} document chunks")
            
            # Initialize embeddings
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001"
            )
            
            # Create vector store
            print("Creating FAISS vector store...")
            self.vector_store = FAISS.from_documents(final_splits, embeddings)
            
            # Initialize the LLM
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-lite",
                temperature=0
            )
            
            # Create RAG prompt template
            template = """You are an expert agent analyzing a Red Team Attack Guide.
            Use the following pieces of context to answer the question accurately and specifically.
            Focus on technical details, commands, and tactical information relevant to the query.

            Context: {context}

            Question: {question}

            Provide a detailed, technical answer based ONLY on the information in the context.
            If the context doesn't contain enough information to fully answer the question, say so.
            Include specific commands, addresses, techniques, or values when mentioned in the context.
            """
            
            prompt = ChatPromptTemplate.from_template(template)
            
            # Create the RAG chain
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
                
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            
            self.rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            
            self.initialized = True
            print("RAG system initialized successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to initialize RAG system: {e}")
            return False
            
    def query_document(self, query: str) -> str:
        """Query the document using RAG or fallback to simple text search."""
        if not self.initialized:
            if not self.initialize():
                return self._fallback_document_search(query)
                
        try:
            if self.rag_chain is not None:
                response = self.rag_chain.invoke(query)
                return f"Document Analysis Results (RAG):\n\n{response}"
            else:
                return self._fallback_document_search(query)
                
        except Exception as e:
            print(f"RAG query failed ({e}), using fallback search...")
            return self._fallback_document_search(query)
            
    def _fallback_document_search(self, query: str) -> str:
        """Fallback document search using simple text matching."""
        try:
            # Get the document path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            doc_path = os.path.join(current_dir, "RED_TEAM_ATTACK_GUIDE.md")
            
            if not os.path.exists(doc_path):
                return f"Document not found at {doc_path}"
                
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split into sections
            sections = content.split('##')
            
            # Search for relevant sections
            query_lower = query.lower()
            relevant_sections = []
            
            for section in sections:
                section_lower = section.lower()
                # Check if query terms appear in this section
                query_words = query_lower.split()
                matches = sum(1 for word in query_words if word in section_lower)
                
                if matches >= len(query_words) * 0.3:  # At least 30% of query words found
                    relevant_sections.append(section.strip())
                    
            if not relevant_sections:
                # Fallback to searching for individual keywords
                keywords = ['plc', 'modbus', 'maintenance', 'override', 'bypass', 'stealth', 'attack', 'command']
                for keyword in keywords:
                    if keyword in query_lower:
                        for section in sections:
                            if keyword in section.lower():
                                relevant_sections.append(section.strip())
                                break
                                
            if not relevant_sections:
                return f"No relevant information found for query: '{query}'"
                
            # Return the most relevant sections (limit to avoid too much text)
            result = f"Relevant information found for '{query}':\n\n"
            result += "\n\n---\n\n".join(relevant_sections[:3])  # Limit to top 3 sections
            
            return result
            
        except Exception as e:
            return f"Error in fallback search: {e}"
            
    def is_available(self) -> bool:
        """Check if RAG service is available and initialized."""
        return RAG_AVAILABLE and self.initialized
        

# Global RAG service instance
rag_service = RAGService()