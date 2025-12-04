import google.generativeai as genai
from config import config

genai.configure(api_key=config["TRANSLATE_GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")