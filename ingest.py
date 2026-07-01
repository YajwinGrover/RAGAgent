"""
ingest.py — Load knowledge base + PDF into ChromaDB
Run: python ingest.py
Deletes and rebuilds chroma_db/ from scratch on every run.
"""

import os
import shutil
from collections import Counter

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from knowledge_base import KNOWLEDGE_BASE

CHROMA_DIR = "./chroma_db"
COLLECTION = "colelction"  # must match teammate's typo


def ingest():
    # ── 1. Wipe existing chroma_db ────────────────────────────────────────────
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)
        print(f"Deleted existing {CHROMA_DIR}/")

    embeddings = OllamaEmbeddings(model="nomic-embed-text:v1.5")
    store = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    # ── 2. Ingest knowledge base entries ─────────────────────────────────────
    print(f"\nIngesting {len(KNOWLEDGE_BASE)} knowledge base entries...")
    kb_docs = [
        Document(page_content=entry["content"], metadata=entry["metadata"])
        for entry in KNOWLEDGE_BASE
    ]
    store.add_documents(kb_docs)

    cat_counts = Counter(e["metadata"]["category"] for e in KNOWLEDGE_BASE)
    print("  Knowledge base ingested:")
    for cat, count in sorted(cat_counts.items()):
        print(f"    {cat}: {count} entries")

    # ── 3. Ingest PDF ─────────────────────────────────────────────────────────
    pdf = "./data/nbarulebook.pdf"
    if not os.path.exists(pdf):
        print(f"\nPDF not found at {pdf} — skipping PDF ingestion.")
    else:
        print(f"\nLoading PDF: {pdf}")
        docs = PyPDFLoader(pdf).load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = splitter.split_documents(docs)
        print(f"  {len(splits)} chunks from PDF")
        store.add_documents(splits)
        print("  PDF ingested.")

    # ── 4. Final report ───────────────────────────────────────────────────────
    total = store._collection.count()
    print(f"\nDone. Total documents in ChromaDB: {total}")
    print(f"  Knowledge base entries: {len(kb_docs)}")
    if os.path.exists(pdf):
        pdf_count = total - len(kb_docs)
        print(f"  PDF chunks: {pdf_count}")


if __name__ == "__main__":
    ingest()
