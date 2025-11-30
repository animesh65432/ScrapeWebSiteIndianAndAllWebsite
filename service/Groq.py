import os
from groq import AsyncGroq as Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment variables")

Groqclient = Groq(api_key=API_KEY)
