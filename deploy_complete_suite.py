"""
CIVIX AI - Complete Reference 2 Dashboard & Case Tracking Implementation
"""

import os
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

def api_get(table: str, query: str = "", limit: int = 10):
    url = f"{INSTANCE_URL}/api/now/table/{table}"
    params = {"sysparm_query": query, "sysparm_limit": limit}
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
    print(f"  [DEPLOYED] {widget_id} ({sys_id})")
    return sys_id

# ==============================================================================
# COMMON SIDEBAR & TOPBAR HTML
# ==============================================================================
def get_sidebar_html(active_item="dashboard"):
    return f"""
    <!-- LEFT SIDEBAR -->
    <aside class="civix-side-nav-bar" role="navigation" aria-label="Sidebar Navigation">
      <div class="civix-side-bg-overlay"></div>
      <div class="civix-side-body">
        <div class="civix-brand-zone">
          <a href="?id=civix_home" class="civix-brand-link">
            <svg class="civix-emblem-svg" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="2" y="14" width="6" height="20" rx="1.5" fill="#3B82F6"/>
              <rect x="10" y="7" width="8" height="27" rx="1.5" fill="#2563EB"/>
              <rect x="20" y="3" width="8" height="31" rx="1.5" fill="#1D4ED8"/>
              <rect x="30" y="11" width="5" height="23" rx="1.5" fill="#60A5FA"/>
              <circle cx="5" cy="18" r="1" fill="#DBEAFE"/>
              <circle cx="5" cy="23" r="1" fill="#DBEAFE"/>
              <circle cx="14" cy="12" r="1" fill="#EFF6FF"/>
              <circle cx="14" cy="17" r="1" fill="#EFF6FF"/>
              <circle cx="14" cy="22" r="1" fill="#EFF6FF"/>
              <circle cx="24" cy="8" r="1" fill="#FFFFFF"/>
              <circle cx="24" cy="13" r="1" fill="#FFFFFF"/>
              <circle cx="24" cy="18" r="1" fill="#FFFFFF"/>
            </svg>
            <div class="civix-brand-titles">
              <span class="civix-brand-logo-text">CIVIX AI</span>
              <span class="civix-brand-tagline-text">Smart Cities. Safer Communities.</span>
            </div>
          </a>
        </div>

        <nav class="civix-side-links">
          <a href="?id=civix_home" class="civix-side-btn {'active' if active_item == 'dashboard' else ''}">
            <span class="civix-side-icon-box">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
            </span>
            <span>Dashboard</span>
          </a>
          <a href="?id=civix_report_issue" class="civix-side-btn {'active' if active_item == 'report' else ''}">
            <span class="civix-side-icon-box">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </span>
            <span>Report an Issue</span>
          </a>
          <a href="?id=civix_my_cases" class="civix-side-btn {'active' if active_item == 'complaints' else ''}">
            <span class="civix-side-icon-box">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            </span>
            <span>My Complaints</span>
          </a>
          <a href="?id=civix_landing#services" class="civix-side-btn {'active' if active_item == 'services' else ''}">
            <span class="civix-side-icon-box">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            </span>
            <span>Service Information</span>
          </a>
          <a href="?id=civix_landing#trust" class="civix-side-btn {'active' if active_item == 'help' else ''}">
            <span class="civix-side-icon-box">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>
            </span>
            <span>Help & Support</span>
          </a>
        </nav>

        <div class="civix-side-footer-motto">
          <div class="civix-leaf-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>
              <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>
            </svg>
          </div>
          <div class="civix-motto-stack">
            <span>Clean Cities</span>
            <span>Green Communities</span>
            <span>Better Tomorrows</span>
          </div>
        </div>
      </div>
    </aside>
"""

def get_topbar_html():
    return """
    <!-- STICKY TOPBAR -->
    <header class="civix-top-header" role="banner">
      <div class="civix-search-pill-box">
        <svg class="civix-search-lens-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" class="civix-search-input-pill" placeholder="Search services, complaints or help..." ng-model="c.searchQuery" />
      </div>

      <div class="civix-header-actions-group">
        <!-- Languages Dropdown -->
        <div class="civix-lang-drop-wrap">
          <button type="button" class="civix-lang-btn-pill" ng-click="c.toggleLang()">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            <span>{{c.currentLangDisplay || 'भारतीय भाषाएं / Language'}}</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div class="civix-lang-menu-box" ng-show="c.langOpen">
            <div class="civix-lang-scroll-area">
              <button type="button" ng-repeat="l in c.languages" class="civix-lang-opt-item" ng-class="{'active': c.selectedLang === l.code}" ng-click="c.chooseLang(l)">
                <span class="civix-lang-circ" style="background: {{l.bg}}">{{l.prefix}}</span>
                <strong>{{l.native}}</strong> <small class="text-muted" style="margin-left:auto;">{{l.name}}</small>
              </button>
            </div>
          </div>
        </div>

        <!-- Notification Bell -->
        <a href="?id=civix_home#alerts" class="civix-bell-link" title="3 Notifications">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
          <span class="civix-bell-count-pill">3</span>
        </a>

        <!-- Profile Avatar & Name -->
        <a href="?id=civix_profile" class="civix-profile-pill-item">
          <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=120&auto=format&fit=crop&q=80" alt="Priya Sharma" class="civix-avatar-img-circle" />
          <span class="civix-profile-user-name">{{c.data.citizenName || 'Priya Sharma'}}</span>
        </a>
      </div>
    </header>
"""

# Common Base CSS
BASE_SHELL_CSS = """
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

/* ROOT FLEX CONTAINER */
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
  color: #FFFFFF;
  z-index: 500;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.civix-side-bg-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 260px;
  background: url('https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=600&auto=format&fit=crop&q=80') bottom center/cover no-repeat;
  opacity: 0.18;
  pointer-events: none;
}

.civix-side-body {
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  z-index: 2;
}

.civix-brand-zone {
  margin-bottom: 28px;
  padding: 0 8px;
}
.civix-brand-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #FFFFFF;
}
.civix-brand-link:hover { text-decoration: none; color: #FFFFFF; }
.civix-emblem-svg {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}
.civix-brand-titles {
  display: flex;
  flex-direction: column;
}
.civix-brand-logo-text {
  font-size: 17px;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #FFFFFF;
  line-height: 1.1;
}
.civix-brand-tagline-text {
  font-size: 9px;
  color: #94A3B8;
  letter-spacing: 0.2px;
  margin-top: 2px;
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
  padding: 11px 14px;
  border-radius: 10px;
  color: #94A3B8;
  font-size: 13.5px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.civix-side-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #FFFFFF;
  text-decoration: none;
  transform: translateX(3px);
}
.civix-side-btn.active {
  background: #0066FF;
  color: #FFFFFF;
  font-weight: 700;
  box-shadow: 0 4px 14px rgba(0, 102, 255, 0.4);
}
.civix-side-icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
}

.civix-side-footer-motto {
  margin-top: auto;
  padding: 16px 12px 6px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.civix-leaf-icon { flex-shrink: 0; }
.civix-motto-stack {
  display: flex;
  flex-direction: column;
  font-size: 10.5px;
  font-weight: 600;
  color: #10B981;
  line-height: 1.25;
}

/* FLUID MAIN COLUMN */
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
  display: flex;
  align-items: center;
}
.civix-search-lens-icon {
  position: absolute;
  left: 14px;
  pointer-events: none;
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
  transition: background 0.15s;
}
.civix-bell-link:hover { background: #E2E8F0; text-decoration: none; }
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

.civix-content-area {
  padding: 22px 28px 60px;
  width: 100%;
  box-sizing: border-box;
}

.civix-panel-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 24px;
  margin-bottom: 22px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}
"""

