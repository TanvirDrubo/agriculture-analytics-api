from typing import Optional
from fastapi import APIRouter, Query

from app.services.crops_service import CropsService

router = APIRouter(prefix="/crops", tags=["Crops"])


# =========================
# 1. YIELD EFFICIENCY
# =========================
@router.get("/yield-efficiency")
def yield_efficiency():
    return CropsService.yield_efficiency()


# =========================
# 2. SEASONAL TREND
# =========================
@router.get("/seasonal-trend")
def seasonal_trend(
    year: Optional[int] = Query(
        None,
        description="Filter by year (e.g., 2022, 2023, 2024)"
    ),
    season: Optional[str] = Query(
        None,
        description="Filter by season (Kharif, Rabi, Zaid)"
    )
):
    return CropsService.seasonal_trend(year, season)


# =========================
# 3. QUALITY BREAKDOWN
# =========================
@router.get("/quality-breakdown")
def quality_breakdown(
    crop_category: Optional[str] = Query(
        None,
        description="Crop category (Cereal, Vegetable, Fruit, Pulse, Oilseed, Cash Crop, Spice)"
    ),
    year: Optional[int] = Query(
        None,
        description="Year filter (2022–2024)"
    ),
    region: Optional[str] = Query(
        None,
        description="Region (Dhaka, Chittagong, Sylhet, etc.)"
    ),
    market_type: Optional[str] = Query(
        None,
        description="Market type (Local, Wholesale, Export, Retail, Government Procurement)"
    ),
    pesticide_residue: Optional[str] = Query(
        None,
        description="Pesticide residue level (None, Trace, Low, High)"
    )
):
    return CropsService.quality_breakdown(
        crop_category=crop_category,
        year=year,
        region=region,
        market_type=market_type,
        pesticide_residue=pesticide_residue
    )