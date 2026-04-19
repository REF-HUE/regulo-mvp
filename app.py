from flask import Flask, render_template, request, send_file, redirect, url_for, session
import sqlite3
import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from feasibility import calculate_feasibility
from johannesburg_zones import (
    JOBURG_ZONES, HEIGHT_ZONES, JOBURG_DATA_SOURCE,
    calculate_joburg_floor_space, get_joburg_zone_params
)
from capetown_zones import (
    CAPETOWN_ZONES, CAPETOWN_DATA_SOURCE,
    get_capetown_zone_params, calculate_capetown_floor_space
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'regulo-systems-2025')

# Use /tmp on Render (writable), local path in development
if os.environ.get('RENDER'):
    DATABASE = '/tmp/zoning.db'
else:
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zoning.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NMBM ZONE DATA
# Source: NMBM Land Use Scheme V6, 19 January 2023
# FAR is estimated — NMBM uses coverage % + height, not FAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ZONE_DATA = {
    "Single Residential Zone 1": {
        "display": "Single Residential Zone 1 (SR1)",
        "land_use": "Single Residential A — dwelling house, second dwelling",
        "coverage": "60%",
        "coverage_numeric": 60.0,
        "floor_area_ratio": 0.6,
        "height": "8.5m",
        "height_numeric": 8.5,
        "setbacks": "Street: 3m | Side: 1.5m | Rear: 1.5m",
        "notes": "Primary single residential zone for erven larger than 600m². A second dwelling or outbuilding is permitted subject to conditions. Coverage may increase to 70% for erven ≤ 600m².",
    },
    "Single Residential Zone 2": {
        "display": "Single Residential Zone 2 (SR2)",
        "land_use": "Single Residential B — dwelling house, shelter",
        "coverage": "80%",
        "coverage_numeric": 80.0,
        "floor_area_ratio": 0.8,
        "height": "8.5m",
        "height_numeric": 8.5,
        "setbacks": "Street: 1m (if required) | Side: 1m (if required) | Rear: 1m (if required)",
        "notes": "Higher-coverage single residential zone typically applied to smaller erven and denser residential areas. Suitable for dwelling houses and informal structures.",
    },
    "General Residential Zone 1": {
        "display": "General Residential Zone 1 (GR1)",
        "land_use": "Low Density Residential — dwelling units, group housing",
        "coverage": "60%",
        "coverage_numeric": 60.0,
        "floor_area_ratio": 1.0,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 15.0,
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "Low-density general residential zone suitable for group housing, cluster developments, and low-rise residential buildings.",
    },
    "General Residential Zone 2": {
        "display": "General Residential Zone 2 (GR2)",
        "land_use": "Residential Buildings — flats, boarding houses, retirement village",
        "coverage": "75%",
        "coverage_numeric": 75.0,
        "floor_area_ratio": 1.5,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 20.0,
        "setbacks": "Street: 5m | Side: 3m or half height (max 10m) | Rear: 3m or half height (max 10m)",
        "notes": "Medium to high-density residential zone. Suitable for blocks of flats, townhouses, student accommodation and retirement villages. Outdoor living area of at least 10% of erf area required.",
    },
    "General Residential Zone 3": {
        "display": "General Residential Zone 3 (GR3)",
        "land_use": "High Density Residential — residential buildings, flats",
        "coverage": "75%",
        "coverage_numeric": 75.0,
        "floor_area_ratio": 2.0,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 25.0,
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "High-density residential zone for multi-storey residential buildings. Subject to Spatial Development Framework height guidelines.",
    },
    "Business Zone 1": {
        "display": "Business Zone 1 (BZ1) — General Business",
        "land_use": "General Business — retail, office, mixed-use, residential",
        "coverage": "100%",
        "coverage_numeric": 100.0,
        "floor_area_ratio": 3.0,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 30.0,
        "setbacks": "Street: 0m | Side: 0m | Rear: 0m",
        "notes": "General Business zone permits the widest range of uses including retail, office, residential buildings, and mixed-use development. No height restriction unless specified by the Spatial Development Framework.",
    },
    "Business Zone 2": {
        "display": "Business Zone 2 (BZ2) — Limited Business",
        "land_use": "Limited Business — retail, trade, neighbourhood commercial",
        "coverage": "70%",
        "coverage_numeric": 70.0,
        "floor_area_ratio": 1.5,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 15.0,
        "setbacks": "Street: 5m | Side: 5m or half height (max 10m) | Rear: 5m or half height (max 10m)",
        "notes": "Limited Business zone for low-intensity neighbourhood commercial development. Scale must be compatible with adjacent residential areas.",
    },
    "Business Zone 3": {
        "display": "Business Zone 3 (BZ3) — Local Business",
        "land_use": "Local Business — corner shops, small offices, service businesses",
        "coverage": "60%",
        "coverage_numeric": 60.0,
        "floor_area_ratio": 1.2,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 10.0,
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "Local Business zone for small-scale commercial uses serving immediate neighbourhood needs. Typically applied to corner sites within residential areas.",
    },
    "Industrial Zone 1": {
        "display": "Industrial Zone 1 (IZ1) — General Industrial",
        "land_use": "General Industrial — manufacturing, warehousing, logistics",
        "coverage": "70%",
        "coverage_numeric": 70.0,
        "floor_area_ratio": 1.0,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 15.0,
        "setbacks": "Street: 6m | Side: 3m | Rear: 3m",
        "notes": "General Industrial zone for manufacturing, warehousing and logistics operations. Environmental impact assessment may be required for certain uses.",
    },
    "Industrial Zone 2": {
        "display": "Industrial Zone 2 (IZ2) — Limited Industrial",
        "land_use": "Limited Industrial — light industry, service industries",
        "coverage": "50%",
        "coverage_numeric": 50.0,
        "floor_area_ratio": 0.8,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 12.0,
        "setbacks": "Street: 6m | Side: 3m | Rear: 3m",
        "notes": "Limited Industrial zone for light industrial and service industry uses. Must be compatible with surrounding land uses and minimise nuisance impacts.",
    },
    "Mixed Use Zone": {
        "display": "Mixed Use Zone (MU)",
        "land_use": "Mixed Use — residential and commercial combination",
        "coverage": "80%",
        "coverage_numeric": 80.0,
        "floor_area_ratio": 2.0,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 20.0,
        "setbacks": "Street: 2m | Side: 2m | Rear: 3m",
        "notes": "Mixed Use zone allowing a combination of residential and commercial development. Encourages active street frontages and pedestrian-friendly environments.",
    },
    "Community Facilities Zone": {
        "display": "Community Facilities Zone (CF)",
        "land_use": "Community Facilities — schools, clinics, places of worship, civic uses",
        "coverage": "60%",
        "coverage_numeric": 60.0,
        "floor_area_ratio": 0.8,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 12.0,
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "Community Facilities zone for public and community-serving uses. Development requires municipal approval and must be compatible with surrounding land uses.",
    },
    "Government Zone": {
        "display": "Government Zone (GOV)",
        "land_use": "Government — municipal, provincial and national government uses",
        "coverage": "60%",
        "coverage_numeric": 60.0,
        "floor_area_ratio": 1.0,
        "height": "No restriction (subject to SDF)",
        "height_numeric": 15.0,
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "Government Zone reserved for public sector facilities and administration buildings.",
    },
    "Open Space Zone 1": {
        "display": "Open Space Zone 1 (OS1) — Public Open Space",
        "land_use": "Public Open Space — parks, recreation, public amenity",
        "coverage": "5%",
        "coverage_numeric": 5.0,
        "floor_area_ratio": 0.05,
        "height": "5m",
        "height_numeric": 5.0,
        "setbacks": "Street: 5m | Side: 3m | Rear: 3m",
        "notes": "Public Open Space zone. Development is severely restricted. Only minor ancillary structures such as ablution facilities or park furniture are permitted.",
    },
    "Open Space Zone 2": {
        "display": "Open Space Zone 2 (OS2) — Private Open Space",
        "land_use": "Private Open Space — private recreation, sport, amenity",
        "coverage": "20%",
        "coverage_numeric": 20.0,
        "floor_area_ratio": 0.2,
        "height": "5m",
        "height_numeric": 5.0,
        "setbacks": "Street: 3m | Side: 2m | Rear: 2m",
        "notes": "Private Open Space zone for private recreational facilities. Limited built structures permitted. Rezoning required for any significant development.",
    },
    "Agricultural Zone": {
        "display": "Agricultural Zone (AG)",
        "land_use": "Agricultural — farming, smallholdings, agricultural industry",
        "coverage": "5%",
        "coverage_numeric": 5.0,
        "floor_area_ratio": 0.1,
        "height": "10m",
        "height_numeric": 10.0,
        "setbacks": "Street: 10m | Side: 5m | Rear: 5m",
        "notes": "Agricultural Zone for farming and related uses. Subdivision and development are strictly controlled. Rezoning is required for any non-agricultural use.",
    },
    "Special Zone": {
        "display": "Special Zone (SP)",
        "land_use": "Special — as defined by specific conditions of approval",
        "coverage": "As per conditions",
        "coverage_numeric": 50.0,
        "floor_area_ratio": 1.0,
        "height": "As per conditions",
        "height_numeric": 10.0,
        "setbacks": "As per conditions of approval",
        "notes": "Special Zone with site-specific development conditions. All parameters are subject to the specific conditions attached to this zone. Consult NMBM for full conditions.",
    },
    "Transport Zone": {
        "display": "Transport Zone (TR)",
        "land_use": "Transport — roads, rail, airports, transport infrastructure",
        "coverage": "50%",
        "coverage_numeric": 50.0,
        "floor_area_ratio": 0.5,
        "height": "No restriction",
        "height_numeric": 10.0,
        "setbacks": "As determined by transport authority",
        "notes": "Transport Zone reserved for transport infrastructure and ancillary uses. Development requires approval from the relevant transport authority.",
    },
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AUTO-SEED ON STARTUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def auto_seed():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id                        INTEGER PRIMARY KEY AUTOINCREMENT,
        erf_number                TEXT,
        suburb                    TEXT,
        city                      TEXT,
        zone                      TEXT,
        land_use                  TEXT,
        coverage                  TEXT,
        floor_area_ratio          REAL,
        height                    TEXT,
        setbacks                  TEXT,
        erf_size                  INTEGER,
        coverage_numeric          REAL,
        height_numeric            REAL,
        heritage_overlay          INTEGER DEFAULT 0,
        environmental_restriction INTEGER DEFAULT 0,
        notes                     TEXT,
        data_source               TEXT
    )
    """)

    cursor.execute("DELETE FROM properties")

    source = "NMBM Land Use Scheme V6 (January 2023)"

    properties = [
        (
            "3864", "Central", "Gqeberha",
            "Business Zone 1 (BZ1) — General Business",
            "General Business — retail, office, mixed-use",
            "100%", 3.0, "No restriction (subject to SDF)",
            "Street: 0m | Side: 0m | Rear: 0m",
            1200, 100.0, 30, 0, 0,
            "General Business zone permits the widest range of uses including retail, office, residential buildings, and mixed-use development.",
            source
        ),
        (
            "1021", "Summerstrand", "Gqeberha",
            "General Residential Zone 2 (GR2)",
            "Residential Buildings — flats, boarding houses, retirement village",
            "75%", 1.5, "No restriction (subject to SDF)",
            "Street: 5m | Side: 3m or half height (max 10m) | Rear: 3m or half height (max 10m)",
            900, 75.0, 20, 0, 0,
            "High-density residential zone. Suitable for blocks of flats, townhouses, student accommodation and retirement villages.",
            source
        ),
        (
            "447", "Walmer", "Gqeberha",
            "Single Residential Zone 1 (SR1)",
            "Single Residential A — dwelling house",
            "60%", 0.6, "8.5m",
            "Street: 3m | Side: 1.5m | Rear: 1.5m",
            750, 60.0, 8.5, 1, 0,
            "Single residential zone for erven larger than 600m². Property falls within a Heritage Overlay.",
            source
        ),
        (
            "2230", "Newton Park", "Gqeberha",
            "Business Zone 2 (BZ2) — Limited Business",
            "Limited Business — retail, trade, neighbourhood commercial",
            "70%", 1.5, "No restriction (subject to SDF)",
            "Street: 5m | Side: 5m or half height (max 10m) | Rear: 5m or half height (max 10m)",
            1500, 70.0, 15, 0, 0,
            "Limited Business zone for low-intensity neighbourhood commercial development.",
            source
        ),
        (
            "781", "Humewood", "Gqeberha",
            "Single Residential Zone 2 (SR2)",
            "Single Residential B — dwelling house, shelter",
            "80%", 0.8, "8.5m",
            "Street: 1m (if required) | Side: 1m (if required) | Rear: 1m (if required)",
            680, 80.0, 8.5, 0, 1,
            "Single Residential B zone with environmental restriction — proximity to coastal system.",
            source
        ),
        (
            "912", "Richmond Hill", "Gqeberha",
            "Business Zone 1 (BZ1) — General Business",
            "General Business — mixed-use residential and commercial",
            "100%", 2.0, "No restriction (subject to SDF)",
            "Street: 0m | Side: 0m | Rear: 0m",
            1100, 100.0, 20, 1, 0,
            "General Business zone in a mixed-use precinct. Heritage overlay applies — Richmond Hill is a heritage-sensitive area.",
            source
        ),
    ]

    cursor.executemany("""
    INSERT INTO properties (
        erf_number, suburb, city, zone, land_use, coverage,
        floor_area_ratio, height, setbacks, erf_size,
        coverage_numeric, height_numeric,
        heritage_overlay, environmental_restriction, notes, data_source
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, properties)

    conn.commit()
    print(f"✅ Database seeded — {len(properties)} properties at {DATABASE}")
    conn.close()

