import os

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from config.config_handler import config
from rag.document_service import load_documents, split_documents

DB_PATH = config["dirs"]["chroma_db"]
DB_NAME = config["rag"]["collection_name"]
EMBEDDING_MODEL = config["model"]["embed_model"]
BASE_URL = config["model"]["base_url"]

embedding_fun = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=BASE_URL,
)


def init_vector_store():
    # 检查向量数据库是否已存在
    if os.path.exists(DB_PATH):
        print("Loading existing vector database...")
        # 直接加载已有的向量库
        return Chroma(
            persist_directory=str(DB_PATH),
            collection_name=DB_NAME,
            embedding_function=embedding_fun  # 建议加上 embedding 函数
        )
    else:
        print("Creating new vector database...")
        # 读取文档
        documents = load_documents()
        if not documents:  # 检查是否成功读取文档
            raise ValueError("No documents loaded")

        # 分割文档
        chunks = split_documents(documents)
        if not chunks:  # 检查是否成功分割
            raise ValueError("No chunks created from documents")

        # 创建并持久化向量库
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_fun,
            persist_directory=str(DB_PATH),
            collection_name=DB_NAME  # 建议指定 collection_name
        )

        print(f"Vector database created successfully with {len(chunks)} chunks")
        return vector_store
