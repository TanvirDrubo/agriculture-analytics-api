from typing import Optional
from fastapi import APIRouter, Query

from app.services.markets_service import MarketService

router = APIRouter(prefix="/markets", tags=["Markets"])


# =========================
# PRICE COMPARISON
# =========================
@router.get("/price-comparison")
def price_comparison(
    market_type: Optional[str] = Query(
        None,
        description="Market type (Local, Wholesale, Export, Retail, Government Procurement)"
    ),
    crop_category: Optional[str] = Query(
        None,
        description="Crop category (Cereal, Vegetable, Fruit, Pulse, Oilseed, Cash Crop, Spice)"
    ),
    year: Optional[int] = Query(
        None,
        description="Year filter (2022–2024)"
    ),
    season: Optional[str] = Query(
        None,
        description="Season (Spring, Summer, Autumn, Winter)"
    ),
    price_tier: Optional[str] = Query(
        None,
        description="Price tier (Low, Medium, High, Premium)"
    ),
    district: Optional[str] = Query(
        None,
        description="Farm district filter"
    )
):
    return MarketService.price_comparison(
        market_type,
        crop_category,
        year,
        season,
        price_tier,
        district
    )