import google.generativeai as genai
from app.core.ai_config import ai_settings
from app.core.ai_tools import AiTools

# Configure Global API Key
genai.configure(api_key=ai_settings.GEMINI_API_KEY)

class AiService:
    @staticmethod
    def process_chat(message: str, tools: AiTools) -> str:
        """
        Processes a chat message using Google Gemini with the provided tools.
        """
        # List of callable functions to expose to Gemini
        # We bind the methods from the 'tools' instance
        tool_functions = [
            tools.create_todo,
            tools.list_todos,
            tools.update_todo,
            tools.mark_todo,
            tools.delete_todo
        ]

        model = genai.GenerativeModel(
            model_name=ai_settings.GEMINI_MODEL,
            tools=tool_functions
        )

        # Start a chat session (stateless for now, or could pass history if stored)
        # For simplicity in this phase, we use a single-turn or short-lived chat with automatic function calling enabled by the SDK.
        chat = model.start_chat(enable_automatic_function_calling=True)

        try:
            response = chat.send_message(message)
            return response.text
        except Exception as e:
            return f"I encountered an error processing your request: {str(e)}"
