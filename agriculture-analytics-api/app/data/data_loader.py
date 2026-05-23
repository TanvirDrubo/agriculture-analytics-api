"""
Data Loader Layer
-----------------
- Centralized safe access to database views
- Prevents invalid table access
- Used by repositories for pandas processing
"""

import pandas as pd
from fastapi import HTTPException
from app.core.db import engine


# =========================
# ALLOWED VIEWS (PRD COMPLIANT)
# =========================
ALLOWED_VIEWS = {
    "vw_harvest_full",
    "vw_revenue_by_crop_year",
    "vw_farm_profitability"
}


# =========================
# DATA LOADER CLASS
# =========================
class DataLoader:

    @staticmethod
    def load_view(view_name: str):
        """
        Loads data from a validated SQL view into a pandas DataFrame.
        """

        # -------------------------
        # VALIDATE VIEW NAME
        # -------------------------
        if view_name not in ALLOWED_VIEWS:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid view name '{view_name}'. Allowed: {list(ALLOWED_VIEWS)}"
            )

        try:
            # -------------------------
            # SAFE QUERY EXECUTION
            # -------------------------
            query = f"SELECT * FROM {view_name}"
            df = pd.read_sql(query, engine)

            # Normalize column names (important for consistency)
            df.columns = df.columns.str.strip().str.lower()

            return df

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database query failed for {view_name}: {str(e)}"
            )