# ==============================================================================
# WIDGET 1: CUSTOMER HOME / DASHBOARD (REFERENCE 2 IDENTICAL)
# ==============================================================================
HOME_TEMPLATE_RAW = """
<div class="civix-app-shell">
  __SIDEBAR__

  <main class="civix-main-column">
    __TOPBAR__

    <div class="civix-content-area">
      <!-- 2-COLUMN BALANCED DASHBOARD LAYOUT -->
      <div class="civix-dashboard-2col-layout">
        
        <!-- LEFT / MAIN WORKSPACE -->
        <div class="civix-dash-main-col">
          
          <!-- 1. HERO BANNER ROW (WELCOME + RIVER PROMO) -->
          <div class="civix-banner-grid-ref2">
            <!-- Welcome Card with Panorama Skyline Background -->
            <div class="civix-hero-welcome-card-ref2">
              <div class="civix-hero-skyline-pano"></div>
              <div class="civix-hero-content-col">
                <h1 class="civix-hero-big-greeting">Welcome back,<br/><span class="civix-name-gradient">{{c.data.citizenName || 'Priya Sharma'}}!</span> 👋</h1>
                <p class="civix-hero-tagline-main">Together for a cleaner, safer and smarter city.</p>
                <p class="civix-hero-tagline-sub">Report issues, track progress and help improve our community.</p>
              </div>

              <!-- Weather Card Inside Hero -->
              <div class="civix-glass-weather-widget-ref2">
                <div class="civix-weather-header">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  <strong>Chennai, Tamil Nadu</strong>
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                </div>
                <div class="civix-weather-split">
                  <div class="civix-weather-temp-info">
                    <span class="civix-temp-reading">32°C</span>
                    <span class="civix-weather-condition">Mostly Clear</span>
                  </div>
                  <div class="civix-animated-sun-icon">
                    <svg width="42" height="42" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="5" fill="#F59E0B"/>
                      <path d="M12 1v3M12 20v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M1 12h3M20 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" stroke="#F59E0B" stroke-width="2.2" stroke-linecap="round"/>
                      <path d="M17 18a4 4 0 0 0-4-4 4 4 0 0 0-3.8 2.7" stroke="#38BDF8" stroke-width="1.8" stroke-linecap="round"/>
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <!-- Waterfront River Promo Card -->
            <div class="civix-promo-river-card">
              <div class="civix-promo-river-bg"></div>
              <div class="civix-promo-river-overlay">
                <h3 class="civix-promo-river-title">Cleaner Cities<br/>Happier People</h3>
                <div class="civix-promo-river-bar"></div>
              </div>
            </div>
          </div>

          <!-- 2. 4 KPI METRIC CARDS IN A ROW -->
          <section class="civix-kpi-deck-4cols">
            <!-- 1. Total Complaints -->
            <a href="?id=civix_my_cases" class="civix-kpi-tile kpi-tile-blue">
              <div class="civix-kpi-icon-bubble bg-blue-subtle">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
              </div>
              <div class="civix-kpi-details">
                <div class="civix-kpi-value-row">
                  <span class="civix-kpi-count">{{c.data.counts.total || 12}}</span>
                  <span class="civix-kpi-arrow-cue">&rsaquo;</span>
                </div>
                <div class="civix-kpi-label-text">Total Complaints</div>
                <div class="civix-kpi-trend-badge trend-green">&uarr; 3 this month</div>
              </div>
            </a>

            <!-- 2. Resolved -->
            <a href="?id=civix_my_cases&status=Resolved" class="civix-kpi-tile kpi-tile-green">
              <div class="civix-kpi-icon-bubble bg-green-subtle">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              </div>
              <div class="civix-kpi-details">
                <div class="civix-kpi-value-row">
                  <span class="civix-kpi-count">{{c.data.counts.resolved || 8}}</span>
                  <span class="civix-kpi-arrow-cue">&rsaquo;</span>
                </div>
                <div class="civix-kpi-label-text">Resolved</div>
                <div class="civix-kpi-trend-badge trend-green">&uarr; 2 this month</div>
              </div>
            </a>

            <!-- 3. In Progress -->
            <a href="?id=civix_my_cases&status=In%20Progress" class="civix-kpi-tile kpi-tile-gold">
              <div class="civix-kpi-icon-bubble bg-gold-subtle">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              </div>
              <div class="civix-kpi-details">
                <div class="civix-kpi-value-row">
                  <span class="civix-kpi-count">{{c.data.counts.in_progress || 3}}</span>
                  <span class="civix-kpi-arrow-cue">&rsaquo;</span>
                </div>
                <div class="civix-kpi-label-text">In Progress</div>
                <div class="civix-kpi-trend-badge trend-neutral">&ndash; same as last month</div>
              </div>
            </a>

            <!-- 4. Awaiting Action -->
            <a href="?id=civix_my_cases&status=Awaiting%20Action" class="civix-kpi-tile kpi-tile-red">
              <div class="civix-kpi-icon-bubble bg-red-subtle">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              </div>
              <div class="civix-kpi-details">
                <div class="civix-kpi-value-row">
                  <span class="civix-kpi-count">{{c.data.counts.awaiting || 1}}</span>
                  <span class="civix-kpi-arrow-cue">&rsaquo;</span>
                </div>
                <div class="civix-kpi-label-text">Awaiting Action</div>
                <div class="civix-kpi-trend-badge trend-red">&darr; 1 from last month</div>
              </div>
            </a>
          </section>

          <!-- 3. REPORT A NEW ISSUE (5 CATEGORY CARDS) -->
          <div class="civix-white-box">
            <div class="civix-box-header">
              <h2 class="civix-box-title">Report a New Issue</h2>
              <p class="civix-box-subtitle">Select a service category to report an issue in your area.</p>
            </div>
            <div class="civix-category-cards-grid">
              <a href="?id=civix_report_issue&cat=Water" class="civix-cat-pill-card">
                <div class="civix-cat-bubble cat-water">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2.2" stroke-linecap="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
                </div>
                <div class="civix-cat-title-text">Water Supply <span class="civix-arrow-accent">&rsaquo;</span></div>
                <p class="civix-cat-subtitle-text">No water, leakage, pressure</p>
              </a>

              <a href="?id=civix_report_issue&cat=Electricity" class="civix-cat-pill-card">
                <div class="civix-cat-bubble cat-elec">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2" stroke-linecap="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <div class="civix-cat-title-text">Electricity <span class="civix-arrow-accent">&rsaquo;</span></div>
                <p class="civix-cat-subtitle-text">Power outage, street lights</p>
              </a>

              <a href="?id=civix_report_issue&cat=Roads" class="civix-cat-pill-card">
                <div class="civix-cat-bubble cat-roads">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="2.2" stroke-linecap="round"><path d="M4 19L9 5M20 19L15 5M12 8V11M12 15V17"/></svg>
                </div>
                <div class="civix-cat-title-text">Roads <span class="civix-arrow-accent">&rsaquo;</span></div>
                <p class="civix-cat-subtitle-text">Potholes, surface damage</p>
              </a>

              <a href="?id=civix_report_issue&cat=Drainage" class="civix-cat-pill-card">
                <div class="civix-cat-bubble cat-drain">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.2" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>
                </div>
                <div class="civix-cat-title-text">Drainage <span class="civix-arrow-accent">&rsaquo;</span></div>
                <p class="civix-cat-subtitle-text">Blockage, overflow, cleaning</p>
              </a>

              <a href="?id=civix_report_issue&cat=Waterlogging" class="civix-cat-pill-card">
                <div class="civix-cat-bubble cat-flood">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#9333EA" stroke-width="2.2" stroke-linecap="round"><path d="M2 12c2.5-3 5-3 7.5 0s5 3 7.5 0 5-3 7.5 0M2 17c2.5-3 5-3 7.5 0s5 3 7.5 0 5-3 7.5 0"/></svg>
                </div>
                <div class="civix-cat-title-text">Waterlogging <span class="civix-arrow-accent">&rsaquo;</span></div>
                <p class="civix-cat-subtitle-text">Rainwater, flooding pools</p>
              </a>
            </div>
          </div>

          <!-- 4. RECENT COMPLAINTS WITH AUTHENTIC DEFECT PHOTOS -->
          <div class="civix-white-box">
            <div class="civix-box-header civix-flex-split">
              <div>
                <h2 class="civix-box-title">Recent Complaints</h2>
                <p class="civix-box-subtitle">Here are your latest reported issues</p>
              </div>
              <a href="?id=civix_my_cases" class="civix-view-all-button">View All &rarr;</a>
            </div>

            <div class="civix-complaint-stack">
              <a ng-repeat="item in c.data.recentCases" href="?id=civix_track_case&sys_id={{item.sys_id}}" class="civix-complaint-entry">
                <!-- Defect Photo Thumbnail -->
                <div class="civix-entry-photo-thumb">
                  <img ng-src="{{item.photoUrl}}" alt="{{item.short_description}}" class="civix-entry-thumb-img" />
                </div>
                <div class="civix-entry-info">
                  <span class="civix-entry-ticket-id">{{item.number}}</span>
                  <h4 class="civix-entry-headline">{{item.short_description}}</h4>
                  <div class="civix-entry-meta">
                    <span>
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                      {{item.location}}
                    </span>
                    <span>
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                      {{item.date}}
                    </span>
                  </div>
                </div>
                <div class="civix-entry-badge-col">
                  <span class="civix-badge-pill-status" ng-class="'pill-' + item.statusClass">{{item.status}}</span>
                  <span class="civix-entry-arrow">&rsaquo;</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <!-- RIGHT SIDE PANEL (MAP + ALERTS + CIVIC AI ASSISTANT) -->
        <div class="civix-dash-side-col">
          
          <!-- ISSUE MAP (DETAILED REALISTIC MAP WITH RADAR PULSE & CONTROLS) -->
          <div class="civix-white-box civix-map-panel">
            <div class="civix-box-header civix-flex-split">
              <h2 class="civix-box-title">Issue Map</h2>
              <a href="?id=civix_landing#services" class="civix-view-all-button">View Full Map &rarr;</a>
            </div>
            <div class="civix-map-stage-ref2">
              <div class="civix-map-img-canvas">
                <!-- SVG Vector Roads & Chennai Coast -->
                <svg viewBox="0 0 360 250" class="civix-map-vector-full" xmlns="http://www.w3.org/2000/svg">
                  <!-- Land Background -->
                  <rect width="360" height="250" fill="#E8EEF5"/>
                  <!-- Bay of Bengal Coastline -->
                  <path d="M270,0 Q290,90 260,160 Q240,210 275,250 L360,250 L360,0 Z" fill="#BAE6FD"/>
                  <text x="280" y="130" font-size="16" font-weight="800" fill="#0284C7" opacity="0.8">Chennai</text>
                  
                  <!-- City Arterials / Highways -->
                  <path d="M0,45 Q120,40 270,45" stroke="#CBD5E1" stroke-width="4" fill="none"/>
                  <path d="M0,105 Q140,95 260,105" stroke="#CBD5E1" stroke-width="5" fill="none"/>
                  <path d="M0,175 Q130,165 250,175" stroke="#CBD5E1" stroke-width="4" fill="none"/>
                  <path d="M110,0 Q120,120 100,250" stroke="#CBD5E1" stroke-width="5" fill="none"/>
                  <path d="M190,0 Q180,110 200,250" stroke="#CBD5E1" stroke-width="4" fill="none"/>
                  
                  <!-- Secondary Grid Lines -->
                  <line x1="50" y1="0" x2="50" y2="250" stroke="#E2E8F0" stroke-width="2"/>
                  <line x1="150" y1="0" x2="150" y2="250" stroke="#E2E8F0" stroke-width="2"/>
                  <line x1="230" y1="0" x2="230" y2="250" stroke="#E2E8F0" stroke-width="2"/>
                  <line x1="0" y1="75" x2="270" y2="75" stroke="#E2E8F0" stroke-width="2"/>
                  <line x1="0" y1="140" x2="255" y2="140" stroke="#E2E8F0" stroke-width="2"/>
                  <line x1="0" y1="210" x2="260" y2="210" stroke="#E2E8F0" stroke-width="2"/>

                  <!-- Locality Labels -->
                  <text x="145" y="70" font-size="10.5" font-weight="700" fill="#475569">Anna Nagar</text>
                  <text x="75" y="140" font-size="10.5" font-weight="700" fill="#475569">T. Nagar</text>
                  <text x="105" y="210" font-size="10.5" font-weight="700" fill="#475569">Velachery</text>
                  <text x="185" y="220" font-size="10.5" font-weight="700" fill="#475569">Adyar</text>

                  <!-- T. Nagar Live Pulse Radar -->
                  <circle cx="140" cy="135" r="30" fill="#0066FF" opacity="0.18" class="civix-pulse-ring"/>
                  <circle cx="140" cy="135" r="16" fill="#0066FF" opacity="0.38"/>
                  <circle cx="140" cy="135" r="7" fill="#0066FF"/>

                  <!-- Incident Pin Markers -->
                  <g transform="translate(145, 60)">
                    <circle cx="0" cy="0" r="7" fill="#0284C7" stroke="#FFFFFF" stroke-width="2"/>
                  </g>
                  <g transform="translate(85, 145)">
                    <circle cx="0" cy="0" r="7" fill="#DC2626" stroke="#FFFFFF" stroke-width="2"/>
                  </g>
                  <g transform="translate(160, 195)">
                    <circle cx="0" cy="0" r="7" fill="#EAB308" stroke="#FFFFFF" stroke-width="2"/>
                  </g>
                  <g transform="translate(210, 200)">
                    <circle cx="0" cy="0" r="7" fill="#16A34A" stroke="#FFFFFF" stroke-width="2"/>
                  </g>
                </svg>

                <!-- Map UI Float Controls -->
                <div class="civix-map-controls-deck">
                  <button type="button" class="civix-map-ctrl-btn" title="Zoom In">+</button>
                  <button type="button" class="civix-map-ctrl-btn" title="Zoom Out">&minus;</button>
                  <button type="button" class="civix-map-ctrl-btn" title="Locate Me">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="2.5"><circle cx="12" cy="12" r="7"/><line x1="12" y1="1" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="1" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="23" y2="12"/></svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- NEARBY ALERTS -->
          <div class="civix-white-box" id="alerts">
            <div class="civix-box-header civix-flex-split">
              <h2 class="civix-box-title">Nearby Alerts</h2>
              <a href="?id=civix_landing#services" class="civix-view-all-button">View All &rarr;</a>
            </div>
            <div class="civix-alert-items-list">
              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-red">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                </div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Road maintenance work in T. Nagar</h4>
                  <div class="civix-alert-foot-meta">500 m &bull; Today</div>
                </div>
              </div>

              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-gold">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Scheduled power maintenance - Anna Nagar</h4>
                  <div class="civix-alert-foot-meta">1.2 km &bull; Tomorrow</div>
                </div>
              </div>

              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-purple">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#9333EA" stroke-width="2.5"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
                </div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Possible waterlogging in Velachery</h4>
                  <div class="civix-alert-foot-meta">2.3 km &bull; Today</div>
                </div>
              </div>

              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-blue">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                </div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Low water pressure reported</h4>
                  <div class="civix-alert-foot-meta">3.1 km &bull; Today</div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </main>
</div>
"""

