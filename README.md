# LangChain-chat

基于 LangChain 和 Ollama 的本地知识库问答系统 (RAG)。

## 预览

![主界面](https://github.com/moqi-y/LangChain-chat/blob/master/images/img.png)

![聊天示例](https://github.com/moqi-y/LangChain-chat/blob/master/images/img_1.png)

## 特性

- **RAG 检索增强生成** - 通过向量相似度搜索从本地文档中检索相关内容，生成准确答案
- **本地 LLM** - 使用 Ollama 运行，支持 qwen3 等模型，无需云端 API
- **流式输出** - 支持流式响应，实时获取 AI 生成内容
- **多格式支持** - 支持加载 `.txt`、PDF、JSON 等格式的文档
- **参考来源追溯** - 回答附带文档来源，方便验证

## 技术栈

| 类别 | 技术 |
|------|------|
| LLM 框架 | LangChain, LangChain Community, LangChain Ollama |
| 本地模型服务 | [Ollama](https://ollama.ai/) |
| 向量数据库 | ChromaDB |
| Web 界面 | Gradio |
| 日志 | Loguru |

## 环境准备

### 1. Python 环境

```bash
# 创建虚拟环境 (可选)
python -m venv .venv

# 激活虚拟环境
# Unix/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install langchain langchain-community langchain-ollama dashscope chromadb gradio loguru pypdf jq -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. Ollama 环境

1. 安装 [Ollama](https://ollama.ai/download)

2. 启动 Ollama 服务：

```bash
ollama serve
```

3. 下载所需模型：

```bash
ollama pull qwen3:0.6b      # 聊天模型
ollama pull nomic-embed-text  # 向量嵌入模型
```

## 配置

编辑 `config/config.yml` 文件：

```yaml
# 模型配置
model:
  base_url: "http://192.168.1.59:11434"  # Ollama 服务地址
  chat_model: "qwen3:0.6b"               # 聊天模型
  embed_model: "nomic-embed-text"        # 嵌入模型
  temperature: 0.7                       # 生成温度

# RAG 配置
rag:
  chunk_size: 500      # 文档分块大小
  chunk_overlap: 50    # 块重叠大小
  top_k: 3            # 检索文档数量
  collection_name: "rag_store"

# 目录配置
dirs:
  data: "data"              # 知识库目录
  chroma_db: "data/chroma_db"  # 向量数据库目录
  logs: "logs"              # 日志目录
```

## 使用

### 1. 添加知识文档

将 `.txt` 文件放入 `data/` 目录，系统启动时会自动向量化并存储。

### 2. 启动应用

```bash
python app.py
```

### 3. 访问界面

打开浏览器访问 http://localhost:7860

## 项目结构

```
LangChain-chat/
├── app.py              # 应用入口 (Gradio UI)
├── agent/              # Agent 模块 (RAG 对话逻辑)
├── config/             # 配置模块
│   └── config.yml      # 配置文件
├── model/              # 模型模块 (LLM 调用)
├── rag/                # RAG 模块 (向量检索)
├── utils/              # 工具模块
│   ├── logger.py       # 日志工具
│   ├── text_splitter_txt.py   # TXT 分块
│   └── text_splitter_pdf.py   # PDF 分块
├── data/               # 知识库文档
│   └── chroma_db/      # 向量数据库存储
└── logs/               # 日志文件
```

## 工作流程

```
用户提问
    │
    ▼
┌─────────────────┐
│  语义检索 (Query)  │
│  在向量数据库中搜索  │
│  相似文档片段      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  构建 Prompt     │
│  将检索内容 + 问题 │
│  组装成完整 prompt│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM 生成答案    │
│  (Ollama/qwen3) │
└────────┬────────┘
         │
         ▼
   返回答案 + 参考来源
```

## License

MIT
