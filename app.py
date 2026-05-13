import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from model.chat_model import chat_rebot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 修正后的生成器函数
def generator():
    # chat_rebot 返回的是一个生成器，需要迭代它
    res_generator = chat_rebot(input="python的虚拟环境怎么创建？")
    print("res_generator:", res_generator)

    # 迭代生成器，逐个 yield 每个 chunk
    for chunk in res_generator:
        print("chunk:", chunk)
        if chunk:
            # chunk 已经是字符串，直接编码
            yield f"data: {chunk}\n\n".encode('utf-8')

    # 发送结束标记
    yield b"data: [DONE]\n\n"


@app.post("/chat")
async def chat(text: str = "test"):
    """测试端点"""
    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)