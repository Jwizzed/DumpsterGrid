import os
import urllib.request
import sqlite3
import pandas as pd
import numpy as np
import re

# Direct raw download URL of SimpleMaps uscities.csv hosted on GitHub
CSV_URL = "https://raw.githubusercontent.com/fahadsultan/csc343/main/data/uscities.csv"
CSV_PATH = os.path.join("data", "uscities.csv")
DB_PATH = "dumpsters.db"

def download_csv():
    print(f"Downloading target locations from SimpleMaps dataset...")
    os.makedirs("data", exist_ok=True)
    if os.path.exists(CSV_PATH):
        print("SimpleMaps local CSV already exists, skipping download.")
        return
        
    try:
        # User-agent header to bypass potential basic scraping blockages
        req = urllib.request.Request(
            CSV_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            with open(CSV_PATH, 'wb') as out_file:
                out_file.write(response.read())
        print("SimpleMaps locations CSV downloaded successfully!")
    except Exception as e:
        print(f"Failed to download SimpleMaps database: {e}")
        raise

def slugify(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def clean_and_seed():
    print("Initiating Python Pandas data cleaning & seeding pipeline...")
    
    # 1. Load SimpleMaps CSV
    df = pd.read_csv(CSV_PATH)
    
    # Ensure population is numeric and drop NaNs
    df['population'] = pd.to_numeric(df['population'], errors='coerce').fillna(0).astype(int)
    
    # Sort descending by population
    df = df.sort_values(by='population', ascending=False)
    
    # 2. Format Slugs Uniformly
    # Merge city and state abbreviation into clean URL slug (e.g. dumpster-rental-austin-tx)
    df['city_slug'] = df['city_ascii'].apply(slugify)
    df['state_slug'] = df['state_id'].apply(slugify)
    df['slug'] = "dumpster-rental-" + df['city_slug'] + "-" + df['state_slug']
    
    # Deduplicate slugs keeping the highest population one
    df = df.drop_duplicates(subset=['slug'], keep='first')
    
    # Enforce the MVP Filter: Keep top 10,000 rows
    df = df.head(10000)
    print(f"Dataset successfully filtered to top {len(df)} unique largest cities.")
    
    # 4. Option C: Programmatic Pricing Formula (The Lean MVP Alternative)
    # High-cost states
    high_cost_states = {'CA', 'NY', 'MA', 'WA', 'NJ', 'HI', 'DC', 'CO', 'OR'}
    # Low-cost states
    low_cost_states = {'MS', 'AL', 'AR', 'WV', 'KY', 'OK', 'IA', 'KS', 'NE', 'ND', 'SD', 'MT', 'WY', 'WV'}
    
    # Baseline pricing plans
    base_10yd = {"low": 300, "high": 380}
    base_20yd = {"low": 400, "high": 490}
    base_30yd = {"low": 500, "high": 590}
    base_40yd = {"low": 600, "high": 690}
    
    # Local multipliers computation
    multipliers = []
    for idx, row in df.iterrows():
        state = row['state_id']
        pop = row['population']
        
        # Base multiplier
        mult = 1.0
        if state in high_cost_states or pop > 300000:
            mult = 1.20
        elif state in low_cost_states or pop < 25000:
            mult = 0.90
            
        # Add slight natural perturbation based on population length to make local numbers look fully unique
        perturbation = (len(str(pop)) % 5) * 0.02 - 0.04
        mult += perturbation
        multipliers.append(round(mult, 2))
        
    df['base_multiplier'] = multipliers
    
    # Apply baseline and round to clean integers as requested by user
    df['avg_low_10yd'] = (df['base_multiplier'] * base_10yd["low"]).astype(int)
    df['avg_high_10yd'] = (df['base_multiplier'] * base_10yd["high"]).astype(int)
    
    df['avg_low_20yd'] = (df['base_multiplier'] * base_20yd["low"]).astype(int)
    df['avg_high_20yd'] = (df['base_multiplier'] * base_20yd["high"]).astype(int)
    
    df['avg_low_30yd'] = (df['base_multiplier'] * base_30yd["low"]).astype(int)
    df['avg_high_30yd'] = (df['base_multiplier'] * base_30yd["high"]).astype(int)
    
    df['avg_low_40yd'] = (df['base_multiplier'] * base_40yd["low"]).astype(int)
    df['avg_high_40yd'] = (df['base_multiplier'] * base_40yd["high"]).astype(int)
    
    # 5. SQLite Seeding
    print("Recompiling SQLite database vault with 10,000 rows...")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create locations table
    cursor.execute("""
    CREATE TABLE locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        state_full TEXT NOT NULL,
        population INTEGER,
        permit_required INTEGER,
        permit_cost REAL,
        landfill_name TEXT,
        base_multiplier REAL,
        phone TEXT,
        slug TEXT UNIQUE,
        avg_low_10yd INTEGER,
        avg_high_10yd INTEGER,
        avg_low_20yd INTEGER,
        avg_high_20yd INTEGER,
        avg_low_30yd INTEGER,
        avg_high_30yd INTEGER,
        avg_low_40yd INTEGER,
        avg_high_40yd INTEGER
    )
    """)
    
    # Bulk insert for maximum execution speed
    insert_data = []
    for idx, row in enumerate(df.to_dict('records')):
        city = row['city']
        state = row['state_id']
        state_full = row['state_name']
        pop = row['population']
        slug = row['slug']
        
        # local dispatch simulated phone routing
        phone = f"800-508-{4000 + (idx % 5000)}"
        
        # Local ROW permit
        permit_required = 1 if (row['base_multiplier'] > 1.05 and pop > 50000) else 0
        permit_cost = 45.00 if permit_required else 0.00
        
        # Local Landfill
        landfill_name = f"{city} County Resource Recovery"
        
        insert_data.append((
            city,
            state,
            state_full,
            pop,
            permit_required,
            permit_cost,
            landfill_name,
            row['base_multiplier'],
            phone,
            slug,
            int(row['avg_low_10yd']),
            int(row['avg_high_10yd']),
            int(row['avg_low_20yd']),
            int(row['avg_high_20yd']),
            int(row['avg_low_30yd']),
            int(row['avg_high_30yd']),
            int(row['avg_low_40yd']),
            int(row['avg_high_40yd'])
        ))
        
    cursor.executemany("""
    INSERT INTO locations (
        city, state, state_full, population, permit_required, permit_cost, landfill_name, base_multiplier, phone, slug,
        avg_low_10yd, avg_high_10yd, avg_low_20yd, avg_high_20yd, avg_low_30yd, avg_high_30yd, avg_low_40yd, avg_high_40yd
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, insert_data)
    
    conn.commit()
    
    # Confirm
    cursor.execute("SELECT COUNT(*) FROM locations")
    seeded_count = cursor.fetchone()[0]
    conn.close()
    
    print(f"Data pipeline finished! Seeded {seeded_count} locations in SQLite database.")

def main():
    download_csv()
    clean_and_seed()

if __name__ == "__main__":
    main()