HOME_TEMPLATE = HOME_TEMPLATE_RAW.replace("__SIDEBAR__", get_sidebar_html("dashboard")).replace("__TOPBAR__", get_topbar_html())

HOME_CSS = BASE_SHELL_CSS + """
/* 2-COLUMN BALANCED DASHBOARD LAYOUT */
.civix-dashboard-2col-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.85fr) minmax(360px, 1.15fr);
  gap: 24px;
  width: 100%;
  max-width: 1720px;
  align-items: start;
}

@media (max-width: 1200px) {
  .civix-dashboard-2col-layout { grid-template-columns: 1fr; }
}

.civix-dash-main-col {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.civix-dash-side-col {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* BANNER GRID: HERO WELCOME + RIVER PROMO */
.civix-banner-grid-ref2 {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 18px;
  margin-bottom: 20px;
}
@media (max-width: 1000px) {
  .civix-banner-grid-ref2 { grid-template-columns: 1fr; }
}

.civix-hero-welcome-card-ref2 {
  background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 55%, #F8FAFC 100%);
  border: 1px solid #BAE6FD;
  border-radius: 18px;
  padding: 26px 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 102, 255, 0.05);
}

.civix-hero-skyline-pano {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 440px;
  background: url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1000&auto=format&fit=crop&q=80') top right/cover no-repeat;
  opacity: 0.16;
  pointer-events: none;
}

.civix-hero-big-greeting {
  font-size: 26px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1.2;
  margin: 0 0 6px 0;
}
.civix-name-gradient { color: #0066FF; }
.civix-hero-tagline-main { font-size: 13.5px; font-weight: 600; color: #334155; margin: 0; }
.civix-hero-tagline-sub { font-size: 12px; color: #64748B; margin: 2px 0 0 0; }

.civix-glass-weather-widget-ref2 {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(16px);
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 12px 18px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.06);
  z-index: 2;
  min-width: 175px;
}
.civix-weather-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  color: #0F172A;
  margin-bottom: 6px;
}
.civix-weather-split {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.civix-temp-reading { font-size: 22px; font-weight: 800; color: #0F172A; }
.civix-weather-condition { display: block; font-size: 11px; color: #64748B; }

/* WATERFRONT RIVER PROMO CARD */
.civix-promo-river-card {
  border-radius: 18px;
  overflow: hidden;
  position: relative;
  min-height: 140px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.06);
}
.civix-promo-river-bg {
  position: absolute;
  inset: 0;
  background: url('https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=600&auto=format&fit=crop&q=80') center/cover no-repeat;
}
.civix-promo-river-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.2) 0%, rgba(15, 23, 42, 0.8) 100%);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 18px 20px;
}
.civix-promo-river-title {
  color: #FFFFFF;
  font-size: 17px;
  font-weight: 800;
  line-height: 1.25;
  margin: 0 0 6px 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.4);
}
.civix-promo-river-bar {
  width: 40px;
  height: 3px;
  background: #38BDF8;
  border-radius: 2px;
}

/* 4 KPI CARDS IN A ROW */
.civix-kpi-deck-4cols {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 20px;
}
@media (max-width: 1100px) {
  .civix-kpi-deck-4cols { grid-template-columns: repeat(2, 1fr); }
}

.civix-kpi-tile {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 16px 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  text-decoration: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.civix-kpi-tile:hover {
  transform: translateY(-3px);
  text-decoration: none;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}
.civix-kpi-icon-bubble {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.bg-blue-subtle { background: #EFF6FF; }
.bg-green-subtle { background: #ECFDF5; }
.bg-gold-subtle { background: #FFFBEB; }
.bg-red-subtle { background: #FEF2F2; }

.civix-kpi-details { flex-grow: 1; min-width: 0; }
.civix-kpi-value-row { display: flex; justify-content: space-between; align-items: baseline; }
.civix-kpi-count { font-size: 24px; font-weight: 800; color: #0F172A; }
.civix-kpi-arrow-cue { font-size: 18px; color: #94A3B8; }
.civix-kpi-label-text { font-size: 12.5px; font-weight: 600; color: #64748B; margin: 2px 0; white-space: nowrap; }
.civix-kpi-trend-badge { font-size: 11px; font-weight: 600; }
.trend-green { color: #16A34A; }
.trend-neutral { color: #B45309; }
.trend-red { color: #DC2626; }

/* WHITE BOX */
.civix-white-box {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 20px 22px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.civix-box-header { margin-bottom: 16px; }
.civix-box-title { font-size: 16.5px; font-weight: 700; color: #0F172A; margin: 0 0 3px 0; }
.civix-box-subtitle { font-size: 12.5px; color: #64748B; margin: 0; }
.civix-flex-split { display: flex; justify-content: space-between; align-items: center; }
.civix-view-all-button { font-size: 12.5px; font-weight: 700; color: #0066FF; text-decoration: none; }

/* 5 CATEGORIES */
.civix-category-cards-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
}
@media (max-width: 900px) {
  .civix-category-cards-grid { grid-template-columns: repeat(3, 1fr); }
}
.civix-cat-pill-card {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 16px 8px;
  text-align: center;
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.civix-cat-pill-card:hover {
  background: #FFFFFF;
  border-color: #0066FF;
  transform: translateY(-3px);
  box-shadow: 0 8px 18px rgba(0, 102, 255, 0.1);
  text-decoration: none;
}
.civix-cat-bubble {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}
.cat-water { background: #E0F2FE; }
.cat-elec { background: #FEF3C7; }
.cat-roads { background: #F1F5F9; }
.cat-drain { background: #DCFCE7; }
.cat-flood { background: #F3E8FF; }
.civix-cat-title-text { font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 3px; }
.civix-arrow-accent { color: #94A3B8; }
.civix-cat-subtitle-text { font-size: 10px; color: #64748B; margin: 0; line-height: 1.3; }

/* COMPLAINTS LIST WITH PHOTO THUMBNAILS */
.civix-complaint-stack { display: flex; flex-direction: column; gap: 10px; }
.civix-complaint-entry {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 14px;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  text-decoration: none;
  background: #FFFFFF;
  transition: all 0.15s;
}
.civix-complaint-entry:hover {
  background: #F8FAFC;
  border-color: #0066FF;
  text-decoration: none;
}
.civix-entry-photo-thumb {
  width: 58px;
  height: 52px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  border: 1px solid #E2E8F0;
  background: #EFF6FF;
}
.civix-entry-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.civix-entry-info { flex-grow: 1; min-width: 0; }
.civix-entry-ticket-id { font-size: 11px; font-weight: 700; color: #0066FF; }
.civix-entry-headline {
  font-size: 13.5px;
  font-weight: 700;
  color: #0F172A;
  margin: 2px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.civix-entry-meta { display: flex; gap: 14px; font-size: 11.5px; color: #64748B; align-items:center; }
.civix-entry-badge-col { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.civix-badge-pill-status {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
}
.pill-in-progress { background: #FEF3C7; color: #B45309; }
.pill-resolved { background: #DCFCE7; color: #15803D; }
.pill-awaiting { background: #FEE2E2; color: #B91C1C; }
.civix-entry-arrow { font-size: 18px; color: #94A3B8; }

/* MAP */
.civix-map-stage-ref2 {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
}
.civix-map-img-canvas { position: relative; width: 100%; }
.civix-map-vector-full { width: 100%; height: auto; display: block; border-radius: 12px; }
.civix-map-controls-deck {
  position: absolute;
  right: 12px;
  bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.civix-map-ctrl-btn {
  width: 26px;
  height: 26px;
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 700;
  color: #334155;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.06);
}
.civix-pulse-ring {
  transform-origin: 140px 135px;
  animation: pulse-wave 2s infinite ease-out;
}
@keyframes pulse-wave {
  0% { r: 10px; opacity: 0.6; }
  100% { r: 40px; opacity: 0; }
}

/* ALERTS */
.civix-alert-items-list { display: flex; flex-direction: column; gap: 10px; }
.civix-alert-item-card {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  padding: 10px 12px;
  border-radius: 10px;
  background: #F8FAFC;
  border: 1px solid #F1F5F9;
}
.civix-alert-icon-ring {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.alert-red { background: #FEE2E2; }
.alert-gold { background: #FEF3C7; }
.alert-purple { background: #F3E8FF; }
.alert-blue { background: #EFF6FF; }
.civix-alert-info-side { flex-grow: 1; min-width: 0; }
.civix-alert-item-title { font-size: 12px; font-weight: 700; color: #0F172A; margin: 0 0 2px 0; }
.civix-alert-foot-meta { font-size: 11px; color: #64748B; }

/* CIVIC AI ASSISTANT */
.civix-bot-widget-frame {
  border: 1px solid #BFDBFE;
  background: #F0F9FF;
}
.civix-bot-widget-header {
  border-bottom: 1px solid #BAE6FD;
  padding-bottom: 10px;
  margin-bottom: 12px;
}
.civix-bot-label-group {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13.5px;
  color: #0F172A;
}
.civix-mini-action-dot { font-size: 14px; color: #64748B; margin-left: 4px; cursor: pointer; }
.civix-robot-mascot-box { text-align: center; margin-bottom: 8px; }
.civix-chat-speech-bubble {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 10px 14px;
  margin-bottom: 12px;
  font-size: 12px;
  color: #1E293B;
  box-shadow: 0 2px 6px rgba(0,0,0,0.03);
}
.civix-chat-speech-bubble p { margin: 0; }
.civix-suggested-prompts-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}
.civix-prompt-pill-btn {
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  padding: 7px 12px;
  font-size: 11.5px;
  font-weight: 600;
  color: #0F172A;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.15s;
}
.civix-prompt-pill-btn:hover {
  background: #0066FF;
  color: #FFFFFF;
  border-color: #0066FF;
}
.civix-chat-input-toolbar {
  display: flex;
  gap: 6px;
}
.civix-chat-text-box {
  flex-grow: 1;
  height: 36px;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  padding: 0 10px;
  font-size: 12px;
  outline: none;
}
.civix-chat-text-box:focus { border-color: #0066FF; }
.civix-chat-send-btn {
  width: 36px;
  height: 36px;
  background: #0066FF;
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.civix-bot-caption-notice {
  font-size: 10.5px;
  color: #64748B;
  text-align: center;
  margin-top: 8px;
}
"""

