"""
CIVIX AI - ServiceNow Portal Deployment & Management Script
Creates and manages all Service Portal components, themes, widgets, and pages for CIVIX AI.
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

INSTANCE_URL = os.getenv("SERVICENOW_INSTANCE_URL", "").rstrip("/")
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")
CIVIX_APP_SYS_ID = "4750065ac37b0f14e54832f1b4013184"
CIVIX_SCOPE = "x_civic_ai"

if not INSTANCE_URL or not USERNAME or not PASSWORD:
    print("Error: Missing credentials in .env")
    sys.exit(1)

session = requests.Session()
session.auth = (USERNAME, PASSWORD)
session.headers.update({
    "Accept": "application/json",
    "Content-Type": "application/json"
})

def api_get(table: str, query: str = "", fields: str = "", limit: int = 10):
    url = f"{INSTANCE_URL}/api/now/table/{table}"
    params = {}
    if query:
        params["sysparm_query"] = query
    if fields:
        params["sysparm_fields"] = fields
    if limit:
        params["sysparm_limit"] = limit
    resp = session.get(url, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json().get("result", [])

def api_post(table: str, data: dict):
    url = f"{INSTANCE_URL}/api/now/table/{table}"
    resp = session.post(url, json=data, timeout=20)
    if resp.status_code not in (200, 201):
        print(f"POST {table} failed: {resp.status_code} - {resp.text}")
    resp.raise_for_status()
    return resp.json().get("result", {})

def api_put(table: str, sys_id: str, data: dict):
    url = f"{INSTANCE_URL}/api/now/table/{table}/{sys_id}"
    resp = session.put(url, json=data, timeout=20)
    resp.raise_for_status()
    return resp.json().get("result", {})

def upsert_record(table: str, query: str, data: dict, label: str = ""):
    existing = api_get(table, query=query, limit=1)
    if existing:
        sys_id = existing[0]["sys_id"]
        res = api_put(table, sys_id, data)
        print(f"[UPDATED] {table} ({label or query}): {sys_id}")
        return sys_id
    else:
        res = api_post(table, data)
        sys_id = res.get("sys_id")
        print(f"[CREATED] {table} ({label or query}): {sys_id}")
        return sys_id

if __name__ == "__main__":
    print(f"Connecting to ServiceNow: {INSTANCE_URL}")
    print(f"Application Scope: {CIVIX_SCOPE} ({CIVIX_APP_SYS_ID})")
    # Quick health check
    res = api_get("sys_app", query=f"sys_id={CIVIX_APP_SYS_ID}", fields="name,scope")
    print("Target Scoped App:", res)
