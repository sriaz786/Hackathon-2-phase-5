from sqlmodel import SQLModel
from app.db.session import engine
from app.models.user import User
from app.models.todo import Todo

def reset_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    print("Database reset successfully.")

if __name__ == "__main__":
    reset_db()
