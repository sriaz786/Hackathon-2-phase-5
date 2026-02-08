import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlmodel import Session, SQLModel, create_engine
from app.models.user import User
from app.models.todo import Todo
from app.core.ai_tools import AiTools
from app.models.audit_log import AiAuditLog

def test_ai_tools_logic():
    # Setup in-memory DB
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Create Dummy User
        user = User(username="testuser", email="test@example.com", hashed_password="pw")
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Init Tools
        tools = AiTools(session=session, user=user)
        
        # 1. Create Todo
        print("Testing CREATE...")
        msg = tools.create_todo("Buy Milk", "Whole milk")
        print(msg)
        assert "Todo created successfully" in msg
        
        todos = session.query(Todo).all()
        assert len(todos) == 1
        assert todos[0].title == "Buy Milk"
        
        # 2. List Todos
        print("Testing LIST...")
        listing = tools.list_todos()
        print(listing)
        assert "Buy Milk" in listing
        
        # 3. Update Todo
        print("Testing UPDATE...")
        msg = tools.update_todo(todos[0].id, title="Buy Bread")
        print(msg)
        assert "updated successfully" in msg
        session.refresh(todos[0])
        assert todos[0].title == "Buy Bread"
        
        # 4. Mark Todo
        print("Testing MARK...")
        msg = tools.mark_todo(todos[0].id, "completed")
        print(msg)
        assert "marked as completed" in msg
        session.refresh(todos[0])
        assert todos[0].status == "completed"
        
        # 5. Delete Todo
        print("Testing DELETE...")
        msg = tools.delete_todo(todos[0].id)
        print(msg)
        assert "deleted successfully" in msg
        todos = session.query(Todo).all()
        assert len(todos) == 0
        
        # Verify Audit Log
        logs = session.query(AiAuditLog).all()
        print(f"Audit Logs: {len(logs)}")
        assert len(logs) >= 5

if __name__ == "__main__":
    try:
        test_ai_tools_logic()
        print("\nAll AI Tool tests passed!")
    except Exception as e:
        print(f"\nTest FAILED: {e}")
        exit(1)
