"""
Market Service Layer
--------------------
- Market price comparison analytics
- PRD-compliant validation
- Safe filtering + aggregation
"""

import pandas as pd
from fastapi import HTTPException

from app.repositories.farms_repo import FarmsRepository
from app.validators.farms_validator import FarmsValidator
from app.validators.crops_validator import CropsValidator
from app.validators.common_validator import VALID_YEARS


class MarketService:

    # =========================
    # PRICE COMPARISON
    # =========================
    @staticmethod
    def price_comparison(
        market_type=None,
        crop_category=None,
        year=None,
        season=None,
        price_tier=None,
        district=None
    ):

        df = FarmsRepository.get_harvest_data()

        if df.empty:
            return {"comparison": []}

        # -------------------------
        # SAFE COLUMN NORMALIZATION
        # -------------------------
        df.columns = df.columns.str.strip().str.lower()

        # -------------------------
        # VALIDATION (PRD COMPLIANCE)
        # -------------------------
        if year:
            if year not in VALID_YEARS:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid year. Allowed: {VALID_YEARS}"
                )

        if market_type:
            allowed_market_types = [
                "Local", "Wholesale", "Export", "Retail", "Government Procurement"
            ]
            if market_type not in allowed_market_types:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid market_type. Allowed: {allowed_market_types}"
                )

        if crop_category:
            allowed_categories = [
                "Cereal", "Vegetable", "Fruit", "Pulse", "Oilseed", "Cash Crop", "Spice"
            ]
            if crop_category not in allowed_categories:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid crop_category. Allowed: {allowed_categories}"
                )

        if price_tier:
            allowed_price_tier = ["Low", "Medium", "High", "Premium"]
            if price_tier not in allowed_price_tier:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid price_tier. Allowed: {allowed_price_tier}"
                )

        # -------------------------
        # SAFE FILTERING
        # -------------------------
        if market_type:
            df = df[df["market_type"] == market_type]

        if crop_category:
            df = df[df["crop_category"] == crop_category]

        if year:
            df = df[df["year"] == year]

        if season:
            df = df[df["season"] == season]

        if price_tier:
            df = df[df["price_tier"] == price_tier]

        if district:
            df = df[df["farm_district"] == district]

        # -------------------------
        # COLUMN SAFETY CHECK
        # -------------------------
        required_cols = [
            "market_name",
            "market_type",
            "price_tier",
            "farm_district",
            "crop_name",
            "quantity_sold_ton",
            "revenue_bdt",
            "price_per_ton_bdt"
        ]

        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise HTTPException(
                status_code=500,
                detail=f"Missing columns: {missing}"
            )

        # -------------------------
        # GROUPING
        # -------------------------
        grouped = df.groupby(
            ["market_name", "market_type", "price_tier", "farm_district", "crop_name"],
            as_index=False
        ).agg({
            "quantity_sold_ton": "sum",
            "revenue_bdt": "sum",
            "price_per_ton_bdt": "mean"
        })

        grouped = grouped.rename(columns={
            "price_per_ton_bdt": "avg_price_per_ton_bdt",
            "farm_district": "district"
        })

        return {
            "comparison": grouped.to_dict(orient="records")
        }