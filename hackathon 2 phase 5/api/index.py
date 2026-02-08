import sys
import os

# Add the backend directory to sys.path so that imports like "from app..." work correctly
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi import FastAPI, Response
import traceback

app = None

try:
    from main import app
except Exception as e:
    # Catch startup errors (like missing env vars, import errors)
    # and return them as a valid HTTP response so we can see them in the browser.
    error_msg = f"Failed to start backend:\n{traceback.format_exc()}"
    print(error_msg) # Log to Vercel logs
    
    app = FastAPI()
    
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
    async def catch_all(path_name: str):
        return Response(content=error_msg, media_type="text/plain", status_code=500)
