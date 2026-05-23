# =========================
# PURE FILTER LOGIC
# NO VALIDATION (IMPORTANT RULE)
# =========================

def apply_filters(df, region=None, year=None, farm_type=None):
    """
    Applies filters safely on dataframe.
    Assumes validation already done in validators.
    """

    if df is None or df.empty:
        return df

    # -------------------------
    # REGION FILTER
    # -------------------------
    if region and "region" in df.columns:
        df = df[df["region"] == region]

    # -------------------------
    # YEAR FILTER
    # -------------------------
    if year and "year" in df.columns:
        df = df[df["year"] == year]

    # -------------------------
    # FARM TYPE FILTER
    # -------------------------
    if farm_type and "farm_type" in df.columns:
        df = df[df["farm_type"] == farm_type]

    return df