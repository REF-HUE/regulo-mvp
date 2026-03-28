# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# REGULO SYSTEMS — johannesburg_zones.py
# Johannesburg Town Planning Scheme zoning parameters
# Source: City of Johannesburg Town Planning Scheme, 1979 (as amended)
#
# Johannesburg uses a HEIGHT ZONE system (A, B, C) that modifies
# FAR and coverage per zone. Height Zone A = lowest intensity,
# Height Zone C = highest intensity.
#
# NOTE: FAR values are official in Johannesburg (unlike NMBM which
# uses coverage + height). Coverage is derived from zone parameters.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JOBURG_DATA_SOURCE = "City of Johannesburg Town Planning Scheme, 1979 (as amended)"

# Height Zone descriptions
HEIGHT_ZONES = {
    "A": "Height Zone A — Low intensity, typically suburban areas",
    "B": "Height Zone B — Medium intensity, transitional areas",
    "C": "Height Zone C — High intensity, urban core and corridors",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ZONE DEFINITIONS
# Each zone contains parameters per Height Zone (A, B, C)
# far = Floor Area Ratio (official)
# coverage = maximum coverage %
# height = maximum height description
# height_numeric = height in metres for feasibility calc
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JOBURG_ZONES = {
    "Residential 1": {
        "display": "Residential 1 — Single Dwelling",
        "land_use": "Single dwelling house per erf",
        "setbacks": "Street: 3m | Side: 1.5m | Rear: 3m",
        "notes": "Single residential zone. One dwelling per erf. Second dwelling (cottage) may be permitted with consent.",
        "height_zones": {
            "A": {"far": 0.40, "coverage": 50, "height": "2 storeys / 8.5m", "height_numeric": 8.5},
            "B": {"far": 0.50, "coverage": 55, "height": "2 storeys / 8.5m", "height_numeric": 8.5},
            "C": {"far": 0.60, "coverage": 60, "height": "2 storeys / 8.5m", "height_numeric": 8.5},
        }
    },
    "Residential 2": {
        "display": "Residential 2 — Two Dwellings",
        "land_use": "Two dwelling units per erf (duplex, semi-detached)",
        "setbacks": "Street: 3m | Side: 1.5m | Rear: 3m",
        "notes": "Allows two dwelling units per erf. Suitable for duplex or semi-detached houses.",
        "height_zones": {
            "A": {"far": 0.50, "coverage": 50, "height": "2 storeys / 8.5m", "height_numeric": 8.5},
            "B": {"far": 0.65, "coverage": 55, "height": "2 storeys / 8.5m", "height_numeric": 8.5},
            "C": {"far": 0.80, "coverage": 60, "height": "3 storeys / 11m", "height_numeric": 11.0},
        }
    },
    "Residential 3": {
        "display": "Residential 3 — Group Housing",
        "land_use": "Group housing, townhouses, cluster developments",
        "setbacks": "Street: 3m | Side: 2m | Rear: 2m",
        "notes": "Group housing zone for townhouse and cluster developments. Minimum erf size typically 200m² per unit.",
        "height_zones": {
            "A": {"far": 0.60, "coverage": 50, "height": "2 storeys / 8.5m", "height_numeric": 8.5},
            "B": {"far": 0.80, "coverage": 55, "height": "3 storeys / 11m", "height_numeric": 11.0},
            "C": {"far": 1.00, "coverage": 60, "height": "3 storeys / 11m", "height_numeric": 11.0},
        }
    },
    "Residential 4": {
        "display": "Residential 4 — Residential Buildings",
        "land_use": "Flats, residential buildings, boarding houses",
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "High-density residential zone for blocks of flats and residential buildings. Parking requirements apply per unit.",
        "height_zones": {
            "A": {"far": 1.00, "coverage": 50, "height": "4 storeys / 14m", "height_numeric": 14.0},
            "B": {"far": 1.50, "coverage": 55, "height": "6 storeys / 20m", "height_numeric": 20.0},
            "C": {"far": 2.50, "coverage": 60, "height": "No restriction (subject to SDP)", "height_numeric": 30.0},
        }
    },
    "Business 1": {
        "display": "Business 1 — General Business",
        "land_use": "Shops, offices, residential, mixed-use, entertainment",
        "setbacks": "Street: 0m | Side: 0m | Rear: 0m (or as per SDP)",
        "notes": "General business zone with widest range of permitted uses. Retail, office, residential, and mixed-use all permitted. No setbacks unless specified by SDP.",
        "height_zones": {
            "A": {"far": 1.50, "coverage": 80, "height": "No restriction", "height_numeric": 20.0},
            "B": {"far": 3.00, "coverage": 90, "height": "No restriction", "height_numeric": 30.0},
            "C": {"far": 5.00, "coverage": 100, "height": "No restriction", "height_numeric": 50.0},
        }
    },
    "Business 2": {
        "display": "Business 2 — Limited Business",
        "land_use": "Offices, limited retail, medical consulting rooms",
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "Limited business zone typically in residential transition areas. Retail limited in scale. Office and consulting rooms primary uses.",
        "height_zones": {
            "A": {"far": 0.60, "coverage": 50, "height": "2 storeys / 8.5m", "height_numeric": 8.5},
            "B": {"far": 1.00, "coverage": 60, "height": "3 storeys / 11m", "height_numeric": 11.0},
            "C": {"far": 1.50, "coverage": 70, "height": "4 storeys / 14m", "height_numeric": 14.0},
        }
    },
    "Business 3": {
        "display": "Business 3 — Corporate/Office",
        "land_use": "Offices, corporate headquarters, conference facilities",
        "setbacks": "Street: 5m | Side: 3m | Rear: 5m",
        "notes": "Corporate office zone. Primarily for office parks and corporate campuses. Limited retail for convenience only.",
        "height_zones": {
            "A": {"far": 0.80, "coverage": 50, "height": "3 storeys / 11m", "height_numeric": 11.0},
            "B": {"far": 1.50, "coverage": 60, "height": "5 storeys / 17m", "height_numeric": 17.0},
            "C": {"far": 2.50, "coverage": 70, "height": "No restriction", "height_numeric": 30.0},
        }
    },
    "Business 4": {
        "display": "Business 4 — Mixed Use",
        "land_use": "Mixed-use development — retail, office, residential combined",
        "setbacks": "Street: 0m | Side: 0m | Rear: 3m",
        "notes": "Mixed-use zone encouraging vertical integration of retail, office, and residential. Active street frontages encouraged.",
        "height_zones": {
            "A": {"far": 1.00, "coverage": 70, "height": "4 storeys / 14m", "height_numeric": 14.0},
            "B": {"far": 2.00, "coverage": 80, "height": "No restriction", "height_numeric": 25.0},
            "C": {"far": 4.00, "coverage": 100, "height": "No restriction", "height_numeric": 50.0},
        }
    },
    "Industrial 1": {
        "display": "Industrial 1 — Light Industrial",
        "land_use": "Light manufacturing, warehousing, distribution",
        "setbacks": "Street: 7.5m | Side: 0m (3m if adjacent to residential) | Rear: 3m",
        "notes": "Light industrial zone. Manufacturing and warehousing permitted. Must not cause nuisance to surrounding areas.",
        "height_zones": {
            "A": {"far": 0.60, "coverage": 60, "height": "No restriction", "height_numeric": 12.0},
            "B": {"far": 0.80, "coverage": 70, "height": "No restriction", "height_numeric": 15.0},
            "C": {"far": 1.00, "coverage": 80, "height": "No restriction", "height_numeric": 20.0},
        }
    },
    "Industrial 2": {
        "display": "Industrial 2 — Heavy Industrial",
        "land_use": "Heavy manufacturing, processing, noxious trades",
        "setbacks": "Street: 10m | Side: 5m | Rear: 5m",
        "notes": "Heavy industrial zone for large-scale manufacturing. Environmental authorisation typically required. Buffer zones apply.",
        "height_zones": {
            "A": {"far": 0.50, "coverage": 50, "height": "No restriction", "height_numeric": 15.0},
            "B": {"far": 0.70, "coverage": 60, "height": "No restriction", "height_numeric": 20.0},
            "C": {"far": 0.80, "coverage": 70, "height": "No restriction", "height_numeric": 25.0},
        }
    },
    "Industrial 3": {
        "display": "Industrial 3 — Service Industrial",
        "land_use": "Service industry, showrooms, motor trade",
        "setbacks": "Street: 5m | Side: 0m | Rear: 3m",
        "notes": "Service industrial zone suitable for motor trade, showrooms, and service-oriented businesses with industrial character.",
        "height_zones": {
            "A": {"far": 0.60, "coverage": 60, "height": "2 storeys / 10m", "height_numeric": 10.0},
            "B": {"far": 0.80, "coverage": 65, "height": "3 storeys / 12m", "height_numeric": 12.0},
            "C": {"far": 1.00, "coverage": 75, "height": "No restriction", "height_numeric": 15.0},
        }
    },
    "Commercial": {
        "display": "Commercial",
        "land_use": "Wholesale, retail warehousing, commercial services",
        "setbacks": "Street: 5m | Side: 0m | Rear: 3m",
        "notes": "Commercial zone for wholesale trade, bulk retail, and large-format commercial operations.",
        "height_zones": {
            "A": {"far": 0.80, "coverage": 60, "height": "No restriction", "height_numeric": 12.0},
            "B": {"far": 1.00, "coverage": 70, "height": "No restriction", "height_numeric": 15.0},
            "C": {"far": 1.50, "coverage": 80, "height": "No restriction", "height_numeric": 20.0},
        }
    },
    "Municipal": {
        "display": "Municipal",
        "land_use": "Municipal services, civic buildings, public facilities",
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "Reserved for municipal facilities and civic infrastructure. Development subject to municipal approval.",
        "height_zones": {
            "A": {"far": 0.50, "coverage": 40, "height": "As per approval", "height_numeric": 12.0},
            "B": {"far": 0.80, "coverage": 50, "height": "As per approval", "height_numeric": 15.0},
            "C": {"far": 1.00, "coverage": 60, "height": "As per approval", "height_numeric": 20.0},
        }
    },
    "Educational": {
        "display": "Educational",
        "land_use": "Schools, universities, training facilities, crèches",
        "setbacks": "Street: 5m | Side: 3m | Rear: 5m",
        "notes": "Educational zone for schools and training institutions. Traffic and parking impacts must be addressed.",
        "height_zones": {
            "A": {"far": 0.50, "coverage": 40, "height": "3 storeys / 11m", "height_numeric": 11.0},
            "B": {"far": 0.80, "coverage": 50, "height": "4 storeys / 14m", "height_numeric": 14.0},
            "C": {"far": 1.00, "coverage": 60, "height": "No restriction", "height_numeric": 20.0},
        }
    },
    "Institutional": {
        "display": "Institutional",
        "land_use": "Hospitals, places of worship, welfare institutions",
        "setbacks": "Street: 5m | Side: 3m | Rear: 5m",
        "notes": "Institutional zone for hospitals, religious facilities, and welfare organisations. Parking and traffic management required.",
        "height_zones": {
            "A": {"far": 0.60, "coverage": 40, "height": "3 storeys / 11m", "height_numeric": 11.0},
            "B": {"far": 1.00, "coverage": 50, "height": "5 storeys / 17m", "height_numeric": 17.0},
            "C": {"far": 1.50, "coverage": 60, "height": "No restriction", "height_numeric": 25.0},
        }
    },
    "Government": {
        "display": "Government",
        "land_use": "National and provincial government facilities",
        "setbacks": "Street: 5m | Side: 3m | Rear: 5m",
        "notes": "Reserved for government facilities. Development parameters subject to specific approval conditions.",
        "height_zones": {
            "A": {"far": 0.60, "coverage": 50, "height": "As per approval", "height_numeric": 12.0},
            "B": {"far": 1.00, "coverage": 60, "height": "As per approval", "height_numeric": 20.0},
            "C": {"far": 1.50, "coverage": 70, "height": "As per approval", "height_numeric": 30.0},
        }
    },
    "Public Open Space": {
        "display": "Public Open Space",
        "land_use": "Parks, playgrounds, public recreation",
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "Public open space. Development severely restricted. Only minor ancillary structures permitted (ablutions, park furniture).",
        "height_zones": {
            "A": {"far": 0.05, "coverage": 5, "height": "5m", "height_numeric": 5.0},
            "B": {"far": 0.05, "coverage": 5, "height": "5m", "height_numeric": 5.0},
            "C": {"far": 0.10, "coverage": 10, "height": "5m", "height_numeric": 5.0},
        }
    },
    "Private Open Space": {
        "display": "Private Open Space",
        "land_use": "Private recreation, sport clubs, golf courses",
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "Private open space for recreational use. Clubhouses and ancillary facilities permitted. Rezoning required for significant development.",
        "height_zones": {
            "A": {"far": 0.10, "coverage": 10, "height": "8.5m", "height_numeric": 8.5},
            "B": {"far": 0.15, "coverage": 15, "height": "8.5m", "height_numeric": 8.5},
            "C": {"far": 0.20, "coverage": 20, "height": "8.5m", "height_numeric": 8.5},
        }
    },
    "Agricultural": {
        "display": "Agricultural",
        "land_use": "Farming, smallholdings, agricultural holdings",
        "setbacks": "Street: 15m | Side: 5m | Rear: 10m",
        "notes": "Agricultural zone. Subdivision and non-agricultural development strictly controlled. Rezoning required for any change of use.",
        "height_zones": {
            "A": {"far": 0.05, "coverage": 5, "height": "8.5m", "height_numeric": 8.5},
            "B": {"far": 0.10, "coverage": 10, "height": "8.5m", "height_numeric": 8.5},
            "C": {"far": 0.15, "coverage": 15, "height": "8.5m", "height_numeric": 8.5},
        }
    },
    "Cemetery": {
        "display": "Cemetery",
        "land_use": "Cemeteries, crematoria, memorial parks",
        "setbacks": "Street: 10m | Side: 5m | Rear: 5m",
        "notes": "Reserved for burial and memorial purposes. Limited ancillary structures only.",
        "height_zones": {
            "A": {"far": 0.05, "coverage": 5, "height": "5m", "height_numeric": 5.0},
            "B": {"far": 0.05, "coverage": 5, "height": "5m", "height_numeric": 5.0},
            "C": {"far": 0.05, "coverage": 5, "height": "5m", "height_numeric": 5.0},
        }
    },
    "Special": {
        "display": "Special",
        "land_use": "As per specific conditions of approval",
        "setbacks": "As per conditions of approval",
        "notes": "Special zone with site-specific development conditions. All parameters subject to the approved conditions. Consult CoJ for full details.",
        "height_zones": {
            "A": {"far": 0.50, "coverage": 40, "height": "As per conditions", "height_numeric": 10.0},
            "B": {"far": 1.00, "coverage": 60, "height": "As per conditions", "height_numeric": 15.0},
            "C": {"far": 2.00, "coverage": 80, "height": "As per conditions", "height_numeric": 25.0},
        }
    },
    "Transport": {
        "display": "Transport",
        "land_use": "Roads, rail reserves, transit facilities, BRT stations",
        "setbacks": "As per transport authority requirements",
        "notes": "Transport zone for infrastructure and transit facilities. Development requires transport authority approval.",
        "height_zones": {
            "A": {"far": 0.30, "coverage": 40, "height": "As per approval", "height_numeric": 10.0},
            "B": {"far": 0.50, "coverage": 50, "height": "As per approval", "height_numeric": 12.0},
            "C": {"far": 0.80, "coverage": 60, "height": "As per approval", "height_numeric": 15.0},
        }
    },
}


def calculate_joburg_floor_space(zone_name, height_zone, erf_size_m2):
    """
    Calculate maximum floor space for a Johannesburg property.

    Args:
        zone_name (str):    Key from JOBURG_ZONES (e.g. "Residential 1")
        height_zone (str):  "A", "B", or "C"
        erf_size_m2 (float): Erf size in square metres

    Returns:
        (max_floor_space, coverage, formula) tuple:
            max_floor_space (float): Maximum gross floor area in m²
            coverage (float):        Maximum coverage percentage
            formula (str):           Human-readable calculation string
    """
    zone = JOBURG_ZONES.get(zone_name)
    if not zone:
        return 0, 0, "Zone not found"

    hz = zone["height_zones"].get(height_zone.upper())
    if not hz:
        return 0, 0, "Height zone not found"

    far = hz["far"]
    coverage = hz["coverage"]
    max_floor_space = erf_size_m2 * far

    formula = f"{erf_size_m2:,.0f} m² × {far} FAR (Height Zone {height_zone.upper()}) = {max_floor_space:,.0f} m²"

    return max_floor_space, coverage, formula


def get_joburg_zone_params(zone_name, height_zone):
    """
    Get full zone parameters for a given zone and height zone.

    Args:
        zone_name (str):   Key from JOBURG_ZONES
        height_zone (str): "A", "B", or "C"

    Returns:
        dict with all parameters, or None if not found
    """
    zone = JOBURG_ZONES.get(zone_name)
    if not zone:
        return None

    hz = zone["height_zones"].get(height_zone.upper())
    if not hz:
        return None

    return {
        "zone_display": zone["display"],
        "land_use": zone["land_use"],
        "setbacks": zone["setbacks"],
        "notes": zone["notes"],
        "far": hz["far"],
        "coverage": hz["coverage"],
        "height": hz["height"],
        "height_numeric": hz["height_numeric"],
        "height_zone": height_zone.upper(),
        "height_zone_desc": HEIGHT_ZONES.get(height_zone.upper(), ""),
    }
