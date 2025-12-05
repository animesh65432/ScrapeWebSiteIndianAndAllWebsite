from config import config
from groq import AsyncGroq as Groq
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)
