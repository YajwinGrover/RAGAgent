"""
tools/vector_tool.py
ChromaDB search tool. Uses Ollama embeddings to match teammate's setup.
Collection name "colelction" kept exactly as teammate created it.
"""

import os
from langchain_core.tools import tool

CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
COLLECTION_NAME = "colelction"  # teammate's typo — do not fix, must match existing DB

_store = None


def _get_store():
    global _store
    if _store is None:
        from langchain_ollama import OllamaEmbeddings
        from langchain_chroma import Chroma
        embeddings = OllamaEmbeddings(model="nomic-embed-text:v1.5")
        _store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_DIR,
        )
    return _store


@tool
def search_vector_db(query: str, num_results: int | str = 3) -> str:
    """
    Search the NBA rulebook stored in ChromaDB using semantic similarity.
    Use this for any questions about NBA rules, fouls, violations, or regulations.
    
    Args:
        query: What to search for, e.g. 'flagrant foul definition' or 'shot clock rules'
        num_results: How many chunks to return (1-5, default 3)
    
    Returns:
        Relevant rule text chunks from the NBA rulebook.
    """
    num_results = max(1, min(5, int(num_results)))
    try:
        store = _get_store()
        docs = store.similarity_search(query, k=num_results)
        if not docs:
            return f"No results found in rulebook for: '{query}'"

        results = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "NBA Rulebook")
            page = doc.metadata.get("page", "")
            page_str = f" | Page {page}" if page else ""
            results.append(f"[Chunk {i} — {source}{page_str}]\n{doc.page_content}")

        return (
            f"Vector DB Results for '{query}'\n"
            f"Source: NBA Rulebook (ChromaDB)\n"
            f"{'─' * 50}\n\n"
            + "\n\n".join(results)
        )
    except Exception as e:
        return (
            f"ChromaDB error: {e}\n"
            "Make sure Ollama is running: ollama serve\n"
            "And nomic-embed-text is pulled: ollama pull nomic-embed-text:v1.5"
        )
