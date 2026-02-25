from flask import Flask, render_template, request
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

if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print("⚠️  Database not found! Run 'python init_db.py' first to create the database.")
    
    print("\n🚀 Starting Regulo MVP...")
    print("📍 Open http://localhost:5000 in your browser\n")
    app.run(debug=True, port=5000)