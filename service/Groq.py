from config import config
from groq import AsyncGroq as Groq

Groqclient = Groq(api_key=config["GROQ_API_KEY"])
