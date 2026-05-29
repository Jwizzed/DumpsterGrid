import os
import sqlite3
import random

# Base list of 150 major US cities across various states with populations and cost multipliers
CITIES_DATA = [
    # Texas
    {"city": "Houston", "state": "TX", "state_full": "Texas", "pop": 2304580, "mult": 1.00, "permit": True, "fee": 50.00, "landfill": "McCarty Road Landfill"},
    {"city": "San Antonio", "state": "TX", "state_full": "Texas", "pop": 1434625, "mult": 0.92, "permit": False, "fee": 0.00, "landfill": "Covel Gardens Landfill"},
    {"city": "Dallas", "state": "TX", "state_full": "Texas", "pop": 1304379, "mult": 1.02, "permit": True, "fee": 60.00, "landfill": "McCommas Bluff Landfill"},
    {"city": "Austin", "state": "TX", "state_full": "Texas", "pop": 961855, "mult": 1.12, "permit": True, "fee": 45.00, "landfill": "Austin Community Landfill"},
    {"city": "Fort Worth", "state": "TX", "state_full": "Texas", "pop": 918915, "mult": 0.98, "permit": False, "fee": 0.00, "landfill": "Southeast Landfill"},
    {"city": "El Paso", "state": "TX", "state_full": "Texas", "pop": 678815, "mult": 0.85, "permit": False, "fee": 0.00, "landfill": "Clint Landfill"},
    {"city": "Arlington", "state": "TX", "state_full": "Texas", "pop": 394266, "mult": 0.95, "permit": False, "fee": 0.00, "landfill": "Arlington Landfill"},
    {"city": "Corpus Christi", "state": "TX", "state_full": "Texas", "pop": 317863, "mult": 0.90, "permit": True, "fee": 30.00, "landfill": "J.C. Elliott Landfill"},
    {"city": "Plano", "state": "TX", "state_full": "Texas", "pop": 285494, "mult": 1.05, "permit": True, "fee": 40.00, "landfill": "NTMWD Landfill"},
    {"city": "Lubbock", "state": "TX", "state_full": "Texas", "pop": 257141, "mult": 0.86, "permit": False, "fee": 0.00, "landfill": "West Texas Landfill"},
    {"city": "Laredo", "state": "TX", "state_full": "Texas", "pop": 255205, "mult": 0.84, "permit": False, "fee": 0.00, "landfill": "City of Laredo Landfill"},
    {"city": "Irving", "state": "TX", "state_full": "Texas", "pop": 239798, "mult": 0.99, "permit": True, "fee": 50.00, "landfill": "Hunter Ferrell Landfill"},
    {"city": "Garland", "state": "TX", "state_full": "Texas", "pop": 239928, "mult": 0.96, "permit": False, "fee": 0.00, "landfill": "Garland Landfill"},
    {"city": "Frisco", "state": "TX", "state_full": "Texas", "pop": 200509, "mult": 1.10, "permit": True, "fee": 55.00, "landfill": "Custer Road Transfer Station"},
    {"city": "McKinney", "state": "TX", "state_full": "Texas", "pop": 195308, "mult": 1.06, "permit": True, "fee": 45.00, "landfill": "McKinney Landfill"},
    
    # California
    {"city": "Los Angeles", "state": "CA", "state_full": "California", "pop": 3898747, "mult": 1.35, "permit": True, "fee": 85.00, "landfill": "Sunshine Canyon Landfill"},
    {"city": "San Diego", "state": "CA", "state_full": "California", "pop": 1386932, "mult": 1.28, "permit": True, "fee": 75.00, "landfill": "Miramar Landfill"},
    {"city": "San Jose", "state": "CA", "state_full": "California", "pop": 1013240, "mult": 1.38, "permit": True, "fee": 90.00, "landfill": "Kirby Canyon Landfill"},
    {"city": "San Francisco", "state": "CA", "state_full": "California", "pop": 873965, "mult": 1.45, "permit": True, "fee": 120.00, "landfill": "Corinda Los Trancos Landfill"},
    {"city": "Fresno", "state": "CA", "state_full": "California", "pop": 542107, "mult": 1.08, "permit": False, "fee": 0.00, "landfill": "Cedar Avenue Landfill"},
    {"city": "Sacramento", "state": "CA", "state_full": "California", "pop": 524943, "mult": 1.18, "permit": True, "fee": 65.00, "landfill": "Kiefer Landfill"},
    {"city": "Long Beach", "state": "CA", "state_full": "California", "pop": 466742, "mult": 1.28, "permit": True, "fee": 80.00, "landfill": "Southeast Resource Recovery"},
    {"city": "Oakland", "state": "CA", "state_full": "California", "pop": 440646, "mult": 1.32, "permit": True, "fee": 95.00, "landfill": "Davis Street Transfer Station"},
    {"city": "Bakersfield", "state": "CA", "state_full": "California", "pop": 403048, "mult": 1.02, "permit": False, "fee": 0.00, "landfill": "Bena Landfill"},
    {"city": "Anaheim", "state": "CA", "state_full": "California", "pop": 346824, "mult": 1.25, "permit": True, "fee": 70.00, "landfill": "Olinda Alpha Landfill"},
    {"city": "Santa Ana", "state": "CA", "state_full": "California", "pop": 310227, "mult": 1.24, "permit": True, "fee": 70.00, "landfill": "Bowerman Landfill"},
    {"city": "Riverside", "state": "CA", "state_full": "California", "pop": 314998, "mult": 1.15, "permit": True, "fee": 50.00, "landfill": "Badlands Landfill"},
    {"city": "Stockton", "state": "CA", "state_full": "California", "pop": 320804, "mult": 1.12, "permit": True, "fee": 55.00, "landfill": "Forward Landfill"},
    {"city": "Chula Vista", "state": "CA", "state_full": "California", "pop": 275487, "mult": 1.22, "permit": True, "fee": 65.00, "landfill": "Otay Landfill"},
    {"city": "Irvine", "state": "CA", "state_full": "California", "pop": 307670, "mult": 1.30, "permit": True, "fee": 75.00, "landfill": "Bee Canyon Landfill"},
    
    # Florida
    {"city": "Jacksonville", "state": "FL", "state_full": "Florida", "pop": 949611, "mult": 0.95, "permit": False, "fee": 0.00, "landfill": "Trail Ridge Landfill"},
    {"city": "Miami", "state": "FL", "state_full": "Florida", "pop": 442241, "mult": 1.18, "permit": True, "fee": 75.00, "landfill": "South Dade Landfill"},
    {"city": "Tampa", "state": "FL", "state_full": "Florida", "pop": 384959, "mult": 1.05, "permit": True, "fee": 40.00, "landfill": "Southeast County Landfill"},
    {"city": "Orlando", "state": "FL", "state_full": "Florida", "pop": 307573, "mult": 1.08, "permit": True, "fee": 45.00, "landfill": "Orange County Landfill"},
    {"city": "St. Petersburg", "state": "FL", "state_full": "Florida", "pop": 258308, "mult": 1.02, "permit": True, "fee": 35.00, "landfill": "Toytown Landfill"},
    {"city": "Hialeah", "state": "FL", "state_full": "Florida", "pop": 223109, "mult": 1.12, "permit": True, "fee": 50.00, "landfill": "North Dade Landfill"},
    {"city": "Tallahassee", "state": "FL", "state_full": "Florida", "pop": 196169, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "Leon County Landfill"},
    {"city": "Fort Lauderdale", "state": "FL", "state_full": "Florida", "pop": 182760, "mult": 1.15, "permit": True, "fee": 60.00, "landfill": "Broward County Landfill"},
    {"city": "Port St. Lucie", "state": "FL", "state_full": "Florida", "pop": 204851, "mult": 0.98, "permit": False, "fee": 0.00, "landfill": "St. Lucie County Landfill"},
    {"city": "Cape Coral", "state": "FL", "state_full": "Florida", "pop": 194049, "mult": 1.00, "permit": False, "fee": 0.00, "landfill": "Lee County Landfill"},
    
    # New York
    {"city": "New York", "state": "NY", "state_full": "New York", "pop": 8335897, "mult": 1.50, "permit": True, "fee": 150.00, "landfill": "Seneca Meadows Landfill"},
    {"city": "Buffalo", "state": "NY", "state_full": "New York", "pop": 278349, "mult": 0.92, "permit": True, "fee": 35.00, "landfill": "Chaffee Landfill"},
    {"city": "Rochester", "state": "NY", "state_full": "New York", "pop": 211328, "mult": 0.94, "permit": True, "fee": 40.00, "landfill": "High Acres Landfill"},
    {"city": "Yonkers", "state": "NY", "state_full": "New York", "pop": 211569, "mult": 1.25, "permit": True, "fee": 75.00, "landfill": "Westchester County Transfer"},
    {"city": "Syracuse", "state": "NY", "state_full": "New York", "pop": 148620, "mult": 0.90, "permit": True, "fee": 30.00, "landfill": "OCRRA Landfill"},
    
    # Illinois
    {"city": "Chicago", "state": "IL", "state_full": "Illinois", "pop": 2746388, "mult": 1.25, "permit": True, "fee": 100.00, "landfill": "CID Recycling & Disposal"},
    {"city": "Aurora", "state": "IL", "state_full": "Illinois", "pop": 180542, "mult": 1.05, "permit": True, "fee": 45.00, "landfill": "Kane County Landfill"},
    {"city": "Naperville", "state": "IL", "state_full": "Illinois", "pop": 149541, "mult": 1.10, "permit": True, "fee": 50.00, "landfill": "DuPage County Landfill"},
    {"city": "Joliet", "state": "IL", "state_full": "Illinois", "pop": 150362, "mult": 1.00, "permit": False, "fee": 0.00, "landfill": "Prairie View Landfill"},
    {"city": "Rockford", "state": "IL", "state_full": "Illinois", "pop": 148655, "mult": 0.92, "permit": False, "fee": 0.00, "landfill": "Winnebago Landfill"},
    
    # Georgia
    {"city": "Atlanta", "state": "GA", "state_full": "Georgia", "pop": 498715, "mult": 1.08, "permit": True, "fee": 50.00, "landfill": "Hickory Ridge Landfill"},
    {"city": "Augusta", "state": "GA", "state_full": "Georgia", "pop": 202081, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "Augusta Solid Waste"},
    {"city": "Columbus", "state": "GA", "state_full": "Georgia", "pop": 206922, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Pine Grove Landfill"},
    {"city": "Savannah", "state": "GA", "state_full": "Georgia", "pop": 147780, "mult": 0.96, "permit": True, "fee": 30.00, "landfill": "Dean Forest Road Landfill"},
    {"city": "Athens", "state": "GA", "state_full": "Georgia", "pop": 128560, "mult": 0.92, "permit": False, "fee": 0.00, "landfill": "Athens-Clarke County Landfill"},
    
    # North Carolina
    {"city": "Charlotte", "state": "NC", "state_full": "North Carolina", "pop": 874579, "mult": 1.00, "permit": False, "fee": 0.00, "landfill": "Speedway Landfill"},
    {"city": "Raleigh", "state": "NC", "state_full": "North Carolina", "pop": 467665, "mult": 1.04, "permit": True, "fee": 35.00, "landfill": "Wilders Grove Landfill"},
    {"city": "Greensboro", "state": "NC", "state_full": "North Carolina", "pop": 299035, "mult": 0.92, "permit": False, "fee": 0.00, "landfill": "White Street Landfill"},
    {"city": "Durham", "state": "NC", "state_full": "North Carolina", "pop": 283506, "mult": 0.98, "permit": True, "fee": 30.00, "landfill": "Durham County Landfill"},
    {"city": "Winston-Salem", "state": "NC", "state_full": "North Carolina", "pop": 249545, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "Hanes Mill Road Landfill"},
    {"city": "Fayetteville", "state": "NC", "state_full": "North Carolina", "pop": 208501, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Wilkes Road Landfill"},
    {"city": "Cary", "state": "NC", "state_full": "North Carolina", "pop": 174721, "mult": 1.06, "permit": True, "fee": 40.00, "landfill": "South Wake Landfill"},
    {"city": "Wilmington", "state": "NC", "state_full": "North Carolina", "pop": 115451, "mult": 0.98, "permit": True, "fee": 35.00, "landfill": "New Hanover Landfill"},
    
    # Ohio
    {"city": "Columbus", "state": "OH", "state_full": "Ohio", "pop": 905748, "mult": 0.96, "permit": True, "fee": 45.00, "landfill": "Franklin County Landfill"},
    {"city": "Cleveland", "state": "OH", "state_full": "Ohio", "pop": 372624, "mult": 0.98, "permit": True, "fee": 50.00, "landfill": "Harvard Road Landfill"},
    {"city": "Cincinnati", "state": "OH", "state_full": "Ohio", "pop": 309317, "mult": 0.98, "permit": True, "fee": 40.00, "landfill": "Rumpke Sanitary Landfill"},
    {"city": "Toledo", "state": "OH", "state_full": "Ohio", "pop": 270871, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Hoffman Road Landfill"},
    {"city": "Akron", "state": "OH", "state_full": "Ohio", "pop": 190265, "mult": 0.86, "permit": False, "fee": 0.00, "landfill": "Hardesty Park Transfer Station"},
    {"city": "Dayton", "state": "OH", "state_full": "Ohio", "pop": 137644, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Stoney Hollow Landfill"},
    
    # Washington
    {"city": "Seattle", "state": "WA", "state_full": "Washington", "pop": 737015, "mult": 1.32, "permit": True, "fee": 90.00, "landfill": "Cedar Hills Landfill"},
    {"city": "Spokane", "state": "WA", "state_full": "Washington", "pop": 228989, "mult": 1.02, "permit": False, "fee": 0.00, "landfill": "Spokane Regional Landfill"},
    {"city": "Tacoma", "state": "WA", "state_full": "Washington", "pop": 219346, "mult": 1.15, "permit": True, "fee": 60.00, "landfill": "Tacoma Landfill"},
    {"city": "Vancouver", "state": "WA", "state_full": "Washington", "pop": 190969, "mult": 1.10, "permit": False, "fee": 0.00, "landfill": "Finley Buttes Landfill"},
    {"city": "Bellevue", "state": "WA", "state_full": "Washington", "pop": 151854, "mult": 1.30, "permit": True, "fee": 80.00, "landfill": "Factoria Transfer Station"},
    
    # Arizona
    {"city": "Phoenix", "state": "AZ", "state_full": "Arizona", "pop": 1608139, "mult": 0.98, "permit": False, "fee": 0.00, "landfill": "SR 85 Landfill"},
    {"city": "Tucson", "state": "AZ", "state_full": "Arizona", "pop": 542629, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "Los Reales Landfill"},
    {"city": "Mesa", "state": "AZ", "state_full": "Arizona", "pop": 504258, "mult": 0.96, "permit": False, "fee": 0.00, "landfill": "Salt River Landfill"},
    {"city": "Chandler", "state": "AZ", "state_full": "Arizona", "pop": 275987, "mult": 0.98, "permit": False, "fee": 0.00, "landfill": "Chandler Landfill"},
    {"city": "Gilbert", "state": "AZ", "state_full": "Arizona", "pop": 267918, "mult": 0.98, "permit": False, "fee": 0.00, "landfill": "Gilbert Waste Station"},
    {"city": "Glendale", "state": "AZ", "state_full": "Arizona", "pop": 248324, "mult": 0.94, "permit": False, "fee": 0.00, "landfill": "Glendale Landfill"},
    {"city": "Scottsdale", "state": "AZ", "state_full": "Arizona", "pop": 241361, "mult": 1.10, "permit": True, "fee": 45.00, "landfill": "Scottsdale Transfer Station"},
    {"city": "Tempe", "state": "AZ", "state_full": "Arizona", "pop": 180587, "mult": 0.96, "permit": False, "fee": 0.00, "landfill": "Tempe Transfer Station"},
    {"city": "Peoria", "state": "AZ", "state_full": "Arizona", "pop": 190985, "mult": 0.94, "permit": False, "fee": 0.00, "landfill": "Peoria Landfill"},
    
    # Colorado
    {"city": "Denver", "state": "CO", "state_full": "Colorado", "pop": 715522, "mult": 1.14, "permit": True, "fee": 55.00, "landfill": "Denver Arapahoe Disposal"},
    {"city": "Colorado Springs", "state": "CO", "state_full": "Colorado", "pop": 478961, "mult": 1.02, "permit": False, "fee": 0.00, "landfill": "Midway Landfill"},
    {"city": "Aurora", "state": "CO", "state_full": "Colorado", "pop": 386261, "mult": 1.05, "permit": False, "fee": 0.00, "landfill": "Denver Regional Landfill"},
    {"city": "Fort Collins", "state": "CO", "state_full": "Colorado", "pop": 169810, "mult": 1.08, "permit": False, "fee": 0.00, "landfill": "Larimer County Landfill"},
    {"city": "Lakewood", "state": "CO", "state_full": "Colorado", "pop": 155984, "mult": 1.10, "permit": True, "fee": 40.00, "landfill": "Rooney Road Recycling"},
    {"city": "Thornton", "state": "CO", "state_full": "Colorado", "pop": 141867, "mult": 1.02, "permit": False, "fee": 0.00, "landfill": "Dad Clark Transfer Station"},
    {"city": "Arvada", "state": "CO", "state_full": "Colorado", "pop": 124402, "mult": 1.08, "permit": True, "fee": 35.00, "landfill": "Jefferson County Disposal"},
    
    # Massachusetts
    {"city": "Boston", "state": "MA", "state_full": "Massachusetts", "pop": 675647, "mult": 1.38, "permit": True, "fee": 110.00, "landfill": "Rochester Environmental"},
    {"city": "Worcester", "state": "MA", "state_full": "Massachusetts", "pop": 206560, "mult": 1.10, "permit": True, "fee": 50.00, "landfill": "Worcester Transfer Station"},
    {"city": "Springfield", "state": "MA", "state_full": "Massachusetts", "pop": 155929, "mult": 1.05, "permit": True, "fee": 45.00, "landfill": "Springfield Landfill"},
    {"city": "Cambridge", "state": "MA", "state_full": "Massachusetts", "pop": 118403, "mult": 1.40, "permit": True, "fee": 120.00, "landfill": "Covanta Haverhill"},
    {"city": "Lowell", "state": "MA", "state_full": "Massachusetts", "pop": 115554, "mult": 1.08, "permit": True, "fee": 50.00, "landfill": "Lowell Recycling Depot"},
    
    # Pennsylvania
    {"city": "Philadelphia", "state": "PA", "state_full": "Pennsylvania", "pop": 1603797, "mult": 1.22, "permit": True, "fee": 75.00, "landfill": "Grows Landfill"},
    {"city": "Pittsburgh", "state": "PA", "state_full": "Pennsylvania", "pop": 302971, "mult": 1.08, "permit": True, "fee": 55.00, "landfill": "Arnoni Landfill"},
    {"city": "Allentown", "state": "PA", "state_full": "Pennsylvania", "pop": 125845, "mult": 1.02, "permit": True, "fee": 40.00, "landfill": "Chrin Sanitary Landfill"},
    {"city": "Erie", "state": "PA", "state_full": "Pennsylvania", "pop": 94834, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Lake View Landfill"},
    {"city": "Reading", "state": "PA", "state_full": "Pennsylvania", "pop": 95112, "mult": 0.94, "permit": True, "fee": 35.00, "landfill": "Pioneer Crossing Landfill"},
    
    # Michigan
    {"city": "Detroit", "state": "MI", "state_full": "Michigan", "pop": 639111, "mult": 1.00, "permit": True, "fee": 45.00, "landfill": "Pine Tree Acres Landfill"},
    {"city": "Grand Rapids", "state": "MI", "state_full": "Michigan", "pop": 198917, "mult": 0.96, "permit": False, "fee": 0.00, "landfill": "South Kent Landfill"},
    {"city": "Warren", "state": "MI", "state_full": "Michigan", "pop": 139387, "mult": 0.98, "permit": True, "fee": 35.00, "landfill": "Macomb Landfill"},
    {"city": "Sterling Heights", "state": "MI", "state_full": "Michigan", "pop": 134346, "mult": 0.96, "permit": False, "fee": 0.00, "landfill": "Clinton Township Transfer"},
    {"city": "Lansing", "state": "MI", "state_full": "Michigan", "pop": 112644, "mult": 0.92, "permit": False, "fee": 0.00, "landfill": "Granger Landfill"},
    
    # North/South General Major US Cities
    {"city": "Indianapolis", "state": "IN", "state_full": "Indiana", "pop": 887642, "mult": 0.94, "permit": False, "fee": 0.00, "landfill": "Southside Landfill"},
    {"city": "Fort Wayne", "state": "IN", "state_full": "Indiana", "pop": 263886, "mult": 0.86, "permit": False, "fee": 0.00, "landfill": "National Serv-All Landfill"},
    {"city": "Nashville", "state": "TN", "state_full": "Tennessee", "pop": 689447, "mult": 1.02, "permit": True, "fee": 45.00, "landfill": "Southern Disposal Landfill"},
    {"city": "Memphis", "state": "TN", "state_full": "Tennessee", "pop": 633104, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "North Shelby Landfill"},
    {"city": "Knoxville", "state": "TN", "state_full": "Tennessee", "pop": 190740, "mult": 0.92, "permit": False, "fee": 0.00, "landfill": "Chestnut Ridge Landfill"},
    {"city": "Las Vegas", "state": "NV", "state_full": "Nevada", "pop": 641903, "mult": 1.10, "permit": True, "fee": 60.00, "landfill": "Apex Regional Landfill"},
    {"city": "Henderson", "state": "NV", "state_full": "Nevada", "pop": 317610, "mult": 1.06, "permit": True, "fee": 50.00, "landfill": "Boulder City Landfill"},
    {"city": "Reno", "state": "NV", "state_full": "Nevada", "pop": 264165, "mult": 1.08, "permit": True, "fee": 45.00, "landfill": "Lockwood Regional Landfill"},
    {"city": "Portland", "state": "OR", "state_full": "Oregon", "pop": 652503, "mult": 1.24, "permit": True, "fee": 75.00, "landfill": "Hillsboro Landfill"},
    {"city": "Eugene", "state": "OR", "state_full": "Oregon", "pop": 176654, "mult": 1.10, "permit": False, "fee": 0.00, "landfill": "Short Mountain Landfill"},
    {"city": "Salem", "state": "OR", "state_full": "Oregon", "pop": 175535, "mult": 1.08, "permit": False, "fee": 0.00, "landfill": "Coffin Butte Landfill"},
    {"city": "Salt Lake City", "state": "UT", "state_full": "Utah", "pop": 200591, "mult": 1.02, "permit": True, "fee": 35.00, "landfill": "Salt Lake County Landfill"},
    {"city": "West Valley City", "state": "UT", "state_full": "Utah", "pop": 140230, "mult": 0.96, "permit": False, "fee": 0.00, "landfill": "Trans-Jordan Landfill"},
    {"city": "Provo", "state": "UT", "state_full": "Utah", "pop": 115162, "mult": 0.94, "permit": False, "fee": 0.00, "landfill": "South Utah Valley Landfill"},
    {"city": "Albuquerque", "state": "NM", "state_full": "New Mexico", "pop": 564559, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "Cerro Colorado Landfill"},
    {"city": "Las Cruces", "state": "NM", "state_full": "New Mexico", "pop": 111385, "mult": 0.84, "permit": False, "fee": 0.00, "landfill": "Amador Transfer Station"},
    {"city": "Kansas City", "state": "MO", "state_full": "Missouri", "pop": 508090, "mult": 0.96, "permit": True, "fee": 40.00, "landfill": "Courtney Ridge Landfill"},
    {"city": "St. Louis", "state": "MO", "state_full": "Missouri", "pop": 301578, "mult": 1.02, "permit": True, "fee": 50.00, "landfill": "Milam Recycling Landfill"},
    {"city": "Springfield", "state": "MO", "state_full": "Missouri", "pop": 169176, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Springfield Noble Hill Landfill"},
    {"city": "Omaha", "state": "NE", "state_full": "Nebraska", "pop": 486051, "mult": 0.94, "permit": False, "fee": 0.00, "landfill": "Douglas County Landfill"},
    {"city": "Lincoln", "state": "NE", "state_full": "Nebraska", "pop": 291082, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "Bluestem Landfill"},
    {"city": "Minneapolis", "state": "MN", "state_full": "Minnesota", "pop": 429954, "mult": 1.15, "permit": True, "fee": 60.00, "landfill": "Pine Bend Landfill"},
    {"city": "St. Paul", "state": "MN", "state_full": "Minnesota", "pop": 311527, "mult": 1.12, "permit": True, "fee": 55.00, "landfill": "Burnsville Landfill"},
    {"city": "Milwaukee", "state": "WI", "state_full": "Wisconsin", "pop": 577222, "mult": 0.98, "permit": True, "fee": 40.00, "landfill": "Emerald Park Landfill"},
    {"city": "Madison", "state": "WI", "state_full": "Wisconsin", "pop": 269840, "mult": 1.05, "permit": True, "fee": 45.00, "landfill": "Dane County Landfill"},
    {"city": "Wichita", "state": "KS", "state_full": "Kansas", "pop": 397532, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Plumb Thicket Landfill"},
    {"city": "Overland Park", "state": "KS", "state_full": "Kansas", "pop": 197238, "mult": 1.02, "permit": False, "fee": 0.00, "landfill": "Johnson County Landfill"},
    {"city": "New Orleans", "state": "LA", "state_full": "Louisiana", "pop": 383997, "mult": 0.98, "permit": True, "fee": 50.00, "landfill": "River Birch Landfill"},
    {"city": "Baton Rouge", "state": "LA", "state_full": "Louisiana", "pop": 227470, "mult": 0.92, "permit": False, "fee": 0.00, "landfill": "East Baton Rouge Landfill"},
    {"city": "Shreveport", "state": "LA", "state_full": "Louisiana", "pop": 187593, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Woolworth Road Landfill"},
    {"city": "Louisville", "state": "KY", "state_full": "Kentucky", "pop": 633045, "mult": 0.92, "permit": False, "fee": 0.00, "landfill": "Outer Loop Landfill"},
    {"city": "Lexington", "state": "KY", "state_full": "Kentucky", "pop": 322570, "mult": 0.95, "permit": False, "fee": 0.00, "landfill": "Bluegrass Landfill"},
    {"city": "Oklahoma City", "state": "OK", "state_full": "Oklahoma", "pop": 681054, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "East Oak Landfill"},
    {"city": "Tulsa", "state": "OK", "state_full": "Oklahoma", "pop": 413066, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Tulsa Fuel & Fiber"},
    {"city": "Des Moines", "state": "IA", "state_full": "Iowa", "pop": 214133, "mult": 0.92, "permit": False, "fee": 0.00, "landfill": "Metro Park East Landfill"},
    {"city": "Cedar Rapids", "state": "IA", "state_full": "Iowa", "pop": 137710, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Cedar Rapids Landfill"},
    {"city": "Richmond", "state": "VA", "state_full": "Virginia", "pop": 226610, "mult": 1.05, "permit": True, "fee": 45.00, "landfill": "Old Dominion Landfill"},
    {"city": "Virginia Beach", "state": "VA", "state_full": "Virginia", "pop": 459470, "mult": 1.04, "permit": False, "fee": 0.00, "landfill": "First Piedmont Landfill"},
    {"city": "Norfolk", "state": "VA", "state_full": "Virginia", "pop": 238005, "mult": 1.02, "permit": True, "fee": 40.00, "landfill": "SPSA Landfill"},
    {"city": "Chesapeake", "state": "VA", "state_full": "Virginia", "pop": 249270, "mult": 1.02, "permit": False, "fee": 0.00, "landfill": "Chesapeake Waste Station"},
    {"city": "Birmingham", "state": "AL", "state_full": "Alabama", "pop": 200733, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "Star Ridge Landfill"},
    {"city": "Mobile", "state": "AL", "state_full": "Alabama", "pop": 187041, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Chastang Landfill"},
    {"city": "Montgomery", "state": "AL", "state_full": "Alabama", "pop": 200602, "mult": 0.86, "permit": False, "fee": 0.00, "landfill": "Montgomery Clean Water Landfill"},
    {"city": "Little Rock", "state": "AR", "state_full": "Arkansas", "pop": 202590, "mult": 0.88, "permit": False, "fee": 0.00, "landfill": "Little Rock Landfill"},
    {"city": "Jackson", "state": "MS", "state_full": "Mississippi", "pop": 153701, "mult": 0.84, "permit": False, "fee": 0.00, "landfill": "Little Dixie Landfill"},
    {"city": "Boise", "state": "ID", "state_full": "Idaho", "pop": 235684, "mult": 1.00, "permit": False, "fee": 0.00, "landfill": "Ada County Landfill"},
    {"city": "Anchorage", "state": "AK", "state_full": "Alaska", "pop": 291247, "mult": 1.30, "permit": False, "fee": 0.00, "landfill": "Anchorage Regional Landfill"},
    {"city": "Honolulu", "state": "HI", "state_full": "Hawaii", "pop": 350964, "mult": 1.48, "permit": True, "fee": 95.00, "landfill": "Waimanalo Gulch Landfill"},
    {"city": "Fargo", "state": "ND", "state_full": "North Dakota", "pop": 125990, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "Fargo Landfill"},
    {"city": "Sioux Falls", "state": "SD", "state_full": "South Dakota", "pop": 192517, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "Sioux Falls Landfill"},
    {"city": "Billings", "state": "MT", "state_full": "Montana", "pop": 117116, "mult": 0.94, "permit": False, "fee": 0.00, "landfill": "Billings Landfill"},
    {"city": "Cheyenne", "state": "WY", "state_full": "Wyoming", "pop": 65132, "mult": 0.96, "permit": False, "fee": 0.00, "landfill": "Cheyenne Landfill"},
    {"city": "Charleston", "state": "WV", "state_full": "West Virginia", "pop": 48864, "mult": 0.90, "permit": False, "fee": 0.00, "landfill": "Charleston Landfill"},
    {"city": "Wilmington", "state": "DE", "state_full": "Delaware", "pop": 70898, "mult": 1.10, "permit": True, "fee": 45.00, "landfill": "Cherry Island Landfill"},
    {"city": "Providence", "state": "RI", "state_full": "Rhode Island", "pop": 190934, "mult": 1.20, "permit": True, "fee": 60.00, "landfill": "Rhode Island Resource Recovery"},
    {"city": "New Haven", "state": "CT", "state_full": "Connecticut", "pop": 134023, "mult": 1.22, "permit": True, "fee": 70.00, "landfill": "New Haven Transfer Station"},
    {"city": "Bridgeport", "state": "CT", "state_full": "Connecticut", "pop": 148654, "mult": 1.22, "permit": True, "fee": 65.00, "landfill": "Bridgeport Landfill"},
    {"city": "Hartford", "state": "CT", "state_full": "Connecticut", "pop": 121054, "mult": 1.20, "permit": True, "fee": 75.00, "landfill": "Hartford Waste Station"},
    {"city": "Manchester", "state": "NH", "state_full": "New Hampshire", "pop": 115644, "mult": 1.12, "permit": False, "fee": 0.00, "landfill": "Manchester Landfill"},
    {"city": "Portland", "state": "ME", "state_full": "Maine", "pop": 68408, "mult": 1.10, "permit": False, "fee": 0.00, "landfill": "ecomaine Landfill"},
    {"city": "Burlington", "state": "VT", "state_full": "Vermont", "pop": 44743, "mult": 1.12, "permit": False, "fee": 0.00, "landfill": "CSWD Landfill"},
]

# Standard baseline metrics for dumpster sizes
DUMPSTER_SIZES = [
    {"size": "10-Yard", "base_price": 320.00, "tons": 2.0, "overage": 65.00, "desc": "Perfect for cleanouts of single rooms, minor landscaping, or small bathroom remodeling projects."},
    {"size": "20-Yard", "base_price": 430.00, "tons": 3.0, "overage": 70.00, "desc": "Ideal for medium-size remodeling, carpet removal, deck demolition, or whole-house cleanouts."},
    {"size": "30-Yard", "base_price": 540.00, "tons": 4.0, "overage": 75.00, "desc": "Designed for major residential renovations, construction additions, or commercial cleanouts."},
    {"size": "40-Yard", "base_price": 650.00, "tons": 5.0, "overage": 80.00, "desc": "Great for large-scale demolition, commercial roof replacements, or major construction projects."},
]

def main():
    print("Initializing SQLite Database Seeder...")
    
    # Ensure directory exists
    os.makedirs("data", exist_ok=True)
    db_path = os.path.join("data", "dumpsters.db")
    
    # If db exists, remove it for clean rebuild
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
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
        phone TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE pricing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER,
        size TEXT NOT NULL,
        base_price REAL,
        included_tonnage REAL,
        overage_fee_per_ton REAL,
        description TEXT,
        FOREIGN KEY (location_id) REFERENCES locations (id)
    )
    """)
    
    # Seed data
    print(f"Seeding {len(CITIES_DATA)} cities...")
    for idx, c in enumerate(CITIES_DATA):
        # Generate clean phone pattern based on location index
        # Programmatic simulated toll-free number or unique regional number
        phone = f"800-508-{4000 + idx}"
        
        cursor.execute("""
        INSERT INTO locations (city, state, state_full, population, permit_required, permit_cost, landfill_name, base_multiplier, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["city"],
            c["state"],
            c["state_full"],
            c["pop"],
            1 if c["permit"] else 0,
            c["fee"],
            c["landfill"],
            c["mult"],
            phone
        ))
        
        location_id = cursor.lastrowid
        
        # Seed sizes and localized pricing
        for s in DUMPSTER_SIZES:
            # Localize base price with multiplier and slight random perturbation (+$5-$15 increments) to look authentic
            local_base = round((s["base_price"] * c["mult"]) / 5.0) * 5.0
            # Add small random variation
            local_base += random.choice([0, 5, 10, 15, -5])
            
            # Localize overage
            local_overage = round((s["overage"] * c["mult"]) / 5.0) * 5.0
            
            cursor.execute("""
            INSERT INTO pricing (location_id, size, base_price, included_tonnage, overage_fee_per_ton, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                location_id,
                s["size"],
                local_base,
                s["tons"],
                local_overage,
                s["desc"]
            ))
            
    conn.commit()
    
    # Confirm seeding
    cursor.execute("SELECT COUNT(*) FROM locations")
    city_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pricing")
    pricing_count = cursor.fetchone()[0]
    
    conn.close()
    print(f"Database successfully generated at {db_path}!")
    print(f"Seeded {city_count} locations with {pricing_count} dynamic pricing matrices.")

if __name__ == "__main__":
    main()
