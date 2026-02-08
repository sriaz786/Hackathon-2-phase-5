
import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from app.core.ai_config import ai_settings

print(f"OS Environ GOOGLE_API_KEY: '{os.environ.get('GOOGLE_API_KEY')}'")
print(f"OS Environ GEMINI_API_KEY: '{os.environ.get('GEMINI_API_KEY')}'")
try:
    print(f"Settings GEMINI_API_KEY: '{ai_settings.GEMINI_API_KEY}'")
except Exception as e:
    print(f"Settings GEMINI_API_KEY Error: {e}")
