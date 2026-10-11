"""
CIVIX AI - Admin & Operations Portal Data Model & Seed Setup (Phase 2)
Creates:
1. Native custom tables in ServiceNow (sys_db_object):
   - u_x_civic_ai_citizen
   - u_x_civic_ai_zone
   - u_x_civic_ai_asset
   - u_x_civic_ai_category
   - u_x_civic_ai_issue_type
   - u_x_civic_ai_sensor
   - u_x_civic_ai_observation
   - u_x_civic_ai_alert
   - u_x_civic_ai_crew
   - u_x_civic_ai_audit
   - u_x_civic_ai_notification
   - u_x_civic_ai_config
2. Columns for all tables via sys_dictionary
3. Seeds realistic, deterministic Greater Chennai Corporation municipal operational records
"""

import os
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

def api_get(table: str, query: str = "", limit: int = 50):
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
        print(f"    [COL] {table_name}.{element}")
    else:
        print(f"    [COL FAIL] {table_name}.{element}: {r.status_code}")

print("=== 1. CREATING NATIVE CIVIX TABLES ===")
tables_to_create = [
    ("u_x_civic_ai_citizen", "CIVIX Citizen Profile"),
    ("u_x_civic_ai_zone", "CIVIX Municipal Zone"),
    ("u_x_civic_ai_asset", "CIVIX Civic Infrastructure Asset"),
    ("u_x_civic_ai_category", "CIVIX Service Category"),
    ("u_x_civic_ai_issue_type", "CIVIX Issue Type"),
    ("u_x_civic_ai_sensor", "CIVIX IoT Sensor"),
    ("u_x_civic_ai_observation", "CIVIX Sensor Observation"),
    ("u_x_civic_ai_alert", "CIVIX IoT Alert"),
    ("u_x_civic_ai_crew", "CIVIX Field Crew Squad"),
    ("u_x_civic_ai_audit", "CIVIX Operational Audit Log"),
    ("u_x_civic_ai_notification", "CIVIX Admin Notification"),
    ("u_x_civic_ai_config", "CIVIX Application Configuration")
]

for tbl_name, tbl_lbl in tables_to_create:
    ensure_table(tbl_name, tbl_lbl)

print("\n=== 2. CREATING TABLE COLUMNS ===")

# 1. Citizen columns
for el, lbl in [
    ("u_citizen_id", "Citizen Identifier"),
    ("u_name", "Full Name"),
    ("u_phone", "Phone Number"),
    ("u_email", "Email Address"),
    ("u_ward", "Registered Ward"),
    ("u_zone", "Municipal Zone"),
    ("u_language", "Preferred Language"),
    ("u_status", "Account Status"),
    ("u_registered_date", "Registration Date"),
    ("u_case_count", "Associated Cases Count")
]:
    ensure_column("u_x_civic_ai_citizen", el, lbl)

# 2. Zone columns
for el, lbl in [
    ("u_zone_code", "Zone Code"),
    ("u_zone_name", "Zone Name"),
    ("u_description", "Description"),
    ("u_executive_engineer", "Executive Engineer"),
    ("u_wards_count", "Wards Count"),
    ("u_status", "Operational Status"),
    ("u_contact_phone", "Helpline Hotline")
]:
    ensure_column("u_x_civic_ai_zone", el, lbl)

# 3. Ward columns (table u_x_civic_ai_ward)
for el, lbl in [
    ("u_ward_code", "Ward Code"),
    ("u_ward_name", "Ward Locality Name"),
    ("u_zone", "Linked Zone"),
    ("u_assistant_engineer", "Assistant Engineer"),
    ("u_description", "Description"),
    ("u_assets_count", "Civic Assets Count"),
    ("u_sensors_count", "Sensors Count"),
    ("u_status", "Active Status")
]:
    ensure_column("u_x_civic_ai_ward", el, lbl)

# 4. Asset columns
for el, lbl in [
    ("u_asset_id", "Asset ID"),
    ("u_asset_name", "Asset Name"),
    ("u_asset_type", "Asset Type"),
    ("u_zone", "Zone"),
    ("u_ward", "Ward"),
    ("u_location", "Location Address"),
    ("u_status", "Operational Status"),
    ("u_linked_sensor", "Linked Sensor ID")
]:
    ensure_column("u_x_civic_ai_asset", el, lbl)

# 5. Service Category columns
for el, lbl in [
    ("u_code", "Category Code"),
    ("u_name", "Category Name"),
    ("u_department", "Responsible Department"),
    ("u_default_sla_hours", "Default SLA Hours"),
    ("u_status", "Active Status")
]:
    ensure_column("u_x_civic_ai_category", el, lbl)

