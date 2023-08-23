from transformers import AutoTokenizer
from transformers import LlamaForCausalLM
import torch
import gradio


device = torch.device("cuda")

model = LlamaForCausalLM.from_pretrained('IDEA-CCNL/Ziya-LLaMA-13B-v1', device_map="auto", offload_folder="offload", torch_dtype=torch.float16)
print("Model loaded successfully")
tokenizer = AutoTokenizer.from_pretrained('IDEA-CCNL/Ziya-LLaMA-13B-v1')
print("Tokenizer loaded successfully")
def chatbot(query):
    print(query)
    inputs = '<human>:' + query.strip() + '\n<bot>:'

    input_ids = tokenizer(inputs, return_tensors="pt").input_ids.to(device)
    generate_ids = model.generate(
                input_ids,
                max_new_tokens=1024, 
                do_sample = True, 
                top_p = 0.85, 
                temperature = 1.0, 
                repetition_penalty=1., 
                eos_token_id=2, 
                bos_token_id=1, 
                pad_token_id=0)
    print(generate_ids)
    output = tokenizer.batch_decode(generate_ids)[0]
    print(output)
    return output

webui = gradio.Interface(fn=chatbot,
                     inputs=gradio.inputs.Textbox(lines=7, label="输入您的文本"),
                     outputs="text",
                     title="AI 知识库聊天机器人")

webui.launch(share=True)