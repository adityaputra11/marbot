from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings 

embeddings = OpenAIEmbeddings()
vector_store = InMemoryVectorStore(embeddings)


def add_to_vector_store(text: str):
    vector_store.add_texts([text])

def search_vector_store(query: str):
    return vector_store.similarity_search(query)