# 6. Issue Type columns
for el, lbl in [
    ("u_code", "Issue Type Code"),
    ("u_name", "Issue Type Name"),
    ("u_category", "Category Name"),
    ("u_default_priority", "Default Priority"),
    ("u_hazard_flag", "Safety Hazard Flag")
]:
    ensure_column("u_x_civic_ai_issue_type", el, lbl)

# 7. IoT Sensor columns
for el, lbl in [
    ("u_sensor_id", "Sensor Identifier"),
    ("u_sensor_type", "Sensor Measurement Type"),
    ("u_asset_id", "Linked Civic Asset"),
    ("u_zone", "Zone"),
    ("u_ward", "Ward"),
    ("u_location", "Physical Location"),
    ("u_connectivity", "Connectivity Status"),
    ("u_last_seen", "Last Seen Timestamp"),
    ("u_battery_pct", "Battery Percentage"),
    ("u_current_value", "Current Reading"),
    ("u_unit", "Measurement Unit"),
    ("u_threshold_limit", "Alert Threshold Limit"),
    ("u_health_status", "Health Status")
]:
    ensure_column("u_x_civic_ai_sensor", el, lbl)

# 8. IoT Observation columns
for el, lbl in [
    ("u_sensor_id", "Sensor ID"),
    ("u_timestamp", "Observation Timestamp"),
    ("u_metric", "Metric Type"),
    ("u_value", "Observed Value"),
    ("u_unit", "Unit"),
    ("u_violation", "Threshold Violation Flag")
]:
    ensure_column("u_x_civic_ai_observation", el, lbl)

# 9. IoT Alert columns
for el, lbl in [
    ("u_alert_id", "Alert Reference"),
    ("u_sensor_id", "Source Sensor"),
    ("u_alert_type", "Alert Type"),
    ("u_severity", "Severity Level"),
    ("u_asset_id", "Asset"),
    ("u_ward", "Ward"),
    ("u_first_seen", "First Triggered Timestamp"),
    ("u_current_value", "Trigger Value"),
    ("u_threshold_limit", "Configured Threshold"),
    ("u_state", "Alert State"),
    ("u_acknowledged_by", "Acknowledged By Officer"),
    ("u_linked_case", "Linked Civic Case"),
    ("u_notes", "Investigation Remarks")
]:
    ensure_column("u_x_civic_ai_alert", el, lbl)

# 10. Field Crew columns
for el, lbl in [
    ("u_crew_id", "Crew ID"),
    ("u_crew_name", "Crew Squad Name"),
    ("u_leader", "Squad Leader Name"),
    ("u_headcount", "Team Headcount"),
    ("u_skills", "Skill Specializations"),
    ("u_zone", "Assigned Zone"),
    ("u_availability", "Availability Status"),
    ("u_active_jobs", "Active Jobs Count"),
    ("u_max_capacity", "Maximum Workload Capacity")
]:
    ensure_column("u_x_civic_ai_crew", el, lbl)

# 11. Operational Audit Log columns
for el, lbl in [
    ("u_timestamp", "Event Timestamp"),
    ("u_actor", "Acting User"),
    ("u_action", "Action Performed"),
    ("u_record_ref", "Record Reference"),
    ("u_module", "Target Module"),
    ("u_old_value", "Previous State"),
    ("u_new_value", "New State"),
    ("u_reason", "Audit Remarks / Reason")
]:
    ensure_column("u_x_civic_ai_audit", el, lbl)

# 12. Admin Notification columns
for el, lbl in [
    ("u_title", "Notification Title"),
    ("u_message", "Notification Message"),
    ("u_type", "Event Type"),
    ("u_target_module", "Target Module"),
    ("u_record_ref", "Related Record"),
    ("u_timestamp", "Timestamp"),
    ("u_is_read", "Read Status")
]:
    ensure_column("u_x_civic_ai_notification", el, lbl)

# 13. Application Config columns
for el, lbl in [
    ("u_key", "Config Key"),
    ("u_value", "Config Value"),
    ("u_category", "Category"),
    ("u_description", "Description")
]:
    ensure_column("u_x_civic_ai_config", el, lbl)

print("\n=== 3. SEEDING DETERMINISTIC MUNICIPAL DATA ===")

def seed_table(table, records, key_field):
    existing = api_get(table, limit=50)
    existing_keys = {r.get(key_field) for r in existing if r.get(key_field)}
    created = 0
    for rec in records:
        key_val = rec.get(key_field)
        if key_val and key_val in existing_keys:
            continue
        res = api_post(table, rec)
        if res:
            created += 1
    print(f"  [{table}] Seeded {created} records (Total existing: {len(existing) + created})")

