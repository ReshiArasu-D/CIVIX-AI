"""
CIVIX AI - Complete Admin & Operations Portal Implementation (Phase 2)
1. Creates / updates Service Portal Page: civix_admin_portal
2. Creates / updates Service Portal Widget: civix_admin_portal_widget
3. Binds widget to page with sp_container, sp_row, sp_column, sp_instance
4. Updates civix_portal_select_widget so Admin & Operations card routes directly to ?id=civix_admin_portal
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
    resp.raise_for_status()
    return resp.json().get("result", {})

def api_put(table: str, sys_id: str, data: dict):
    url = f"{INSTANCE_URL}/api/now/table/{table}/{sys_id}"
    resp = session.put(url, json=data, timeout=25)
    resp.raise_for_status()
    return resp.json().get("result", {})

def ensure_sp_page(page_id: str, title: str):
    existing = api_get("sp_page", query=f"id={page_id}", limit=1)
    if existing:
        print(f"  [PAGE EXISTS] {page_id} ({existing[0]['sys_id']})")
        return existing[0]["sys_id"]
    payload = {
        "id": page_id,
        "title": title,
        "sys_scope": APP_SYS_ID
    }
    res = api_post("sp_page", payload)
    print(f"  [PAGE CREATED] {page_id} ({res.get('sys_id')})")
    return res.get("sys_id")

def ensure_sp_widget(widget_id: str, name: str, template: str, css: str, client_script: str, server_script: str):
    existing = api_get("sp_widget", query=f"id={widget_id}", limit=1)
    payload = {
        "id": widget_id,
        "name": name,
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "sys_scope": APP_SYS_ID
    }
    if existing:
        sys_id = existing[0]["sys_id"]
        api_put("sp_widget", sys_id, payload)
        print(f"  [WIDGET UPDATED] {widget_id} ({sys_id})")
        return sys_id
    else:
        res = api_post("sp_widget", payload)
        sys_id = res.get("sys_id")
        print(f"  [WIDGET CREATED] {widget_id} ({sys_id})")
        return sys_id

def ensure_page_layout(page_id: str, page_sys_id: str, widget_sys_id: str):
    containers = api_get("sp_container", query=f"sp_page={page_sys_id}", limit=1)
    if containers:
        container_sys_id = containers[0]["sys_id"]
    else:
        c_res = api_post("sp_container", {"sp_page": page_sys_id, "order": 1, "sys_scope": APP_SYS_ID})
        container_sys_id = c_res.get("sys_id")
    
    rows = api_get("sp_row", query=f"sp_container={container_sys_id}", limit=1)
    if rows:
        row_sys_id = rows[0]["sys_id"]
    else:
        r_res = api_post("sp_row", {"sp_container": container_sys_id, "order": 1, "sys_scope": APP_SYS_ID})
        row_sys_id = r_res.get("sys_id")
    
    cols = api_get("sp_column", query=f"sp_row={row_sys_id}", limit=1)
    if cols:
        col_sys_id = cols[0]["sys_id"]
    else:
        cl_res = api_post("sp_column", {"sp_row": row_sys_id, "size": 12, "order": 1, "sys_scope": APP_SYS_ID})
        col_sys_id = cl_res.get("sys_id")
    
    instances = api_get("sp_instance", query=f"sp_column={col_sys_id}", limit=1)
    if instances:
        inst_sys_id = instances[0]["sys_id"]
        api_put("sp_instance", inst_sys_id, {"sp_widget": widget_sys_id})
        print(f"  [INSTANCE UPDATED] Bound widget to page {page_id}")
    else:
        api_post("sp_instance", {"sp_column": col_sys_id, "sp_widget": widget_sys_id, "order": 1, "sys_scope": APP_SYS_ID})
        print(f"  [INSTANCE CREATED] Bound widget to page {page_id}")

print("=== 1. PREPARING SERVICE PORTAL PAGE civix_admin_portal ===")
page_sys_id = ensure_sp_page("civix_admin_portal", "CIVIX AI - Admin & Operations Portal")

# Load template, css, client, server from separate files for clean maintainability
with open("d:/tcs/admin_portal_template.html", "r", encoding="utf-8") as f:
    ADMIN_TEMPLATE = f.read()

with open("d:/tcs/admin_portal_style.css", "r", encoding="utf-8") as f:
    ADMIN_CSS = f.read()

with open("d:/tcs/admin_portal_client.js", "r", encoding="utf-8") as f:
    ADMIN_CLIENT = f.read()

with open("d:/tcs/admin_portal_server.js", "r", encoding="utf-8") as f:
    ADMIN_SERVER = f.read()

print("=== 2. DEPLOYING civix_admin_portal_widget ===")
widget_sys_id = ensure_sp_widget(
    "civix_admin_portal_widget",
    "CIVIX AI - Admin & Operations Portal Widget",
    ADMIN_TEMPLATE,
    ADMIN_CSS,
    ADMIN_CLIENT,
    ADMIN_SERVER
)

print("=== 3. WIRING PAGE LAYOUT ===")
ensure_page_layout("civix_admin_portal", page_sys_id, widget_sys_id)

print("=== 4. UPDATING PORTAL SELECTION TO LINK DIRECTLY TO ADMIN PORTAL ===")
portal_sel = api_get("sp_widget", query="id=civix_portal_select_widget", limit=1)
if portal_sel:
    psys = portal_sel[0]["sys_id"]
    ptmpl = portal_sel[0]["template"]
    # Ensure Admin card links to ?id=civix_admin_portal
    if '?id=civix_admin_portal' not in ptmpl:
        ptmpl = ptmpl.replace('href="?id=civix_login&role=admin"', 'href="?id=civix_admin_portal"')
        ptmpl = ptmpl.replace('href="/now/nav/ui/classic/params/target/incident_list.do"', 'href="?id=civix_admin_portal"')
        api_put("sp_widget", psys, {"template": ptmpl})
        print("  [SUCCESS] Portal Selection updated to link directly to Admin & Operations Portal!")

print("=== CIVIX AI ADMIN & OPERATIONS PORTAL DEPLOYED SUCCESSFULLY ===")
