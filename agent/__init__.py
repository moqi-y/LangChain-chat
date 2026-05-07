"""
Agent模块：负责处理用户输入，检索相关文档，并调用模型回答问题
"""

from model import get_chat_model, DEFAULT_MODEL
from rag import search_similar
from config import get_agent_config, get_rag_config

_agent_config = get_agent_config()
_rag_config = get_rag_config()

DEFAULT_SYSTEM_PROMPT = _agent_config.get("system_prompt", "你是一个智能助手，你要根据提供给你的参考资料，回答用户的问题。参考内容可能包含多个来源，请综合这些信息进行回答。")
DEFAULT_K = _rag_config.get("top_k", 3)


def chat_with_rag(
    user_input: str,
    k: int = None,
    include_reference: bool = True,
) -> dict:
    """
    处理用户输入，检索相关文档并调用模型回答问题

    输入参数:
        user_input: str, 用户输入的问题
        k: int, 检索相关文档的数量，默认为配置中的top_k
        include_reference: bool, 是否在返回结果中包含参考来源，默认为True

    返回:
        dict: 包含answer(回答内容)和references(参考来源列表)的字典
    """
    results = search_similar(user_input, k=k or DEFAULT_K)

    context = "\n\n".join([
        f"参考文档{i + 1}（{r['source']}）:\n{r['content']}"
        for i, r in enumerate(results)
    ])

    prompt = f"""根据以下参考资料回答用户问题。

参考资料：
{context}

用户问题：{user_input}

请根据以上参考资料回答问题，如果参考资料中没有相关信息，请如实说明。"""

    llm = get_chat_model()
    response = llm.stream(prompt)

    if include_reference:
        return {
            "answer": response.content,
            "references": [{"source": r["source"], "content": r["content"]} for r in results],
        }
    else:
        return {"answer": response.content}


def chat_with_rag_stream(
    user_input: str,
    k: int = None,
):
    """
    流式处理用户输入，检索相关文档并调用模型回答问题（流式输出）

    输入参数:
        user_input: str, 用户输入的问题
        k: int, 检索相关文档的数量，默认为配置中的top_k

    yields:
        str: 模型生成的文本片段
    """
    results = search_similar(user_input, k=k or DEFAULT_K)

    context = "\n\n".join([
        f"参考文档{i + 1}（{r['source']}）:\n{r['content']}"
        for i, r in enumerate(results)
    ])

    prompt = f"""根据以下参考资料回答用户问题。

参考资料：
{context}

用户问题：{user_input}

请根据以上参考资料回答问题，如果参考资料中没有相关信息，请如实说明。"""

    llm = get_chat_model()

    for chunk in llm.stream(prompt):
        yield chunk.content


__all__ = [
    "chat_with_rag",
    "chat_with_rag_stream",
    "DEFAULT_SYSTEM_PROMPT",
]