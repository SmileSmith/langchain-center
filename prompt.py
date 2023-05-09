from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from dotenv.main import load_dotenv
import gradio as gr
import os
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

load_dotenv()

openai_api_key = os.environ['OPENAI_API_KEY']

with open('prompts/drip_table/template.txt', 'r', encoding="utf-8") as f:
    template = f.read()
with open('prompts/drip_table/defined.md', 'r', encoding="utf-8") as f:
    defined = f.read()

prompt = PromptTemplate(
    input_variables=["history", "human_input"],
    template=template.replace("{context}", defined)
)

chatgpt_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, openai_api_key=openai_api_key, streaming=True),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
)

def chatbot_reset ():
    chatgpt_chain.memory.clear()



def chatbot_predict(human_input, history=[]):
    response = chatgpt_chain.predict(human_input=human_input)
    print(response)
    history.append((human_input, response))
    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        bot_message = chatgpt_chain.predict(human_input=history[-1][0])
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch()

