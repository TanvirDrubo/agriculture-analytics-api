"""
Crops Service Layer
-------------------
- Business logic for crop analytics
- PRD-compliant validation
- Safe pandas transformations
"""

import pandas as pd
from fastapi import HTTPException

from app.repositories.crops_repo import CropsRepository
from app.validators.crops_validator import CropsValidator


class CropsService:

    # =========================
    # 1. YIELD EFFICIENCY
    # =========================
    @staticmethod
    def yield_efficiency():

        df = CropsRepository.get_yield_data()

        if df.empty:
            return {"data": []}

        # -------------------------
        # SAFE COLUMN NORMALIZATION
        # -------------------------
        df.columns = df.columns.str.strip().str.lower()

        required_cols = ["total_sold_ton", "total_harvests"]

        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise HTTPException(
                status_code=500,
                detail=f"Missing columns: {missing}"
            )

        # -------------------------
        # NUMERIC SAFETY
        # -------------------------
        df["total_sold_ton"] = pd.to_numeric(df["total_sold_ton"], errors="coerce").fillna(0)
        df["total_harvests"] = pd.to_numeric(df["total_harvests"], errors="coerce").fillna(0)

        df["total_harvests"] = df["total_harvests"].replace(0, 1)

        df["efficiency_pct"] = (
            df["total_sold_ton"] / df["total_harvests"]
        ) * 100

        return {"data": df.to_dict(orient="records")}

    # =========================
    # 2. SEASONAL TREND
    # =========================
    @staticmethod
    def seasonal_trend(year=None, season=None):

        # -------------------------
        # VALIDATION (PRD REQUIRED)
        # -------------------------
        CropsValidator.validate_year(year)
        CropsValidator.validate_season(season)

        df = CropsRepository.get_harvest_data()

        if df.empty:
            return {"trend": []}

        df.columns = df.columns.str.strip().str.lower()

        # -------------------------
        # SAFE FILTERING
        # -------------------------
        if year:
            df = df[df["year"] == year]

        if season:
            df = df[df["season"] == season]

        required_cols = ["crop_name", "quantity_sold_ton", "revenue_bdt"]

        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise HTTPException(
                status_code=500,
                detail=f"Missing columns: {missing}"
            )

        grouped = df.groupby(
            ["crop_name", "season"],
            as_index=False
        ).agg({
            "quantity_sold_ton": "sum",
            "revenue_bdt": "sum",
            "net_profit_bdt": "sum"
        })

        return {"trend": grouped.to_dict(orient="records")}

    # =========================
    # 3. QUALITY BREAKDOWN
    # =========================
    @staticmethod
    def quality_breakdown(
        crop_category=None,
        year=None,
        region=None,
        market_type=None,
        pesticide_residue=None
    ):

        # -------------------------
        # VALIDATION (PRD COMPLIANCE)
        # -------------------------
        CropsValidator.validate_year(year)
        CropsValidator.validate_season(season=None)  # safe optional validation

        df = CropsRepository.get_harvest_data()

        if df.empty:
            return {"total_records": 0, "grade_distribution": {}}

        df.columns = df.columns.str.strip().str.lower()

        # -------------------------
        # SAFE FILTERS
        # -------------------------
        if crop_category and "crop_category" in df.columns:
            df = df[df["crop_category"] == crop_category]

        if year and "year" in df.columns:
            df = df[df["year"] == year]

        if region and "region" in df.columns:
            df = df[df["region"] == region]

        if market_type and "market_type" in df.columns:
            df = df[df["market_type"] == market_type]

        if pesticide_residue and "pesticide_residue" in df.columns:
            df = df[df["pesticide_residue"] == pesticide_residue]

        if "quality_grade" not in df.columns:
            raise HTTPException(
                status_code=500,
                detail="Missing column: quality_grade"
            )

        # -------------------------
        # OUTPUT
        # -------------------------
        return {
            "total_records": len(df),
            "grade_distribution": df["quality_grade"].value_counts().to_dict()
        }