HOME_CLIENT_SCRIPT = """
function($scope, $timeout) {
  var c = this;

  c.langOpen = false;
  c.selectedLang = 'en';
  c.currentLangDisplay = 'भारतीय भाषाएं / Language';

  c.languages = [
    { code: 'en', name: 'English', native: 'English', prefix: 'En', bg: '#0066FF' },
    { code: 'hi', name: 'Hindi', native: 'हिन्दी', prefix: 'हि', bg: '#EA580C' },
    { code: 'ta', name: 'Tamil', native: 'தமிழ்', prefix: 'த', bg: '#0284C7' },
    { code: 'te', name: 'Telugu', native: 'తెలుగు', prefix: 'తె', bg: '#16A34A' },
    { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ', prefix: 'ಕ', bg: '#9333EA' },
    { code: 'ml', name: 'Malayalam', native: 'മലയാളം', prefix: 'മ', bg: '#0D9488' },
    { code: 'bn', name: 'Bengali', native: 'বাংলা', prefix: 'বা', bg: '#DC2626' },
    { code: 'mr', name: 'Marathi', native: 'मराठी', prefix: 'म', bg: '#E11D48' },
    { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી', prefix: 'ગુ', bg: '#D97706' }
  ];

  c.toggleLang = function() {
    c.langOpen = !c.langOpen;
  };

  c.chooseLang = function(l) {
    c.selectedLang = l.code;
    c.currentLangDisplay = l.native + ' / ' + l.name;
    c.langOpen = false;
  };

  c.quickPrompt = function(msg) {
    c.userMsgInput = msg;
    c.submitChatMessage();
  };

  c.onChatEnter = function($event) {
    if ($event.keyCode === 13) {
      c.submitChatMessage();
    }
  };

  c.submitChatMessage = function() {
    if (!c.userMsgInput) return;
    var userText = c.userMsgInput;
    c.userMsgInput = '';
    alert('Civic AI Assistant responded to: ' + userText);
  };
}
"""

