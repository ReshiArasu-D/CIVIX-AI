"""
CIVIX AI - Complete Premium Portal Suite Deployment
Deploys unified Plus Jakarta Sans styling, zero-margin flex shell,
and high-level interactive design across Home, Dashboard, Report an Issue,
My Complaints, and Case Tracking.
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

INSTANCE_URL = os.getenv("SERVICENOW_INSTANCE_URL", "").rstrip("/")
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")
APP_SYS_ID = "4750065ac37b0f14e54832f1b4013184"

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

def api_put(table: str, sys_id: str, data: dict):
    url = f"{INSTANCE_URL}/api/now/table/{table}/{sys_id}"
    resp = session.put(url, json=data, timeout=25)
    resp.raise_for_status()
    return resp.json().get("result", {})

def update_widget(widget_id: str, template: str, css: str, client_script: str, server_script: str):
    res = api_get("sp_widget", query=f"id={widget_id}", limit=1)
    if not res:
        print(f"Widget {widget_id} not found!")
        return None
    sys_id = res[0]["sys_id"]
    payload = {
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "sys_scope": APP_SYS_ID,
        "sys_package": APP_SYS_ID,
        "public": "true"
    }
    api_put("sp_widget", sys_id, payload)
    print(f"  [UPDATED] {widget_id} ({sys_id})")
    return sys_id

# Update global theme
def update_theme():
    print("\n--- 1. Updating Theme with 'Plus Jakarta Sans' & Zero Margins ---")
    css_vars = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

$font-family-base: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
$font-family-sans-serif: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;

$navbar-height: 0px !important;
$grid-gutter-width: 0px !default;
$container-large-desktop: 100% !important;
$container-desktop: 100% !important;
$container-tablet: 100% !important;
$body-bg: #F8FAFC !important;
"""
    api_put("sp_theme", "9b84c616c3bb0f14e54832f1b401319b", {"css_variables": css_vars.strip()})
    print("  [SUCCESS] Theme updated.")


# SHARED SHELL CSS (NO HORIZONTAL OVERFLOW, ZERO-SCROLLBAR, PLUS JAKARTA SANS)
SHELL_CSS_BASE = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

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

.sp-page-root, #page_root, .page, .container, .container-fluid, .row, .col-xs-12, .col-sm-12, .col-md-12 {
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

/* ROOT FLEX CONTAINER: NO 100vw, NO HORIZONTAL SCROLLBAR */
.civix-app-shell {
  display: flex;
  width: 100%;
  max-width: 100%;
  min-height: 100vh;
  background: #F8FAFC;
  overflow-x: hidden;
  position: relative;
}

/* STICKY LEFT SIDEBAR (240px) */
.civix-side-nav-bar {
  width: 240px;
  min-width: 240px;
  max-width: 240px;
  flex-shrink: 0;
  height: 100vh;
  position: sticky;
  top: 0;
  background: #0B192C;
  z-index: 500;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 16px rgba(0,0,0,0.15);
  overflow-y: auto;
}
.civix-side-bg-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(180deg, #0A192F 0%, #0F284E 50%, #0A192F 100%);
  opacity: 0.98;
}
.civix-side-body {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 22px 14px;
}
.civix-brand-zone {
  margin-bottom: 28px;
  padding-left: 4px;
}
.civix-brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}
.civix-brand-link:hover { text-decoration: none; }
.civix-emblem-svg { width: 34px; height: 34px; flex-shrink: 0; }
.civix-brand-titles { display: flex; flex-direction: column; }
.civix-brand-logo-text {
  font-size: 20px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: 0.5px;
  line-height: 1.1;
}
.civix-brand-tagline-text {
  font-size: 9px;
  color: #94A3B8;
  font-weight: 500;
}

.civix-side-links {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-grow: 1;
}
.civix-side-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 16px;
  border-radius: 10px;
  color: #CBD5E1;
  font-size: 13.5px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.civix-side-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #FFFFFF;
  transform: translateX(3px);
  text-decoration: none;
}
.civix-side-btn.active {
  background: #0066FF;
  color: #FFFFFF;
  font-weight: 600;
  box-shadow: 0 4px 14px rgba(0, 102, 255, 0.4);
}
.civix-side-icon-box {
  font-size: 15px;
  width: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.civix-side-footer-motto {
  margin-top: auto;
  padding-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.civix-leaf-icon { flex-shrink: 0; }
.civix-motto-stack {
  display: flex;
  flex-direction: column;
  font-size: 10px;
  font-weight: 600;
  color: #22C55E;
  line-height: 1.35;
}

/* FLUID WORKSPACE */
.civix-main-column {
  flex: 1;
  min-width: 0;
  width: calc(100% - 240px);
  display: flex;
  flex-direction: column;
  background: #F8FAFC;
  overflow-x: hidden;
}

/* STICKY TOPBAR */
.civix-top-header {
  position: sticky;
  top: 0;
  width: 100%;
  height: 68px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid #E2E8F0;
  padding: 0 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 400;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.civix-search-pill-box {
  flex: 1;
  max-width: 480px;
  position: relative;
}
.civix-search-lens-icon {
  position: absolute;
  left: 14px;
  top: 12px;
  color: #94A3B8;
  font-size: 14px;
}
.civix-search-input-pill {
  width: 100%;
  height: 38px;
  background: #F1F5F9;
  border: 1px solid transparent;
  border-radius: 20px;
  padding: 0 16px 0 38px;
  font-size: 13px;
  color: #0F172A;
  outline: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.civix-search-input-pill:focus {
  background: #FFFFFF;
  border-color: #0066FF;
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}
.civix-header-actions-group {
  display: flex;
  align-items: center;
  gap: 16px;
}

.civix-lang-drop-wrap { position: relative; }
.civix-lang-btn-pill {
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 7px 14px;
  font-size: 12.5px;
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.15s;
}
.civix-lang-btn-pill:hover { background: #E2E8F0; }
.civix-lang-menu-box {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 230px;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(0,0,0,0.12);
  z-index: 1000;
  overflow: hidden;
}
.civix-lang-scroll-area { max-height: 280px; overflow-y: auto; }
.civix-lang-opt-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 14px;
  border: none;
  background: transparent;
  font-size: 12.5px;
  cursor: pointer;
  color: #1E293B;
  transition: background 0.15s;
}
.civix-lang-opt-item:hover, .civix-lang-opt-item.active {
  background: #EFF6FF;
  color: #0066FF;
}
.civix-lang-circ {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  color: #FFFFFF;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.civix-bell-link {
  position: relative;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #F1F5F9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #334155;
  text-decoration: none;
}
.civix-bell-count-pill {
  position: absolute;
  top: -2px;
  right: -2px;
  background: #EF4444;
  color: #FFFFFF;
  font-size: 9.5px;
  font-weight: 700;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.civix-profile-pill-item {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  text-decoration: none;
}
.civix-profile-pill-item:hover { text-decoration: none; }
.civix-avatar-img-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #E2E8F0;
}
.civix-profile-user-name {
  font-size: 13.5px;
  font-weight: 700;
  color: #0F172A;
}

/* CONTENT BODY */
.civix-content-area {
  padding: 22px 28px 60px;
  width: 100%;
  box-sizing: border-box;
}

/* WHITE CARD BASE */
.civix-panel-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 20px 22px;
  margin-bottom: 20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}
"""

print("Writing complete suite deployment code...")
