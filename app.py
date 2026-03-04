from flask import Flask, render_template, request, send_file
from pdf_generator import generate_property_pdf
import sqlite3
import os

app = Flask(__name__)

# Get database path
DB_PATH = 'database.db'

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle search requests"""
    query = request.form.get('search_query', '').strip()
    
    if not query:
        return render_template('results.html', error="Please enter a stand number or address")
    
    # Search database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Search by stand number or address (case insensitive)
    cursor.execute("""
        SELECT * FROM properties 
        WHERE LOWER(stand_number) = LOWER(?) 
        OR LOWER(address) LIKE LOWER(?)
        OR LOWER(suburb) LIKE LOWER(?)
    """, (query, f'%{query}%', f'%{query}%'))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        # Convert to dictionary
        property_data = {
            'stand_number': result['stand_number'],
            'address': result['address'],
            'suburb': result['suburb'],
            'municipality': result['municipality'],
            'zoning': result['zoning'],
            'coverage': result['coverage'],
            'height': result['height'],
            'setback_street': result['setback_street'],
            'setback_side': result['setback_side'],
            'setback_rear': result['setback_rear'],
            'parking': result['parking'],
            'allowed_uses': result['allowed_uses'],
            'restrictions': result['restrictions']
        }
        return render_template('results.html', data=property_data)
    else:
        return render_template('results.html', 
                             error=f"Property '{query}' not found in our database. Currently we only have data for 5 test properties.")

@app.route('/download-pdf/<stand_number>')
def download_pdf(stand_number):
    """Generate and download PDF report for a property"""
    
    # Get property data from database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM properties 
        WHERE LOWER(stand_number) = LOWER(?)
    """, (stand_number,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return "Property not found", 404
    
    # Convert to dictionary
    property_data = {
        'stand_number': result['stand_number'],
        'address': result['address'],
        'suburb': result['suburb'],
        'municipality': result['municipality'],
        'zoning': result['zoning'],
        'coverage': result['coverage'],
        'height': result['height'],
        'setback_street': result['setback_street'],
        'setback_side': result['setback_side'],
        'setback_rear': result['setback_rear'],
        'parking': result['parking'],
        'allowed_uses': result['allowed_uses'],
        'restrictions': result['restrictions']
    }
    
    # Generate PDF
    pdf_buffer = generate_property_pdf(property_data)
    
    # Create filename
    filename = f"Regulo_Report_{property_data['stand_number']}_{property_data['suburb']}.pdf"
    
    # Send PDF as download
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )

# Auto-create database if it doesn't exist
if not os.path.exists(DB_PATH):
    print("📊 Creating database on startup...")
    from init_db import init_database
    init_database()

if __name__ == '__main__':
    print("\n🚀 Starting Regulo MVP...")
    app.run(debug=True)