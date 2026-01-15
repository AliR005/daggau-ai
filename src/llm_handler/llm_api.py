from openai import OpenAI
from llm_handler.prompt_loader import load_system_prompt

from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


def get_answer_from_ai(history_and_question: list[str]):
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEY)
    system_prompt = load_system_prompt()

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": system_prompt}] + history_and_question,
        temperature=0.2,
    )
    return completion.choices[0].message.content
