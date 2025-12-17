import google.generativeai as genai
from config import config

genai.configure(api_key=config["GEMINI_API_KEY_TRANSLATE"])

model = genai.GenerativeModel("gemini-2.5-flash")