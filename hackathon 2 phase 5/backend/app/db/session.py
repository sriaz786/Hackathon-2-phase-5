from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Verify DATABASE_URL is set
if not settings.DATABASE_URL:
    # raise ValueError("DATABASE_URL environment variable is not set")
    print("DATABASE_URL is missing. Engine will not be created.")

# Handle 'postgres://' case for SQLAlchemy compatibility and use psycopg2 driver
connection_string = str(settings.DATABASE_URL) if settings.DATABASE_URL else ""

if connection_string:
    if "postgresql+psycopg2" not in connection_string and "postgresql://" not in connection_string:
        connection_string = connection_string.replace("postgres://", "postgresql+psycopg2://")
    elif "postgres://" in connection_string and "postgresql+psycopg2" not in connection_string:
        connection_string = connection_string.replace("postgres://", "postgresql+psycopg2://")

    # Create engine with SSL for Neon/psycopg2
    engine = create_engine(
        connection_string, 
        echo=True,
        connect_args={"sslmode": "require"}
    )
else:
    engine = None
    print("WARNING: DATABASE_URL not set. Database operations will fail.")

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
