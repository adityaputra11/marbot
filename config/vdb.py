import os
import hashlib
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document




QDRANTKEY=os.getenv("QDRANT_API_KEY")
QDRANTAPIBASE= os.getenv("QDRANT_API_BASE")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
print(QDRANTAPIBASE)
print(QDRANTKEY)

client = QdrantClient(
    url=QDRANTAPIBASE, 
    api_key=QDRANTKEY,
    timeout=120
)

def get_client():
    return client

def get_collections():
    return client.get_collections()

def create_collection(name:str):
    return client.recreate_collection(
    collection_name=name,
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
)
    
def get_vector_store(name:str):
    vector_store = QdrantVectorStore(
    client=client,
    collection_name=name,
    embedding=embeddings,
    )
    return vector_store

def generate(name:str,text: str):
    return get_vector_store(name).add_texts([text])

def retrieval(name:str, query: str):
    return  get_vector_store(name).similarity_search(query)

def hash_file(filepath: str) -> str:
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()
    

def check_duplicate_file(path: str, name: str) -> bool:
    collections_response = client.get_collections()
    collections = collections_response.collections
    exists = any(c.name == name for c in collections)

    if not exists:
        create_collection(name)

    file_hash = hash_file(path)
    result = client.scroll(
        collection_name=name,
        scroll_filter=Filter(
            must=[FieldCondition(key="source_id", match=MatchValue(value=file_hash))]
        )
    )

    is_duplicate = len(result[0]) > 0
    return is_duplicate 
def generate_from_file(path:str, name:str):
        if check_duplicate_file(path, name):
             return 
        with open(path, "r") as f:
            text = f.read()
        
        file_hash = hash_file(path)
        print(file_hash)

        doc = Document(page_content=text, metadata={"source_id": file_hash})
        print(f"doc:{doc}")

        # split dan insert
        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
        all_splits = splitter.split_documents([doc])

        # insert ke Qdrant
        _ = get_vector_store(name).add_documents(documents=all_splits)
        return


        