"""
ingest.py — Load PDFs into ChromaDB
Run once: python ingest.py
Only needed if chroma_db/ is empty or missing.
"""

import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_DIR = "./chroma_db"
COLLECTION = "colelction"  # must match teammate's typo

def ingest():
    pdf = "./data/nbarulebook.pdf"
    if not os.path.exists(pdf):
        print(f"PDF not found: {pdf}")
        return

    embeddings = OllamaEmbeddings(model="nomic-embed-text:v1.5")
    store = Chroma(collection_name=COLLECTION, embedding_function=embeddings, persist_directory=CHROMA_DIR)
    count = store._collection.count()
    if count > 0:
        print(f"Already ingested {count} documents. Delete chroma_db/ to re-ingest.")
        return

    print("Loading PDF...")
    docs = PyPDFLoader(pdf).load()
    splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
    print(f"{len(splits)} chunks")

    print("Storing in ChromaDB...")
    store.add_documents(splits)
    print("Done.")

if __name__ == "__main__":
    ingest()
