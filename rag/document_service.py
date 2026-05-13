import os
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.config_handler import config

# 文档目录
BASE_DIR = config['dirs']['data']
CHUNK_SIZE = config['rag']['chunk_size']
CHUNK_OVERLAP = config['rag']['chunk_overlap']


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
    for file_name in os.listdir(data_dir):
        print("file_path:", file_name)
        loader = TextLoader(os.path.join(BASE_DIR, str(file_name)), encoding=encoding)
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = file_name
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
