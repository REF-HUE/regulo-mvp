from flask import Flask, render_template, request, send_file, redirect, url_for
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

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zoning.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────────
# AUTO-SEED ON STARTUP
# ─────────────────────────────────────────────

def auto_seed():
    """Create and seed the database if it doesn't exist."""
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
        notes                     TEXT
    )
    """)

    existing = cursor.execute("SELECT COUNT(*) FROM properties").fetchone()[0]

    if existing == 0:
        properties = [
            ("3864", "Central", "Gqeberha", "Business 1", "Commercial / Mixed Use", "80%", 3.0, "20m", "Street: 0m | Side: 2m | Rear: 3m", 1200, 80.0, 20, 0, 0, "Prime commercial zoning suitable for retail, office, or mixed-use development."),
            ("1021", "Summerstrand", "Gqeberha", "Residential 3", "Medium Density Residential", "60%", 1.2, "10m", "Street: 3m | Side: 2m | Rear: 3m", 900, 60.0, 10, 0, 0, "Suitable for townhouse or sectional title development."),
            ("447", "Walmer", "Gqeberha", "Residential 1", "Single Residential", "50%", 0.8, "8m", "Street: 4.5m | Side: 1.5m | Rear: 3m", 750, 50.0, 8, 1, 0, "Property falls within a heritage protection overlay. Additional approvals may be required."),
            ("2230", "Newton Park", "Gqeberha", "Business 2", "Commercial / Retail", "75%", 2.5, "15m", "Street: 0m | Side: 2m | Rear: 3m", 1500, 75.0, 15, 0, 0, "High-visibility commercial node suitable for retail or office park development."),
            ("781", "Humewood", "Gqeberha", "Residential 2", "Low to Medium Density Residential", "60%", 1.0, "10m", "Street: 4m | Side: 1.5m | Rear: 3m", 680, 60.0, 10, 0, 1, "Environmental sensitivity zone — proximity to coastal dune system. EIA may be required."),
            ("912", "Richmond Hill", "Gqeberha", "Mixed Use", "Mixed Use — Residential / Commercial", "70%", 2.0, "14m", "Street: 2m | Side: 2m | Rear: 3m", 1100, 70.0, 14, 1, 0, "Heritage overlay applies. Mixed-use development potential subject to heritage authority approval."),
        ]

        cursor.executemany("""
        INSERT INTO properties (
            erf_number, suburb, city, zone, land_use, coverage,
            floor_area_ratio, height, setbacks, erf_size,
            coverage_numeric, height_numeric,
            heritage_overlay, environmental_restriction, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, properties)

        conn.commit()
        print(f"✅ Database seeded — {len(properties)} properties inserted.")
    else:
        print(f"✅ Database ready — {existing} properties found.")

    conn.close()

auto_seed()


# ─────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


# ─────────────────────────────────────────────
# SEARCH / RESULTS
# ─────────────────────────────────────────────

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
                    return render_template('index.html',
                                           error=f"ERF {erf_number} was not found in our database. "
                                                 f"Please check the number and try again.")
        else:
            prop = db.execute(
                "SELECT * FROM properties WHERE erf_number = ?",
                (erf_number,)
            ).fetchone()
            db.close()

            if not prop:
                return render_template('index.html',
                                       error=f"ERF {erf_number} was not found in our database. "
                                             f"Please check the number and try again.")

        property_data = dict(prop)

        score, notes, grade, grade_text, buildable_area = calculate_feasibility(property_data)
        property_data['feasibility_score']      = score
        property_data['feasibility_notes']      = notes
        property_data['feasibility_grade']      = grade
        property_data['feasibility_grade_text'] = grade_text
        property_data['buildable_area']         = buildable_area

        return render_template('result.html', property=property_data)

    return redirect(url_for('index'))


# ─────────────────────────────────────────────
# PDF REPORT
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# PDF BUILDER
# ─────────────────────────────────────────────

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
                                 spaceAfter=4)
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

    content.append(Paragraph("REGULO SYSTEMS", title_style))
    content.append(Paragraph("Zoning Intelligence Report", sub_style))
    content.append(Paragraph(
        f"Generated: {datetime.now().strftime('%d %B %Y at %H:%M')}",
        sub_style
    ))
    content.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))

    content.append(Paragraph("Property Details", section_style))

    details = [
        ["ERF Number",       p.get('erf_number', 'N/A')],
        ["Suburb",           p.get('suburb', 'N/A')],
        ["Zone",             p.get('zone', 'N/A')],
        ["Land Use",         p.get('land_use', 'N/A')],
        ["Erf Size",         f"{p.get('erf_size', 'N/A')} m²"],
        ["Max Coverage",     p.get('coverage', 'N/A')],
        ["Max Height",       p.get('height', 'N/A')],
        ["Setbacks",         p.get('setbacks', 'N/A')],
        ["Floor Area Ratio", str(p.get('floor_area_ratio', 'N/A'))],
    ]

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

    if p.get('buildable_area'):
        content.append(Paragraph("Maximum Buildable Floor Area", section_style))
        far  = p.get('floor_area_ratio', 'N/A')
        size = p.get('erf_size', 'N/A')
        ba_data = [[
            Paragraph(
                f"<font size=26><b>{p['buildable_area']}</b></font>",
                ParagraphStyle('BA', parent=styles['Normal'],
                               textColor=BLUE, alignment=TA_CENTER)
            ),
            Paragraph(
                f"<b>ERF size × Floor Area Ratio</b><br/>"
                f"<font size=9 color='grey'>{size} m² × {far} = {p['buildable_area']}<br/>"
                f"Maximum gross floor area permissible on this erf.</font>",
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
            'Grade', parent=styles['Normal'], textColor=grade_color, alignment=TA_CENTER
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


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)