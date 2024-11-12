from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import requests

def load_data(file_path):
    loader = TextLoader(file_path)
    documents = loader.load()
    return documents

def create_vector_store(documents):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store

def retrieve_data():
    """Retrieve relevant data from external sources."""
    # Example URLs
    urls = [
        "https://www.freecodecamp.org/news/sense-walkthrough-hackthebox/",
        "https://medium.com/@heyrm/usage-machine-hackthebox-writeup-journey-through-exploitation-16397895490f"
    ]
    data = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            data.append(response.text)
        else:
            print(f"Failed to retrieve data from {url}")
    return data
    