import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY was not found.")
    exit()

print("API key found. Testing Groq...")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key
)

response = llm.invoke(
    "Say hello and explain in one sentence what you can do."
)

print("\nGroq response:")
print(response.content)