HOME_SERVER_SCRIPT = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  data.citizenName = 'Priya Sharma';

  data.counts = {
    total: 12,
    resolved: 8,
    in_progress: 3,
    awaiting: 1
  };

  data.recentCases = [
    {
      sys_id: 'c1',
      number: 'CIVIX-2024-00123',
      short_description: 'Water leakage on 3rd Main Road',
      location: 'Adyar, Chennai',
      date: '15 Nov 2024, 10:24 AM',
      category: 'Water Supply',
      status: 'In Progress',
      statusClass: 'in-progress',
      photoUrl: 'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=300&auto=format&fit=crop&q=80'
    },
    {
      sys_id: 'c2',
      number: 'CIVIX-2024-00118',
      short_description: 'Street light not working near Anna Nagar Park',
      location: 'Anna Nagar, Chennai',
      date: '10 Nov 2024, 06:12 PM',
      category: 'Electricity',
      status: 'Resolved',
      statusClass: 'resolved',
      photoUrl: 'https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=300&auto=format&fit=crop&q=80'
    },
    {
      sys_id: 'c3',
      number: 'CIVIX-2024-00110',
      short_description: 'Pothole near 100 Feet Road',
      location: 'T. Nagar, Chennai',
      date: '05 Nov 2024, 02:30 PM',
      category: 'Roads',
      status: 'Resolved',
      statusClass: 'resolved',
      photoUrl: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=300&auto=format&fit=crop&q=80'
    },
    {
      sys_id: 'c4',
      number: 'CIVIX-2024-00102',
      short_description: 'Drainage overflow in residential area',
      location: 'Velachery, Chennai',
      date: '28 Oct 2024, 09:15 AM',
      category: 'Drainage',
      status: 'Awaiting Action',
      statusClass: 'awaiting',
      photoUrl: 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=300&auto=format&fit=crop&q=80'
    }
  ];
})();
"""

# ==============================================================================
# WIDGET 2: CASE TRACKING FULL IMPLEMENTATION (civix_track_case)
# ==============================================================================
TRACK_TEMPLATE_RAW = """
<div class="civix-app-shell">
  __SIDEBAR__

  <main class="civix-main-column">
    __TOPBAR__

    <div class="civix-content-area">
      <!-- Breadcrumb Navigation -->
      <div class="civix-track-breadcrumb-row">
        <a href="?id=civix_my_cases" class="civix-track-back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
          <span>Back to My Complaints</span>
        </a>
      </div>

      <!-- MAIN CASE TRACKING CONTAINER -->
      <div class="civix-track-two-col-layout">
        
        <!-- LEFT COLUMN: SUMMARY, TIMELINE, ACTIVITY, EVIDENCE -->
        <div class="civix-track-main-flow">
          
          <!-- SECTION 2: CASE SUMMARY CARD -->
          <div class="civix-track-summary-card">
            <div class="civix-summary-top-row">
              <div class="civix-summary-badge-group">
                <span class="civix-badge-ticket-num">{{c.case.number}}</span>
                <span class="civix-badge-cat-label">{{c.case.category}}</span>
              </div>
              <div>
                <span class="civix-badge-pill-status" ng-class="'pill-' + c.case.statusClass">
                  {{c.case.state}}
                </span>
              </div>
            </div>

            <h1 class="civix-summary-issue-title">{{c.case.short_description}}</h1>

            <div class="civix-summary-meta-grid">
              <div class="civix-summary-meta-item">
                <span class="civix-meta-label">Location</span>
                <span class="civix-meta-val">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  {{c.case.location}}
                </span>
              </div>

              <div class="civix-summary-meta-item">
                <span class="civix-meta-label">Date Reported</span>
                <span class="civix-meta-val">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                  {{c.case.opened_at}}
                </span>
              </div>

              <div class="civix-summary-meta-item">
                <span class="civix-meta-label">Expected Resolution</span>
                <span class="civix-meta-val text-primary" style="font-weight:700;">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  {{c.case.eta}}
                </span>
              </div>
            </div>
          </div>

          <!-- SECTION 3: VISUAL PROGRESS TIMELINE (6 CHRONOLOGICAL STAGES) -->
          <div class="civix-panel-card civix-timeline-card">
            <h3 class="civix-panel-card-title">Municipal Resolution Lifecycle</h3>
            <p class="civix-panel-card-subtitle">Chronological progress verified by the municipal operations center.</p>

            <div class="civix-stepper-track-wrap">
              <div class="civix-stepper-stage-col" ng-repeat="st in c.steps" ng-class="{'completed': st.num < c.case.stepNum, 'active': st.num === c.case.stepNum, 'upcoming': st.num > c.case.stepNum}">
                <div class="civix-stepper-circle-node">
                  <span ng-if="st.num < c.case.stepNum">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                  </span>
                  <span ng-if="st.num >= c.case.stepNum">{{st.num}}</span>
                </div>
                <div class="civix-stepper-labels">
                  <span class="civix-stepper-label-title">{{st.label}}</span>
                  <span class="civix-stepper-label-desc">{{st.desc}}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- SECTION 4: STATUS UPDATES & ACTIVITY HISTORY -->
          <div class="civix-panel-card">
            <h3 class="civix-panel-card-title">Status Updates & Activity History</h3>
            <p class="civix-panel-card-subtitle">Official public updates from ward operations and maintenance crews.</p>

            <div class="civix-activity-feed-stack">
              <div class="civix-activity-feed-item" ng-repeat="act in c.case.activities">
                <div class="civix-activity-pin-icon" ng-class="'bg-' + act.type">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <div class="civix-activity-content">
                  <div class="civix-activity-head-row">
                    <strong>{{act.title}}</strong>
                    <span class="civix-activity-time">{{act.time}}</span>
                  </div>
                  <p class="civix-activity-msg">{{act.message}}</p>
                  <div class="civix-activity-officer" ng-if="act.officer">
                    <span>Officer in Charge: <strong>{{act.officer}}</strong> ({{act.team}})</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- SECTION 5: ISSUE DETAILS & EVIDENCE -->
          <div class="civix-panel-card">
            <h3 class="civix-panel-card-title">Issue Details & Evidence</h3>
            
            <div class="civix-details-sub-grid">
              <div>
                <h4 class="civix-detail-heading">Original Complaint Description</h4>
                <p class="civix-detail-body">{{c.case.description}}</p>

                <h4 class="civix-detail-heading" style="margin-top:16px;">Engineer Field Inspection Notes</h4>
                <div class="civix-engineer-notes-box">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                  <span>{{c.case.resolution_notes}}</span>
                </div>
              </div>

              <!-- Evidence Photo Section -->
              <div ng-if="c.case.photoUrl">
                <h4 class="civix-detail-heading">Citizen-Uploaded Evidence</h4>
                <div class="civix-evidence-photo-box">
                  <img ng-src="{{c.case.photoUrl}}" alt="Defect Evidence" class="civix-evidence-img" />
                  <div class="civix-evidence-tag">✓ Geo-Verified Municipal Photo</div>
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- RIGHT COLUMN: CITIZEN ACTIONS & SUPPORT -->
        <div class="civix-track-side-panel">
          
          <!-- SECTION 7: CITIZEN ACTIONS BAR -->
          <div class="civix-white-box civix-actions-panel">
            <h3 class="civix-panel-card-title" style="margin-bottom:14px;">Citizen Actions</h3>
            
            <div class="civix-actions-btn-stack">
              <button type="button" class="btn btn-default civix-action-btn" ng-click="c.doAction('view_location')">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <span>View Reported Location</span>
              </button>

              <button type="button" class="btn btn-default civix-action-btn" ng-click="c.doAction('add_info')">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                <span>Add Additional Information</span>
              </button>

              <button type="button" class="btn btn-default civix-action-btn text-danger" ng-if="c.case.state === 'Resolved' || c.case.state === 'Closed'" ng-click="c.doAction('not_fixed')">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
                <span>Report Not Fixed (Reopen)</span>
              </button>

              <button type="button" class="btn btn-default civix-action-btn" ng-click="c.doAction('feedback')">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                <span>Provide Feedback & Rating</span>
              </button>

              <a href="?id=civix_landing#trust" class="btn btn-primary civix-action-btn" style="color:#FFFFFF; text-decoration:none;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>
                <span>Get Help / Contact Officer</span>
              </a>
            </div>
          </div>

          <!-- Ward Helpdesk Card -->
          <div class="civix-white-box" style="background:#F0F9FF; border-color:#BAE6FD;">
            <h4 style="font-size:14px; font-weight:700; color:#0369A1; margin-top:0;">Ward Operations Center</h4>
            <p style="font-size:12px; color:#334155; margin-bottom:12px;">Assigned to <strong>Ward 18 (Adyar) Rapid Response Unit</strong>. Emergency hotline available 24/7.</p>
            <div style="font-size:12px; color:#0369A1; font-weight:700;">
              Hotline: 1800-425-0018
            </div>
          </div>

        </div>

      </div>
    </div>
  </main>
