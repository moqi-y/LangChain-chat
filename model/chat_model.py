import json

from langchain_ollama import ChatOllama

from config.config_handler import config
from rag.vector_service import init_vector_store

MODEL = config["model"]["chat_model"]
PROMPT = config["agent"]["system_prompt"]
BASE_URL = config["model"]["base_url"]


def chat_rebot(input: str):
    db = init_vector_store()
    res = db.similarity_search(
        query=input,
        k=3
    )
    docs = []  # 参考资料
    resource = []  # 参考文档
    for i in res:
        docs.append(dict(i)['page_content'])
        resource.append(dict(i)['metadata']['source'])
    llm = ChatOllama(
        model=MODEL,
        base_url=BASE_URL
    )
    context = "\n\n".join(docs)
    resource_text = "\n\n".join(resource)
    messages = [
        ("system", f"{PROMPT}，参考资料：{context},根据参考资料回答用户的问题,"),
        ("user", input)
    ]
    for chunk in llm.stream(messages):
        content = chunk.content
        # 返回 JSON 格式
        yield json.dumps({"type": "content", "data": content}, ensure_ascii=False)

    # 输出参考资料
    yield json.dumps({"type": "reference", "data": resource_text}, ensure_ascii=False)
