"""
CIVIX AI - Field Worker Portal Data Model & Seed Setup
1. Registers all necessary dictionary columns for u_x_civic_ai_work_order and u_x_civic_ai_evidence
2. Seeds realistic Greater Chennai Corporation work orders across diverse states, priorities, and wards
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
session.headers.update({
    "Accept": "application/json",
    "Content-Type": "application/json"
})

def api_get(table: str, query: str = "", limit: int = 50):
    url = f"{INSTANCE_URL}/api/now/table/{table}"
    params = {"sysparm_query": query, "sysparm_limit": limit}
    resp = session.get(url, params=params, timeout=25)
    resp.raise_for_status()
    return resp.json().get("result", [])

def ensure_column(table_name: str, element: str, label: str, internal_type: str = "string", max_length: str = "255"):
    existing = api_get("sys_dictionary", query=f"name={table_name}^element={element}", limit=1)
    if existing:
        return
    url = f"{INSTANCE_URL}/api/now/table/sys_dictionary"
    payload = {
        "name": table_name,
        "element": element,
        "column_label": label,
        "internal_type": internal_type,
        "max_length": max_length,
        "sys_scope": APP_SYS_ID
    }
    resp = session.post(url, json=payload, timeout=25)
    if resp.status_code in [200, 201]:
        print(f"  [COL CREATED] {table_name}.{element} ({label})")
    else:
        print(f"  [COL FAILED] {table_name}.{element}: {resp.status_code}")

print("=== 1. CREATING WORK ORDER COLUMNS ===")
wo_cols = [
    ("u_number", "Work Order Number", "string", "100"),
    ("u_case_number", "Linked Case Number", "string", "100"),
    ("u_category", "Category", "string", "100"),
    ("u_short_description", "Short Description", "string", "255"),
    ("u_description", "Full Description", "string", "4000"),
    ("u_priority", "Priority", "string", "40"),
    ("u_state", "Work Order State", "string", "50"),
    ("u_location", "Location Address", "string", "255"),
    ("u_ward", "Ward Locality", "string", "100"),
    ("u_zone", "Municipal Zone", "string", "100"),
    ("u_landmark", "Landmark", "string", "255"),
    ("u_latitude", "Latitude", "string", "50"),
    ("u_longitude", "Longitude", "string", "50"),
    ("u_assigned_to", "Assigned User", "string", "100"),
    ("u_assigned_name", "Assigned Technician Name", "string", "150"),
    ("u_assigned_date", "Assigned Timestamp", "string", "50"),
    ("u_target_sla", "Target SLA Due", "string", "50"),
    ("u_arrival_otp", "Arrival Verification OTP", "string", "10"),
    ("u_arrival_verified", "Arrival Verified Flag", "string", "20"),
    ("u_arrival_timestamp", "Arrival Timestamp", "string", "50"),
    ("u_work_start_timestamp", "Work Start Timestamp", "string", "50"),
    ("u_work_complete_timestamp", "Work Complete Timestamp", "string", "50"),
    ("u_resolution_outcome", "Resolution Outcome", "string", "100"),
    ("u_completion_notes", "Completion Report", "string", "4000"),
    ("u_hold_reason", "Hold / Obstacle Reason", "string", "500"),
    ("u_progress_updates", "Progress Activity Log", "string", "4000"),
    ("u_verification_status", "Verification Outcome", "string", "50"),
    ("u_verification_notes", "Verification Auditor Notes", "string", "1000")
]

for el, lbl, itype, mlen in wo_cols:
    ensure_column("u_x_civic_ai_work_order", el, lbl, itype, mlen)

print("\n=== 2. CREATING EVIDENCE COLUMNS ===")
ev_cols = [
    ("u_work_order", "Work Order Number", "string", "100"),
    ("u_case_number", "Case Number", "string", "100"),
    ("u_evidence_type", "Evidence Category", "string", "50"),
    ("u_file_name", "File Name", "string", "255"),
    ("u_caption", "Caption", "string", "255"),
    ("u_uploaded_by", "Uploaded By", "string", "100"),
    ("u_uploaded_at", "Upload Timestamp", "string", "50"),
    ("u_photo_url", "Photo Data or Path", "string", "4000")
]

for el, lbl, itype, mlen in ev_cols:
    ensure_column("u_x_civic_ai_evidence", el, lbl, itype, mlen)

print("\n=== 3. SEEDING REALISTIC FIELD WORK ORDERS ===")
# Check existing work orders
existing_wos = api_get("u_x_civic_ai_work_order", query="u_numberISNOTEMPTY", limit=20)
print(f"Existing work orders found: {len(existing_wos)}")

seed_orders = [
    {
        "u_number": "WO-2026-00101",
        "u_case_number": "CIV-2026-00841",
        "u_category": "Roads & Potholes",
        "u_short_description": "Dangerous bitumen pothole crater on LB Road Depot Junction",
        "u_description": "Road surface eroded following monsoon showers. Deep crater obstructing bus transit and two-wheeler traffic. Requires immediate cold mix patching.",
        "u_priority": "1 - Critical",
        "u_state": "Assigned",
        "u_location": "LB Road near Adyar Bus Depot Signal",
        "u_ward": "Ward 172 - Adyar",
        "u_zone": "Zone 13 - Adyar",
        "u_landmark": "Opposite Adyar Ananda Bhavan signal",
        "u_latitude": "13.0067",
        "u_longitude": "80.2570",
        "u_assigned_to": "worker.adyar",
        "u_assigned_name": "Karthik Selvam",
        "u_assigned_date": "2026-10-10 08:30:00",
        "u_target_sla": "2026-10-11 12:00:00",
        "u_arrival_otp": "4829",
        "u_arrival_verified": "false",
        "u_arrival_timestamp": "",
        "u_work_start_timestamp": "",
        "u_work_complete_timestamp": "",
        "u_resolution_outcome": "",
        "u_completion_notes": "",
        "u_hold_reason": "",
        "u_progress_updates": '[{"time":"2026-10-10 08:30","category":"Assigned","text":"Work order dispatched to Ward 172 Rapid Response Crew"}]',
        "u_verification_status": "Pending",
        "u_verification_notes": ""
    },
    {
        "u_number": "WO-2026-00102",
        "u_case_number": "CIV-2026-00829",
        "u_category": "Drainage & Overflow",
        "u_short_description": "Stormwater drain silt blockage causing localized overflow",
        "u_description": "Manhole chamber backed up with plastic waste and silt. Sewage overflow spilling onto walkway near Gandhi Mandapam Rd.",
        "u_priority": "2 - High",
        "u_state": "In Progress",
        "u_location": "Gandhi Mandapam Road near Kotturpuram Turn",
        "u_ward": "Ward 172 - Adyar",
        "u_zone": "Zone 13 - Adyar",
        "u_landmark": "Near Anna University Gate 4",
        "u_latitude": "13.0112",
        "u_longitude": "80.2435",
        "u_assigned_to": "worker.adyar",
        "u_assigned_name": "Karthik Selvam",
        "u_assigned_date": "2026-10-10 07:15:00",
        "u_target_sla": "2026-10-11 16:30:00",
        "u_arrival_otp": "7134",
        "u_arrival_verified": "true",
        "u_arrival_timestamp": "2026-10-10 08:05:00",
        "u_work_start_timestamp": "2026-10-10 08:15:00",
        "u_work_complete_timestamp": "",
        "u_resolution_outcome": "",
        "u_completion_notes": "",
        "u_hold_reason": "",
        "u_progress_updates": '[{"time":"2026-10-10 08:05","category":"Arrival Verified","text":"Technician on site verified with OTP 7134"},{"time":"2026-10-10 08:15","category":"Work Started","text":"Suction super-sucker machine deployed to clear chamber"},{"time":"2026-10-10 09:30","category":"Progress","text":"Main barrel de-silted; secondary pipe inspection in progress"}]',
        "u_verification_status": "Pending",
        "u_verification_notes": ""
    },
    {
        "u_number": "WO-2026-00103",
        "u_case_number": "CIV-2026-00815",
        "u_category": "Electricity & Lights",
        "u_short_description": "Non-functional sodium streetlight fixture sparking in wind",
        "u_description": "Overhead street lamp pole loose wiring causing intermittent sparking and blacked-out pedestrian stretch.",
        "u_priority": "2 - High",
        "u_state": "On Hold",
        "u_location": "2nd Avenue, Besant Nagar Beach Road",
        "u_ward": "Ward 175 - Besant Nagar",
        "u_zone": "Zone 13 - Adyar",
        "u_landmark": "Adjacent to Co-optex junction",
        "u_latitude": "13.0002",
        "u_longitude": "80.2689",
        "u_assigned_to": "worker.adyar",
        "u_assigned_name": "Karthik Selvam",
        "u_assigned_date": "2026-10-09 14:00:00",
        "u_target_sla": "2026-10-11 10:00:00",
        "u_arrival_otp": "3912",
        "u_arrival_verified": "true",
        "u_arrival_timestamp": "2026-10-09 15:10:00",
        "u_work_start_timestamp": "2026-10-09 15:20:00",
        "u_work_complete_timestamp": "",
        "u_resolution_outcome": "",
        "u_completion_notes": "",
        "u_hold_reason": "High-voltage main cable requires 400V shutoff clearance from TANGEDCO substation engineer.",
        "u_progress_updates": '[{"time":"2026-10-09 15:20","category":"Work Started","text":"Fixture opened for wiring check"},{"time":"2026-10-09 16:45","category":"On Hold","text":"Hold requested: Substation power shutdown coordination required"}]',
        "u_verification_status": "Pending",
        "u_verification_notes": ""
    },
    {
        "u_number": "WO-2026-00104",
        "u_case_number": "CIV-2026-00790",
        "u_category": "Water Supply",
        "u_short_description": "Drinking water distribution pipe joint leakage repaired",
        "u_description": "Underground 150mm distribution feeder cracked causing low pressure and water accumulation on pavement.",
        "u_priority": "3 - Moderate",
        "u_state": "Completed",
        "u_location": "Canal Bank Road, Gandhi Nagar",
        "u_ward": "Ward 172 - Adyar",
        "u_zone": "Zone 13 - Adyar",
        "u_landmark": "Near Childrens Park Gate",
        "u_latitude": "13.0135",
        "u_longitude": "80.2520",
        "u_assigned_to": "worker.adyar",
        "u_assigned_name": "Karthik Selvam",
        "u_assigned_date": "2026-10-08 10:00:00",
        "u_target_sla": "2026-10-09 18:00:00",
        "u_arrival_otp": "8241",
        "u_arrival_verified": "true",
        "u_arrival_timestamp": "2026-10-08 11:00:00",
        "u_work_start_timestamp": "2026-10-08 11:20:00",
        "u_work_complete_timestamp": "2026-10-08 16:40:00",
        "u_resolution_outcome": "Resolved",
        "u_completion_notes": "Excavation completed, replaced fractured collar clamp with standard high-pressure ductile iron fitting. Pressure restored to 1.8 bar without leaks.",
        "u_hold_reason": "",
        "u_progress_updates": '[{"time":"2026-10-08 11:20","category":"Work Started","text":"Trench excavation commenced"},{"time":"2026-10-08 15:30","category":"Progress","text":"Clamp fitted and pressure test conducted successfully"},{"time":"2026-10-08 16:40","category":"Completed","text":"Trench backfilled and work completed"}]',
        "u_verification_status": "Verified",
        "u_verification_notes": "Ward Assistant Engineer verified on-site water pressure restoration and clean trench compaction on 09-Oct-2026."
    },
    {
        "u_number": "WO-2026-00105",
        "u_case_number": "CIV-2026-00860",
        "u_category": "Waterlogging & Floods",
        "u_short_description": "Underpass stormwater pump de-clogging and flood clearance",
        "u_description": "Heavy runoff accumulation in Thiruvanmiyur MRTS subway approach. Sump pump clogged by plastic debris.",
        "u_priority": "1 - Critical",
        "u_state": "Assigned",
        "u_location": "Thiruvanmiyur Railway Subway Approach",
        "u_ward": "Ward 179 - Thiruvanmiyur",
        "u_zone": "Zone 13 - Adyar",
        "u_landmark": "Opposite Tidal Park back gate",
        "u_latitude": "12.9868",
        "u_longitude": "80.2485",
        "u_assigned_to": "admin",
        "u_assigned_name": "Operations Emergency Response Unit",
        "u_assigned_date": "2026-10-10 11:00:00",
        "u_target_sla": "2026-10-10 20:00:00",
        "u_arrival_otp": "6290",
        "u_arrival_verified": "false",
        "u_arrival_timestamp": "",
        "u_work_start_timestamp": "",
        "u_work_complete_timestamp": "",
        "u_resolution_outcome": "",
        "u_completion_notes": "",
        "u_hold_reason": "",
        "u_progress_updates": '[{"time":"2026-10-10 11:00","category":"Assigned","text":"High-priority drainage pump clearance task assigned to emergency squad"}]',
        "u_verification_status": "Pending",
        "u_verification_notes": ""
    }
]

for wo in seed_orders:
    # Check if this work order exists by u_number
    existing = api_get("u_x_civic_ai_work_order", query=f"u_number={wo['u_number']}", limit=1)
    if existing:
        sys_id = existing[0]["sys_id"]
        session.put(f"{INSTANCE_URL}/api/now/table/u_x_civic_ai_work_order/{sys_id}", json=wo)
        print(f"  [UPDATED WO] {wo['u_number']} ({wo['u_category']}) - State: {wo['u_state']}")
    else:
        resp = session.post(f"{INSTANCE_URL}/api/now/table/u_x_civic_ai_work_order", json=wo)
        if resp.status_code == 201:
            print(f"  [CREATED WO] {wo['u_number']} ({wo['u_category']}) - State: {wo['u_state']}")
        else:
            print(f"  [CREATE WO FAILED] {wo['u_number']}: {resp.status_code}")

print("\n=== DATA MODEL SETUP COMPLETE ===")
