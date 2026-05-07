# """
# 应用入口文件
# """
#
# from agent import chat_with_rag_stream
#
#
# def main():
#     query = input("请输入你的问题: ")
#     print(f"\n用户问题: {query}")
#     print("-" * 50)
#     print("AI回答: ", end="", flush=True)
#
#     for chunk in chat_with_rag_stream(query):
#         print(chunk, end="", flush=True)
#
#     print("\n" + "-" * 50)
#
#
# if __name__ == "__main__":
#     main()


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


ui = gr.ChatInterface(
    fn=chat,
    title="RAG智能助手",
    description="基于本地知识库的自然语言问答系统",
    examples=[
        ["python的虚拟环境怎么使用"],
        ["Docker运行报错怎么解决"],
    ],
)

if __name__ == "__main__":
    logger.info("启动Gradio Web应用")
    ui.launch(server_port=7860)

