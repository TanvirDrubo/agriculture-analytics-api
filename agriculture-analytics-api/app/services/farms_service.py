"""
Farms Service Layer
-------------------
- Business logic for farm analytics
- PRD-compliant validation
- Safe pandas aggregation
"""

import pandas as pd
from fastapi import HTTPException

from app.repositories.farms_repo import FarmsRepository
from app.utils.filters import apply_filters

from app.validators.farms_validator import FarmsValidator
from app.validators.crops_validator import CropsValidator
from app.validators.common_validator import VALID_YEARS


class FarmsService:

    # =========================
    # 1. FARM SUMMARY
    # =========================
    @staticmethod
    def summary(region=None, year=None, farm_type=None):

        # -------------------------
        # VALIDATION (PRD REQUIRED)
        # -------------------------
        FarmsValidator.validate_region(region)
        FarmsValidator.validate_farm_type(farm_type)

        if year:
            if year not in VALID_YEARS:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid year. Allowed: {VALID_YEARS}"
                )

        df = FarmsRepository.get_harvest_data()

        if df.empty:
            return {"total_farms": 0, "data": []}

        df.columns = df.columns.str.strip().str.lower()

        # -------------------------
        # FILTERING (SAFE LAYER)
        # -------------------------
        df = apply_filters(df, region, year, farm_type)

        # -------------------------
        # GROUPING
        # -------------------------
        grouped = df.groupby(
            ["farm_name", "region", "farm_type"],
            as_index=False
        ).agg({
            "revenue_bdt": "sum",
            "input_cost_bdt": "sum",
            "net_profit_bdt": "sum",
            "quantity_lost_ton": "sum",
            "quantity_harvested_ton": "sum"
        })

        # -------------------------
        # DERIVED METRIC
        # -------------------------
        grouped["avg_loss_pct"] = (
            grouped["quantity_lost_ton"] /
            grouped["quantity_harvested_ton"].replace(0, 1)
        ) * 100

        grouped = grouped.rename(columns={
            "revenue_bdt": "total_revenue_bdt",
            "input_cost_bdt": "total_cost_bdt"
        })

        return {
            "total_farms": grouped["farm_name"].nunique(),
            "filters_applied": {
                "region": region,
                "year": year,
                "farm_type": farm_type
            },
            "data": grouped.to_dict(orient="records")
        }

    # =========================
    # 2. FARM PERFORMANCE
    # =========================
    @staticmethod
    def farm_performance(farm_id, year=None, crop_category=None, market_type=None):

        df = FarmsRepository.get_harvest_data()

        if "farm_id" not in df.columns:
            raise HTTPException(
                status_code=500,
                detail="farm_id missing in dataset"
            )

        df.columns = df.columns.str.strip().str.lower()

        df = df[df["farm_id"] == farm_id]

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail="Farm not found"
            )

        # -------------------------
        # VALIDATION (OPTIONAL FILTERS)
        # -------------------------
        if year:
            if year not in VALID_YEARS:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid year. Allowed: {VALID_YEARS}"
                )
            df = df[df["year"] == year]

        if market_type:
            # safe validation (no missing function call)
            allowed_market_types = ["Local", "Wholesale", "Export", "Retail", "Government Procurement"]

            if market_type not in allowed_market_types:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid market_type. Allowed: {allowed_market_types}"
                )

            df = df[df["market_type"] == market_type]

        if crop_category:
            allowed_categories = ["Cereal", "Vegetable", "Fruit", "Pulse", "Oilseed", "Cash Crop", "Spice"]

            if crop_category not in allowed_categories:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid crop_category. Allowed: {allowed_categories}"
                )

            df = df[df["crop_category"] == crop_category]

        # -------------------------
        # GROUPING
        # -------------------------
        grouped = df.groupby(
            ["crop_name", "year", "market_type", "quality_grade"],
            as_index=False
        ).agg({
            "quantity_sold_ton": "sum",
            "revenue_bdt": "sum",
            "net_profit_bdt": "sum"
        })

        farm_info = df.iloc[0]

        return {
            "farm_id": farm_id,
            "farm_name": farm_info["farm_name"],
            "owner": farm_info.get("owner_name", "N/A"),
            "region": farm_info["region"],
            "performance": grouped.to_dict(orient="records")
        }
    
    # =========================
    # 3. TOP FARMS
    # =========================
    @staticmethod
    def top_farms(metric: str = "profit", limit: int = 10):

        # -------------------------
        # VALIDATION
        # -------------------------
        FarmsValidator.validate_metric(metric)

        df = FarmsRepository.get_harvest_data()

        if df.empty:
            return {"data": []}

        df.columns = df.columns.str.strip().str.lower()

        metric_map = {
            "profit": "net_profit_bdt",
            "revenue": "revenue_bdt"
        }

        metric_col = metric_map.get(metric)

        if metric_col not in df.columns:
            raise HTTPException(500, f"Missing column: {metric_col}")

        grouped = df.groupby(
            ["farm_id", "farm_name", "region"],
            as_index=False
        ).agg({
            metric_col: "sum"
        })

        grouped = grouped.sort_values(
            by=metric_col,
            ascending=False
        ).head(limit)

        return {
            "metric": metric,
            "top_farms": grouped.to_dict(orient="records")
        }
    

    # =========================
    # 4. LOSS ANALYSIS
    # =========================
    @staticmethod
    def loss_analysis(region=None, year=None, season=None, quality_grade=None, crop_category=None):

        df = FarmsRepository.get_harvest_data()

        if df.empty:
            return {"data": []}

        df.columns = df.columns.str.strip().str.lower()

        # -------------------------
        # VALIDATION
        # -------------------------
        FarmsValidator.validate_region(region)

        if year and year not in VALID_YEARS:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid year. Allowed: {VALID_YEARS}"
            )

        # -------------------------
        # FILTERS
        # -------------------------
        if region:
            df = df[df["region"] == region]

        if year:
            df = df[df["year"] == year]

        if season:
            df = df[df["season"] == season]

        if quality_grade:
            df = df[df["quality_grade"] == quality_grade]

        if crop_category:
            df = df[df["crop_category"] == crop_category]

        # -------------------------
        # CHECK REQUIRED COLUMNS
        # -------------------------
        required_cols = ["quantity_lost_ton", "quantity_harvested_ton"]

        for col in required_cols:
            if col not in df.columns:
                raise HTTPException(500, f"Missing column: {col}")

        # -------------------------
        # AGGREGATION
        # -------------------------
        grouped = df.groupby(
            ["region", "crop_category"],
            as_index=False
        ).agg({
            "quantity_lost_ton": "sum",
            "quantity_harvested_ton": "sum"
        })

        grouped["loss_pct"] = (
            grouped["quantity_lost_ton"] /
            grouped["quantity_harvested_ton"].replace(0, 1)
        ) * 100

        return {
            "filters": {
                "region": region,
                "year": year,
                "season": season,
                "quality_grade": quality_grade,
                "crop_category": crop_category
            },
            "analysis": grouped.to_dict(orient="records")
        }