# 1. ZONES (Greater Chennai Corporation 5 Major Divisions)
zones_data = [
    {
        "u_zone_code": "Z13",
        "u_zone_name": "Zone 13 - Adyar",
        "u_description": "South Chennai coastal & IT corridor zone including Adyar, Besant Nagar, and Thiruvanmiyur",
        "u_executive_engineer": "Er. K. Balasubramanian, M.E.",
        "u_wards_count": "14",
        "u_status": "Active",
        "u_contact_phone": "044-24422201"
    },
    {
        "u_zone_code": "Z09",
        "u_zone_name": "Zone 9 - T. Nagar",
        "u_description": "Central commercial business hub including T. Nagar, Pondy Bazaar, and Thousand Lights",
        "u_executive_engineer": "Er. R. Srinivasan, B.E.",
        "u_wards_count": "16",
        "u_status": "Active",
        "u_contact_phone": "044-28341902"
    },
    {
        "u_zone_code": "Z05",
        "u_zone_name": "Zone 5 - Royapuram",
        "u_description": "North Chennai dense historic commercial & port zone including George Town and Royapuram Beach",
        "u_executive_engineer": "Er. M. Abdul Rahman, M.E.",
        "u_wards_count": "15",
        "u_status": "Active",
        "u_contact_phone": "044-25951230"
    },
    {
        "u_zone_code": "Z08",
        "u_zone_name": "Zone 8 - Anna Nagar",
        "u_description": "West-Central residential and major commercial sector with wide arterial avenues",
        "u_executive_engineer": "Er. S. Gayathri Devi, B.E.",
        "u_wards_count": "15",
        "u_status": "Active",
        "u_contact_phone": "044-26213456"
    },
    {
        "u_zone_code": "Z10",
        "u_zone_name": "Zone 10 - Kodambakkam",
        "u_description": "Central sector connecting Vadapalani, West Mambalam, and Ashok Nagar",
        "u_executive_engineer": "Er. P. Venkatesan, M.Tech.",
        "u_wards_count": "16",
        "u_status": "Active",
        "u_contact_phone": "044-24835678"
    }
]
seed_table("u_x_civic_ai_zone", zones_data, "u_zone_code")

# 2. WARDS
wards_data = [
    {
        "u_ward_code": "W172",
        "u_ward_name": "Ward 172 - Adyar Bus Depot",
        "u_zone": "Zone 13 - Adyar",
        "u_assistant_engineer": "Er. V. Murugan (94440-12345)",
        "u_description": "Arterial junction covering LB Road, Depot signal, and Lattice Bridge approaches",
        "u_assets_count": "48",
        "u_sensors_count": "6",
        "u_status": "Active"
    },
    {
        "u_ward_code": "W179",
        "u_ward_name": "Ward 179 - Thiruvanmiyur",
        "u_zone": "Zone 13 - Adyar",
        "u_assistant_engineer": "Er. S. Jayaraman (94440-71720)",
        "u_description": "Coastal and IT hub encompassing Thiruvanmiyur MRTS subway and East Coast Road intake",
        "u_assets_count": "54",
        "u_sensors_count": "5",
        "u_status": "Active"
    },
    {
        "u_ward_code": "W180",
        "u_ward_name": "Ward 180 - Besant Nagar",
        "u_zone": "Zone 13 - Adyar",
        "u_assistant_engineer": "Er. G. Radhakrishnan (94440-88214)",
        "u_description": "Residential beach enclave with Elliott's Beach and historic Kalakshetra zone",
        "u_assets_count": "42",
        "u_sensors_count": "4",
        "u_status": "Active"
    },
    {
        "u_ward_code": "W114",
        "u_ward_name": "Ward 114 - T. Nagar Central",
        "u_zone": "Zone 9 - T. Nagar",
        "u_assistant_engineer": "Er. N. Senthil Kumar (94440-55412)",
        "u_description": "High-footfall commercial shopping precinct centered around Panagal Park",
        "u_assets_count": "62",
        "u_sensors_count": "7",
        "u_status": "Active"
    },
    {
        "u_ward_code": "W117",
        "u_ward_name": "Ward 117 - Pondy Bazaar",
        "u_zone": "Zone 9 - T. Nagar",
        "u_assistant_engineer": "Er. D. Vijayan (94440-66987)",
        "u_description": "Pedestrian plaza corridor and stormwater canal interlink",
        "u_assets_count": "51",
        "u_sensors_count": "4",
        "u_status": "Active"
    },
    {
        "u_ward_code": "W050",
        "u_ward_name": "Ward 050 - Royapuram Beach",
        "u_zone": "Zone 5 - Royapuram",
        "u_assistant_engineer": "Er. A. Farooq (94440-33211)",
        "u_description": "Historic coastal fishing harbor and cargo transit approach",
        "u_assets_count": "38",
        "u_sensors_count": "3",
        "u_status": "Active"
    }
]
seed_table("u_x_civic_ai_ward", wards_data, "u_ward_code")

