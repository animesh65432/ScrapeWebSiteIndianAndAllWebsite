from config import config
from openai import AsyncOpenAI as OpenAI

client = OpenAI(
    base_url="https://api.agentrouter.org/v1",
    api_key="sk-iEE6u1Uzzdt6tD6y0p7e7yA7r6UVZLJpTYY8Jt23tZluuChn"
)
