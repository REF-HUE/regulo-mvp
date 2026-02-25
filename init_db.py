import sqlite3
import os

DB_PATH = 'database.db'

def init_database():
    """Create database and populate with test data"""
    
    # Remove old database if exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️  Removed old database")
    
    # Create new database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
    CREATE TABLE properties (
        stand_number TEXT PRIMARY KEY,
        address TEXT NOT NULL,
        suburb TEXT NOT NULL,
        municipality TEXT NOT NULL,
        zoning TEXT NOT NULL,
        coverage TEXT NOT NULL,
        height TEXT NOT NULL,
        setback_street TEXT NOT NULL,
        setback_side TEXT NOT NULL,
        setback_rear TEXT NOT NULL,
        parking TEXT NOT NULL,
        allowed_uses TEXT NOT NULL,
        restrictions TEXT NOT NULL
    )
    ''')
    
    print("✅ Created properties table")
    
    # Insert test data (5 realistic Johannesburg properties)
    test_properties = [
        {
            'stand_number': '123',
            'address': 'Stand 123, Main Road',
            'suburb': 'Bryanston',
            'municipality': 'City of Johannesburg',
            'zoning': 'Residential 1',
            'coverage': 'Maximum 50%',
            'height': '2 storeys (8m maximum)',
            'setback_street': '5 meters',
            'setback_side': '1.5 meters',
            'setback_rear': '3 meters',
            'parking': '2 bays per dwelling',
            'allowed_uses': 'Single dwelling, Granny flat (with neighbour consent), Home office',
            'restrictions': '⚠️ Neighbour consent required for second dwelling. Check title deed for servitudes.'
        },
        {
            'stand_number': '456',
            'address': 'Stand 456, Oak Avenue',
            'suburb': 'Sandton',
            'municipality': 'City of Johannesburg',
            'zoning': 'Residential 2',
            'coverage': 'Maximum 60%',
            'height': '3 storeys (11m maximum)',
            'setback_street': '4 meters',
            'setback_side': '1.5 meters',
            'setback_rear': '3 meters',
            'parking': '2 bays per dwelling unit',
            'allowed_uses': 'Multiple dwellings (max 3 units), Townhouses, Group housing',
            'restrictions': '⚠️ Traffic impact assessment required for 3+ units. Municipal approval needed for shared driveways.'
        },
        {
            'stand_number': '789',
            'address': 'Stand 789, Church Street',
            'suburb': 'Rosebank',
            'municipality': 'City of Johannesburg',
            'zoning': 'Business 1',
            'coverage': 'Maximum 70%',
            'height': '4 storeys (15m maximum)',
            'setback_street': '3 meters',
            'setback_side': '0 meters (if firewall)',
            'setback_rear': '3 meters',
            'parking': '1 bay per 40m² GLA',
            'allowed_uses': 'Offices, Retail, Restaurants, Medical suites',
            'restrictions': '⚠️ Fire certificate required. Parking must comply with SANS 10400-T. Rezoning may be needed for residential use.'
        },
        {
            'stand_number': '234',
            'address': 'Stand 234, Park Lane',
            'suburb': 'Fourways',
            'municipality': 'City of Johannesburg',
            'zoning': 'Residential 1',
            'coverage': 'Maximum 50%',
            'height': '2 storeys (8m maximum)',
            'setback_street': '5 meters',
            'setback_side': '1.5 meters',
            'setback_rear': '3 meters',
            'parking': '2 bays per dwelling',
            'allowed_uses': 'Single dwelling, Granny flat (with consent), Home office (max 50m²)',
            'restrictions': '⚠️ Estate rules may be stricter than municipal zoning. Check with Homeowners Association before design.'
        },
        {
            'stand_number': '567',
            'address': 'Stand 567, Industrial Road',
            'suburb': 'Midrand',
            'municipality': 'City of Johannesburg',
            'zoning': 'Industrial 1',
            'coverage': 'Maximum 80%',
            'height': '12 meters maximum (single storey warehouse typical)',
            'setback_street': '6 meters',
            'setback_side': '3 meters',
            'setback_rear': '3 meters',
            'parking': '1 bay per 100m² GLA',
            'allowed_uses': 'Warehousing, Light manufacturing, Logistics, Storage facilities',
            'restrictions': '⚠️ Environmental impact assessment may be required. Stormwater management plan mandatory. Heavy vehicle access approval needed.'
        }
    ]
    
    for prop in test_properties:
        cursor.execute('''
        INSERT INTO properties VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            prop['stand_number'],
            prop['address'],
            prop['suburb'],
            prop['municipality'],
            prop['zoning'],
            prop['coverage'],
            prop['height'],
            prop['setback_street'],
            prop['setback_side'],
            prop['setback_rear'],
            prop['parking'],
            prop['allowed_uses'],
            prop['restrictions']
        ))
        print(f"✅ Added: {prop['address']}, {prop['suburb']}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Database created successfully!")
    print(f"📊 Added {len(test_properties)} test properties")
    print(f"\n🔍 Try searching for: 123, 456, 789, Bryanston, Sandton, Industrial\n")

if __name__ == '__main__':
    init_database()