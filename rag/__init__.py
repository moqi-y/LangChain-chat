"""
RAG模块：负责加载文档、创建向量库和相似度搜索
"""

from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from config import get_rag_config, get_dirs_config, get_model_config

_dirs_config = get_dirs_config()
_rag_config = get_rag_config()
_model_config = get_model_config()

BASE_DIR = Path(_dirs_config.get("data", "data"))
CHROMA_DIR = Path(_dirs_config.get("chroma_db", "data/chroma_db"))
CHUNK_SIZE = _rag_config.get("chunk_size", 500)
CHUNK_OVERLAP = _rag_config.get("chunk_overlap", 50)
TOP_K = _rag_config.get("top_k", 3)
COLLECTION_NAME = _rag_config.get("collection_name", "rag_store")
BASE_URL = _model_config.get("base_url", "http://192.168.1.59:11434")
EMBED_MODEL = _model_config.get("embed_model", "nomic-embed-text")


def load_documents(
    data_dir: str | Path = None,
    encoding: str = "utf-8",
) -> list:
    """
    加载指定目录下的所有txt文档文件

    输入参数:
        data_dir: str | Path, 文件目录路径，默认为项目data目录
        encoding: str, 文件编码格式，默认为utf-8

    返回:
        list: Document对象列表，每个Document包含page_content和metadata
    """
    if data_dir is None:
        data_dir = BASE_DIR
    else:
        data_dir = Path(data_dir)

    documents = []
    for file_path in data_dir.glob("*.txt"):
        loader = TextLoader(str(file_path), encoding=encoding)
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = file_path.name
        documents.extend(docs)

    return documents


def split_documents(
    documents: list,
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> list:
    """
    将文档列表分割成更小的文本块

    输入参数:
        documents: list, Document对象列表
        chunk_size: int, 每个文本块的最大字符数，默认为500
        chunk_overlap: int, 相邻文本块之间的重叠字符数，默认为50

    返回:
        list: 分割后的Document对象列表
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size or CHUNK_SIZE,
        chunk_overlap=chunk_overlap or CHUNK_OVERLAP,
        length_function=len,
    )
    return text_splitter.split_documents(documents)


def create_vector_store(
    chunks: list,
    collection_name: str = None,
    embed_model: str = None,
    base_url: str = None,
) -> Chroma:
    """
    创建Chroma向量数据库

    输入参数:
        chunks: list, 分割后的Document对象列表
        collection_name: str, 向量存储集合的名称，默认为"rag_store"
        embed_model: str, 嵌入模型名称，默认为"nomic-embed-text"
        base_url: str, Ollama服务的基础URL，默认为本地地址

    返回:
        Chroma: Chroma向量存储对象
    """
    embeddings = OllamaEmbeddings(
        model=embed_model or EMBED_MODEL,
        base_url=base_url or BASE_URL,
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name or COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
    )

    return vector_store


def load_or_create_vector_store(
    collection_name: str = None,
    embed_model: str = None,
    base_url: str = None,
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> Chroma:
    """
    加载已存在的向量库或创建新的向量库

    输入参数:
        collection_name: str, 向量存储集合的名称，默认为"rag_store"
        embed_model: str, 嵌入模型名称，默认为"nomic-embed-text"
        base_url: str, Ollama服务的基础URL，默认为本地地址
        chunk_size: int, 文档分块的大小，默认为500
        chunk_overlap: int, 文档分块的重叠大小，默认为50

    返回:
        Chroma: Chroma向量存储对象
    """
    embeddings = OllamaEmbeddings(
        model=embed_model or EMBED_MODEL,
        base_url=base_url or BASE_URL,
    )

    if CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir()):
        vector_store = Chroma(
            collection_name=collection_name or COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=str(CHROMA_DIR),
        )
    else:
        documents = load_documents()
        chunks = split_documents(documents, chunk_size, chunk_overlap)
        vector_store = create_vector_store(
            chunks,
            collection_name,
            embed_model,
            base_url,
        )

    return vector_store


def search_similar(
    query: str,
    k: int = None,
    collection_name: str = None,
) -> list:
    """
    在向量库中搜索与输入查询最相似的文档

    输入参数:
        query: str, 用户输入的查询文本
        k: int, 返回最相似的文档数量，默认为3
        collection_name: str, 向量存储集合的名称，默认为"rag_store"

    返回:
        list: 包含k个字典的列表，每个字典有content(内容)和source(来源)字段
    """
    vector_store = load_or_create_vector_store(collection_name=collection_name)

    results = vector_store.similarity_search(query, k=k or TOP_K)

    return [
        {"content": doc.page_content, "source": doc.metadata.get("source", "")}
        for doc in results
    ]


__all__ = [
    "load_documents",
    "split_documents",
    "create_vector_store",
    "load_or_create_vector_store",
    "search_similar",
    "BASE_DIR",
    "CHROMA_DIR",
]