# 3. CITIZENS
citizens_data = [
    {
        "u_citizen_id": "CIT-9021",
        "u_name": "S. Rajesh Kumar",
        "u_phone": "+91 98401 23456",
        "u_email": "rajesh.kumar@gmail.com",
        "u_ward": "Ward 172 - Adyar",
        "u_zone": "Zone 13 - Adyar",
        "u_language": "English",
        "u_status": "Verified",
        "u_registered_date": "2025-08-14",
        "u_case_count": "2"
    },
    {
        "u_citizen_id": "CIT-9022",
        "u_name": "Priya Sundaram",
        "u_phone": "+91 98402 34567",
        "u_email": "priya.sundaram@outlook.com",
        "u_ward": "Ward 179 - Thiruvanmiyur",
        "u_zone": "Zone 13 - Adyar",
        "u_language": "Tamil",
        "u_status": "Verified",
        "u_registered_date": "2025-09-02",
        "u_case_count": "1"
    },
    {
        "u_citizen_id": "CIT-9023",
        "u_name": "M. Anbarasan",
        "u_phone": "+91 98403 45678",
        "u_email": "anbarasan.m@yahoo.in",
        "u_ward": "Ward 172 - Adyar",
        "u_zone": "Zone 13 - Adyar",
        "u_language": "Tamil",
        "u_status": "Verified",
        "u_registered_date": "2025-10-18",
        "u_case_count": "1"
    },
    {
        "u_citizen_id": "CIT-9024",
        "u_name": "Lakshmi Narayanan",
        "u_phone": "+91 98404 56789",
        "u_email": "lakshmi.narayanan@chennaicivic.org",
        "u_ward": "Ward 180 - Besant Nagar",
        "u_zone": "Zone 13 - Adyar",
        "u_language": "English",
        "u_status": "Verified",
        "u_registered_date": "2026-01-10",
        "u_case_count": "1"
    },
    {
        "u_citizen_id": "CIT-9025",
        "u_name": "Deepa Venkatesh",
        "u_phone": "+91 98405 67890",
        "u_email": "deepa.venkatesh@gmail.com",
        "u_ward": "Ward 114 - T. Nagar Central",
        "u_zone": "Zone 9 - T. Nagar",
        "u_language": "English",
        "u_status": "Active",
        "u_registered_date": "2026-02-20",
        "u_case_count": "0"
    }
]
seed_table("u_x_civic_ai_citizen", citizens_data, "u_citizen_id")

# 4. CIVIC ASSETS
assets_data = [
    {
        "u_asset_id": "AST-RDS-101",
        "u_asset_name": "LB Road Bitumen Arterial Stretch (Depot to Bridge)",
        "u_asset_type": "Road Infrastructure",
        "u_zone": "Zone 13 - Adyar",
        "u_ward": "Ward 172 - Adyar",
        "u_location": "LB Road near Adyar Bus Depot Signal",
        "u_status": "Active / Needs Paving",
        "u_linked_sensor": "IOT-SEN-102"
    },
    {
        "u_asset_id": "AST-DRN-204",
        "u_asset_name": "Thiruvanmiyur MRTS Railway Subway Stormwater Sump",
        "u_asset_type": "Stormwater Drainage",
        "u_zone": "Zone 13 - Adyar",
        "u_ward": "Ward 179 - Thiruvanmiyur",
        "u_location": "Thiruvanmiyur Railway Subway Approach",
        "u_status": "Alert / Desilting Active",
        "u_linked_sensor": "IOT-SEN-104"
    },
    {
        "u_asset_id": "AST-LGT-305",
        "u_asset_name": "Kasturba Nagar 3rd Cross High-Mast Sodium Lighting",
        "u_asset_type": "Street Lighting",
        "u_zone": "Zone 13 - Adyar",
        "u_ward": "Ward 172 - Adyar",
        "u_location": "3rd Cross St near Kasturba Nagar Park",
        "u_status": "Maintenance Pending",
        "u_linked_sensor": "IOT-SEN-103"
    },
    {
        "u_asset_id": "AST-WTR-412",
        "u_asset_name": "Besant Avenue Ductile Iron Water Distribution Main",
        "u_asset_type": "Water Supply Pipeline",
        "u_zone": "Zone 13 - Adyar",
        "u_ward": "Ward 180 - Besant Nagar",
        "u_location": "Besant Avenue Rd near Theosophical Society",
        "u_status": "Operational",
        "u_linked_sensor": "IOT-SEN-105"
    },
    {
        "u_asset_id": "AST-FLD-501",
        "u_asset_name": "Adyar River Estuary Sluice Gate Flood Sensor Station",
        "u_asset_type": "Flood Protection",
        "u_zone": "Zone 13 - Adyar",
        "u_ward": "Ward 172 - Adyar",
        "u_location": "Thiru Vi Ka Bridge Estuary",
        "u_status": "Operational / Online",
        "u_linked_sensor": "IOT-SEN-101"
    }
]
seed_table("u_x_civic_ai_asset", assets_data, "u_asset_id")

