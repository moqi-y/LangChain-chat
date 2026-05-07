from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_pdf_splitter(
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )


def split_pdf_file(
    file_path: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = create_pdf_splitter(chunk_size, chunk_overlap)
    chunks = text_splitter.split_documents(documents)

    return chunks


__all__ = ["create_pdf_splitter", "split_pdf_file"]