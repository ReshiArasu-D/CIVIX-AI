"""
CIVIX AI - Synchronize Case ID and Worker ID Schema and Data
1. Ensures u_worker_id on u_x_civic_ai_work_order
2. Registers all dictionary columns on u_x_civic_ai_case
3. Populates u_x_civic_ai_case with mapped records matching the 5 work orders
4. Updates u_x_civic_ai_work_order records with u_worker_id = 'EMP-9021'
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
        print(f"  [COL EXISTS] {table_name}.{element}")
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
        print(f"  [COL FAILED] {table_name}.{element}: {resp.status_code} {resp.text[:150]}")

print("=== 1. ENSURING WORK ORDER WORKER ID COLUMN ===")
ensure_column("u_x_civic_ai_work_order", "u_worker_id", "Worker Employee ID", "string", "50")

print("\n=== 2. ENSURING CASE DICTIONARY COLUMNS ===")
case_cols = [
    ("u_number", "Case Number", "string", "100"),
    ("u_work_order_number", "Linked Work Order Number", "string", "100"),
    ("u_worker_id", "Assigned Worker ID", "string", "50"),
    ("u_worker_name", "Assigned Worker Name", "string", "150"),
    ("u_category", "Category", "string", "100"),
    ("u_short_description", "Short Description", "string", "255"),
    ("u_description", "Full Description", "string", "4000"),
    ("u_priority", "Priority", "string", "40"),
    ("u_state", "Case State", "string", "50"),
    ("u_location", "Location Address", "string", "255"),
    ("u_ward", "Ward Locality", "string", "100"),
    ("u_zone", "Municipal Zone", "string", "100"),
    ("u_citizen_name", "Citizen Name", "string", "150"),
    ("u_citizen_phone", "Citizen Phone", "string", "50"),
    ("u_resolution_notes", "Resolution Notes", "string", "4000"),
    ("u_created_date", "Created Date", "string", "50")
]

for el, lbl, itype, mlen in case_cols:
    ensure_column("u_x_civic_ai_case", el, lbl, itype, mlen)

print("\n=== 3. UPDATING WORK ORDERS WITH WORKER ID ===")
wos = api_get("u_x_civic_ai_work_order", query="", limit=50)
for wo in wos:
    sys_id = wo.get("sys_id")
    num = wo.get("u_number")
    if not num:
        # Delete empty record if any
        session.delete(f"{INSTANCE_URL}/api/now/table/u_x_civic_ai_work_order/{sys_id}")
        print(f"  [DELETED EMPTY WORK ORDER] {sys_id}")
        continue
    
    worker_id = "EMP-9021" if "worker.adyar" in (wo.get("u_assigned_to") or "") or "Karthik" in (wo.get("u_assigned_name") or "") else "EMP-1044"
    update_payload = {
        "u_worker_id": worker_id
    }
    r = session.patch(f"{INSTANCE_URL}/api/now/table/u_x_civic_ai_work_order/{sys_id}", json=update_payload)
    print(f"  [UPDATED WO] {num} -> Worker ID: {worker_id} (Status: {r.status_code})")

print("\n=== 4. SEEDING / SYNCHRONIZING CASES TABLE ===")
cases_data = [
    {
        "u_number": "CIV-2026-00841",
        "u_work_order_number": "WO-2026-00101",
        "u_worker_id": "EMP-9021",
        "u_worker_name": "Karthik Selvam",
        "u_category": "Roads & Potholes",
        "u_short_description": "Dangerous bitumen pothole crater on LB Road Depot Junction",
        "u_description": "Road surface eroded following monsoon showers. Deep crater obstructing bus transit and two-wheeler traffic. Requires immediate cold mix patching.",
        "u_priority": "1 - Critical",
        "u_state": "In Progress",
        "u_location": "LB Road near Adyar Bus Depot Signal",
        "u_ward": "Ward 172 - Adyar",
        "u_zone": "Zone 13 - Adyar",
        "u_citizen_name": "S. Rajesh Kumar",
        "u_citizen_phone": "+91 98401 23456",
        "u_created_date": "2026-10-10 08:00:00",
        "u_resolution_notes": "Assigned to Ward 172 Rapid Response Crew. Technician arrived and cold-mix bituminous repair in progress."
    },
    {
        "u_number": "CIV-2026-00829",
        "u_work_order_number": "WO-2026-00102",
        "u_worker_id": "EMP-9021",
        "u_worker_name": "Karthik Selvam",
        "u_category": "Drainage & Overflow",
        "u_short_description": "Stormwater drain silt blockage causing localized overflow",
        "u_description": "Manhole chamber backed up with plastic waste and silt. Sewage overflow spilling onto walkway near Gandhi Mandapam Rd.",
        "u_priority": "2 - High",
        "u_state": "In Progress",
        "u_location": "Gandhi Mandapam Road near Kotturpuram Turn",
        "u_ward": "Ward 172 - Adyar",
        "u_zone": "Zone 13 - Adyar",
        "u_citizen_name": "M. Lakshmi Narayanan",
        "u_citizen_phone": "+91 94440 98765",
        "u_created_date": "2026-10-10 07:00:00",
        "u_resolution_notes": "Suction super-sucker unit deployed on site. Main barrel de-silting active."
    },
    {
        "u_number": "CIV-2026-00815",
        "u_work_order_number": "WO-2026-00103",
        "u_worker_id": "EMP-9021",
        "u_worker_name": "Karthik Selvam",
        "u_category": "Electricity & Lights",
        "u_short_description": "Non-functional sodium streetlight fixture sparking in wind",
        "u_description": "Overhead street lamp pole loose wiring causing intermittent sparking and blacked-out pedestrian stretch.",
        "u_priority": "2 - High",
        "u_state": "On Hold",
        "u_location": "2nd Avenue, Besant Nagar Beach Road",
        "u_ward": "Ward 175 - Besant Nagar",
        "u_zone": "Zone 13 - Adyar",
        "u_citizen_name": "P. Divya",
        "u_citizen_phone": "+91 97910 55432",
        "u_created_date": "2026-10-09 19:30:00",
        "u_resolution_notes": "TANGEDCO feeder isolation required before technician can access overhead lamp safely."
    },
    {
        "u_number": "CIV-2026-00790",
        "u_work_order_number": "WO-2026-00104",
        "u_worker_id": "EMP-9021",
        "u_worker_name": "Karthik Selvam",
        "u_category": "Solid Waste & Garbage",
        "u_short_description": "Overflowing community dustbin cluster on 4th Main Road",
        "u_description": "Three municipal bin dumpsters overflowing with wet municipal waste spilling onto road margin.",
        "u_priority": "3 - Moderate",
        "u_state": "Completed",
        "u_location": "4th Main Road, Gandhi Nagar, Adyar",
        "u_ward": "Ward 172 - Adyar",
        "u_zone": "Zone 13 - Adyar",
        "u_citizen_name": "K. Venkatesh",
        "u_citizen_phone": "+91 98842 11223",
        "u_created_date": "2026-10-09 11:00:00",
        "u_resolution_notes": "Compactor truck #TN-09-GCC-4411 deployed. All 3 bins emptied, swept, and bleached."
    },
    {
        "u_number": "CIV-2026-00860",
        "u_work_order_number": "WO-2026-00105",
        "u_worker_id": "EMP-1044",
        "u_worker_name": "Operations Emergency Response Unit",
        "u_category": "Public Safety & Hazards",
        "u_short_description": "Large fallen banyan branch obstructing carriageway",
        "u_description": "Heavy banyan tree branch snapped across both road lanes near 2nd Avenue Roundabout, completely stopping vehicular traffic.",
        "u_priority": "1 - Critical",
        "u_state": "Assigned",
        "u_location": "2nd Avenue Roundabout, Anna Nagar East",
        "u_ward": "Ward 102 - Anna Nagar",
        "u_zone": "Zone 8 - Anna Nagar",
        "u_citizen_name": "A. Balasubramanian",
        "u_citizen_phone": "+91 94441 66778",
        "u_created_date": "2026-10-10 10:15:00",
        "u_resolution_notes": "Hydraulic chainsaw unit and wood chipper dispatched to clear carriageway."
    }
]

for cd in cases_data:
    existing = api_get("u_x_civic_ai_case", query=f"u_number={cd['u_number']}", limit=1)
    if existing:
        sys_id = existing[0].get("sys_id")
        r = session.patch(f"{INSTANCE_URL}/api/now/table/u_x_civic_ai_case/{sys_id}", json=cd)
        print(f"  [UPDATED CASE] {cd['u_number']} <-> {cd['u_work_order_number']} | Worker: {cd['u_worker_id']} (Status: {r.status_code})")
    else:
        r = session.post(f"{INSTANCE_URL}/api/now/table/u_x_civic_ai_case", json=cd)
        print(f"  [CREATED CASE] {cd['u_number']} <-> {cd['u_work_order_number']} | Worker: {cd['u_worker_id']} (Status: {r.status_code})")

print("\n=== SYNCHRONIZATION COMPLETE ===")