# 5. SERVICE CATEGORIES
categories_data = [
    {
        "u_code": "CAT-ROADS",
        "u_name": "Roads & Infrastructure",
        "u_department": "Highways & Special Roads Division",
        "u_default_sla_hours": "24",
        "u_status": "Active"
    },
    {
        "u_code": "CAT-DRAIN",
        "u_name": "Waterlogging & Floods",
        "u_department": "Stormwater Drainage Dept",
        "u_default_sla_hours": "12",
        "u_status": "Active"
    },
    {
        "u_code": "CAT-LIGHT",
        "u_name": "Street Lighting & Electrical",
        "u_department": "Electrical Engineering Wing",
        "u_default_sla_hours": "24",
        "u_status": "Active"
    },
    {
        "u_code": "CAT-WATER",
        "u_name": "Water Supply & Sewage",
        "u_department": "Chennai Metro Water (CMWSSB)",
        "u_default_sla_hours": "24",
        "u_status": "Active"
    },
    {
        "u_code": "CAT-WASTE",
        "u_name": "Solid Waste & Sanitation",
        "u_department": "GCC Solid Waste Management",
        "u_default_sla_hours": "12",
        "u_status": "Active"
    },
    {
        "u_code": "CAT-SAFETY",
        "u_name": "Public Safety & Trees",
        "u_department": "Parks & Disaster Response",
        "u_default_sla_hours": "8",
        "u_status": "Active"
    }
]
seed_table("u_x_civic_ai_category", categories_data, "u_code")

# 6. ISSUE TYPES
issue_types_data = [
    {
        "u_code": "ISS-POTHOLE",
        "u_name": "Dangerous Bitumen Pothole Crater",
        "u_category": "Roads & Infrastructure",
        "u_default_priority": "1 - Critical",
        "u_hazard_flag": "true"
    },
    {
        "u_code": "ISS-FLOOD",
        "u_name": "Subway Stormwater Pump Clogging / Inundation",
        "u_category": "Waterlogging & Floods",
        "u_default_priority": "1 - Critical",
        "u_hazard_flag": "true"
    },
    {
        "u_code": "ISS-SPARK",
        "u_name": "Non-functional Light Fixture Sparking in Wind",
        "u_category": "Street Lighting & Electrical",
        "u_default_priority": "2 - High",
        "u_hazard_flag": "true"
    },
    {
        "u_code": "ISS-SILT",
        "u_name": "Stormwater Drain Silt Blockage Overflow",
        "u_category": "Waterlogging & Floods",
        "u_default_priority": "2 - High",
        "u_hazard_flag": "false"
    },
    {
        "u_code": "ISS-LEAK",
        "u_name": "Drinking Water Pipeline Joint Leakage",
        "u_category": "Water Supply & Sewage",
        "u_default_priority": "3 - Moderate",
        "u_hazard_flag": "false"
    },
    {
        "u_code": "ISS-TREE",
        "u_name": "Fallen Banyan Tree Roadway Obstruction",
        "u_category": "Public Safety & Trees",
        "u_default_priority": "1 - Critical",
        "u_hazard_flag": "true"
    }
]
seed_table("u_x_civic_ai_issue_type", issue_types_data, "u_code")

