import json
from pathlib import Path
from typing import List, Union

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    JSONLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
    CSVLoader,
)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .logger import logger


LOADER_MAPPING = {
    ".txt": TextLoader,
    ".text": TextLoader,
    ".pdf": PyPDFLoader,
    ".json": JSONLoader,
    ".jsonl": JSONLoader,
    ".md": UnstructuredMarkdownLoader,
    ".markdown": UnstructuredMarkdownLoader,
    ".html": UnstructuredHTMLLoader,
    ".htm": UnstructuredHTMLLoader,
    ".csv": CSVLoader,
}


def load_document(
    file_path: str,
    encoding: str = "utf-8",
    jq_schema: str = None,
) -> List[Document]:
    """加载文档，自动根据后缀选择合适的加载器
    
    Args:
        file_path: 文件路径
        encoding: 文本文件编码，默认 utf-8
        jq_schema: JSON 文件的 jq schema，用于提取数据
    
    Returns:
        Document 列表
    """
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext not in LOADER_MAPPING:
        logger.warning(f"不支持的文件格式: {ext}，支持格式: {list(LOADER_MAPPING.keys())}")
        return []
    
    loader_cls = LOADER_MAPPING[ext]
    
    try:
        if ext in (".json", ".jsonl"):
            loader = loader_cls(file_path, jq_schema=jq_schema)
        elif ext in (".pdf"):
            loader = loader_cls(file_path)
        else:
            loader = loader_cls(file_path, encoding=encoding)
        
        documents = loader.load()
        logger.info(f"成功加载 {file_path}，共 {len(documents)} 个文档")
        return documents
    
    except Exception as e:
        logger.error(f"加载文件失败 {file_path}: {e}")
        return []


def load_and_split_document(
    file_path: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    encoding: str = "utf-8",
    jq_schema: str = None,
) -> List[Document]:
    """加载并分割文档
    
    Args:
        file_path: 文件路径
        chunk_size: 块大小
        chunk_overlap: 块重叠大小
        encoding: 文本文件编码
        jq_schema: JSON 文件的 jq schema
    
    Returns:
        分割后的 Document 列表
    """
    documents = load_document(file_path, encoding, jq_schema)
    
    if not documents:
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    logger.info(f"文档分割完成，共 {len(chunks)} 个块")
    
    return chunks


def get_supported_formats() -> List[str]:
    """获取支持的文件格式"""
    return list(LOADER_MAPPING.keys())


__all__ = [
    "load_document",
    "load_and_split_document",
    "get_supported_formats",
]