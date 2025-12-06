from config import config
from groq import AsyncGroq as Groq
from openai import OpenAI

client = OpenAI(
    api_key=config["OPENAI_API_KEY"]
)
