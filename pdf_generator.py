from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO

def generate_property_pdf(property_data):
    """
    Generate a professional property feasibility PDF report.
    
    Args:
        property_data: Dictionary containing property information
        
    Returns:
        BytesIO object containing the PDF
    """
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Custom heading style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Body text style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    # Title
    title = Paragraph("REGULO", title_style)
    elements.append(title)
    
    subtitle = Paragraph("Property Feasibility Report", styles['Heading2'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.5*cm))
    
    # Property Header
    property_header = Paragraph(
        f"<b>{property_data['address']}</b><br/>{property_data['suburb']}, {property_data['municipality']}",
        styles['Heading3']
    )
    elements.append(property_header)
    elements.append(Spacer(1, 0.5*cm))
    
    # Zoning Section
    elements.append(Paragraph("ZONING CLASSIFICATION", heading_style))
    zoning_text = f"<b>{property_data['zoning']}</b>"
    elements.append(Paragraph(zoning_text, body_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # Building Limits Table
    elements.append(Paragraph("BUILDING LIMITS", heading_style))
    
    limits_data = [
        ['Parameter', 'Requirement'],
        ['Coverage', property_data['coverage']],
        ['Height', property_data['height']],
    ]
    
    limits_table = Table(limits_data, colWidths=[6*cm, 8*cm])
    limits_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(limits_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Setbacks Table
    elements.append(Paragraph("SETBACK REQUIREMENTS", heading_style))
    
    setbacks_data = [
        ['Location', 'Distance'],
        ['Street Setback', property_data['setback_street']],
        ['Side Setback', property_data['setback_side']],
        ['Rear Setback', property_data['setback_rear']],
    ]
    
    setbacks_table = Table(setbacks_data, colWidths=[6*cm, 8*cm])
    setbacks_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(setbacks_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Parking
    elements.append(Paragraph("PARKING REQUIREMENTS", heading_style))
    parking_text = property_data['parking']
    elements.append(Paragraph(parking_text, body_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Permitted Uses
    elements.append(Paragraph("PERMITTED USES", heading_style))
    uses_text = property_data['allowed_uses']
    elements.append(Paragraph(uses_text, body_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Restrictions
    elements.append(Paragraph("RESTRICTIONS & WARNINGS", heading_style))
    restrictions_box = Paragraph(
        f'<font color="#856404"><b>⚠️ {property_data["restrictions"]}</b></font>',
        body_style
    )
    elements.append(restrictions_box)
    elements.append(Spacer(1, 0.5*cm))
    
    # Disclaimer
    elements.append(Spacer(1, 1*cm))
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#721c24'),
        alignment=TA_LEFT,
        leftIndent=0.5*cm,
        rightIndent=0.5*cm
    )
    
    disclaimer_text = """
    <b>LEGAL DISCLAIMER:</b> This report provides preliminary guidance only and should not be 
    relied upon as professional advice. Zoning regulations, title deed conditions, and municipal 
    requirements can be complex and subject to change. Always consult a registered architect or 
    professional consultant before proceeding with any design or development work.
    """
    
    elements.append(Paragraph(disclaimer_text, disclaimer_style))
    
    # Footer
    elements.append(Spacer(1, 0.5*cm))
    footer_text = """
    <para align=center>
    <font size=9 color="#666">
    Generated by <b>REGULO</b> - Property Intelligence Platform<br/>
    regulo-mvp.onrender.com
    </font>
    </para>
    """
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF from buffer
    buffer.seek(0)
    return buffer