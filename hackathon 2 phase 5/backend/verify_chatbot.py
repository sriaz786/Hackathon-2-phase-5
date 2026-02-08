
import sys
import os
from sqlmodel import Session, create_engine, select

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from app.core.ai_service import AiService
from app.core.ai_tools import AiTools
from app.models.user import User
from app.core.config import settings

# Setup DB connection
engine = create_engine(settings.DATABASE_URL)

def verify_chatbot():
    with Session(engine) as session:
        # 1. Get or create a dummy user for testing
        user = session.exec(select(User)).first()
        if not user:
            print("No user found in DB. Creating a test user.")
            user = User(email="test@example.com", full_name="Test User", hashed_password="pwd")
            session.add(user)
            session.commit()
            session.refresh(user)
        
        print(f"Using user: {user.email} (ID: {user.id})")

        # 2. Initialize AiTools
        tools = AiTools(session=session, user=user)

        # 3. Test Chatbot with a simple 'Create Todo' request
        message = "Create a todo called 'Buy Milk' to verify API key"
        print(f"Sending message: '{message}'")
        
        try:
            response = AiService.process_chat(message, tools)
            print("--- Chatbot Response ---")
            print(response)
            print("------------------------")
            
            if "encountered an error" in response:
                print("FAILED: Chatbot returned an error.")
                sys.exit(1)
            else:
                print("SUCCESS: Chatbot responded.")
                
        except Exception as e:
            print(f"FAILED: Exception occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    verify_chatbot()
