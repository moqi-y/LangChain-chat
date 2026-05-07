"""
模型模块：负责模型加载和调用
"""

from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from config import get_model_config

_model_config = get_model_config()
BASE_URL = _model_config.get("base_url", "http://192.168.1.59:11434")
DEFAULT_MODEL = _model_config.get("chat_model", "qwen3:0.6b")
DEFAULT_EMBED_MODEL = _model_config.get("embed_model", "nomic-embed-text")
DEFAULT_TEMPERATURE = _model_config.get("temperature", 0.7)


def get_chat_model(
    model: str = None,
    temperature: float = None,
    **kwargs,
) -> ChatOllama:
    """
    获取聊天模型实例

    输入参数:
        model: str, 模型名称，默认为配置中的chat_model
        temperature: float, 温度参数，默认为配置中的temperature
        **kwargs: 其他参数

    返回:
        ChatOllama: 聊天模型实例
    """
    return ChatOllama(
        base_url=BASE_URL,
        model=model or DEFAULT_MODEL,
        temperature=temperature if temperature is not None else DEFAULT_TEMPERATURE,
        **kwargs,
    )


def get_embedding_model(
    model: str = None,
    **kwargs,
) -> OllamaEmbeddings:
    """
    获取嵌入模型实例

    输入参数:
        model: str, 嵌入模型名称，默认为配置中的embed_model
        **kwargs: 其他参数

    返回:
        OllamaEmbeddings: 嵌入模型实例
    """
    return OllamaEmbeddings(
        base_url=BASE_URL,
        model=model or DEFAULT_EMBED_MODEL,
        **kwargs,
    )


def invoke_model(
    prompt: str,
    system_prompt: str | None = None,
    model: str = None,
    temperature: float = None,
) -> str:
    """
    调用模型进行推理

    输入参数:
        prompt: str, 用户输入
        system_prompt: str, 系统提示词
        model: str, 模型名称
        temperature: float, 温度参数

    返回:
        str: 模型输出
    """
    llm = get_chat_model(model=model, temperature=temperature)

    if system_prompt:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt),
        ]
    else:
        messages = [HumanMessage(content=prompt)]

    response = llm.invoke(messages)
    return response.content


__all__ = [
    "get_chat_model",
    "invoke_model",
    "get_embedding_model",
    "BASE_URL",
    "DEFAULT_MODEL",
    "DEFAULT_EMBED_MODEL",
]