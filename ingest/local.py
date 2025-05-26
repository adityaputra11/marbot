import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import Settings

settings = Settings()

def create_vector_store():
    # Inisialisasi embedding model dari HuggingFace
    embeddings = OpenAIEmbeddings(
       model="text-embedding-3-small",
       api_key=settings.ai.open_api_key
    )
    # Load dan split dokumen dari Wikipedia
    loader = WebBaseLoader("https://en.wikipedia.org/wiki/Artificial_intelligence")
    documents = loader.load()
    
    # Split dokumen menjadi chunks yang lebih kecil
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    
    # Buat vector store menggunakan FAISS
    vectorstore = FAISS.from_documents(
        documents=texts,
        embedding=embeddings
    )
    
    # Simpan vector store ke local
    vectorstore.save_local(f"{settings.vectorstore.vectorstore_path}/local")
    
    return vectorstore

def load_vector_store():
    # Load vector store dari local
    embeddings = OpenAIEmbeddings(
       model="text-embedding-3-small",
       api_key=settings.ai.open_api_key
    )
    
    vectorstore = FAISS.load_local(
        f"{settings.vectorstore.vectorstore_path}/local",
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    return vectorstore

def search_similar_docs(query: str, k: int = 4):
    print("Loading vector store...")
    # Load vector store
    vectorstore = load_vector_store()
    
    # Cari dokumen yang mirip
    docs = vectorstore.similarity_search(query, k=k)
    
    return docs
