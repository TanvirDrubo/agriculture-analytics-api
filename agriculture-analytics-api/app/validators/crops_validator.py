from fastapi import HTTPException

# Import shared valid values from common validator
# This ensures consistency across all services (farms, crops, markets)
from app.validators.common_validator import VALID_SEASONS


class CropsValidator:
    """
    CropsValidator
    --------------
    Handles validation logic for crop-related API inputs.

    Responsibility:
    - Validate query parameters (year, season, etc.)
    - Ensure inputs are within allowed business rules
    - Raise HTTP 422 errors for invalid user input

    NOTE:
    - No DB logic here
    - No pandas/data processing here
    - Only input validation
    """


    @staticmethod
    def validate_year(year: int):
        """
        Validate year input for crop analytics.

        Rules:
        - year is optional (None allowed)
        - if provided, must be within realistic range (2000–2100)
        """

        if year is not None and (year < 2000 or year > 2100):
            raise HTTPException(
                status_code=422,
                detail="Invalid year range. Year must be between 2000 and 2100."
            )


    @staticmethod
    def validate_season(season: str):
        """
        Validate crop season input.

        Allowed seasons are defined in:
        VALID_SEASONS = ["Kharif", "Rabi", "Zaid"]

        Rules:
        - season is optional (None allowed)
        - if provided, must be one of predefined seasons
        """

        if season and season not in VALID_SEASONS:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid season. Allowed values: {VALID_SEASONS}"
            )