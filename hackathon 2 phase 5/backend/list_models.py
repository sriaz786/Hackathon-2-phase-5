
import sys
import os
import google.generativeai as genai
from app.core.ai_config import ai_settings

genai.configure(api_key=ai_settings.GEMINI_API_KEY)

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
