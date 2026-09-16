from http import client
import logging

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from typing import Dict, List, Optional
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".")
    
    # Look for ChromaDB directories
    # TODO: Create list of directories that match specific criteria (directory type and name pattern)
    candidate_dirs = []
    for d in current_dir.iterdir():
        if not d.is_dir():
            continue

        name_lower = d.name.lower()
        has_chroma_name = "chroma" in name_lower
        has_chroma_db_file = (d / "chroma.sqlite3").exists()
        is_special_project_db = d.name in {"_openai", "demo_chroma_db"}

        if has_chroma_name or has_chroma_db_file or is_special_project_db:
            candidate_dirs.append(d)


    # TODO: Loop through each discovered directory
        # TODO: Wrap connection attempt in try-except block for error handling
        
            # TODO: Initialize database client with directory path and configuration settings
            
            # TODO: Retrieve list of available collections from the database
    for directory in candidate_dirs:
        try:
            client = chromadb.PersistentClient(path=str(directory))
            collections = client.list_collections()

            if not collections:
                key = f"{directory.name}_empty"
                backends[key] = {
                    "directory": str(directory),
                    "collection_name": None,
                    "display_name": f"{directory.name} - no collections yet",
                    "count": 0,
                }
                continue
            # TODO: Loop through each collection found
                # TODO: Create unique identifier key combining directory and collection names
                # TODO: Build information dictionary containing:
                    # TODO: Store directory path as string
                    # TODO: Store collection name
                    # TODO: Create user-friendly display name
                    # TODO: Get document count with fallback for unsupported operations
                # TODO: Add collection information to backends dictionary
            for collection in collections:
                key = f"{directory.name}_{collection.name}"

                try:
                    count = client.get_collection(collection.name).count()
                except Exception:
                    count = "unknown"

                backends[key] = {
                    "directory": str(directory),
                    "collection_name": collection.name,
                    "display_name": f"{directory.name} - {collection.name}",
                    "count": count,
                }
        # TODO: Handle connection or access errors gracefully
            # TODO: Create fallback entry for inaccessible directories
            # TODO: Include error information in display name with truncation
            # TODO: Set appropriate fallback values for missing information
        except Exception as e:
            error_info = str(e)[:50]
            backends[directory.name] = {
                "directory": str(directory),
                "collection_name": None,
                "display_name": f"{directory.name} - Error: {error_info}",
                "count": "unknown",
            }
            logging.warning(f"Failed to access {directory}: {e}")


    # TODO: Return complete backends dictionary with all discovered collections
    print("Discovered ChromaDB backends:", backends)
    return backends

def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""

    if not Path(chroma_dir).exists():
        raise ValueError(f"Chroma directory does not exist: {chroma_dir}")

    # TODO: Create a chomadb persistentclient
    client = chromadb.PersistentClient(path=chroma_dir)        
    
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small",
        api_base="https://openai.vocareum.com/v1"
    )
    # TODO: Return the collection with the collection_name
    collection = client.get_collection(
        name=collection_name,
        embedding_function=openai_ef
    )
    print(f"Initialized RAG system with collection: {collection_name} at {chroma_dir}")  # Debugging statement to confirm initialization
    return collection, True, "RAG system initialized successfully"


def retrieve_documents(collection, query: str, n_results: int = 3, 
                      mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""

    # TODO: Initialize filter variable to None (represents no filtering)
    where_filter = None
    # TODO: Check if filter parameter exists and is not set to "all" or equivalent
    # TODO: If filter conditions are met, create filter dictionary with appropriate field-value pairs
    if mission_filter and mission_filter.lower() not in ["all","any","none"]:
        where_filter = {"mission": mission_filter}
    # TODO: Execute database query with the following parameters:
        # TODO: Pass search query in the required format
        # TODO: Set maximum number of results to return
        # TODO: Apply conditional filter (None for no filtering, dictionary for specific filtering)

    # TODO: Return query results to caller

    try:
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter
            ) 
            print("Query results:", results)  

            return results 
      
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return None


def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""
    
    # TODO: Initialize list with header text for context section

    context_parts = ["#### Retrieved Information:\n"]

    # TODO: Loop through paired documents and their metadata using enumeration
        # TODO: Extract mission information from metadata with fallback value
        # TODO: Clean up mission name formatting (replace underscores, capitalize)
        # TODO: Extract source information from metadata with fallback value  
        # TODO: Extract category information from metadata with fallback value
    
    for i, (doc, meta) in enumerate(zip(documents, metadatas)):
        mission = meta.get("mission", "Unknown Mission")
        mission = mission.replace("_", " ").title()
        source = meta.get("source", "Unknown Source")
        category = meta.get("category", "Unknown Category")
        category = category.replace("_", " ").title()
       
       
        # TODO: Clean up category name formatting (replace underscores, capitalize)
        
        # TODO: Create formatted source header with index number and extracted information
        # TODO: Add source header to context parts list
        
        context_parts.append(f"### Document {i+1} (Mission: {mission}, Source: {source}, Category: {category})\n")


        # TODO: Check document length and truncate if necessary
        # TODO: Add truncated or full document content to context parts list

    max_length = 1000  # Define maximum length for document content
    if len(doc) > max_length:
        doc = doc[:max_length] + "... (truncated)"

        # TODO: Add truncated or full document content to context parts list
    context_parts.append(doc.strip())

    # TODO: Join all context parts with newlines and return formatted string
    print("Formatted context:", "\n".join(context_parts))  
    
    return "\n".join(context_parts)