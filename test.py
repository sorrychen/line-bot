import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("LINE_BOT_API_KEY"))

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful cafe assistant."},
        {"role": "user", "content": "請問菜單有什麼?"},
    ]
)
gpt_response = completion.choices[0].message.content
# print(gpt_response)

token_usage = completion.usage
print(token_usage)

print("--------------------") 

output_tokens = token_usage.completion_tokens
input_tokens = token_usage.prompt_tokens

print(output_tokens)
print(input_tokens)