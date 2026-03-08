def calculate_feasibility(property_data):
    """
    Calculate feasibility score and maximum buildable floor area.

    Args:
        property_data: Dictionary containing property information

    Returns:
        score (int):          0-100 feasibility score
        notes (list):         Factors affecting the score
        grade (str):          A, B, C, D, or F
        grade_text (str):     Human-readable grade label
        buildable_area (str): Formatted max floor area string, or None
    """
    score = 100
    notes = []

    # ── Coverage constraint ───────────────────
    coverage = property_data.get('coverage_numeric', 100)
    if coverage < 40:
        score -= 20
        notes.append("⚠️ Low coverage allowance (under 40%)")
    elif coverage < 50:
        score -= 10
        notes.append("⚠️ Moderate coverage restriction")
    else:
        notes.append("✓ Good coverage allowance")

    # ── Height constraint ─────────────────────
    height = property_data.get('height_numeric', 10)
    if height <= 1:
        score -= 20
        notes.append("⚠️ Severe height restriction (single storey only)")
    elif height <= 2:
        score -= 10
        notes.append("⚠️ Height limited to 2 storeys")
    else:
        notes.append("✓ Favorable height allowance")

    # ── Heritage overlay ──────────────────────
    if property_data.get('heritage_overlay', 0) == 1:
        score -= 25
        notes.append("⚠️ Heritage overlay - additional approvals required")
    else:
        notes.append("✓ No heritage restrictions")

    # ── Environmental restriction ─────────────
    if property_data.get('environmental_restriction', 0) == 1:
        score -= 20
        notes.append("⚠️ Environmental constraints apply")
    else:
        notes.append("✓ No environmental restrictions")

    # ── Grade ─────────────────────────────────
    if score >= 90:
        grade, grade_text = "A", "Excellent"
    elif score >= 80:
        grade, grade_text = "B", "Good"
    elif score >= 70:
        grade, grade_text = "C", "Fair"
    elif score >= 60:
        grade, grade_text = "D", "Limited"
    else:
        grade, grade_text = "F", "Restricted"

    # ── Maximum Buildable Floor Area ──────────
    buildable_area = None
    try:
        erf_size = float(property_data.get('erf_size') or 0)
        far = float(property_data.get('floor_area_ratio') or 0)
        if erf_size > 0 and far > 0:
            area = erf_size * far
            buildable_area = f"{area:,.0f} m²"
    except (ValueError, TypeError):
        pass  # leave as None if data is missing or non-numeric

    return score, notes, grade, grade_text, buildable_area