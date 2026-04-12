# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CAPE TOWN ZONE DATA
# Source: City of Cape Town Zoning Scheme Regulations (November 2012)
# Cape Town uses "Floor Factor" (equivalent to FAR)
# Coverage is not specified for SR1 — uses floor factor + height instead
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAPETOWN_DATA_SOURCE = "City of Cape Town Zoning Scheme Regulations (November 2012)"

CAPETOWN_ZONES = {
    # ── SINGLE RESIDENTIAL ──────────────────────────────────────────────
    "Single Residential Zone 1 (SR1)": {
        "zone_display": "Single Residential Zone 1 — Conventional Housing (SR1)",
        "land_use": "Dwelling house, private road and additional use rights",
        "height": "9.0m wallplate / 11.0m roof (erven >650m²); 8.0m / 10.0m (erven ≤650m²)",
        "height_numeric": 9.0,
        "setbacks": "Street: 3.5–6.0m (varies by erf size) | Side: 0–6.0m (varies by erf size)",
        "notes": "Primary single residential zone. Floor factor and setbacks vary by erf size. Erven >2000m² have max floor space of 1500m². Additional use rights include home occupation, bed and breakfast, and home child care.",
        "erf_tiers": [
            {"min": 2001, "max": 99999, "floor_factor": None, "max_floor_space": 1500, "coverage": None, "height_wallplate": 9.0, "height_roof": 11.0, "street_bl": 6.0, "side_bl": 6.0},
            {"min": 1001, "max": 2000, "floor_factor": None, "max_floor_space": 1500, "coverage": None, "height_wallplate": 9.0, "height_roof": 11.0, "street_bl": 4.5, "side_bl": 3.0},
            {"min": 651, "max": 1000, "floor_factor": None, "max_floor_space": 1500, "coverage": None, "height_wallplate": 9.0, "height_roof": 11.0, "street_bl": 3.5, "side_bl": 3.0},
            {"min": 351, "max": 650, "floor_factor": 1.0, "max_floor_space": None, "coverage": None, "height_wallplate": 8.0, "height_roof": 10.0, "street_bl": 3.5, "side_bl": 0.0},
            {"min": 201, "max": 350, "floor_factor": 1.0, "max_floor_space": None, "coverage": None, "height_wallplate": 8.0, "height_roof": 10.0, "street_bl": 3.5, "side_bl": 0.0},
            {"min": 0, "max": 200, "floor_factor": 1.0, "max_floor_space": None, "coverage": None, "height_wallplate": 8.0, "height_roof": 10.0, "street_bl": 1.0, "side_bl": 0.0},
        ],
    },

    "Single Residential Zone 2 (SR2)": {
        "zone_display": "Single Residential Zone 2 — Incremental Housing (SR2)",
        "land_use": "Dwelling house, second dwelling, utility service, private road, urban agriculture, open space and additional use rights",
        "floor_factor": 1.0,
        "coverage": None,
        "height": "6.0m dwelling units / 8.0m other buildings",
        "height_numeric": 6.0,
        "setbacks": "Formal township: 0–1.0m | No formal township: 3.0m perimeter, 2.5m between shelters",
        "notes": "Incremental housing zone. Consent uses include group housing, boarding house, place of worship, institution, clinic, restaurant, guest house, shop, service trade. Approval of building plans required.",
    },

    # ── GENERAL RESIDENTIAL ─────────────────────────────────────────────
    "General Residential Zone 1 (GR1)": {
        "zone_display": "General Residential Subzone 1 — Group Housing (GR1)",
        "land_use": "Dwelling house, group housing, private road, open space and additional use rights",
        "floor_factor": None,
        "coverage": None,
        "density": "35 du/ha",
        "height": "8.0m wallplate / 10.0m roof",
        "height_numeric": 8.0,
        "setbacks": "Street: 5.0m (external), 0.0m (internal road) | Side: 3.0m (external), 0.0m (internal)",
        "notes": "Group housing zone. Density of 35 dwelling units per hectare. Requires design principles, open space provision, and site development plan. Flats and home occupation as additional use rights.",
    },

    "General Residential Zone 2 (GR2)": {
        "zone_display": "General Residential Subzone 2 (GR2)",
        "land_use": "Dwelling house, second dwelling, group housing, boarding house, flats, private road and open space",
        "floor_factor": 1.0,
        "coverage": 60,
        "height": "15.0m to top of roof",
        "height_numeric": 15.0,
        "setbacks": "Street: 4.5m | Side: 4.5m or 0.6H (0m up to 15m height for 18m from street and 60%)",
        "notes": "Low-rise general residential zone. Parking and access, screening, wind mitigation provisions apply. Dwelling house and second dwelling permitted outside group housing scheme.",
    },

    "General Residential Zone 3 (GR3)": {
        "zone_display": "General Residential Subzone 3 (GR3)",
        "land_use": "Dwelling house, second dwelling, group housing, boarding house, flats, private road and open space",
        "floor_factor": 1.0,
        "coverage": 60,
        "height": "20.0m to top of roof",
        "height_numeric": 20.0,
        "setbacks": "Street: 4.5m | Side: 4.5m or 0.6H (0m up to 15m height for 18m from street and 60%)",
        "notes": "Medium-rise general residential zone. Same uses and provisions as GR2 with increased height allowance.",
    },

    "General Residential Zone 4 (GR4)": {
        "zone_display": "General Residential Subzone 4 (GR4)",
        "land_use": "Dwelling house, second dwelling, group housing, boarding house, flats, private road and open space",
        "floor_factor": 1.5,
        "coverage": 60,
        "height": "24.0m to top of roof",
        "height_numeric": 24.0,
        "setbacks": "Street: 4.5m | Side: 4.5m or 0.6H (0m up to 15m height for 18m from street and 60%)",
        "notes": "Medium-high-rise general residential zone. Consent uses include institution, hospital, place of instruction, place of worship, place of assembly, shop.",
    },

    "General Residential Zone 5 (GR5)": {
        "zone_display": "General Residential Subzone 5 (GR5)",
        "land_use": "Dwelling house, second dwelling, group housing, boarding house, flats, private road and open space",
        "floor_factor": 2.5,
        "coverage": 60,
        "height": "35.0m to top of roof",
        "height_numeric": 35.0,
        "setbacks": "Street: 4.5m (9m above 25m height) | Side: 4.5m or 0.6H (0m up to 15m height for 18m from street); 15m above 25m height",
        "notes": "High-rise general residential zone. Increased setbacks above 25m height. Consent uses include institution, hospital, hotel, conference facility, guest house.",
    },

    "General Residential Zone 6 (GR6)": {
        "zone_display": "General Residential Subzone 6 (GR6)",
        "land_use": "Dwelling house, second dwelling, group housing, boarding house, flats, private road and open space",
        "floor_factor": 5.0,
        "coverage": 60,
        "height": "50.0m to top of roof",
        "height_numeric": 50.0,
        "setbacks": "Street: 4.5m (9m above 25m height) | Side: 4.5m or 0.6H (0m up to 15m height for 18m from street); 15m above 25m height",
        "notes": "Highest-density general residential zone. Maximum floor factor of 5.0. Same consent uses as GR5.",
    },

    # ── COMMUNITY ───────────────────────────────────────────────────────
    "Community Zone 1 (CO1)": {
        "zone_display": "Community Zone 1 — Local (CO1)",
        "land_use": "Place of instruction, place of worship, clinic, rooftop base telecommunication station and open space",
        "floor_factor": 0.8,
        "coverage": 60,
        "height": "12.0m to top of roof",
        "height_numeric": 12.0,
        "setbacks": "Street: 5.0m | Side: 5.0m",
        "notes": "Local community facilities zone. Consent uses include institution, hospital, place of assembly, cemetery, freestanding base telecommunication station, urban agriculture.",
    },

    "Community Zone 2 (CO2)": {
        "zone_display": "Community Zone 2 — Regional (CO2)",
        "land_use": "Institution, hospital, place of instruction, place of worship, place of assembly, rooftop base telecommunication station and open space",
        "floor_factor": 2.0,
        "coverage": 60,
        "height": "18.0m to top of roof",
        "height_numeric": 18.0,
        "setbacks": "Street: 5.0m | Side: 5.0m",
        "notes": "Regional community facilities zone. Consent uses include boarding house, conference facility, cemetery, crematorium, funeral parlour, freestanding base telecommunication station, urban agriculture.",
    },

    # ── LOCAL BUSINESS ──────────────────────────────────────────────────
    "Local Business Zone 1 (LB1)": {
        "zone_display": "Local Business Zone 1 — Intermediate Business (LB1)",
        "land_use": "Office, dwelling house, boarding house, utility services, flats and additional use rights",
        "height": "8.0–9.0m wallplate / 10.0–11.0m roof (varies by erf size)",
        "height_numeric": 9.0,
        "setbacks": "Street: 3.5m | Side: 0–3.0m (varies by erf size)",
        "notes": "Intermediate business zone. Floor factor of 1.0 across all erf sizes. Consent uses include place of instruction, place of worship, institution, clinic, place of assembly, guest house, shop, informal trading, service trade.",
        "erf_tiers": [
            {"min": 1001, "max": 99999, "floor_factor": 1.0, "coverage": None, "height_wallplate": 9.0, "height_roof": 11.0, "street_bl": 3.5, "side_bl": 3.0},
            {"min": 651, "max": 1000, "floor_factor": 1.0, "coverage": None, "height_wallplate": 9.0, "height_roof": 11.0, "street_bl": 3.5, "side_bl": 3.0},
            {"min": 351, "max": 650, "floor_factor": 1.0, "coverage": None, "height_wallplate": 8.0, "height_roof": 10.0, "street_bl": 3.5, "side_bl": 0.0},
            {"min": 201, "max": 350, "floor_factor": 1.0, "coverage": None, "height_wallplate": 8.0, "height_roof": 10.0, "street_bl": 3.5, "side_bl": 0.0},
            {"min": 0, "max": 200, "floor_factor": 1.0, "coverage": None, "height_wallplate": 8.0, "height_roof": 10.0, "street_bl": 1.0, "side_bl": 0.0},
        ],
    },

    "Local Business Zone 2 (LB2)": {
        "zone_display": "Local Business Zone 2 — Local Business (LB2)",
        "land_use": "Shop, office, dwelling house, second dwelling, bed and breakfast establishment, boarding house, flats, place of instruction, place of worship, institution, clinic, guest house, service trade, utility service, rooftop base telecommunication station, private road and open space",
        "floor_factor": 1.0,
        "coverage": 75,
        "height": "12.0m to top of roof",
        "height_numeric": 12.0,
        "setbacks": "Street: 0.0m | Side: 0.0m",
        "notes": "Local business zone permitting a wide mix of uses including retail, residential and community. Canopy projection, street corners, parking and access, loading, screening provisions apply. Service station and motor repair garage as consent uses.",
    },

    # ── GENERAL BUSINESS ────────────────────────────────────────────────
    "General Business Zone 1 (GB1)": {
        "zone_display": "General Business Subzone 1 (GB1)",
        "land_use": "Business premises, dwelling house, second dwelling, boarding house, flats, place of instruction, place of worship, hospital, place of assembly, place of entertainment, hotel, conference facility, service trade, authority use, utility service, rooftop base telecommunication station, multiple parking garage, private road and open space",
        "floor_factor": 1.5,
        "coverage": 100,
        "height": "15.0m",
        "height_numeric": 15.0,
        "setbacks": "Street: 0.0m up to 10m height, 4.5m above 10m | Side: 0.0m",
        "notes": "General business zone. Residential incentive available in respect of GB7. Hotel floor space concession. Canopy or balcony projection permitted. Public pedestrian footway along street boundary.",
    },

    "General Business Zone 2 (GB2)": {
        "zone_display": "General Business Subzone 2 (GB2)",
        "land_use": "Business premises, dwelling house, second dwelling, boarding house, flats, place of instruction, place of worship, hospital, place of assembly, place of entertainment, hotel, conference facility, service trade, authority use, utility service, rooftop base telecommunication station, multiple parking garage, private road and open space",
        "floor_factor": 2.0,
        "coverage": 100,
        "height": "15.0m",
        "height_numeric": 15.0,
        "setbacks": "Street: 0.0m up to 10m height, 4.5m above 10m | Side: 0.0m",
        "notes": "General business zone with higher density than GB1. Same permitted uses and provisions.",
    },

    "General Business Zone 3 (GB3)": {
        "zone_display": "General Business Subzone 3 (GB3)",
        "land_use": "Business premises, dwelling house, second dwelling, boarding house, flats, place of instruction, place of worship, hospital, place of assembly, place of entertainment, hotel, conference facility, service trade, authority use, utility service, rooftop base telecommunication station, multiple parking garage, private road and open space",
        "floor_factor": 2.0,
        "coverage": 100,
        "height": "25.0m",
        "height_numeric": 25.0,
        "setbacks": "Street: 0.0m up to 10m height, 4.5m above 10m | Side: 0.0m",
        "notes": "General business zone. Higher height allowance than GB1/GB2.",
    },

    "General Business Zone 4 (GB4)": {
        "zone_display": "General Business Subzone 4 (GB4)",
        "land_use": "Business premises, dwelling house, second dwelling, boarding house, flats, place of instruction, place of worship, hospital, place of assembly, place of entertainment, hotel, conference facility, service trade, authority use, utility service, rooftop base telecommunication station, multiple parking garage, private road and open space",
        "floor_factor": 3.0,
        "coverage": 100,
        "height": "25.0m",
        "height_numeric": 25.0,
        "setbacks": "Street: 0.0m up to 10m height, 4.5m above 10m | Side: 0.0m",
        "notes": "General business zone with high density. Floor factor 3.0.",
    },

    "General Business Zone 5 (GB5)": {
        "zone_display": "General Business Subzone 5 (GB5)",
        "land_use": "Business premises, dwelling house, second dwelling, boarding house, flats, place of instruction, place of worship, hospital, place of assembly, place of entertainment, hotel, conference facility, service trade, authority use, utility service, rooftop base telecommunication station, multiple parking garage, private road and open space",
        "floor_factor": 4.0,
        "coverage": 100,
        "height": "25.0m",
        "height_numeric": 25.0,
        "setbacks": "Street: 0.0m | Side: 0.0m",
        "notes": "High-density general business zone. Floor factor 4.0.",
    },

    "General Business Zone 6 (GB6)": {
        "zone_display": "General Business Subzone 6 (GB6)",
        "land_use": "Business premises, dwelling house, second dwelling, boarding house, flats, place of instruction, place of worship, hospital, place of assembly, place of entertainment, hotel, conference facility, service trade, authority use, utility service, rooftop base telecommunication station, multiple parking garage, private road and open space",
        "floor_factor": 6.0,
        "coverage": 100,
        "height": "38.0m",
        "height_numeric": 38.0,
        "setbacks": "Street: 0.0m up to 25m height, ½(H-25m) above 25m | Side: 0.0m",
        "notes": "High-rise general business zone. Floor factor 6.0. Increased setbacks above 25m height.",
    },

    "General Business Zone 7 (GB7)": {
        "zone_display": "General Business Subzone 7 (GB7)",
        "land_use": "Business premises, dwelling house, second dwelling, boarding house, flats, place of instruction, place of worship, hospital, place of assembly, place of entertainment, hotel, conference facility, service trade, authority use, utility service, rooftop base telecommunication station, multiple parking garage, private road and open space",
        "floor_factor": 12.0,
        "coverage": 100,
        "height": "60.0m",
        "height_numeric": 60.0,
        "setbacks": "Street: 0.0m up to 38m height, ½(H-38m) above 38m | Side: 0.0m",
        "notes": "Highest-density general business zone. Floor factor 12.0. CBD-scale development. Increased setbacks above 38m height.",
    },

    # ── MIXED USE ───────────────────────────────────────────────────────
    "Mixed Use Zone 1 (MU1)": {
        "zone_display": "Mixed Use Subzone 1 (MU1)",
        "land_use": "Business premises, industry, dwelling house, second dwelling, boarding house, flats, place of instruction, place of worship, institution, hospital, place of assembly, place of entertainment, hotel, conference facility, authority use, utility service, rooftop base telecommunication station, transport use, multiple parking garage, private road and open space",
        "floor_factor": 1.5,
        "coverage": 75,
        "height": "15.0m",
        "height_numeric": 15.0,
        "setbacks": "Street: 0.0m up to 10m height, 4.5m above 10m | Side: 0.0m",
        "notes": "Low-rise mixed use zone. Canopy or balcony projection permitted. Parking and access, loading, screening provisions apply.",
    },

    "Mixed Use Zone 2 (MU2)": {
        "zone_display": "Mixed Use Subzone 2 (MU2)",
        "land_use": "Business premises, industry, dwelling house, second dwelling, boarding house, flats, place of instruction, place of worship, institution, hospital, place of assembly, place of entertainment, hotel, conference facility, authority use, utility service, rooftop base telecommunication station, transport use, multiple parking garage, private road and open space",
        "floor_factor": 4.0,
        "coverage": 100,
        "height": "25.0m",
        "height_numeric": 25.0,
        "setbacks": "Street: 0.0m up to 10m height, 4.5m above 10m | Side: 0.0m",
        "notes": "Medium-rise mixed use zone. Higher density and coverage than MU1.",
    },

    "Mixed Use Zone 3 (MU3)": {
        "zone_display": "Mixed Use Subzone 3 (MU3)",
        "land_use": "Business premises, industry, dwelling house, second dwelling, boarding house, flats, place of instruction, place of worship, institution, hospital, place of assembly, place of entertainment, hotel, conference facility, authority use, utility service, rooftop base telecommunication station, transport use, multiple parking garage, private road and open space",
        "floor_factor": 6.0,
        "coverage": 100,
        "height": "38.0m",
        "height_numeric": 38.0,
        "setbacks": "Street: 0.0m up to 25m height, ½(H-25m) above 25m | Side: 0.0m",
        "notes": "High-rise mixed use zone. Floor factor 6.0. Increased setbacks above 25m height.",
    },

    # ── INDUSTRIAL ──────────────────────────────────────────────────────
    "General Industry Zone 1 (GI1)": {
        "zone_display": "General Industry Subzone 1 (GI1)",
        "land_use": "Industry, restaurant, service station, motor repair garage, funeral parlour, scrap yard, authority use, utility service, crematorium, rooftop base telecommunication station, freestanding base telecommunication station, multiple parking garage, open space and additional use rights",
        "floor_factor": 1.5,
        "coverage": 75,
        "height": "18.0m",
        "height_numeric": 18.0,
        "setbacks": "Street: 5.0m | Side: 3.0m",
        "notes": "General industrial zone. Consent uses include place of worship, institution, clinic, place of assembly, adult entertainment business, office, shop, warehouse, wind turbine infrastructure, container site.",
    },

    "General Industry Zone 2 (GI2)": {
        "zone_display": "General Industry Subzone 2 (GI2)",
        "land_use": "Industry, restaurant, service station, motor repair garage, funeral parlour, scrap yard, authority use, utility service, crematorium, rooftop base telecommunication station, freestanding base telecommunication station, multiple parking garage, open space and additional use rights",
        "floor_factor": 4.0,
        "coverage": 75,
        "height": "18.0m (no restriction for manufacturing buildings)",
        "height_numeric": 18.0,
        "setbacks": "Street: 5.0m | Side: 3.0m",
        "notes": "Higher-density industrial zone. No height restriction for manufacturing buildings. Same uses as GI1.",
    },

    "Risk Industry Zone (RI)": {
        "zone_display": "Risk Industry Zone (RI)",
        "land_use": "Noxious trade, risk activity, crematorium, rooftop base telecommunication station, freestanding base telecommunication station, private road, open space and additional use rights",
        "floor_factor": 2.0,
        "coverage": 75,
        "height": "18.0m (no restriction for noxious trade, risk activity or manufacturing buildings)",
        "height_numeric": 18.0,
        "setbacks": "Street: 5.0m | Side: 5.0m",
        "notes": "Risk industry zone for hazardous activities. Boundary walls, hazardous substances provisions, screening requirements apply. Consent uses include shop, restaurant, informal trading, service station, motor repair garage, industry, scrap yard.",
    },

    # ── TRANSPORT ───────────────────────────────────────────────────────
    "Transport Zone 1 (TR1)": {
        "zone_display": "Transport Zone 1 — Transport Use (TR1)",
        "land_use": "Transport use, multiple parking garage, utility service, warehouse, rooftop base telecommunication station and container site",
        "floor_factor": 2.0,
        "coverage": 75,
        "height": "15.0m for stacked shipping containers; 18.0m for other buildings",
        "height_numeric": 15.0,
        "setbacks": "Street: 0.0m | Side: 3.0m",
        "notes": "Transport use zone. Consent uses include business premises, flats, place of assembly, place of entertainment, hotel, conference facility, service station, motor repair garage, service trade, freestanding base telecommunication station, airport, helicopter landing pad, informal trading, industry.",
    },

    # ── AGRICULTURAL / RURAL ────────────────────────────────────────────
    "Agricultural Zone (AG)": {
        "zone_display": "Agricultural Zone (AG)",
        "land_use": "Agriculture, intensive horticulture, dwelling house, riding stables, environmental conservation use, environmental facilities, rooftop base telecommunication station and additional use rights",
        "floor_factor": None,
        "coverage": None,
        "max_floor_space": "1500m² for all dwelling units; 100m² for farm shop",
        "height": "9.0m wallplate / 11.0m roof (dwelling house); 12.0m (agricultural buildings)",
        "height_numeric": 9.0,
        "setbacks": ">20ha: Street 30m, Side 30m | ≤20ha: Street 15m, Side 15m",
        "notes": "Agricultural zone. Minimum subdivision size applies. Second dwelling and additional dwelling units as additional use rights. Consent uses include guest house, hotel, tourist accommodation, tourist facilities, intensive animal farming, harvesting of natural resources, mine, farm shop.",
    },

    "Rural Zone (RU)": {
        "zone_display": "Rural Zone (RU)",
        "land_use": "Dwelling house, agriculture and additional use rights",
        "floor_factor": None,
        "coverage": 40,
        "max_floor_space": "1500m² for all buildings; 100m² for farm shop",
        "height": "9.0m wallplate / 11.0m roof",
        "height_numeric": 9.0,
        "setbacks": "Street: 10.0m | Side: 5.0m",
        "notes": "Rural zone. Minimum subdivision size of 1500m². Additional use rights include second dwelling, home occupation, bed and breakfast. Consent uses include guest house, tourist accommodation, tourist facilities, harvesting of natural resources, mine.",
    },
}


