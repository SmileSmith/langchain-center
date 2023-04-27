from llama_index import SimpleDirectoryReader, LangchainEmbedding, GPTListIndex,GPTSimpleVectorIndex, PromptHelper, LLMPredictor, ServiceContext
from langchain import OpenAI
from dotenv.main import load_dotenv
import gradio
import sys
import os

load_dotenv()

favorite_language = os.environ['LANGUAGE']
openai_api_key = os.environ['OPENAI_API_KEY']
docs_dir = os.environ['DOC_DIRS']

def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 2000
    max_chunk_overlap = 20
    chunk_size_limit = 600
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs, api_key=openai_api_key))
    documents = SimpleDirectoryReader(directory_path).load_data()
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    index = GPTSimpleVectorIndex.from_documents(documents,service_context=service_context)
    index.save_to_disk('index.json')
    return index

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

webui = gradio.Interface(fn=chatbot,
                     inputs=gradio.inputs.Textbox(lines=7, label="输入您的文本"),
                     outputs="text",
                     title="AI 知识库聊天机器人")

index = construct_index(docs_dir)
webui.launch(share=True)
