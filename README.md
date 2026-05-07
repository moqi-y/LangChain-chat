"# LangChain-chat" 

### 激活虚拟环境：
- 在 Unix 或 macOS 上：     
`source .venv/bin/activate`
- 在 Windows 上：       
`.venv\Scripts\activate`

### 安装环境依赖

```bash
pip install langchain langchain-community langchain-ollama dashscope chromadb -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## RAG

向量计算模型：`text-embedding-v1`,使用余弦相似度算法实现。
向量数据库：`chromadb`
向量数据库地址：`http://localhost:8000`

### json文档加载

安装JSONLoader的jq依赖包

```bash
pip install jq -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### PyPDFLoader文档加载

安装PyPDFLoader的依赖包

```bash
pip install pypdf -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### streamlit 库

```bash
pip install streamlit -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> run

```bash
streamlit run app.py
```