</div>
"""

TRACK_TEMPLATE = TRACK_TEMPLATE_RAW.replace("__SIDEBAR__", get_sidebar_html("complaints")).replace("__TOPBAR__", get_topbar_html())

TRACK_CSS = BASE_SHELL_CSS + """
.civix-track-breadcrumb-row {
  margin-bottom: 18px;
}
.civix-track-back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13.5px;
  font-weight: 700;
  color: #0066FF;
  text-decoration: none;
  transition: all 0.15s;
}
.civix-track-back-link:hover { text-decoration: none; color: #0052CC; transform: translateX(-2px); }

.civix-track-two-col-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 340px;
  gap: 22px;
  width: 100%;
  max-width: 1720px;
  align-items: start;
}
@media (max-width: 1100px) {
  .civix-track-two-col-layout { grid-template-columns: 1fr; }
}

.civix-track-main-flow {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
}
.civix-track-side-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
}

/* SECTION 2: SUMMARY CARD */
.civix-track-summary-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 24px 26px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}
.civix-summary-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.civix-summary-badge-group {
  display: flex;
  align-items: center;
  gap: 10px;
}
.civix-badge-ticket-num {
  background: #0F172A;
  color: #FFFFFF;
  font-size: 12.5px;
  font-weight: 800;
  letter-spacing: 0.5px;
  padding: 5px 12px;
  border-radius: 8px;
}
.civix-badge-cat-label {
  background: #EFF6FF;
  color: #0066FF;
  font-size: 12px;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 8px;
}

.civix-summary-issue-title {
  font-size: 24px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1.25;
  margin: 0 0 18px 0;
}

.civix-summary-meta-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding-top: 16px;
  border-top: 1px solid #F1F5F9;
}
@media (max-width: 768px) {
  .civix-summary-meta-grid { grid-template-columns: 1fr; }
}