def get_capetown_zone_params(zone_key, erf_size=None):
    """Get zoning parameters for a Cape Town zone.

    For zones with erf-size tiers (SR1, LB1), erf_size determines
    which tier's parameters apply.
    """
    zone = CAPETOWN_ZONES.get(zone_key)
    if not zone:
        return None

    # Check if zone has erf-size tiers
    if "erf_tiers" in zone and erf_size:
        tier = None
        for t in zone["erf_tiers"]:
            if t["min"] <= erf_size <= t["max"]:
                tier = t
                break
        if not tier:
            tier = zone["erf_tiers"][-1]  # fallback to smallest tier

        floor_factor = tier.get("floor_factor")
        max_floor_space = tier.get("max_floor_space")
        coverage = tier.get("coverage")
        height_numeric = tier.get("height_roof", zone.get("height_numeric", 10.0))

        return {
            "zone_display": zone["zone_display"],
            "land_use": zone["land_use"],
            "floor_factor": floor_factor,
            "max_floor_space": max_floor_space,
            "coverage": coverage,
            "height": zone["height"],
            "height_numeric": height_numeric,
            "setbacks": f"Street: {tier['street_bl']}m | Side: {tier['side_bl']}m",
            "notes": zone["notes"],
        }

    # Standard zone (no tiers)
    return {
        "zone_display": zone["zone_display"],
        "land_use": zone["land_use"],
        "floor_factor": zone.get("floor_factor"),
        "coverage": zone.get("coverage"),
        "height": zone["height"],
        "height_numeric": zone["height_numeric"],
        "setbacks": zone["setbacks"],
        "notes": zone["notes"],
    }


