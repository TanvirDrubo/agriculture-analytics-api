from fastapi import HTTPException

# Import shared validation constants from a single source of truth
# This avoids duplication across services and keeps rules consistent
from app.validators.common_validator import (
    VALID_REGIONS,
    VALID_FARM_TYPES,
    VALID_METRICS
)


class FarmsValidator:
    """
    FarmsValidator
    --------------
    This class contains ONLY validation logic for farm-related inputs.

    Responsibility:
    - Validate request parameters before they reach service layer
    - Ensure only allowed values enter business logic
    - Raise HTTP 422 errors for invalid inputs

    NOTE:
    - No business logic here
    - No pandas / DB logic here
    """


    @staticmethod
    def validate_region(region: str):
        """
        Validate farm region input.

        Rules:
        - region can be None (optional filter)
        - if provided, must exist in VALID_REGIONS list
        """
        if region and region not in VALID_REGIONS:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid region. Allowed values: {VALID_REGIONS}"
            )


    @staticmethod
    def validate_farm_type(farm_type: str):
        """
        Validate farm type input.

        Rules:
        - Optional parameter (can be None)
        - Must be one of predefined farm types
        """
        if farm_type and farm_type not in VALID_FARM_TYPES:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid farm_type. Allowed values: {VALID_FARM_TYPES}"
            )


    @staticmethod
    def validate_metric(metric: str):
        """
        Validate metric input used in analytics endpoints.

        Example metrics:
        - profit
        - revenue

        Rules:
        - Must be in VALID_METRICS list
        """
        if metric and metric not in VALID_METRICS:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid metric. Allowed values: {VALID_METRICS}"
            )