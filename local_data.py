from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI,VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from dotenv.main import load_dotenv
import os
import sys
import logging

# 记录日志
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()

# 参考https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/directory_loader.html 搭建webui，支持选项
openai_api_key = os.environ['OPENAI_API_KEY']
docs_dir = os.environ['DOC_DIRS']
persist_dir="stores"

def construct_vectorstore(docs_path, vectorstore_path):
    # 加载文件夹中的所有txt类型的文件
    loader = DirectoryLoader(docs_path, glob='**/*.md')
    # 将数据转成 document 对象，每个文件会作为一个 document
    documents = loader.load()

    # 初始化加载器
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    # 切割加载的 document
    split_docs = text_splitter.split_documents(documents)

    # 初始化 openai 的 embeddings 对象
    embeddings = OpenAIEmbeddings()
    # 将 document 通过 openai 的 embeddings 对象计算 embedding向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
    vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory=vectorstore_path)
    # 持久化
    Chroma.persist(vectorstore)

    return vectorstore

# 将 document 通过 openai 的 embeddings 对象计算 embedding向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
docsearch = construct_vectorstore(docs_dir, persist_dir)

query="HiBox如何安装"

# 测试向量化匹配
search_result = docsearch.similarity_search_with_score(query)
print(search_result)

# 测试MMR
retriever = docsearch.as_retriever(search_type="mmr")
retrieve_result = retriever.get_relevant_documents(query)
print(retrieve_result)

# 创建问答对象
# qa = VectorDBQA.from_chain_type(llm=OpenAI(temperature=0, max_tokens=2048, openai_api_key=openai_api_key), chain_type="stuff", vectorstore=docsearch, return_source_documents=True)
# 进行问答
# result = qa({"query": query})
# print(result)