def calculate_capetown_floor_space(zone_key, erf_size):
    """Calculate maximum buildable floor space for a Cape Town zone.

    Cape Town uses 'floor factor' (equivalent to FAR).
    Some zones (SR1 large erven) use a fixed max floor space instead.
    """
    params = get_capetown_zone_params(zone_key, erf_size)
    if not params:
        return None, None, "Zone not found"

    floor_factor = params.get("floor_factor")
    max_floor_space = params.get("max_floor_space")

    if max_floor_space and not floor_factor:
        # Fixed max (e.g., SR1 erven >650m²)
        if isinstance(max_floor_space, (int, float)):
            formula = f"Fixed maximum: {max_floor_space} m²"
            return f"{int(max_floor_space)} m²", params.get("coverage"), formula
        else:
            formula = f"Fixed maximum: {max_floor_space}"
            return max_floor_space, params.get("coverage"), formula

    if floor_factor:
        result = erf_size * floor_factor
        # Apply cap if both floor_factor and max_floor_space exist
        if max_floor_space and isinstance(max_floor_space, (int, float)):
            result = min(result, max_floor_space)
        formula = f"{erf_size} m² × {floor_factor} = {int(result)} m²"
        return f"{int(result)} m²", params.get("coverage"), formula

    return "N/a", params.get("coverage"), "Floor factor not specified for this zone"
