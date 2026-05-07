"""
应用入口文件
"""

from agent import chat_with_rag_stream


def main():
    query = input("请输入你的问题: ")
    print(f"\n用户问题: {query}")
    print("-" * 50)
    print("AI回答: ", end="", flush=True)

    for chunk in chat_with_rag_stream(query):
        print(chunk, end="", flush=True)
    
    print("\n" + "-" * 50)


if __name__ == "__main__":
    main()