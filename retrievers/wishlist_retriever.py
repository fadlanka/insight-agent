from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from config.settings import WISHLIST_DB_PATH, TOP_K

def get_wishlist_retriever():
    embeddings = OllamaEmbeddings(model="llama3")
    db = FAISS.load_local(
        WISHLIST_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return db.as_retriever(search_kwargs={"k": TOP_K})
