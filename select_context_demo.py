from selective_context import SelectiveContext

with open('prompts/drip_table/template.txt', 'r', encoding="utf-8") as f:
    template = f.read()
with open('prompts/drip_table/defined.md', 'r', encoding="utf-8") as f:
    defined = f.read()

# prompt = template.replace("{context}", defined)
prompt = template

sc = SelectiveContext(lang='zh')
# sc = SelectiveContext(model_type="gpt2", lang='en')
context, reduced_content = sc(prompt)
print(context)
print(reduced_content)