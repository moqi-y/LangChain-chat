from model.chat_model import chat_rebot
from rag.document_service import load_documents, split_documents
from rag.vector_service import init_vector_store


if __name__ == '__main__':
    ai_response = chat_rebot("python环境虚拟环境怎么安装？")
    for response in ai_response:
        print(response, end='', flush=True)
