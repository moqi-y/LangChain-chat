from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_txt_splitter(
        chunk_size: int = 500,
        chunk_overlap: int = 50,
) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )


def split_txt_file(
        file_path: str,
        encoding: str = "utf-8",
        chunk_size: int = 200,
        chunk_overlap: int = 50,
):
    loader = TextLoader(file_path, encoding=encoding)
    documents = loader.load()

    text_splitter = create_txt_splitter(chunk_size, chunk_overlap)
    chunks = text_splitter.split_documents(documents)

    return chunks


__all__ = ["create_txt_splitter", "split_txt_file"]

if __name__ == '__main__':
    # Example usage
    chunks = split_txt_file("../data/Docker运行报错wsl问题排查方案.txt")
    for chunk in chunks:
        print(chunk)
