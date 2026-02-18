import os
from dotenv import load_dotenv
from openai import OpenAI

# FORCE load .env from current directory
load_dotenv(dotenv_path=".env", override=True)

print("API KEY =", os.getenv("OPENROUTER_API_KEY"))
print("MODEL =", os.getenv("OPENROUTER_MODEL"))

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

response = client.chat.completions.create(
    model=os.getenv("OPENROUTER_MODEL"),
    messages=[
        {"role": "user", "content": "Reply with the word OK only."}
    ],
    max_tokens=5,
)

print(response.choices[0].message.content)
