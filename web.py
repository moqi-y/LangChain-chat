"""
Gradio Web应用 - 聊天界面
"""

import gradio as gr
from agent import chat_with_rag_stream
from utils import logger


def chat(message, history):
    """处理聊天输入"""
    response_text = ""
    for chunk in chat_with_rag_stream(message):
        if isinstance(chunk, tuple):
            continue
        response_text += chunk.content
        yield response_text


demo = gr.ChatInterface(
    fn=chat,
    title="RAG智能助手",
    description="基于本地知识库的自然语言问答系统",
    examples=[
        ["python的虚拟环境怎么使用"],
        ["Docker运行报错怎么解决"],
    ],
)

if __name__ == "__main__":
    demo.launch(server_port=7860)
