"""
CIVIX AI - Comprehensive Screen & Widget Generator
Generates all 11 Phase 1 screens, widgets, and container hierarchies inside ServiceNow.
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
APP_SYS_ID = "4750065ac37b0f14e54832f1b4013184"
APP_SCOPE = "x_civic_ai"
THEME_SYS_ID = "9b84c616c3bb0f14e54832f1b401319b"
HEADER_WIDGET_SYS_ID = "e78482dac33b0f14e54832f1b40131ca"
FOOTER_WIDGET_SYS_ID = "6784c616c3bb0f14e54832f1b40131bd"

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
    resp = session.get(url, params=params, timeout=25)
    resp.raise_for_status()
    return resp.json().get("result", [])

def api_post(table: str, data: dict):
    url = f"{INSTANCE_URL}/api/now/table/{table}"
    resp = session.post(url, json=data, timeout=25)
    if resp.status_code not in (200, 201):
        print(f"POST {table} failed: {resp.status_code} - {resp.text[:300]}")
    resp.raise_for_status()
    return resp.json().get("result", {})

def api_put(table: str, sys_id: str, data: dict):
    url = f"{INSTANCE_URL}/api/now/table/{table}/{sys_id}"
    resp = session.put(url, json=data, timeout=25)
    resp.raise_for_status()
    return resp.json().get("result", {})

def upsert(table: str, query: str, data: dict, label: str = ""):
    data["sys_scope"] = APP_SYS_ID
    data["sys_package"] = APP_SYS_ID
    existing = api_get(table, query=query, limit=1)
    if existing:
        sys_id = existing[0]["sys_id"]
        res = api_put(table, sys_id, data)
        print(f"  [UPDATED] {table} ({label or query}): {sys_id}")
        return sys_id
    else:
        res = api_post(table, data)
        sys_id = res.get("sys_id")
        print(f"  [CREATED] {table} ({label or query}): {sys_id}")
        return sys_id

def create_page_structure(page_id: str, page_title: str, is_public: bool, widget_sys_id: str):
    """Creates sp_page, sp_container, sp_row, sp_column, and sp_instance."""
    # 1. Page
    page_data = {
        "id": page_id,
        "title": f"CIVIX AI - {page_title}",
        "public": "true" if is_public else "false"
    }
    page_sys_id = upsert("sp_page", f"id={page_id}", page_data, f"Page: {page_id}")

    # 2. Container
    cont_data = {
        "sp_page": page_sys_id,
        "width": "fluid",
        "order": 1
    }
    cont_sys_id = upsert("sp_container", f"sp_page={page_sys_id}", cont_data, f"Container for {page_id}")

    # 3. Row
    row_data = {
        "sp_container": cont_sys_id,
        "order": 1
    }
    row_sys_id = upsert("sp_row", f"sp_container={cont_sys_id}", row_data, f"Row for {page_id}")

    # 4. Column
    col_data = {
        "sp_row": row_sys_id,
        "size": 12,
        "order": 1
    }
    col_sys_id = upsert("sp_column", f"sp_row={row_sys_id}", col_data, f"Col for {page_id}")

    # 5. Instance
    inst_data = {
        "sp_column": col_sys_id,
        "sp_widget": widget_sys_id,
        "title": page_title,
        "order": 1
    }
    inst_sys_id = upsert("sp_instance", f"sp_column={col_sys_id}", inst_data, f"Instance for {page_id}")
    return page_sys_id

print("Screen Generator loaded.")
