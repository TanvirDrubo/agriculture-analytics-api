"""
Main FastAPI Application
------------------------
- Entry point of Agriculture Analytics API
- Includes routers for farms, crops, markets
- Adds startup checks + health endpoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# SQLAlchemy text() is REQUIRED for raw SQL execution
from sqlalchemy import text

from app.api import farms, crops, markets
from app.core.db import engine


# =========================
# APP INITIALIZATION
# =========================
app = FastAPI(
    title="Agriculture Analytics API",
    version="1.0.0",
    description="PRD-compliant agriculture analytics system using FastAPI + Pandas + MySQL"
)


# =========================
# CORS (SAFE DEFAULT)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTERS
# =========================
app.include_router(farms.router)
app.include_router(crops.router)
app.include_router(markets.router)


# =========================
# HEALTH CHECK ENDPOINT
# =========================
@app.get("/")
def root():
    """
    Simple API health check.
    Useful for:
    - Load balancers
    - Monitoring tools
    """
    return {
        "status": "running",
        "message": "Agriculture Analytics API is active"
    }


# =========================
# STARTUP EVENT (DB CHECK)
# =========================
@app.on_event("startup")
def startup_event():
    """
    Runs when FastAPI starts.

    Purpose:
    - Verify database connectivity
    - Fail fast if DB is down
    """

    try:
        # ✅ FIX: wrap SQL in text()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        print("✅ Database connection successful")

    except Exception as e:
        print("❌ Database connection failed:", str(e))
        raise e