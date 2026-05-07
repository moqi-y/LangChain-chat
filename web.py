"""
Gradio Web应用 - 聊天界面
"""

import gradio as gr
from agent import chat_with_rag


def chat(message: str, history: list) -> tuple[str, list]:
    if not message.strip():
        return "", history
    
    result = chat_with_rag(message)
    answer = result["answer"]
    
    references = result.get("references", [])
    if references:
        answer += "\n\n---\n**参考来源：**\n" + "\n".join([f"• {r['source']}" for r in references])
    
    history.append((message, answer))
    return "", history


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