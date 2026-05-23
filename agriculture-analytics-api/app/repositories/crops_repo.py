"""
Crops Repository Layer
----------------------
- Fetches crop-related views using DataLoader
- Keeps database access consistent and safe
"""

from fastapi import HTTPException
from app.data.data_loader import DataLoader


class CropsRepository:

    @staticmethod
    def get_yield_data():
        """
        Returns crop yield efficiency dataset
        """
        try:
            return DataLoader.load_view("vw_revenue_by_crop_year")

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load yield data: {str(e)}"
            )

    @staticmethod
    def get_harvest_data():
        """
        Returns full harvest dataset for crop analytics
        """
        try:
            return DataLoader.load_view("vw_harvest_full")

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load harvest data: {str(e)}"
            )