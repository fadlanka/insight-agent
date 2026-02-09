import os
import sys

# Ensure project root is on sys.path when running this file directly
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from config.settings import DAILY_DB_PATH

def ingest_daily_log(dir_path):
    # Support legacy JSON logs and new TXT logs
    json_loader = DirectoryLoader(dir_path, glob="*.json", loader_cls=TextLoader)
    txt_loader = DirectoryLoader(dir_path, glob="*.txt", loader_cls=TextLoader)
    docs = json_loader.load() + txt_loader.load()
    if not docs:
        # No data yet; skip ingestion instead of crashing
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model="llama3")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(DAILY_DB_PATH)

if __name__ == "__main__":
    ingest_daily_log("data/daily_logs")