# 7. IOT SENSORS
sensors_data = [
    {
        "u_sensor_id": "IOT-SEN-101",
        "u_sensor_type": "Ultrasonic Flood Water Level",
        "u_asset_id": "AST-FLD-501",
        "u_zone": "Zone 13 - Adyar",
        "u_ward": "Ward 172 - Adyar",
        "u_location": "Thiru Vi Ka Bridge Estuary Sensor Pylon",
        "u_connectivity": "Online",
        "u_last_seen": "2026-10-11 04:45:00",
        "u_battery_pct": "96%",
        "u_current_value": "42.8",
        "u_unit": "cm (Water Depth)",
        "u_threshold_limit": "85.0",
        "u_health_status": "Healthy"
    },
    {
        "u_sensor_id": "IOT-SEN-102",
        "u_sensor_type": "Air Quality Index (PM2.5 / PM10)",
        "u_asset_id": "AST-RDS-101",
        "u_zone": "Zone 13 - Adyar",
        "u_ward": "Ward 172 - Adyar",
        "u_location": "LB Road near Adyar Bus Depot Signal Post",
        "u_connectivity": "Online",
        "u_last_seen": "2026-10-11 04:42:00",
        "u_battery_pct": "89%",
        "u_current_value": "114",
        "u_unit": "AQI",
        "u_threshold_limit": "200",
        "u_health_status": "Healthy"
    },
    {
        "u_sensor_id": "IOT-SEN-103",
        "u_sensor_type": "Streetlight Current Transformer CT",
        "u_asset_id": "AST-LGT-305",
        "u_zone": "Zone 13 - Adyar",
        "u_ward": "Ward 172 - Adyar",
        "u_location": "Kasturba 3rd Cross Junction Feeder Pillar",
        "u_connectivity": "Warning",
        "u_last_seen": "2026-10-11 04:30:00",
        "u_battery_pct": "74%",
        "u_current_value": "48.2",
        "u_unit": "Amperes (Phase Surge)",
        "u_threshold_limit": "40.0",
        "u_health_status": "Warning (Surge Detected)"
    },
    {
        "u_sensor_id": "IOT-SEN-104",
        "u_sensor_type": "Subway Sump Silt Level Radar",
        "u_asset_id": "AST-DRN-204",
        "u_zone": "Zone 13 - Adyar",
        "u_ward": "Ward 179 - Thiruvanmiyur",
        "u_location": "Thiruvanmiyur MRTS Subway Drainage Sump",
        "u_connectivity": "Alert",
        "u_last_seen": "2026-10-11 04:38:00",
        "u_battery_pct": "82%",
        "u_current_value": "84.5",
        "u_unit": "% Silt Volume Capacity",
        "u_threshold_limit": "75.0",
        "u_health_status": "Critical Threshold Breach"
    },
    {
        "u_sensor_id": "IOT-SEN-105",
        "u_sensor_type": "Acoustic Pipe Leak Transducer",
        "u_asset_id": "AST-WTR-412",
        "u_zone": "Zone 13 - Adyar",
        "u_ward": "Ward 180 - Besant Nagar",
        "u_location": "Besant Avenue Main Sump Manhole 14",
        "u_connectivity": "Online",
        "u_last_seen": "2026-10-11 04:40:00",
        "u_battery_pct": "91%",
        "u_current_value": "18.4",
        "u_unit": "dB (Acoustic Vibration)",
        "u_threshold_limit": "45.0",
        "u_health_status": "Healthy"
    }
]
seed_table("u_x_civic_ai_sensor", sensors_data, "u_sensor_id")

# 8. IOT ALERTS
alerts_data = [
    {
        "u_alert_id": "ALR-2026-0041",
        "u_sensor_id": "IOT-SEN-104",
        "u_alert_type": "Stormwater Sump Silt Critical Threshold Breach",
        "u_severity": "1 - Critical",
        "u_asset_id": "AST-DRN-204",
        "u_ward": "Ward 179 - Thiruvanmiyur",
        "u_first_seen": "2026-10-10 18:30:00",
        "u_current_value": "84.5%",
        "u_threshold_limit": "75.0%",
        "u_state": "Active / Unacknowledged",
        "u_acknowledged_by": "",
        "u_linked_case": "CIV-2026-00860",
        "u_notes": "Sump volume reached 84.5% due to plastic silt debris. Risk of railway subway flooding during high tide."
    },
    {
        "u_alert_id": "ALR-2026-0042",
        "u_sensor_id": "IOT-SEN-103",
        "u_alert_type": "Streetlight Feeder Phase Overcurrent Surge",
        "u_severity": "2 - High",
        "u_asset_id": "AST-LGT-305",
        "u_ward": "Ward 172 - Adyar",
        "u_first_seen": "2026-10-10 20:15:00",
        "u_current_value": "48.2 A",
        "u_threshold_limit": "40.0 A",
        "u_state": "Acknowledged",
        "u_acknowledged_by": "Er. V. Murugan (AE Ward 172)",
        "u_linked_case": "CIV-2026-00815",
        "u_notes": "High wind causing arcing on fixture terminal. Linemen crew dispatched with insulated cherry picker."
    }
]
seed_table("u_x_civic_ai_alert", alerts_data, "u_alert_id")

