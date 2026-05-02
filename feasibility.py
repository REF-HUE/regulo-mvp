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
    score = 80
    notes = []

    # — Coverage constraint
    # Bonus only for genuinely high-density coverage (>75%)
    # Neutral for 50–75% (normal residential range)
    # Deductions below 50%
    coverage = property_data.get('coverage_numeric', 100)
    if coverage < 40:
        score -= 20
        notes.append("-  Low coverage allowance (under 40%)")
    elif coverage < 50:
        score -= 10
        notes.append("-  Moderate coverage restriction (under 50%)")
    elif coverage > 75:
        score += 5
        notes.append("+  High coverage allowance (above 75%)")

    # — Height constraint
    # Bonus only for genuinely multi-storey capable (>10m)
    # Neutral for 6–10m (standard residential heights)
    # Deductions below 6m
    height = property_data.get('height_numeric', 10)
    if height < 3:
        score -= 20
        notes.append("-  Severe height restriction (under 3m)")
    elif height < 6:
        score -= 10
        notes.append("-  Height restriction applies (under 6m)")
    elif height > 10:
        score += 5
        notes.append("+  Multi-storey height allowance")

    # — Heritage overlay
    # Absent = silent (not a positive feature, just normal)
    if property_data.get('heritage_overlay', 0) == 1:
        score -= 20
        notes.append("-  Heritage overlay applies (additional approvals required)")

    # — Environmental restriction
    # Absent = silent
    if property_data.get('environmental_restriction', 0) == 1:
        score -= 15
        notes.append("-  Environmental constraints apply")

    # — Grade
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

    # — Maximum Buildable Floor Area
    buildable_area = None
    try:
        erf_size = float(property_data.get('erf_size') or 0)
        far = float(property_data.get('floor_area_ratio') or 0)
        if erf_size > 0 and far > 0:
            area = erf_size * far
            buildable_area = f"{area:,.0f} m²"
    except (ValueError, TypeError):
        pass

    return score, notes, grade, grade_text, buildable_area