auto_seed()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ANALYTICS — visit tracking
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def init_analytics():
    """Create visits table if it doesn't exist. Never deletes visit data."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visits (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        page       TEXT,
        ip         TEXT,
        referrer   TEXT,
        user_agent TEXT,
        timestamp  TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("✅ Analytics table ready")

init_analytics()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BOT FILTER — exclude crawlers and link-preview bots
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BOT_SIGNATURES = [
    'bot', 'crawler', 'spider', 'httpclient', 'slurp', 'mediapartners',
    'facebookexternalhit', 'twitterbot', 'linkedinbot', 'whatsapp',
    'telegrambot', 'discordbot', 'bingpreview', 'googlebot',
    'yandexbot', 'baiduspider', 'duckduckbot', 'semrushbot',
    'ahrefsbot', 'mj12bot', 'dotbot', 'petalbot',
]


def is_bot(user_agent_string):
    """Return True if the user-agent looks like a bot or crawler."""
    ua_lower = user_agent_string.lower()
    return any(sig in ua_lower for sig in BOT_SIGNATURES)


@app.before_request
def log_visit():
    """Log every page visit to the database — bots are excluded."""
    if request.path.startswith('/static') or request.path == '/favicon.ico':
        return

    ua = str(request.user_agent)
    if is_bot(ua):
        return

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO visits (page, ip, referrer, user_agent, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """, (
            request.path,
            request.headers.get('X-Forwarded-For', request.remote_addr),
            request.referrer or '',
            ua,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        conn.close()
    except Exception:
        pass


@app.route('/admin/analytics')
def analytics():
    """Simple analytics dashboard — password protected via query param."""
    key = request.args.get('key', '')
    if key != os.environ.get('ANALYTICS_KEY', 'regulo2026'):
        return "Unauthorized", 401

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    total = cursor.execute("SELECT COUNT(*) as count FROM visits").fetchone()['count']
    unique = cursor.execute("SELECT COUNT(DISTINCT ip) as count FROM visits").fetchone()['count']

    today = datetime.now().strftime('%Y-%m-%d')
    today_count = cursor.execute(
        "SELECT COUNT(*) as count FROM visits WHERE timestamp LIKE ?", (f"{today}%",)
    ).fetchone()['count']

    pages = cursor.execute("""
        SELECT page, COUNT(*) as count FROM visits
        GROUP BY page ORDER BY count DESC LIMIT 20
    """).fetchall()

    daily = cursor.execute("""
        SELECT DATE(timestamp) as day, COUNT(*) as count FROM visits
        GROUP BY DATE(timestamp) ORDER BY day DESC LIMIT 14
    """).fetchall()

    recent = cursor.execute("""
        SELECT page, ip, referrer, user_agent, timestamp FROM visits
        ORDER BY id DESC LIMIT 20
    """).fetchall()

    conn.close()

    return render_template('analytics.html',
                           total=total, unique=unique, today_count=today_count,
                           pages=pages, daily=daily, recent=recent)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HOME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/')
def index():
    return render_template('index.html')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NMBM SEARCH / RESULTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        erf_number = request.form.get('erf_number', '').strip()
        suburb     = request.form.get('suburb', '').strip()

        if not erf_number:
            return render_template('index.html', error="Please enter an ERF number.")

        db = get_db()

        if suburb:
            prop = db.execute(
                "SELECT * FROM properties WHERE erf_number = ? AND LOWER(suburb) = LOWER(?)",
                (erf_number, suburb)
            ).fetchone()

            if not prop:
                erf_exists = db.execute(
                    "SELECT suburb FROM properties WHERE erf_number = ?",
                    (erf_number,)
                ).fetchone()
                db.close()

                if erf_exists:
                    actual_suburb = erf_exists['suburb']
                    return render_template('index.html',
                                           error=f"ERF {erf_number} was not found in {suburb}. "
                                                 f"It is registered in {actual_suburb}. "
                                                 f"Try leaving the suburb blank, or enter \"{actual_suburb}\".")
                else:
                    return redirect(url_for('zone_lookup', erf_number=erf_number, suburb=suburb))
        else:
            prop = db.execute(
                "SELECT * FROM properties WHERE erf_number = ?",
                (erf_number,)
            ).fetchone()
            db.close()

            if not prop:
                return redirect(url_for('zone_lookup', erf_number=erf_number))

        property_data = dict(prop)
        property_data['is_dynamic'] = False
        property_data['municipality'] = 'nmbm'

        score, notes, grade, grade_text, buildable_area = calculate_feasibility(property_data)
        property_data['feasibility_score']      = score
        property_data['feasibility_notes']      = notes
        property_data['feasibility_grade']      = grade
        property_data['feasibility_grade_text'] = grade_text
        property_data['buildable_area']         = buildable_area

        return render_template('result.html', property=property_data)

    return redirect(url_for('index'))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NMBM ZONE LOOKUP — for ERFs not in database
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/zone-lookup', methods=['GET', 'POST'])
def zone_lookup():
    zones = sorted(ZONE_DATA.keys())

    if request.method == 'GET':
        erf_number = request.args.get('erf_number', '')
        suburb     = request.args.get('suburb', '')
        return render_template('zone_lookup.html',
                               erf_number=erf_number,
                               suburb=suburb,
                               zones=zones)

    erf_number  = request.form.get('erf_number', '').strip() or 'Unknown'
    suburb      = request.form.get('suburb', 'Gqeberha').strip()
    zone_key    = request.form.get('zone', '').strip()
    erf_size_raw = request.form.get('erf_size', '').strip()
    heritage    = 1 if request.form.get('heritage_overlay') else 0
    enviro      = 1 if request.form.get('environmental_restriction') else 0

    if not zone_key or not erf_size_raw:
        return render_template('zone_lookup.html',
                               erf_number=erf_number, suburb=suburb, zones=zones,
                               error="Please select a zone and enter the ERF size.")

    try:
        erf_size = int(erf_size_raw)
        if erf_size <= 0:
            raise ValueError
    except ValueError:
        return render_template('zone_lookup.html',
                               erf_number=erf_number, suburb=suburb, zones=zones,
                               error="ERF size must be a positive number in m².")

    zone = ZONE_DATA.get(zone_key)
    if not zone:
        return render_template('zone_lookup.html',
                               erf_number=erf_number, suburb=suburb, zones=zones,
                               error="Invalid zone selected.")

    property_data = {
        'erf_number':               erf_number,
        'suburb':                   suburb,
        'city':                     'Gqeberha',
        'zone':                     zone['display'],
        'land_use':                 zone['land_use'],
        'coverage':                 zone['coverage'],
        'coverage_numeric':         zone['coverage_numeric'],
        'floor_area_ratio':         zone['floor_area_ratio'],
        'height':                   zone['height'],
        'height_numeric':           zone['height_numeric'],
        'setbacks':                 zone['setbacks'],
        'erf_size':                 erf_size,
        'heritage_overlay':         heritage,
        'environmental_restriction': enviro,
        'notes':                    zone['notes'],
        'data_source':              'NMBM Land Use Scheme V6 (January 2023)',
        'is_dynamic':               True,
        'municipality':             'nmbm',
    }

    score, notes, grade, grade_text, buildable_area = calculate_feasibility(property_data)
    property_data['feasibility_score']      = score
    property_data['feasibility_notes']      = notes
    property_data['feasibility_grade']      = grade
    property_data['feasibility_grade_text'] = grade_text
    property_data['buildable_area']         = buildable_area

    session['dynamic_property'] = property_data
    return render_template('result.html', property=property_data)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# JOHANNESBURG SEARCH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/joburg', methods=['GET'])
def joburg_index():
    """Redirect to Joburg zone lookup form."""
    return redirect(url_for('joburg_lookup'))


@app.route('/joburg-lookup', methods=['GET', 'POST'])
def joburg_lookup():
    zones = sorted(JOBURG_ZONES.keys())
    height_zones = HEIGHT_ZONES

    if request.method == 'GET':
        erf_number = request.args.get('erf_number', '')
        suburb     = request.args.get('suburb', '')
        return render_template('joburg_lookup.html',
                               erf_number=erf_number,
                               suburb=suburb,
                               zones=zones,
                               height_zones=height_zones)

    # POST — generate Johannesburg result
    erf_number   = request.form.get('erf_number', '').strip() or 'Unknown'
    suburb       = request.form.get('suburb', '').strip() or 'Johannesburg'
    zone_key     = request.form.get('zone', '').strip()
    height_zone  = request.form.get('height_zone', '').strip().upper()
    erf_size_raw = request.form.get('erf_size', '').strip()
    heritage     = 1 if request.form.get('heritage_overlay') else 0
    enviro       = 1 if request.form.get('environmental_restriction') else 0

    if not zone_key or not height_zone or not erf_size_raw:
        return render_template('joburg_lookup.html',
                               erf_number=erf_number, suburb=suburb,
                               zones=zones, height_zones=height_zones,
                               error="Please select a zone, height zone, and enter the ERF size.")

    if height_zone not in ('A', 'B', 'C'):
        return render_template('joburg_lookup.html',
                               erf_number=erf_number, suburb=suburb,
                               zones=zones, height_zones=height_zones,
                               error="Please select a valid Height Zone (A, B, or C).")

    try:
        erf_size = int(erf_size_raw)
        if erf_size <= 0:
            raise ValueError
    except ValueError:
        return render_template('joburg_lookup.html',
                               erf_number=erf_number, suburb=suburb,
                               zones=zones, height_zones=height_zones,
                               error="ERF size must be a positive number in m².")

    params = get_joburg_zone_params(zone_key, height_zone)
    if not params:
        return render_template('joburg_lookup.html',
                               erf_number=erf_number, suburb=suburb,
                               zones=zones, height_zones=height_zones,
                               error="Invalid zone or height zone selected.")

    max_floor_space, coverage_pct, formula = calculate_joburg_floor_space(zone_key, height_zone, erf_size)

    property_data = {
        'erf_number':               erf_number,
        'suburb':                   suburb,
        'city':                     'Johannesburg',
        'zone':                     params['zone_display'],
        'land_use':                 params['land_use'],
        'coverage':                 f"{params['coverage']}%",
        'coverage_numeric':         float(params['coverage']),
        'floor_area_ratio':         params['far'],
        'height':                   params['height'],
        'height_numeric':           params['height_numeric'],
        'setbacks':                 params['setbacks'],
        'erf_size':                 erf_size,
        'heritage_overlay':         heritage,
        'environmental_restriction': enviro,
        'notes':                    params['notes'],
        'data_source':              JOBURG_DATA_SOURCE,
        'is_dynamic':               True,
        'municipality':             'johannesburg',
        'height_zone':              height_zone,
        'height_zone_desc':         params['height_zone_desc'],
        'joburg_formula':           formula,
    }

    score, notes, grade, grade_text, buildable_area = calculate_feasibility(property_data)
    property_data['feasibility_score']      = score
    property_data['feasibility_notes']      = notes
    property_data['feasibility_grade']      = grade
    property_data['feasibility_grade_text'] = grade_text
    property_data['buildable_area']         = buildable_area

    session['dynamic_property'] = property_data
    return render_template('result.html', property=property_data)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CAPE TOWN SEARCH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/capetown', methods=['GET'])
def capetown_index():
    """Redirect to Cape Town zone lookup form."""
    return redirect(url_for('capetown_lookup'))


@app.route('/capetown-lookup', methods=['GET', 'POST'])
def capetown_lookup():
    zones = sorted(CAPETOWN_ZONES.keys())

    if request.method == 'GET':
        erf_number = request.args.get('erf_number', '')
        suburb     = request.args.get('suburb', '')
        return render_template('capetown_lookup.html',
                               erf_number=erf_number,
                               suburb=suburb,
                               zones=zones)

    # POST — generate Cape Town result
    erf_number   = request.form.get('erf_number', '').strip() or 'Unknown'
    suburb       = request.form.get('suburb', '').strip() or 'Cape Town'
    zone_key     = request.form.get('zone', '').strip()
    erf_size_raw = request.form.get('erf_size', '').strip()
    heritage     = 1 if request.form.get('heritage_overlay') else 0
    enviro       = 1 if request.form.get('environmental_restriction') else 0

    if not zone_key or not erf_size_raw:
        return render_template('capetown_lookup.html',
                               erf_number=erf_number, suburb=suburb,
                               zones=zones,
                               error="Please select a zone and enter the ERF size.")

    try:
        erf_size = int(erf_size_raw)
        if erf_size <= 0:
            raise ValueError
    except ValueError:
        return render_template('capetown_lookup.html',
                               erf_number=erf_number, suburb=suburb,
                               zones=zones,
                               error="ERF size must be a positive number in m².")

    params = get_capetown_zone_params(zone_key, erf_size)
    if not params:
        return render_template('capetown_lookup.html',
                               erf_number=erf_number, suburb=suburb,
                               zones=zones,
                               error="Invalid zone selected.")

    max_floor_space, coverage_pct, formula = calculate_capetown_floor_space(zone_key, erf_size)

    # Determine coverage and floor factor for the property data
    floor_factor = params.get('floor_factor') or 0
    coverage = params.get('coverage')

    property_data = {
        'erf_number':               erf_number,
        'suburb':                   suburb,
        'city':                     'Cape Town',
        'zone':                     params['zone_display'],
        'land_use':                 params['land_use'],
        'coverage':                 f"{coverage}%" if coverage else "N/a (floor factor controls)",
        'coverage_numeric':         float(coverage) if coverage else 60.0,
        'floor_area_ratio':         floor_factor,
        'height':                   params['height'],
        'height_numeric':           params['height_numeric'],
        'setbacks':                 params['setbacks'],
        'erf_size':                 erf_size,
        'heritage_overlay':         heritage,
        'environmental_restriction': enviro,
        'notes':                    params['notes'],
        'data_source':              CAPETOWN_DATA_SOURCE,
        'is_dynamic':               True,
        'municipality':             'capetown',
        'capetown_formula':         formula,
    }

    score, notes, grade, grade_text, buildable_area = calculate_feasibility(property_data)
    property_data['feasibility_score']      = score
    property_data['feasibility_notes']      = notes
    property_data['feasibility_grade']      = grade
    property_data['feasibility_grade_text'] = grade_text
    property_data['buildable_area']         = buildable_area

    session['dynamic_property'] = property_data
    return render_template('result.html', property=property_data)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PDF REPORT — known NMBM ERF
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/generate_pdf/<erf_number>')
def generate_pdf(erf_number):
    db = get_db()
    prop = db.execute(
        "SELECT * FROM properties WHERE erf_number = ?", (erf_number,)
    ).fetchone()
    db.close()

    if not prop:
        return "Property not found", 404

    property_data = dict(prop)
    property_data['municipality'] = 'nmbm'

    score, notes, grade, grade_text, buildable_area = calculate_feasibility(property_data)
    property_data['feasibility_score']      = score
    property_data['feasibility_notes']      = notes
    property_data['feasibility_grade']      = grade
    property_data['feasibility_grade_text'] = grade_text
    property_data['buildable_area']         = buildable_area

    pdf_buffer = build_pdf(property_data)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Regulo_Zoning_Report_ERF{erf_number}.pdf",
        mimetype='application/pdf'
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PDF REPORT — dynamic (NMBM zone lookup + Johannesburg)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/generate_pdf_dynamic')
def generate_pdf_dynamic():
    property_data = session.get('dynamic_property')

    if not property_data:
        return redirect(url_for('index'))

    pdf_buffer = build_pdf(property_data)
    erf = property_data.get('erf_number', 'manual')

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Regulo_Zoning_Report_ERF{erf}.pdf",
        mimetype='application/pdf'
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PDF BUILDER — supports both NMBM and Johannesburg
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_pdf(p):
    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=A4,
                               topMargin=20*mm, bottomMargin=20*mm,
                               leftMargin=20*mm, rightMargin=20*mm)

    styles  = getSampleStyleSheet()
    content = []

    DARK  = colors.HexColor('#1a1a2e')
    BLUE  = colors.HexColor('#4361ee')
    LIGHT = colors.HexColor('#f8f9fa')

    GRADE_COLOURS = {
        'A': colors.HexColor('#2d6a4f'),
        'B': colors.HexColor('#52b788'),
        'C': colors.HexColor('#d4a017'),
        'D': colors.HexColor('#f4a261'),
        'F': colors.HexColor('#e63946'),
    }

    title_style = ParagraphStyle('Title', parent=styles['Normal'],
                                 fontSize=22, textColor=DARK,
                                 fontName='Helvetica-Bold', alignment=TA_CENTER,
                                 spaceAfter=20)
    sub_style   = ParagraphStyle('Sub', parent=styles['Normal'],
                                 fontSize=10, textColor=colors.grey,
                                 alignment=TA_CENTER, spaceAfter=2)
    section_style = ParagraphStyle('Section', parent=styles['Normal'],
                                   fontSize=13, textColor=BLUE,
                                   fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6)
    body_style  = ParagraphStyle('Body', parent=styles['Normal'],
                                 fontSize=10, leading=14)
    note_style  = ParagraphStyle('Note', parent=styles['Normal'],
                                 fontSize=9, leading=13, leftIndent=8)
    source_style = ParagraphStyle('Source', parent=styles['Normal'],
                                  fontSize=8, textColor=colors.grey,
                                  leading=11, spaceBefore=4)

    # Determine municipality context
    is_joburg = p.get('municipality') == 'johannesburg'
    is_capetown = p.get('municipality') == 'capetown'
    city_name = p.get('city', 'Gqeberha')

    # Municipality display name
    if is_joburg:
        muni_name = "City of Johannesburg"
    elif is_capetown:
        muni_name = "City of Cape Town"
    else:
        muni_name = "Nelson Mandela Bay Municipality"

    content.append(Paragraph("REGULO SYSTEMS", title_style))
    content.append(Paragraph("Zoning Intelligence Report", sub_style))
    content.append(Paragraph(
        f"Generated: {datetime.now().strftime('%d %B %Y at %H:%M')}",
        sub_style
    ))
    content.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))

    content.append(Paragraph("Property Details", section_style))

    details = [
        ["ERF Number",     p.get('erf_number', 'N/A')],
        ["Suburb",         p.get('suburb', 'N/A')],
        ["Municipality",   muni_name],
        ["Zone",           p.get('zone', 'N/A')],
        ["Land Use",       p.get('land_use', 'N/A')],
        ["Erf Size",       f"{p.get('erf_size', 'N/A')} m²"],
        ["Max Coverage",   p.get('coverage', 'N/A')],
        ["Max Height",     p.get('height', 'N/A')],
        ["Setbacks",       p.get('setbacks', 'N/A')],
    ]

    # Add Height Zone row for Johannesburg
    if is_joburg and p.get('height_zone'):
        details.append(["Height Zone", f"Height Zone {p['height_zone']}"])
        details.append(["Floor Area Ratio", str(p.get('floor_area_ratio', 'N/A'))])
    elif is_capetown:
        details.append(["Floor Factor", str(p.get('floor_area_ratio', 'N/A'))])
    else:
        details.append(["Floor Area Ratio (est.)", str(p.get('floor_area_ratio', 'N/A'))])

    tbl = Table(details, colWidths=[60*mm, 110*mm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHT),
        ('FONTNAME',   (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 9),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, LIGHT]),
        ('PADDING',    (0, 0), (-1, -1), 6),
    ]))
    content.append(tbl)

    if p.get('data_source'):
        if is_joburg:
            content.append(Paragraph(
                f"Source: {p['data_source']}. FAR values are official under the Johannesburg Town Planning Scheme.",
                source_style
            ))
        elif is_capetown:
            content.append(Paragraph(
                f"Source: {p['data_source']}. Floor Factor values are from the City of Cape Town Zoning Scheme Regulations.",
                source_style
            ))
        else:
            content.append(Paragraph(
                f"Source: {p['data_source']}. Floor Area Ratio is estimated — NMBM does not publish official FAR values.",
                source_style
            ))

    if p.get('buildable_area'):
        content.append(Paragraph("Estimated Maximum Buildable Floor Area", section_style))
        far  = p.get('floor_area_ratio', 'N/A')
        size = p.get('erf_size', 'N/A')

        if is_joburg and p.get('joburg_formula'):
            formula_text = p['joburg_formula']
            far_note = "FAR is official under the Johannesburg Town Planning Scheme."
        elif is_capetown and p.get('capetown_formula'):
            formula_text = p['capetown_formula']
            far_note = "Floor Factor is from the City of Cape Town Zoning Scheme Regulations."
        else:
            formula_text = f"{size} m² × {far} = {p['buildable_area']}"
            far_note = "Estimated maximum gross floor area. FAR is not officially published by NMBM."

        ba_data = [[
            Paragraph(
                f"<font size=26><b>{p['buildable_area']}</b></font>",
                ParagraphStyle('BA', parent=styles['Normal'],
                               textColor=BLUE, alignment=TA_CENTER)
            ),
            Paragraph(
                f"<b>ERF size × FAR</b><br/>"
                f"<font size=9 color='grey'>{formula_text}<br/>"
                f"{far_note}</font>",
                ParagraphStyle('BAText', parent=styles['Normal'], fontSize=10, leading=15)
            )
        ]]
        ba_tbl = Table(ba_data, colWidths=[50*mm, 120*mm])
        ba_tbl.setStyle(TableStyle([
            ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), DARK),
            ('BOX',        (0, 0), (-1, -1), 1, BLUE),
            ('PADDING',    (0, 0), (-1, -1), 12),
        ]))
        content.append(ba_tbl)

    content.append(Paragraph("Feasibility Assessment", section_style))

    grade       = p.get('feasibility_grade', 'F')
    grade_text  = p.get('feasibility_grade_text', 'Restricted')
    score       = p.get('feasibility_score', 0)
    grade_color = GRADE_COLOURS.get(grade, colors.grey)

    score_data = [[
        Paragraph(f"<font size=28><b>{grade}</b></font>", ParagraphStyle(
            'Grade', parent=styles['Normal'], textColor=grade_color, alignment=TA_CENTER, leading=34
        )),
        Paragraph(
            f"<b>{score}/100 — {grade_text}</b><br/>"
            f"<font size=9 color='grey'>Development feasibility rating based on zoning constraints</font>",
            ParagraphStyle('ScoreText', parent=styles['Normal'], fontSize=11, leading=16)
        )
    ]]
    score_tbl = Table(score_data, colWidths=[30*mm, 140*mm])
    score_tbl.setStyle(TableStyle([
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT),
        ('BOX',        (0, 0), (-1, -1), 1, grade_color),
        ('PADDING',    (0, 0), (-1, -1), 10),
    ]))
    content.append(score_tbl)
    content.append(Spacer(1, 8))

    notes = p.get('feasibility_notes', [])
    if notes:
        content.append(Paragraph("Score Factors:", body_style))
        for note in notes:
            content.append(Paragraph(note, note_style))

    if p.get('heritage_overlay') or p.get('environmental_restriction'):
        content.append(Spacer(1, 8))
        content.append(Paragraph("Special Conditions", section_style))
        if p.get('heritage_overlay'):
            content.append(Paragraph(
                "This property falls within a <b>Heritage Overlay</b>. "
                "Additional approvals from SAHRA or the local heritage authority may be required.",
                body_style
            ))
        if p.get('environmental_restriction'):
            content.append(Paragraph(
                "This property has <b>Environmental Restrictions</b>. "
                "An Environmental Impact Assessment (EIA) may be required before development.",
                body_style
            ))

    if p.get('notes'):
        content.append(Spacer(1, 8))
        content.append(Paragraph("Additional Notes", section_style))
        content.append(Paragraph(p['notes'], body_style))

    content.append(Spacer(1, 16))
    content.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    content.append(Spacer(1, 6))
    disclaimer = ParagraphStyle('Disclaimer', parent=styles['Normal'],
                                fontSize=7.5, textColor=colors.grey, leading=11)
    content.append(Paragraph(
        "<b>Disclaimer:</b> This report is generated from municipal zoning data and is intended for "
        "informational purposes only. It does not constitute professional planning or legal advice. "
        "Always verify constraints with the relevant municipality before making development decisions. "
        "Regulo Systems (Pty) Ltd accepts no liability for decisions made based on this report.",
        disclaimer
    ))

    doc.build(content)
    buffer.seek(0)
    return buffer


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RUN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == '__main__':
    app.run(debug=True)