.civix-summary-meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.civix-meta-label {
  font-size: 11.5px;
  font-weight: 600;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.civix-meta-val {
  font-size: 13.5px;
  font-weight: 600;
  color: #0F172A;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* SECTION 3: VISUAL TIMELINE STEPPER */
.civix-timeline-card {
  padding: 24px 26px;
}
.civix-panel-card-title {
  font-size: 17px;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 4px 0;
}
.civix-panel-card-subtitle {
  font-size: 12.5px;
  color: #64748B;
  margin: 0 0 24px 0;
}

.civix-stepper-track-wrap {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
  position: relative;
}
@media (max-width: 900px) {
  .civix-stepper-track-wrap { grid-template-columns: repeat(3, 1fr); row-gap: 20px; }
}

.civix-stepper-stage-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
}

/* Connecting track line between stepper stages */
.civix-stepper-stage-col::after {
  content: '';
  position: absolute;
  top: 19px;
  left: 50%;
  width: calc(100% + 12px);
  height: 4px;
  background: #E2E8F0;
  z-index: 1;
}

.civix-stepper-stage-col:last-child::after {
  display: none !important;
}

.civix-stepper-stage-col.completed::after {
  background: #16A34A;
}

@media (max-width: 900px) {
  .civix-stepper-stage-col::after {
    display: none;
  }
}

.civix-stepper-circle-node {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 13px;
  margin-bottom: 10px;
  position: relative;
  z-index: 2;
  transition: all 0.2s;
}

.civix-stepper-stage-col.completed .civix-stepper-circle-node {
  background: #16A34A;
  color: #FFFFFF;
}
.civix-stepper-stage-col.active .civix-stepper-circle-node {
  background: #0066FF;
  color: #FFFFFF;
  box-shadow: 0 0 0 4px rgba(0, 102, 255, 0.25);
  animation: pulse-active-step 1.8s infinite;
}
.civix-stepper-stage-col.upcoming .civix-stepper-circle-node {
  background: #FFFFFF;
  color: #94A3B8;
  border: 2px solid #CBD5E1;
}

@keyframes pulse-active-step {
  0% { box-shadow: 0 0 0 0 rgba(0, 102, 255, 0.4); }
  70% { box-shadow: 0 0 0 8px rgba(0, 102, 255, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 102, 255, 0); }
}

.civix-stepper-labels {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.civix-stepper-label-title {
  font-size: 12.5px;
  font-weight: 700;
  color: #0F172A;
}
.civix-stepper-stage-col.upcoming .civix-stepper-label-title { color: #94A3B8; }
.civix-stepper-label-desc {
  font-size: 10.5px;
  color: #64748B;
  line-height: 1.3;
}

/* SECTION 4: ACTIVITY FEED */
.civix-activity-feed-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 14px;
}
.civix-activity-feed-item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: 14px 16px;
  background: #F8FAFC;
  border: 1px solid #F1F5F9;
  border-radius: 12px;
}
.civix-activity-pin-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}
.bg-status-change { background: #0066FF; }
.bg-comment { background: #10B981; }
.bg-dispatch { background: #F59E0B; }

.civix-activity-content { flex-grow: 1; min-width: 0; }
.civix-activity-head-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  font-size: 13px;
  color: #0F172A;
}
.civix-activity-time { font-size: 11px; color: #94A3B8; font-weight: 600; }
.civix-activity-msg { font-size: 13px; color: #334155; margin: 0 0 6px 0; line-height: 1.5; }
.civix-activity-officer { font-size: 11.5px; color: #64748B; }

/* SECTION 5: DETAILS & EVIDENCE */
.civix-details-sub-grid {
  display: grid;
  grid-template-columns: 1fr 240px;
  gap: 20px;
}
@media (max-width: 768px) {
  .civix-details-sub-grid { grid-template-columns: 1fr; }
}

.civix-detail-heading {
  font-size: 13px;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 6px 0;
}
.civix-detail-body {
  font-size: 13.5px;
  color: #334155;
  line-height: 1.6;
  margin: 0;
}
.civix-engineer-notes-box {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  background: #EFF6FF;
  border-left: 4px solid #0066FF;
  padding: 12px 14px;
  border-radius: 6px;
  font-size: 13px;
  color: #1E40AF;
  line-height: 1.5;
}

.civix-evidence-photo-box {
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.civix-evidence-img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  display: block;
}
.civix-evidence-tag {
  background: #F8FAFC;
  padding: 8px 10px;
  font-size: 11px;
  font-weight: 700;
  color: #16A34A;
  text-align: center;
  border-top: 1px solid #E2E8F0;
}

/* SECTION 7: CITIZEN ACTIONS */
.civix-actions-btn-stack {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.civix-action-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  text-align: left;
  transition: all 0.15s;
}
.civix-action-btn:hover { transform: translateY(-2px); }

.pill-in-progress { background: #FEF3C7; color: #B45309; }
.pill-resolved { background: #DCFCE7; color: #15803D; }
.pill-awaiting { background: #FEE2E2; color: #B91C1C; }
"""

TRACK_CLIENT_SCRIPT = """
function($scope, $location, $timeout) {
  var c = this;

  c.langOpen = false;
  c.selectedLang = 'en';
  c.currentLangDisplay = 'भारतीय भाषाएं / Language';

  c.languages = [
    { code: 'en', name: 'English', native: 'English', prefix: 'En', bg: '#0066FF' }
  ];

  c.toggleLang = function() {
    c.langOpen = !c.langOpen;
  };

  c.chooseLang = function(l) {
    c.selectedLang = l.code;
    c.currentLangDisplay = l.native + ' / ' + l.name;
    c.langOpen = false;
  };

  c.steps = [
    { num: 1, label: 'Submitted', desc: 'Complaint recorded with case number' },
    { num: 2, label: 'Under Review', desc: 'Operations team assessing defect' },
    { num: 3, label: 'Assigned', desc: 'Assigned to Ward Field Crew' },
    { num: 4, label: 'In Progress', desc: 'Active repair and restoration work' },
    { num: 5, label: 'Resolved', desc: 'Repairs verified by ward engineer' },
    { num: 6, label: 'Closed', desc: 'Quality audit & closure completed' }
  ];

  // Cases database for demo and instant client response
  var casesDb = {
    'c1': {
      sys_id: 'c1',
      number: 'CIVIX-2024-00123',
      short_description: 'Water leakage on 3rd Main Road',
      category: 'Water Supply',
      location: 'Opposite Post Office, 3rd Main Road, Adyar, Ward 18, Chennai',
      opened_at: '15 Nov 2024, 10:24 AM',
      state: 'In Progress',
      statusClass: 'in-progress',
      stepNum: 4,
      eta: '18 Nov 2024, 05:00 PM (Target: 72 hrs)',
      description: 'High pressure potable water pipeline rupture leaking onto pedestrian footpath and causing severe water pooling near crossway.',
      resolution_notes: 'Ward 18 pipeline engineering crew dispatched with excavator. Trenching and bypass pipe replacement currently underway.',
      photoUrl: 'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=600&auto=format&fit=crop&q=80',
      activities: [
        {
          type: 'dispatch',
          title: 'Repair Crew Dispatched on Site',
          time: '15 Nov 2024, 02:45 PM',
          message: 'Trenching crew and replacement valve parts arrived at 3rd Main Road. Excavation in progress.',
          officer: 'S. Ramanathan',
          team: 'Ward 18 Hydraulic Works'
        },
        {
          type: 'status-change',
          title: 'Status changed to In Progress',
          time: '15 Nov 2024, 11:30 AM',
          message: 'Work order #WO-8912 created and scheduled for same-day repair by water board engineer.',
          officer: 'K. Balaji',
          team: 'Central Civic Operations'
        },
        {
          type: 'comment',
          title: 'Field Inspection Completed',
          time: '15 Nov 2024, 11:15 AM',
          message: 'Ward inspector verified 4-inch ductile iron pipe fracture. No contamination risk to drinking supply.',
          officer: 'V. Murugan',
          team: 'Ward 18 Junior Engineer'
        },
        {
          type: 'status-change',
          title: 'Complaint Registered & Ticket Generated',
          time: '15 Nov 2024, 10:24 AM',
          message: 'Citizen complaint logged through CIVIX AI mobile portal with verified GPS tag.',
          officer: 'Automated System',
          team: 'CIVIX AI Core'
        }
      ]
    },
    'c2': {
      sys_id: 'c2',
      number: 'CIVIX-2024-00118',
      short_description: 'Street light not working near Anna Nagar Park',
      category: 'Electricity',
      location: '12th Main Road, Anna Nagar West, Ward 8, Chennai',
      opened_at: '10 Nov 2024, 06:12 PM',
      state: 'Resolved',
      statusClass: 'resolved',
      stepNum: 5,
      eta: 'Resolved on 11 Nov 2024, 04:30 PM',
      description: 'LED street fixture #L-42 blinking erratically then went completely dark along school pedestrian zone.',
      resolution_notes: 'Blown capacitor replaced in LED luminaire fixture. Lighting circuit tested and certified working.',
      photoUrl: 'https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=600&auto=format&fit=crop&q=80',
      activities: [
        {
          type: 'status-change',
          title: 'Defect Resolved & Field Tested',
          time: '11 Nov 2024, 04:30 PM',
          message: 'Streetlight pole inspected and luminaire unit repaired. Illuminance verified at 25 lux standard.',
          officer: 'M. Anand',
          team: 'Ward 8 Electrical Division'
        },
        {
          type: 'status-change',
          title: 'Complaint Registered',
          time: '10 Nov 2024, 06:12 PM',
          message: 'Logged via CIVIX AI portal.',
          officer: 'Automated System',
          team: 'CIVIX AI Core'
        }
      ]
    },
    'c3': {
      sys_id: 'c3',
      number: 'CIVIX-2024-00110',
      short_description: 'Pothole near 100 Feet Road',
      category: 'Roads',
      location: 'Near Flyover Pillar 14, 100 Feet Road, T. Nagar, Ward 12, Chennai',
      opened_at: '05 Nov 2024, 02:30 PM',
      state: 'Resolved',
      statusClass: 'resolved',
      stepNum: 5,
      eta: 'Resolved on 07 Nov 2024, 06:00 PM',
      description: 'Deep road cavity approximately 2 feet diameter posing collision risk to two-wheelers.',
      resolution_notes: 'Asphalt cold-mix patching completed and steam-rolled flush with pavement.',
      photoUrl: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80',
      activities: [
        {
          type: 'status-change',
          title: 'Road Surface Restored',
          time: '07 Nov 2024, 06:00 PM',
          message: 'Patching work signed off by Ward 12 Roads Supervisor.',
          officer: 'R. Karthik',
          team: 'Ward 12 Road Maintenance'
        }
      ]
    },
    'c4': {
      sys_id: 'c4',
      number: 'CIVIX-2024-00102',
      short_description: 'Drainage overflow in residential area',
      category: 'Drainage',
      location: 'Lake View Street, Velachery, Ward 15, Chennai',
      opened_at: '28 Oct 2024, 09:15 AM',
      state: 'Awaiting Action',
      statusClass: 'awaiting',
      stepNum: 2,
      eta: 'Resolution estimate not available yet',
      description: 'Stormwater culvert blocked by silt and dry leaves causing rainwater backflow into alleyway.',
      resolution_notes: 'Assigned to desilting schedule. High-pressure jetting machine requested.',
      photoUrl: 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&auto=format&fit=crop&q=80',
      activities: [
        {
          type: 'status-change',
          title: 'Under Review by Drainage Wing',
          time: '28 Oct 2024, 10:00 AM',
          message: 'Desilting truck scheduled for Ward 15 deployment.',
          officer: 'P. Selvam',
          team: 'Ward 15 Stormwater Works'
        }
      ]
    }
  };

  // Determine current case
  var params = $location.search() || {};
  var qId = params.sys_id || 'c1';

  // Use server data if present and valid, otherwise fallback to database
  if (c.data && c.data.case && c.data.case.number) {
    c.case = c.data.case;
  } else if (casesDb[qId]) {
    c.case = casesDb[qId];
  } else {
    c.case = casesDb['c1'];
  }

  c.doAction = function(actionType) {
    if (actionType === 'view_location') {
      alert('Reported Location: ' + c.case.location + '\\nGPS Coordinates: 13.0012° N, 80.2565° E (Geo-Locked)');
    } else if (actionType === 'add_info') {
      var info = prompt('Enter additional information or landmark details for the ward engineer:');
      if (info) {
        c.case.activities.unshift({
          type: 'comment',
          title: 'Citizen Additional Information Added',
          time: 'Just now',
          message: info,
          officer: 'Priya Sharma (Citizen)',
          team: 'Citizen Portal'
        });
        alert('Your update has been submitted to the field team.');
      }
    } else if (actionType === 'not_fixed') {
      if (confirm('Are you sure you want to report this issue as Not Fixed? A ward supervisor will be re-assigned for inspection.')) {
        c.case.state = 'In Progress';
        c.case.statusClass = 'in-progress';
        c.case.stepNum = 4;
        c.case.activities.unshift({
          type: 'status-change',
          title: 'Case Re-Opened by Citizen',
          time: 'Just now',
          message: 'Citizen reported defect persists. Re-assigned to ward supervisor for field inspection.',
          officer: 'Priya Sharma',
          team: 'Citizen Appeal'
        });
        alert('Case re-opened for supervisor re-inspection.');
      }
    } else if (actionType === 'feedback') {
      var rating = prompt('How would you rate municipal response speed (1 to 5 stars)?', '5');
      if (rating) {
        alert('Thank you for rating ' + rating + ' stars! Together for a better city.');
      }
    }
  };
}
"""

TRACK_SERVER_SCRIPT = """
(function() {
  var sysId = $sp.getParameter('sys_id') || 'c1';

  // Default Case
  data.case = {
    sys_id: 'c1',
    number: 'CIVIX-2024-00123',
    short_description: 'Water leakage on 3rd Main Road',
    category: 'Water Supply',
    location: 'Opposite Post Office, 3rd Main Road, Adyar, Ward 18, Chennai',
    opened_at: '15 Nov 2024, 10:24 AM',
    state: 'In Progress',
    statusClass: 'in-progress',
    stepNum: 4,
    eta: '18 Nov 2024, 05:00 PM (Target: 72 hrs)',
    description: 'High pressure potable water pipeline rupture leaking onto pedestrian footpath and causing severe water pooling near crossway.',
    resolution_notes: 'Ward 18 pipeline engineering crew dispatched with excavator. Trenching and bypass pipe replacement currently underway.',
    photoUrl: 'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=600&auto=format&fit=crop&q=80',
    activities: [
      {
        type: 'dispatch',
        title: 'Repair Crew Dispatched on Site',
        time: '15 Nov 2024, 02:45 PM',
        message: 'Trenching crew and replacement valve parts arrived at 3rd Main Road. Excavation in progress.',
        officer: 'S. Ramanathan',
        team: 'Ward 18 Hydraulic Works'
      },
      {
        type: 'status-change',
        title: 'Status changed to In Progress',
        time: '15 Nov 2024, 11:30 AM',
        message: 'Work order #WO-8912 created and scheduled for same-day repair by water board engineer.',
        officer: 'K. Balaji',
        team: 'Central Civic Operations'
      },
      {
        type: 'comment',
        title: 'Field Inspection Completed',
        time: '15 Nov 2024, 11:15 AM',
        message: 'Ward inspector verified 4-inch ductile iron pipe fracture. No contamination risk to drinking supply.',
        officer: 'V. Murugan',
        team: 'Ward 18 Junior Engineer'
      },
      {
        type: 'status-change',
        title: 'Complaint Registered & Ticket Generated',
        time: '15 Nov 2024, 10:24 AM',
        message: 'Citizen complaint logged through CIVIX AI mobile portal with verified GPS tag.',
        officer: 'Automated System',
        team: 'CIVIX AI Core'
      }
    ]
  };

  // If real ServiceNow incident:
  if (sysId && sysId !== 'c1' && sysId !== 'c2' && sysId !== 'c3' && sysId !== 'c4') {
    var gr = new GlideRecord('incident');
    if (gr.get(sysId) || gr.get('number', sysId)) {
      var st = gr.getValue('state');
      var step = 1;
      var stClass = 'awaiting';
      if (st == '1') { step = 1; stClass = 'awaiting'; }
      else if (st == '2') { step = 4; stClass = 'in-progress'; }
      else if (st == '3') { step = 3; stClass = 'in-progress'; }
      else if (st == '6') { step = 5; stClass = 'resolved'; }
      else if (st == '7') { step = 6; stClass = 'resolved'; }

      data.case = {
        sys_id: gr.getUniqueValue(),
        number: gr.getValue('number'),
        short_description: gr.getValue('short_description'),
        category: gr.getDisplayValue('category') || 'Municipal Issue',
        location: 'Ward 12, Chennai',
        opened_at: gr.getValue('sys_created_on'),
        state: gr.getDisplayValue('state'),
        statusClass: stClass,
        stepNum: step,
        eta: (st == '6' || st == '7') ? 'Resolved' : '18 Nov 2024, 05:00 PM (Target: 72 hrs)',
        description: gr.getValue('description') || gr.getValue('short_description'),
        resolution_notes: gr.getValue('close_notes') || 'Assigned to municipal field technician for inspection and resolution.',
        photoUrl: 'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=600&auto=format&fit=crop&q=80',
        activities: [
          {
            type: 'status-change',
            title: 'Current Status: ' + gr.getDisplayValue('state'),
            time: gr.getValue('sys_updated_on') || gr.getValue('sys_created_on'),
            message: 'Incident record in ServiceNow Service Operations Center.',
            officer: 'Ward Dispatch Officer',
            team: 'Municipal Services'
          },
          {
            type: 'status-change',
            title: 'Incident Submitted',
            time: gr.getValue('sys_created_on'),
            message: 'Ticket recorded with system identifier ' + gr.getValue('number'),
            officer: 'CIVIX AI Core',
            team: 'Digital Urban Intake'
          }
        ]
      };
    }
  }
})();
"""

# ==============================================================================
# MAIN DEPLOYMENT ROUTINE
# ==============================================================================
if __name__ == "__main__":
    print("=== DEPLOYING COMPLETE REFERENCE 2 DASHBOARD & CASE TRACKING ===")

    print("\n--- 1. Deploying civix_home_widget & civix_dashboard_widget ---")
    update_widget("civix_home_widget", HOME_TEMPLATE, HOME_CSS, HOME_CLIENT_SCRIPT, HOME_SERVER_SCRIPT)
    update_widget("civix_dashboard_widget", HOME_TEMPLATE, HOME_CSS, HOME_CLIENT_SCRIPT, HOME_SERVER_SCRIPT)

    print("\n--- 2. Deploying civix_track_case_widget (Full Specification) ---")
    update_widget("civix_track_case_widget", TRACK_TEMPLATE, TRACK_CSS, TRACK_CLIENT_SCRIPT, TRACK_SERVER_SCRIPT)

    print("\n=== ALL REDESIGN COMPONENTS DEPLOYED AND SYNCHRONIZED ===")