# 9. FIELD CREWS
crews_data = [
    {
        "u_crew_id": "CRW-Z13-01",
        "u_crew_name": "Zone 13 Rapid Asphalt Paving Squad",
        "u_leader": "Karthik Selvam (EMP-9021)",
        "u_headcount": "6",
        "u_skills": "Bitumen Cold Mix, Plate Compactor, Trench Cutting, Road Repair",
        "u_zone": "Zone 13 - Adyar",
        "u_availability": "On Duty / Executing",
        "u_active_jobs": "2",
        "u_max_capacity": "4"
    },
    {
        "u_crew_id": "CRW-Z13-02",
        "u_crew_name": "Operations Emergency Desilting Squad",
        "u_leader": "S. Munusamy (EMP-1044)",
        "u_headcount": "8",
        "u_skills": "Heavy Sludge Sump Vacuum, De-clogging Pumps, Drainage Flushing",
        "u_zone": "Zone 13 - Adyar",
        "u_availability": "On Duty / Available",
        "u_active_jobs": "1",
        "u_max_capacity": "3"
    },
    {
        "u_crew_id": "CRW-ELE-03",
        "u_crew_name": "South Chennai Emergency Electrical Linemen",
        "u_leader": "R. Prakash (EMP-3310)",
        "u_headcount": "4",
        "u_skills": "HT/LT Feeder Isolation, High Mast Pole Repair, Sodium/LED Replacement",
        "u_zone": "Zone 13 - Adyar",
        "u_availability": "On Call / Standby",
        "u_active_jobs": "1",
        "u_max_capacity": "3"
    },
    {
        "u_crew_id": "CRW-Z09-01",
        "u_crew_name": "Zone 9 Central Commercial Maintenance Crew",
        "u_leader": "V. Dhanasekaran (EMP-5012)",
        "u_headcount": "5",
        "u_skills": "Paver Block Masonry, Footpath Bollard Repair, Pedestrian Plaza",
        "u_zone": "Zone 9 - T. Nagar",
        "u_availability": "Available",
        "u_active_jobs": "0",
        "u_max_capacity": "4"
    }
]
seed_table("u_x_civic_ai_crew", crews_data, "u_crew_id")

# 10. AUDIT LOGS
audit_data = [
    {
        "u_timestamp": "2026-10-10 08:30:15",
        "u_actor": "Admin S. Ramanathan, IAS",
        "u_action": "Case Priority Escalation",
        "u_record_ref": "CIV-2026-00841",
        "u_module": "Case Management",
        "u_old_value": "P2 - High (Score 62)",
        "u_new_value": "P1 - Critical (Score 78)",
        "u_reason": "High-speed bus corridor hazard re-evaluated; deterministic safety override applied."
    },
    {
        "u_timestamp": "2026-10-10 08:32:00",
        "u_actor": "Admin S. Ramanathan, IAS",
        "u_action": "Work Order Assigned",
        "u_record_ref": "WO-2026-00101",
        "u_module": "Work Orders & Crews",
        "u_old_value": "Pending Assignment",
        "u_new_value": "Assigned to Karthik Selvam (EMP-9021)",
        "u_reason": "Deterministic crew fit matched Zone 13 Rapid Asphalt Paving Squad (Fit: 92%)."
    },
    {
        "u_timestamp": "2026-10-10 11:11:34",
        "u_actor": "Karthik Selvam (EMP-9021)",
        "u_action": "On-Site Arrival Verified",
        "u_record_ref": "WO-2026-00101",
        "u_module": "Field Execution",
        "u_old_value": "Assigned",
        "u_new_value": "Arrival Verified (Beacon OTP: 4829)",
        "u_reason": "Technician arrived physically on site at LB Road Depot Junction."
    },
    {
        "u_timestamp": "2026-10-10 18:35:00",
        "u_actor": "System IoT Sentinel",
        "u_action": "Threshold Breach Triggered",
        "u_record_ref": "IOT-SEN-104",
        "u_module": "IoT Monitoring",
        "u_old_value": "Normal (68% Silt)",
        "u_new_value": "Critical Alert (84.5% Silt)",
        "u_reason": "Automated radar threshold limit 75.0% exceeded at MRTS Subway Sump."
    },
    {
        "u_timestamp": "2026-10-10 18:40:22",
        "u_actor": "Officer K. Meenakshi",
        "u_action": "Case Created from Alert",
        "u_record_ref": "CIV-2026-00860",
        "u_module": "Case Management",
        "u_old_value": "Alert Unassigned",
        "u_new_value": "Linked to Case CIV-2026-00860",
        "u_reason": "Manual operator conversion of IoT threshold breach to municipal case."
    },
    {
        "u_timestamp": "2026-10-10 20:18:10",
        "u_actor": "Er. V. Murugan (AE Ward 172)",
        "u_action": "Alert Acknowledged",
        "u_record_ref": "ALR-2026-0042",
        "u_module": "IoT Monitoring",
        "u_old_value": "Active / Unacknowledged",
        "u_new_value": "Acknowledged",
        "u_reason": "Insulated emergency lineman crew dispatched to Kasturba Mast."
    }
]
seed_table("u_x_civic_ai_audit", audit_data, "u_record_ref")

