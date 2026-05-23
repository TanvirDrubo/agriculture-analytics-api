"""
Farms Repository Layer
----------------------
- Accesses farm-level views
- Ensures consistent schema normalization
- Generates farm_id if missing (PRD requirement)
"""

import pandas as pd
from fastapi import HTTPException
from app.core.db import engine


class FarmsRepository:

    @staticmethod
    def get_harvest_data():
        """
        Loads full farm harvest dataset from DB view
        """

        try:
            df = pd.read_sql("SELECT * FROM vw_harvest_full", engine)

            # -------------------------
            # CLEAN COLUMN NAMES
            # -------------------------
            df.columns = df.columns.str.strip().str.lower()

            # -------------------------
            # PRD MANDATORY: FARM ID
            # -------------------------
            if "farm_id" not in df.columns:
                df["farm_id"] = df["farm_name"].factorize()[0] + 1

            return df

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load farm harvest data: {str(e)}"
            )

    @staticmethod
    def get_profitability():
        """
        Returns farm profitability view
        """
        try:
            df = pd.read_sql("SELECT * FROM vw_farm_profitability", engine)
            df.columns = df.columns.str.strip().str.lower()
            return df

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load profitability data: {str(e)}"
            )
    



    