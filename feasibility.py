import re

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

    Also sets, in place on property_data (for the template/PDF to display):
        buildable_basis   (str): short label for how the figure was derived
        buildable_formula (str): human-readable derivation
    """
    score = 80
    notes = []

    # Coverage constraint
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

    # Height constraint
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

    # Heritage overlay
    if property_data.get('heritage_overlay', 0) == 1:
        score -= 20
        notes.append("-  Heritage overlay applies (additional approvals required)")

    # Environmental restriction
    if property_data.get('environmental_restriction', 0) == 1:
        score -= 15
        notes.append("-  Environmental constraints apply")

    # Grade
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

    # Maximum Buildable Floor Area.
    # NMBM does NOT publish a Floor Area Ratio - it regulates by coverage % plus
    # a height limit, so for NMBM we derive the envelope from the official
    # coverage limit and the stated storeys. Joburg (official FAR) and Cape Town
    # (official Floor Factor) keep using erf size x FAR.
    STOREY_HEIGHT_M = 3.0  # residential floor-to-floor (m); used only when storeys aren't stated

    buildable_area = None
    property_data['buildable_basis'] = None
    property_data['buildable_formula'] = None

    # Zones where a floor-area figure is meaningless - don't show one.
    zone_text = " ".join(str(property_data.get(k, "")) for k in
                         ("zone", "zone_key", "zone_code", "zone_display",
                          "display", "land_use")).lower()
    NON_DEVELOPABLE = ("special", "parking", "open space", "private open",
                       "public open", "institutional", "transport",
                       "undetermined", "agricultur", "conservation")
    is_non_developable = any(t in zone_text for t in NON_DEVELOPABLE)

    try:
        erf_size = float(property_data.get('erf_size') or 0)
        municipality = (property_data.get('municipality') or '').lower()

        if erf_size > 0 and not is_non_developable:
            if municipality == 'nmbm':
                cov = float(property_data.get('coverage_numeric') or 0)

                # Prefer the storey count the scheme states (e.g. "2 storeys (~6m)"
                # or the code "2 FLRS"); only derive from metres when none is given.
                storeys = 0
                hmatch = re.search(r'(\d+)\s*(storey|floor|flr)',
                                   str(property_data.get('height', '')), re.IGNORECASE)
                if hmatch:
                    storeys = int(hmatch.group(1))
                else:
                    h_m = float(property_data.get('height_numeric') or 0)
                    if h_m > 0:
                        storeys = max(1, int(h_m // STOREY_HEIGHT_M))

                if cov > 0 and storeys > 0:
                    footprint = (cov / 100.0) * erf_size
                    area = footprint * storeys
                    buildable_area = f"{area:,.0f} m²"
                    property_data['buildable_basis'] = "Estimated envelope (coverage × storeys)"
                    property_data['buildable_formula'] = (
                        f"{cov:.0f}% coverage × {erf_size:,.0f} m² "
                        f"× {storeys} storey{'s' if storeys != 1 else ''}. "
                        f"NMBM regulates by coverage and height, not FAR — "
                        f"this is an estimated maximum gross floor area."
                    )
            else:
                # Johannesburg / Cape Town - official FAR or Floor Factor
                far = float(property_data.get('floor_area_ratio') or 0)
                if far > 0:
                    area = erf_size * far
                    buildable_area = f"{area:,.0f} m²"
                    if municipality in ('joburg', 'johannesburg', 'jhb'):
                        src_name = "Johannesburg Town Planning Scheme"
                    elif municipality in ('capetown', 'cape town', 'cct', 'ct'):
                        src_name = "City of Cape Town Zoning Scheme"
                    else:
                        src_name = "the applicable town planning scheme"
                    property_data['buildable_basis'] = "Official FAR"
                    property_data['buildable_formula'] = (
                        f"{erf_size:,.0f} m² × {far} FAR "
                        f"(Floor Area Ratio, official under the {src_name})."
                    )
    except (ValueError, TypeError):
        pass

    return score, notes, grade, grade_text, buildable_area