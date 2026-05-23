from typing import Optional
from fastapi import APIRouter, Query

from app.services.farms_service import FarmsService

router = APIRouter(prefix="/farms", tags=["Farms"])


# =========================
# 1. FARM SUMMARY
# =========================
@router.get("/summary")
def farm_summary(
    region: Optional[str] = Query(
        None,
        description="Region filter (Dhaka, Chittagong, Sylhet, Rajshahi, Khulna, Rangpur, Barisal, Mymensingh)"
    ),
    year: Optional[int] = Query(
        None,
        description="Year filter (2022–2024)"
    ),
    farm_type: Optional[str] = Query(
        None,
        description="Farm type (Small, Medium, Large, Commercial)"
    )
):
    return FarmsService.summary(region, year, farm_type)


# =========================
# 2. FARM PERFORMANCE
# =========================
@router.get("/{farm_id}/performance")
def farm_performance(
    farm_id: int,
    year: Optional[int] = Query(
        None,
        description="Year filter (2022–2024)"
    ),
    crop_category: Optional[str] = Query(
        None,
        description="Crop category (Cereal, Vegetable, Fruit, Pulse, Oilseed, Cash Crop, Spice)"
    ),
    market_type: Optional[str] = Query(
        None,
        description="Market type (Local, Wholesale, Export, Retail, Government Procurement)"
    )
):
    return FarmsService.farm_performance(
        farm_id,
        year,
        crop_category,
        market_type
    )


# =========================
# 3. TOP FARMS
# =========================
@router.get("/top")
def top_farms(
    metric: str = Query(
        "profit",
        description="Metric to rank farms (profit, revenue, cost, loss)"
    ),
    limit: int = Query(
        10,
        description="Number of top farms to return"
    )
):
    return FarmsService.top_farms(metric, limit)


# =========================
# 4. LOSS ANALYSIS
# =========================
@router.get("/loss-analysis")
def loss_analysis(
    region: Optional[str] = Query(
        None,
        description="Region filter"
    ),
    year: Optional[int] = Query(
        None,
        description="Year filter (2022–2024)"
    ),
    season: Optional[str] = Query(
        None,
        description="Season (Spring, Summer, Autumn, Winter)"
    ),
    quality_grade: Optional[str] = Query(
        None,
        description="Quality grade (A, B, C, D)"
    ),
    crop_category: Optional[str] = Query(
        None,
        description="Crop category filter"
    )
):
    return FarmsService.loss_analysis(
        region,
        year,
        season,
        quality_grade,
        crop_category
    )