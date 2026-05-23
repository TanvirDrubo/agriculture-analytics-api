"""
Database Connection Layer
-------------------------
- Creates SQLAlchemy engine
- Provides safe connection validation
- Used across repositories for pandas SQL queries
"""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.core.config import settings


# =========================
# DATABASE URL BUILDER
# =========================
DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)


# =========================
# CREATE ENGINE (GLOBAL)
# =========================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,     # ensures stale connections are removed
    pool_recycle=3600,      # avoids MySQL timeout issues
    echo=False              # set True only for debugging SQL
)


# =========================
# CONNECTION VALIDATION
# =========================
def test_connection():
    """
    Runs a simple query to verify DB connection at startup.
    Helps catch configuration errors early.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")

    except OperationalError as e:
        print("❌ Database connection failed")
        raise Exception(f"DB Connection Error: {str(e)}")


# Run validation at import time (safe for FastAPI startup)
test_connection()