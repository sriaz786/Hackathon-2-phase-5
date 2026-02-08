from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api import api_router
from app.db.session import create_db_and_tables

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
     # Fallback for dev if not set
     app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://hackathonfinal-ecru.vercel.app"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("startup")
def on_startup():
    # Tables already exist in Neon database - disable auto-create to avoid conflicts
    try:
        create_db_and_tables()
    except Exception as e:
        print(f"Error creating tables: {e}")
    pass

from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}", "type": type(exc).__name__},
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    try:
        from app.db.session import engine
        from sqlmodel import Session, select
        with Session(engine) as session:
            session.exec(select(1)).first()
        return {"message": "Welcome to Todo API Phase II", "database": "connected"}
    except Exception as e:
        return {"message": "Welcome to Todo API Phase II", "database": "error", "detail": str(e)}
