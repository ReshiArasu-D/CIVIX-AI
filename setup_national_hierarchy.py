"""
CIVIX AI - National Geographic Hierarchy Setup & Idempotent Master Data Seed
Extends CIVIX AI with:
1. Tables:
   - u_x_civic_ai_op_zone (Operational Zones: North, South, East & Northeast, West & Central)
   - u_x_civic_ai_state (28 States + 8 Union Territories = 36 entities)
   - u_x_civic_ai_district (Administrative Districts)
   - u_x_civic_ai_local_body (Urban Local Bodies - Municipal Corp, Municipality, Town Panchayat)
2. Dictionary columns for hierarchy relationships & cascading references
3. Idempotent seeds for:
   - 4 Operational Zones
   - 36 States & UTs (28 States, 8 UTs)
   - Real District (Chennai) and Local Body (Greater Chennai Corporation)
   - Preserves & links all existing Chennai Zones, Wards, Cases, Assets, and Sensors
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

INSTANCE_URL = os.getenv("SERVICENOW_INSTANCE_URL", "https://dev187180.service-now.com").rstrip("/")
USERNAME = os.getenv("SERVICENOW_USERNAME", "admin")
PASSWORD = os.getenv("SERVICENOW_PASSWORD", "mn%XC1^ScdA4")
APP_SYS_ID = "4750065ac37b0f14e54832f1b4013184"

session = requests.Session()
session.auth = (USERNAME, PASSWORD)
session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})

def api_get(table: str, query: str = "", limit: int = 100):
    url = f"{INSTANCE_URL}/api/now/table/{table}"
    params = {"sysparm_query": query, "sysparm_limit": limit}
    resp = session.get(url, params=params, timeout=25)
    resp.raise_for_status()
    return resp.json().get("result", [])

def api_post(table: str, data: dict):
    url = f"{INSTANCE_URL}/api/now/table/{table}"
    resp = session.post(url, json=data, timeout=25)
    if resp.status_code in [200, 201]:
        return resp.json().get("result", {})
    print(f"POST {table} failed: {resp.status_code} - {resp.text[:140]}")
    return None

def api_put(table: str, sys_id: str, data: dict):
    url = f"{INSTANCE_URL}/api/now/table/{table}/{sys_id}"
    resp = session.put(url, json=data, timeout=25)
    if resp.status_code in [200, 201]:
        return resp.json().get("result", {})
    print(f"PUT {table}/{sys_id} failed: {resp.status_code} - {resp.text[:140]}")
    return None

def ensure_table(name: str, label: str):
    existing = api_get("sys_db_object", query=f"name={name}", limit=1)
    if existing:
        print(f"  [TABLE EXISTS] {name} ({label})")
        return existing[0]["sys_id"]
    payload = {
        "name": name,
        "label": label,
        "sys_scope": APP_SYS_ID,
        "is_extendable": "false"
    }
    r = session.post(f"{INSTANCE_URL}/api/now/table/sys_db_object", json=payload, timeout=25)
    if r.status_code in [200, 201]:
        print(f"  [TABLE CREATED] {name} ({label})")
        return r.json().get("result", {}).get("sys_id")
    print(f"  [TABLE FAILED] {name}: {r.status_code} {r.text[:120]}")
    return None

def ensure_column(table_name: str, element: str, label: str, internal_type: str = "string", max_length: str = "255"):
    existing = api_get("sys_dictionary", query=f"name={table_name}^element={element}", limit=1)
    if existing:
        return
    payload = {
        "name": table_name,
        "element": element,
        "column_label": label,
        "internal_type": internal_type,
        "max_length": max_length,
        "sys_scope": APP_SYS_ID
    }
    r = session.post(f"{INSTANCE_URL}/api/now/table/sys_dictionary", json=payload, timeout=25)
    if r.status_code in [200, 201]:
        print(f"    [COL CREATED] {table_name}.{element}")
    else:
        print(f"    [COL ERROR] {table_name}.{element}: {r.status_code}")

print("=== 1. ENSURING NATIONAL HIERARCHY TABLES ===")
ensure_table("u_x_civic_ai_op_zone", "CIVIX Operational Zone")
ensure_table("u_x_civic_ai_state", "CIVIX State and Union Territory")
ensure_table("u_x_civic_ai_district", "CIVIX Administrative District")
ensure_table("u_x_civic_ai_local_body", "CIVIX Urban Local Body")

print("\n=== 2. ENSURING HIERARCHY DICTIONARY COLUMNS ===")
# Operational Zone columns
ensure_column("u_x_civic_ai_op_zone", "u_zone_code", "Zone Code", "string", "40")
ensure_column("u_x_civic_ai_op_zone", "u_zone_name", "Zone Official Name", "string", "150")
ensure_column("u_x_civic_ai_op_zone", "u_short_name", "Short Name", "string", "80")
ensure_column("u_x_civic_ai_op_zone", "u_description", "Description", "string", "500")
ensure_column("u_x_civic_ai_op_zone", "u_headquarters", "Command Headquarters", "string", "100")
ensure_column("u_x_civic_ai_op_zone", "u_status", "Status", "string", "40")

# State and UT columns
ensure_column("u_x_civic_ai_state", "u_name", "State / UT Name", "string", "150")
ensure_column("u_x_civic_ai_state", "u_code", "Official Code", "string", "20")
ensure_column("u_x_civic_ai_state", "u_type", "Administrative Type", "string", "40")
ensure_column("u_x_civic_ai_state", "u_op_zone_code", "Operational Zone Code", "string", "40")
ensure_column("u_x_civic_ai_state", "u_op_zone_name", "Operational Zone Name", "string", "150")
ensure_column("u_x_civic_ai_state", "u_capital", "Capital / Admin Center", "string", "100")
ensure_column("u_x_civic_ai_state", "u_status", "Status", "string", "40")

# District columns
ensure_column("u_x_civic_ai_district", "u_name", "District Name", "string", "150")
ensure_column("u_x_civic_ai_district", "u_code", "District Code", "string", "40")
ensure_column("u_x_civic_ai_district", "u_state_name", "Parent State / UT", "string", "150")
ensure_column("u_x_civic_ai_district", "u_state_code", "State Code", "string", "20")
ensure_column("u_x_civic_ai_district", "u_op_zone", "Operational Zone", "string", "150")
ensure_column("u_x_civic_ai_district", "u_status", "Status", "string", "40")

# Urban Local Body columns
ensure_column("u_x_civic_ai_local_body", "u_name", "Local Body Name", "string", "150")
ensure_column("u_x_civic_ai_local_body", "u_code", "Local Body Code", "string", "40")
ensure_column("u_x_civic_ai_local_body", "u_type", "Local Body Type", "string", "60")
ensure_column("u_x_civic_ai_local_body", "u_district_name", "Parent District", "string", "150")
ensure_column("u_x_civic_ai_local_body", "u_state_name", "Parent State / UT", "string", "150")
ensure_column("u_x_civic_ai_local_body", "u_op_zone", "Operational Zone", "string", "150")
ensure_column("u_x_civic_ai_local_body", "u_status", "Status", "string", "40")

# Hierarchy references on existing tables
for tbl in ["u_x_civic_ai_zone", "u_x_civic_ai_ward", "u_x_civic_ai_case", "u_x_civic_ai_sensor", "u_x_civic_ai_asset"]:
    ensure_column(tbl, "u_op_zone", "Operational Zone", "string", "150")
    ensure_column(tbl, "u_state_name", "State / UT", "string", "150")
    ensure_column(tbl, "u_district_name", "District", "string", "150")
    ensure_column(tbl, "u_local_body_name", "Local Body", "string", "150")

print("\n=== 3. SEEDING 4 CONFIGURABLE OPERATIONAL ZONES (IDEMPOTENT) ===")
FOUR_ZONES = [
    {
        "u_zone_code": "OZ-01",
        "u_zone_name": "Zone 1 — North Zone",
        "u_short_name": "North Zone",
        "u_description": "Covers northern states and UTs including Jammu and Kashmir, Ladakh, Punjab, Haryana, Himachal Pradesh, Uttarakhand, Uttar Pradesh, Rajasthan, Delhi NCT, and Chandigarh.",
        "u_headquarters": "New Delhi / Chandigarh",
        "u_status": "Active"
    },
    {
        "u_zone_code": "OZ-02",
        "u_zone_name": "Zone 2 — South Zone",
        "u_short_name": "South Zone",
        "u_description": "Covers southern peninsular states and UTs including Tamil Nadu, Kerala, Karnataka, Andhra Pradesh, Telangana, Puducherry, and Lakshadweep.",
        "u_headquarters": "Chennai / Bengaluru",
        "u_status": "Active"
    },
    {
        "u_zone_code": "OZ-03",
        "u_zone_name": "Zone 3 — East & Northeast Zone",
        "u_short_name": "East & Northeast Zone",
        "u_description": "Covers eastern and northeastern states and UTs including Bihar, Jharkhand, Odisha, West Bengal, Sikkim, Assam, Arunachal Pradesh, Manipur, Meghalaya, Mizoram, Nagaland, Tripura, and Andaman & Nicobar Islands.",
        "u_headquarters": "Kolkata / Guwahati",
        "u_status": "Active"
    },
    {
        "u_zone_code": "OZ-04",
        "u_zone_name": "Zone 4 — West & Central Zone",
        "u_short_name": "West & Central Zone",
        "u_description": "Covers western and central states and UTs including Gujarat, Maharashtra, Goa, Madhya Pradesh, Chhattisgarh, and Dadra & Nagar Haveli and Daman & Diu.",
        "u_headquarters": "Mumbai / Ahmedabad",
        "u_status": "Active"
    }
]

for oz in FOUR_ZONES:
    existing = api_get("u_x_civic_ai_op_zone", query=f"u_zone_code={oz['u_zone_code']}", limit=1)
    if existing:
        api_put("u_x_civic_ai_op_zone", existing[0]["sys_id"], oz)
        print(f"  [OP ZONE UPDATED] {oz['u_zone_code']} - {oz['u_zone_name']}")
    else:
        api_post("u_x_civic_ai_op_zone", oz)
        print(f"  [OP ZONE SEEDED] {oz['u_zone_code']} - {oz['u_zone_name']}")

print("\n=== 4. SEEDING 28 STATES & 8 UNION TERRITORIES (36 ENTITIES) ===")
STATES_AND_UTS = [
    # --- ZONE 1: NORTH ZONE (6 States, 4 UTs = 10) ---
    {"u_name": "Jammu and Kashmir", "u_code": "JK", "u_type": "Union Territory", "u_op_zone_code": "OZ-01", "u_op_zone_name": "Zone 1 — North Zone", "u_capital": "Srinagar / Jammu", "u_status": "Active"},
    {"u_name": "Ladakh", "u_code": "LA", "u_type": "Union Territory", "u_op_zone_code": "OZ-01", "u_op_zone_name": "Zone 1 — North Zone", "u_capital": "Leh", "u_status": "Active"},
    {"u_name": "Himachal Pradesh", "u_code": "HP", "u_type": "State", "u_op_zone_code": "OZ-01", "u_op_zone_name": "Zone 1 — North Zone", "u_capital": "Shimla", "u_status": "Active"},
    {"u_name": "Punjab", "u_code": "PB", "u_type": "State", "u_op_zone_code": "OZ-01", "u_op_zone_name": "Zone 1 — North Zone", "u_capital": "Chandigarh", "u_status": "Active"},
    {"u_name": "Haryana", "u_code": "HR", "u_type": "State", "u_op_zone_code": "OZ-01", "u_op_zone_name": "Zone 1 — North Zone", "u_capital": "Chandigarh", "u_status": "Active"},
    {"u_name": "Uttarakhand", "u_code": "UK", "u_type": "State", "u_op_zone_code": "OZ-01", "u_op_zone_name": "Zone 1 — North Zone", "u_capital": "Dehradun", "u_status": "Active"},
    {"u_name": "Uttar Pradesh", "u_code": "UP", "u_type": "State", "u_op_zone_code": "OZ-01", "u_op_zone_name": "Zone 1 — North Zone", "u_capital": "Lucknow", "u_status": "Active"},
    {"u_name": "Rajasthan", "u_code": "RJ", "u_type": "State", "u_op_zone_code": "OZ-01", "u_op_zone_name": "Zone 1 — North Zone", "u_capital": "Jaipur", "u_status": "Active"},
    {"u_name": "National Capital Territory of Delhi", "u_code": "DL", "u_type": "Union Territory", "u_op_zone_code": "OZ-01", "u_op_zone_name": "Zone 1 — North Zone", "u_capital": "New Delhi", "u_status": "Active"},
    {"u_name": "Chandigarh", "u_code": "CH", "u_type": "Union Territory", "u_op_zone_code": "OZ-01", "u_op_zone_name": "Zone 1 — North Zone", "u_capital": "Chandigarh", "u_status": "Active"},

    # --- ZONE 2: SOUTH ZONE (5 States, 2 UTs = 7) ---
    {"u_name": "Tamil Nadu", "u_code": "TN", "u_type": "State", "u_op_zone_code": "OZ-02", "u_op_zone_name": "Zone 2 — South Zone", "u_capital": "Chennai", "u_status": "Active"},
    {"u_name": "Kerala", "u_code": "KL", "u_type": "State", "u_op_zone_code": "OZ-02", "u_op_zone_name": "Zone 2 — South Zone", "u_capital": "Thiruvananthapuram", "u_status": "Active"},
    {"u_name": "Karnataka", "u_code": "KA", "u_type": "State", "u_op_zone_code": "OZ-02", "u_op_zone_name": "Zone 2 — South Zone", "u_capital": "Bengaluru", "u_status": "Active"},
    {"u_name": "Andhra Pradesh", "u_code": "AP", "u_type": "State", "u_op_zone_code": "OZ-02", "u_op_zone_name": "Zone 2 — South Zone", "u_capital": "Amaravati", "u_status": "Active"},
    {"u_name": "Telangana", "u_code": "TG", "u_type": "State", "u_op_zone_code": "OZ-02", "u_op_zone_name": "Zone 2 — South Zone", "u_capital": "Hyderabad", "u_status": "Active"},
    {"u_name": "Puducherry", "u_code": "PY", "u_type": "Union Territory", "u_op_zone_code": "OZ-02", "u_op_zone_name": "Zone 2 — South Zone", "u_capital": "Puducherry", "u_status": "Active"},
    {"u_name": "Lakshadweep", "u_code": "LD", "u_type": "Union Territory", "u_op_zone_code": "OZ-02", "u_op_zone_name": "Zone 2 — South Zone", "u_capital": "Kavaratti", "u_status": "Active"},

    # --- ZONE 3: EAST & NORTHEAST ZONE (12 States, 1 UT = 13) ---
    {"u_name": "Bihar", "u_code": "BR", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Patna", "u_status": "Active"},
    {"u_name": "Jharkhand", "u_code": "JH", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Ranchi", "u_status": "Active"},
    {"u_name": "Odisha", "u_code": "OD", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Bhubaneswar", "u_status": "Active"},
    {"u_name": "West Bengal", "u_code": "WB", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Kolkata", "u_status": "Active"},
    {"u_name": "Sikkim", "u_code": "SK", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Gangtok", "u_status": "Active"},
    {"u_name": "Assam", "u_code": "AS", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Dispur", "u_status": "Active"},
    {"u_name": "Arunachal Pradesh", "u_code": "AR", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Itanagar", "u_status": "Active"},
    {"u_name": "Manipur", "u_code": "MN", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Imphal", "u_status": "Active"},
    {"u_name": "Meghalaya", "u_code": "ML", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Shillong", "u_status": "Active"},
    {"u_name": "Mizoram", "u_code": "MZ", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Aizawl", "u_status": "Active"},
    {"u_name": "Nagaland", "u_code": "NL", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Kohima", "u_status": "Active"},
    {"u_name": "Tripura", "u_code": "TR", "u_type": "State", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Agartala", "u_status": "Active"},
    {"u_name": "Andaman and Nicobar Islands", "u_code": "AN", "u_type": "Union Territory", "u_op_zone_code": "OZ-03", "u_op_zone_name": "Zone 3 — East & Northeast Zone", "u_capital": "Port Blair", "u_status": "Active"},

    # --- ZONE 4: WEST & CENTRAL ZONE (5 States, 1 UT = 6) ---
    {"u_name": "Gujarat", "u_code": "GJ", "u_type": "State", "u_op_zone_code": "OZ-04", "u_op_zone_name": "Zone 4 — West & Central Zone", "u_capital": "Gandhinagar", "u_status": "Active"},
    {"u_name": "Maharashtra", "u_code": "MH", "u_type": "State", "u_op_zone_code": "OZ-04", "u_op_zone_name": "Zone 4 — West & Central Zone", "u_capital": "Mumbai", "u_status": "Active"},
    {"u_name": "Goa", "u_code": "GA", "u_type": "State", "u_op_zone_code": "OZ-04", "u_op_zone_name": "Zone 4 — West & Central Zone", "u_capital": "Panaji", "u_status": "Active"},
    {"u_name": "Madhya Pradesh", "u_code": "MP", "u_type": "State", "u_op_zone_code": "OZ-04", "u_op_zone_name": "Zone 4 — West & Central Zone", "u_capital": "Bhopal", "u_status": "Active"},
    {"u_name": "Chhattisgarh", "u_code": "CG", "u_type": "State", "u_op_zone_code": "OZ-04", "u_op_zone_name": "Zone 4 — West & Central Zone", "u_capital": "Raipur", "u_status": "Active"},
    {"u_name": "Dadra and Nagar Haveli and Daman and Diu", "u_code": "DD", "u_type": "Union Territory", "u_op_zone_code": "OZ-04", "u_op_zone_name": "Zone 4 — West & Central Zone", "u_capital": "Daman", "u_status": "Active"}
]

state_count = sum(1 for x in STATES_AND_UTS if x["u_type"] == "State")
ut_count = sum(1 for x in STATES_AND_UTS if x["u_type"] == "Union Territory")
print(f"Catalogue Verification: Total={len(STATES_AND_UTS)}, States={state_count}, UTs={ut_count}")
assert len(STATES_AND_UTS) == 36, "Catalogue must contain exactly 36 entities"
assert state_count == 28, "Catalogue must contain exactly 28 states"
assert ut_count == 8, "Catalogue must contain exactly 8 union territories"

for st in STATES_AND_UTS:
    existing = api_get("u_x_civic_ai_state", query=f"u_code={st['u_code']}", limit=1)
    if existing:
        api_put("u_x_civic_ai_state", existing[0]["sys_id"], st)
        print(f"  [STATE/UT UPDATED] [{st['u_code']}] {st['u_name']} ({st['u_type']}) -> {st['u_op_zone_code']}")
    else:
        api_post("u_x_civic_ai_state", st)
        print(f"  [STATE/UT SEEDED] [{st['u_code']}] {st['u_name']} ({st['u_type']}) -> {st['u_op_zone_code']}")

print("\n=== 5. SEEDING AUTHORITATIVE DISTRICTS & LOCAL BODIES ===")
# 1. Chennai District (Tamil Nadu, South Zone)
DISTRICTS = [
    {
        "u_name": "Chennai",
        "u_code": "DIS-TN-CHE",
        "u_state_name": "Tamil Nadu",
        "u_state_code": "TN",
        "u_op_zone": "Zone 2 — South Zone",
        "u_status": "Active"
    },
    {
        "u_name": "Coimbatore",
        "u_code": "DIS-TN-CBE",
        "u_state_name": "Tamil Nadu",
        "u_state_code": "TN",
        "u_op_zone": "Zone 2 — South Zone",
        "u_status": "Active"
    },
    {
        "u_name": "Bengaluru Urban",
        "u_code": "DIS-KA-BLR",
        "u_state_name": "Karnataka",
        "u_state_code": "KA",
        "u_op_zone": "Zone 2 — South Zone",
        "u_status": "Active"
    },
    {
        "u_name": "New Delhi",
        "u_code": "DIS-DL-NDL",
        "u_state_name": "National Capital Territory of Delhi",
        "u_state_code": "DL",
        "u_op_zone": "Zone 1 — North Zone",
        "u_status": "Active"
    },
    {
        "u_name": "Mumbai Suburban",
        "u_code": "DIS-MH-MUM",
        "u_state_name": "Maharashtra",
        "u_state_code": "MH",
        "u_op_zone": "Zone 4 — West & Central Zone",
        "u_status": "Active"
    },
    {
        "u_name": "Kolkata",
        "u_code": "DIS-WB-KOL",
        "u_state_name": "West Bengal",
        "u_state_code": "WB",
        "u_op_zone": "Zone 3 — East & Northeast Zone",
        "u_status": "Active"
    }
]

for d in DISTRICTS:
    existing = api_get("u_x_civic_ai_district", query=f"u_code={d['u_code']}", limit=1)
    if existing:
        api_put("u_x_civic_ai_district", existing[0]["sys_id"], d)
        print(f"  [DISTRICT UPDATED] {d['u_name']} ({d['u_state_name']})")
    else:
        api_post("u_x_civic_ai_district", d)
        print(f"  [DISTRICT SEEDED] {d['u_name']} ({d['u_state_name']})")

LOCAL_BODIES = [
    {
        "u_name": "Greater Chennai Corporation",
        "u_code": "ULB-GCC-01",
        "u_type": "Municipal Corporation",
        "u_district_name": "Chennai",
        "u_state_name": "Tamil Nadu",
        "u_op_zone": "Zone 2 — South Zone",
        "u_status": "Active"
    },
    {
        "u_name": "Bruhat Bengaluru Mahanagara Palike",
        "u_code": "ULB-BBMP-01",
        "u_type": "Municipal Corporation",
        "u_district_name": "Bengaluru Urban",
        "u_state_name": "Karnataka",
        "u_op_zone": "Zone 2 — South Zone",
        "u_status": "Active"
    },
    {
        "u_name": "Municipal Corporation of Delhi",
        "u_code": "ULB-MCD-01",
        "u_type": "Municipal Corporation",
        "u_district_name": "New Delhi",
        "u_state_name": "National Capital Territory of Delhi",
        "u_op_zone": "Zone 1 — North Zone",
        "u_status": "Active"
    },
    {
        "u_name": "Brihanmumbai Municipal Corporation",
        "u_code": "ULB-BMC-01",
        "u_type": "Municipal Corporation",
        "u_district_name": "Mumbai Suburban",
        "u_state_name": "Maharashtra",
        "u_op_zone": "Zone 4 — West & Central Zone",
        "u_status": "Active"
    },
    {
        "u_name": "Kolkata Municipal Corporation",
        "u_code": "ULB-KMC-01",
        "u_type": "Municipal Corporation",
        "u_district_name": "Kolkata",
        "u_state_name": "West Bengal",
        "u_op_zone": "Zone 3 — East & Northeast Zone",
        "u_status": "Active"
    }
]

for lb in LOCAL_BODIES:
    existing = api_get("u_x_civic_ai_local_body", query=f"u_code={lb['u_code']}", limit=1)
    if existing:
        api_put("u_x_civic_ai_local_body", existing[0]["sys_id"], lb)
        print(f"  [LOCAL BODY UPDATED] {lb['u_name']} ({lb['u_type']})")
    else:
        api_post("u_x_civic_ai_local_body", lb)
        print(f"  [LOCAL BODY SEEDED] {lb['u_name']} ({lb['u_type']})")

print("\n=== 6. PRESERVING & LINKING EXISTING CHENNAI RECORDS TO HIERARCHY ===")
# Link existing Municipal Zones to Greater Chennai Corporation, Chennai, Tamil Nadu, Zone 2 — South Zone
m_zones = api_get("u_x_civic_ai_zone", limit=50)
for mz in m_zones:
    sid = mz["sys_id"]
    api_put("u_x_civic_ai_zone", sid, {
        "u_op_zone": "Zone 2 — South Zone",
        "u_state_name": "Tamil Nadu",
        "u_district_name": "Chennai",
        "u_local_body_name": "Greater Chennai Corporation"
    })
print(f"  [MUNICIPAL ZONES LINKED] {len(m_zones)} zones connected to South Zone / Tamil Nadu / Chennai")

# Link existing Wards
m_wards = api_get("u_x_civic_ai_ward", limit=50)
for mw in m_wards:
    sid = mw["sys_id"]
    api_put("u_x_civic_ai_ward", sid, {
        "u_op_zone": "Zone 2 — South Zone",
        "u_state_name": "Tamil Nadu",
        "u_district_name": "Chennai",
        "u_local_body_name": "Greater Chennai Corporation",
        "u_municipal_zone": mw.get("u_zone", "")
    })
print(f"  [WARDS LINKED] {len(m_wards)} wards connected to South Zone / Tamil Nadu / Chennai")

# Link existing Cases
m_cases = api_get("u_x_civic_ai_case", limit=100)
for mc in m_cases:
    sid = mc["sys_id"]
    api_put("u_x_civic_ai_case", sid, {
        "u_op_zone": "Zone 2 — South Zone",
        "u_state_name": "Tamil Nadu",
        "u_district_name": "Chennai",
        "u_local_body_name": "Greater Chennai Corporation"
    })
print(f"  [CASES LINKED] {len(m_cases)} cases connected to South Zone / Tamil Nadu / Chennai")

# Link existing Sensors & Assets
m_sensors = api_get("u_x_civic_ai_sensor", limit=50)
for ms in m_sensors:
    sid = ms["sys_id"]
    api_put("u_x_civic_ai_sensor", sid, {
        "u_op_zone": "Zone 2 — South Zone",
        "u_state_name": "Tamil Nadu",
        "u_district_name": "Chennai",
        "u_local_body_name": "Greater Chennai Corporation"
    })

m_assets = api_get("u_x_civic_ai_asset", limit=50)
for ma in m_assets:
    sid = ma["sys_id"]
    api_put("u_x_civic_ai_asset", sid, {
        "u_op_zone": "Zone 2 — South Zone",
        "u_state_name": "Tamil Nadu",
        "u_district_name": "Chennai",
        "u_local_body_name": "Greater Chennai Corporation"
    })
print(f"  [SENSORS & ASSETS LINKED] {len(m_sensors)} sensors & {len(m_assets)} assets connected to hierarchy")

print("\n=== 7. FINAL VALIDATION CHECKS ===")
all_op_zones = api_get("u_x_civic_ai_op_zone", limit=10)
print(f"Total Operational Zones in DB: {len(all_op_zones)}")
for oz in all_op_zones:
    print(f"  - {oz.get('u_zone_code')}: {oz.get('u_zone_name')}")

all_states = api_get("u_x_civic_ai_state", limit=100)
db_states = [s for s in all_states if s.get("u_type") == "State"]
db_uts = [s for s in all_states if s.get("u_type") == "Union Territory"]
print(f"Total States & UTs in DB: {len(all_states)} (States: {len(db_states)}, UTs: {len(db_uts)})")

for z_code in ["OZ-01", "OZ-02", "OZ-03", "OZ-04"]:
    count = sum(1 for s in all_states if s.get("u_op_zone_code") == z_code)
    print(f"  Operational Zone {z_code}: {count} States & UTs assigned")

print("\n=== SETUP COMPLETE ===")
