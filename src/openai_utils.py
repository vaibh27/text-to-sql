import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_model(messages: list, model: str = "gpt-4o") -> str:
    """
    Send a list of messages to OpenAI chat completion and return the assistant's reply.
    """
    # print(messages)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content.strip()
