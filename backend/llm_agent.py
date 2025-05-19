import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(question, context):
    prompt = f"""
You are an expert UAV assistant. Use the flight data below to answer the user's question.

Flight Data:
{context}

Question:
{question}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful UAV flight assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            timeout=15
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM Error: {str(e)}"

def ask_llm_with_memory(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            temperature=0.3,
            timeout=15
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM Error: {str(e)}"