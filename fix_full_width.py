import os
import requests
from dotenv import load_dotenv

load_dotenv()

INSTANCE_URL = os.getenv("SERVICENOW_INSTANCE_URL", "").rstrip("/")
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")

session = requests.Session()
session.auth = (USERNAME, PASSWORD)
session.headers.update({
    "Accept": "application/json",
    "Content-Type": "application/json"
})

def api_get(table: str, query: str = ""):
    url = f"{INSTANCE_URL}/api/now/table/{table}"
    params = {"sysparm_query": query} if query else {}
    resp = session.get(url, params=params, timeout=25)
    resp.raise_for_status()
    return resp.json().get("result", [])

def api_put(table: str, sys_id: str, data: dict):
    url = f"{INSTANCE_URL}/api/now/table/{table}/{sys_id}"
    resp = session.put(url, json=data, timeout=25)
    resp.raise_for_status()
    return resp.json().get("result", {})

def make_all_containers_fluid():
    print("--- 1. Making all CIVIX page containers fluid (bootstrap_alt = true) ---")
    pages = api_get("sp_page", "idSTARTSWITHcivix")
    print(f"Found {len(pages)} CIVIX pages.")
    
    total_conts = 0
    updated_conts = 0
    for pg in pages:
        page_id = pg["id"]
        page_sys_id = pg["sys_id"]
        conts = api_get("sp_container", f"sp_page={page_sys_id}")
        for c in conts:
            total_conts += 1
            c_sys_id = c["sys_id"]
            alt = str(c.get("bootstrap_alt", "")).lower()
            if alt != "true":
                api_put("sp_container", c_sys_id, {"bootstrap_alt": "true"})
                print(f"  [UPDATED] Page '{page_id}' Container {c_sys_id} -> bootstrap_alt = true")
                updated_conts += 1
            else:
                print(f"  [OK] Page '{page_id}' Container {c_sys_id} already fluid.")
    print(f"Done. {updated_conts}/{total_conts} containers updated to fluid.")

def update_theme_global_full_width():
    print("\n--- 2. Updating Theme CSS to guarantee 100% edge-to-edge full width ---")
    theme_id = "9b84c616c3bb0f14e54832f1b401319b"
    
    theme_css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

$font-family-base: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
$font-family-sans-serif: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;

$navbar-height: 0px !important;
$grid-gutter-width: 0px !default;
$container-large-desktop: 100% !important;
$container-desktop: 100% !important;
$container-tablet: 100% !important;
$body-bg: #F8FAFC !important;

/* 100% EDGE-TO-EDGE FULL-WIDTH RESET */
* {
  box-sizing: border-box !important;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
  min-height: 100vh !important;
  background-color: #F8FAFC !important;
  overflow-x: hidden !important;
}

#page_root, .sp-page-root, .page, main {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
}

/* OVERRIDE BOOTSTRAP .container AND .container-fluid TO STRETCH 100% */
.container, .container-fluid {
  width: 100% !important;
  max-width: 100% !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  padding-left: 0 !important;
  padding-right: 0 !important;
}

.row {
  margin-left: 0 !important;
  margin-right: 0 !important;
  width: 100% !important;
}

.col-xs-12, .col-sm-12, .col-md-12, .col-lg-12, [class*="col-"] {
  padding-left: 0 !important;
  padding-right: 0 !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
}

header.sp-header, nav.navbar-inverse, .navbar, footer.civix-footer {
  display: none !important;
}
"""
    api_put("sp_theme", theme_id, {"css_variables": theme_css.strip()})
    print("  [SUCCESS] Theme updated with full-width edge-to-edge rules.")

if __name__ == "__main__":
    make_all_containers_fluid()
    update_theme_global_full_width()
