from typing import List, Optional
from sqlmodel import Session, select
import logging

logger = logging.getLogger(__name__)

from app.models.todo import Todo
from app.models.user import User
from app.models.audit_log import AiAuditLog

class AiTools:
    def __init__(self, session: Session, user: User):
        self.session = session
        self.user = user

    def create_todo(self, title: str, description: Optional[str] = None) -> str:
        """Creates a new todo item.
        
        Args:
            title: The title of the todo.
            description: An optional description of the todo.
        """
        todo = Todo(title=title, description=description, user_id=self.user.id)
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        self._log_action("create_todo", f"Title: {title}", f"Created ID: {todo.id}")
        return f"Todo created successfully with ID: {todo.id}"

    def list_todos(self) -> str:
        """Lists all todos for the current user."""
        statement = select(Todo).where(Todo.user_id == self.user.id)
        todos = self.session.exec(statement).all()
        if not todos:
            return "You have no todos."
        
        result = "Your todos:\n"
        for todo in todos:
            status = "[x]" if todo.status == "completed" else "[ ]"
            result += f"{todo.id}. {status} {todo.title} - {todo.description or ''}\n"
        
        self._log_action("list_todos", None, f"Listed {len(todos)} todos")
        return result

    def update_todo(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None) -> str:
        """Updates a todo item.
        
        Args:
            todo_id: The ID of the todo to update.
            title: The new title (optional).
            description: The new description (optional).
        """
        todo = self.session.get(Todo, todo_id)
        if not todo or todo.user_id != self.user.id:
            return f"Error: Todo with ID {todo_id} not found or access denied."
        
        updates = []
        if title is not None:
            todo.title = title
            updates.append(f"title='{title}'")
        if description is not None:
            todo.description = description
            updates.append(f"description='{description}'")
            
        if not updates:
            return "No changes requested."

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        self._log_action("update_todo", f"ID: {todo_id}, {', '.join(updates)}", "Updated")
        return f"Todo {todo_id} updated successfully."

    def mark_todo(self, todo_id: int, status: str) -> str:
        """Marks a todo as 'completed' or 'pending'.
        
        Args:
            todo_id: The ID of the todo.
            status: The new status. Must be 'completed' or 'pending'.
        """
        if status not in ["completed", "pending"]:
            return "Error: Status must be 'completed' or 'pending'."

        todo = self.session.get(Todo, todo_id)
        if not todo or todo.user_id != self.user.id:
            return f"Error: Todo with ID {todo_id} not found or access denied."
        
        todo.status = status
        self.session.add(todo)
        self.session.commit()
        self._log_action("mark_todo", f"ID: {todo_id} -> {status}", "Success")
        return f"Todo {todo_id} marked as {status}."

    def delete_todo(self, todo_id: int) -> str:
        """Deletes a todo item.
        
        Args:
            todo_id: The ID of the todo to delete.
        """
        todo = self.session.get(Todo, todo_id)
        if not todo or todo.user_id != self.user.id:
            return f"Error: Todo with ID {todo_id} not found or access denied."
        
        self.session.delete(todo)
        self.session.commit()
        self._log_action("delete_todo", f"ID: {todo_id}", "Deleted")
        return f"Todo {todo_id} deleted successfully."

    def _log_action(self, action: str, input_data: Optional[str], result: Optional[str]):
        # Simple logging to DB
        try:
            log_entry = AiAuditLog(
                user_id=self.user.id,
                action=action,
                input_data=input_data,
                result=result
            )
            self.session.add(log_entry)
            self.session.commit()
        except Exception as e:
            print(f"Failed to log AI action: {e}")