# 11. NOTIFICATIONS
notifications_data = [
    {
        "u_title": "P1 Emergency Work Order Dispatched",
        "u_message": "WO-2026-00101 (LB Road Crater Pothole) dispatched to Karthik Selvam. Mandatory 4h response SLA active.",
        "u_type": "Emergency",
        "u_target_module": "Work Orders & Crews",
        "u_record_ref": "WO-2026-00101",
        "u_timestamp": "2026-10-10 08:32:00",
        "u_is_read": "false"
    },
    {
        "u_title": "IoT Critical Sump Breach Alert",
        "u_message": "Sensor IOT-SEN-104 exceeded 80% capacity limit at Thiruvanmiyur MRTS Subway. Desilting squad required.",
        "u_type": "IoT Alert",
        "u_target_module": "IoT Monitoring",
        "u_record_ref": "ALR-2026-0041",
        "u_timestamp": "2026-10-10 18:35:00",
        "u_is_read": "false"
    },
    {
        "u_title": "New Citizen Complaint Registered",
        "u_message": "CIV-2026-00860 submitted by Priya Sundaram in Ward 179. Awaiting administrative triage.",
        "u_type": "Ticket",
        "u_target_module": "Ticket Management",
        "u_record_ref": "CIV-2026-00860",
        "u_timestamp": "2026-10-10 18:38:00",
        "u_is_read": "false"
    },
    {
        "u_title": "Work Order Completed Awaiting Verification",
        "u_message": "WO-2026-00104 (Besant Avenue DI Pipe Joint) marked Completed by tech. Verification audit pending.",
        "u_type": "Verification",
        "u_target_module": "Work Orders & Crews",
        "u_record_ref": "WO-2026-00104",
        "u_timestamp": "2026-10-10 16:45:00",
        "u_is_read": "false"
    }
]
seed_table("u_x_civic_ai_notification", notifications_data, "u_title")

# 12. CONFIGURATION
configs_data = [
    {"u_key": "sla.target.p1.hours", "u_value": "4", "u_category": "SLA", "u_description": "P1 Critical Emergency Target SLA Resolution in Hours"},
    {"u_key": "sla.target.p2.hours", "u_value": "24", "u_category": "SLA", "u_description": "P2 High Priority Target SLA Resolution in Hours"},
    {"u_key": "sla.target.p3.hours", "u_value": "72", "u_category": "SLA", "u_description": "P3 Moderate Priority Target SLA Resolution in Hours"},
    {"u_key": "sla.target.p4.hours", "u_value": "168", "u_category": "SLA", "u_description": "P4 Low Routine Priority Target SLA Resolution in Hours"},
    {"u_key": "priority.weight.severity", "u_value": "30", "u_category": "Scoring", "u_description": "Severity Factor Weight (0-5 normalized)"},
    {"u_key": "priority.weight.people", "u_value": "25", "u_category": "Scoring", "u_description": "Affected Population Factor Weight"},
    {"u_key": "priority.weight.urgency", "u_value": "20", "u_category": "Scoring", "u_description": "Temporal Urgency Factor Weight"},
    {"u_key": "priority.weight.essential", "u_value": "15", "u_category": "Scoring", "u_description": "Essential Service Disruption Factor Weight"},
    {"u_key": "priority.weight.confidence", "u_value": "10", "u_category": "Scoring", "u_description": "Verification Confidence Weight"},
    {"u_key": "iot.flood.threshold.cm", "u_value": "85.0", "u_category": "IoT", "u_description": "Estuary & Bridge Ultrasonic Flood Alert Limit in cm"},
    {"u_key": "iot.silt.threshold.pct", "u_value": "75.0", "u_category": "IoT", "u_description": "Subway Drainage Sump Silt Alert Limit %"},
    {"u_key": "iot.current.surge.amperes", "u_value": "40.0", "u_category": "IoT", "u_description": "Streetlight Phase Feeder Current Surge Limit in Amperes"}
]
seed_table("u_x_civic_ai_config", configs_data, "u_key")

print("\n=== PHASE 2 DATA MODEL SETUP COMPLETED SUCCESSFULLY ===")
