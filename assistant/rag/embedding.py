import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

def embed_and_store(chunks, persist_directory="vector_store"):
    os.makedirs(persist_directory, exist_ok=True)
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    return vectordb

def load_vectorstore(persist_directory="vector_store"):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    return vectordb
