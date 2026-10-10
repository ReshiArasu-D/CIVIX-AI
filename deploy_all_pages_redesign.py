"""
CIVIX AI - Comprehensive Multi-Page Premium Redesign
Deploys the unified Plus Jakarta Sans design system, zero-scrollbar flex shell,
and micro-animations across all portal pages.
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

# 1. Update Theme with 'Plus Jakarta Sans'
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


# ==============================================================================
# COMMON HEADER & SIDEBAR HTML PARTIALS
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
            <span class="civix-side-icon-box"><i class="glyphicon glyphicon-home"></i></span>
            <span>Dashboard</span>
          </a>
          <a href="?id=civix_report_issue" class="civix-side-btn {'active' if active_item == 'report' else ''}">
            <span class="civix-side-icon-box"><i class="glyphicon glyphicon-edit"></i></span>
            <span>Report an Issue</span>
          </a>
          <a href="?id=civix_my_cases" class="civix-side-btn {'active' if active_item == 'complaints' else ''}">
            <span class="civix-side-icon-box"><i class="glyphicon glyphicon-list-alt"></i></span>
            <span>My Complaints</span>
          </a>
          <a href="?id=civix_landing#services" class="civix-side-btn {'active' if active_item == 'services' else ''}">
            <span class="civix-side-icon-box"><i class="glyphicon glyphicon-info-sign"></i></span>
            <span>Service Information</span>
          </a>
          <a href="?id=civix_landing#trust" class="civix-side-btn {'active' if active_item == 'help' else ''}">
            <span class="civix-side-icon-box"><i class="glyphicon glyphicon-headphones"></i></span>
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
        <span class="glyphicon glyphicon-search civix-search-lens-icon"></span>
        <input type="text" class="civix-search-input-pill" placeholder="Search services, complaints or help..." ng-model="c.searchQuery" />
      </div>

      <div class="civix-header-actions-group">
        <!-- Languages Dropdown -->
        <div class="civix-lang-drop-wrap">
          <button type="button" class="civix-lang-btn-pill" ng-click="c.toggleLang()">
            <span class="glyphicon glyphicon-globe text-primary"></span>
            <span>{{c.currentLangDisplay || 'भारतीय भाषाएं / Language'}}</span>
            <span class="glyphicon glyphicon-chevron-down" style="font-size:9px;"></span>
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
        <a href="#alerts" class="civix-bell-link" title="3 Notifications">
          <span class="glyphicon glyphicon-bell"></span>
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

# Common Shell CSS applied to all pages
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
  padding: 24px;
  margin-bottom: 22px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}
"""

COMMON_CLIENT_SCRIPT = """
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
}
"""

print("Base setup ready.")

# ==============================================================================
# WIDGET 1: CUSTOMER HOME / DASHBOARD
# ==============================================================================
HOME_TEMPLATE = f"""
<div class="civix-app-shell">
  {get_sidebar_html("dashboard")}

  <main class="civix-main-column">
    {get_topbar_html()}

    <div class="civix-content-area">
      <!-- 1. HERO BANNER ROW -->
      <section class="civix-banner-grid">
        <div class="civix-hero-welcome-card">
          <div class="civix-hero-skyline-overlay"></div>
          <div class="civix-hero-content-col">
            <h1 class="civix-hero-big-greeting">Welcome back,<br/><span class="civix-name-gradient">{{c.data.citizenName || 'Priya Sharma'}}!</span> 👋</h1>
            <p class="civix-hero-tagline-main">Together for a cleaner, safer and smarter city.</p>
            <p class="civix-hero-tagline-sub">Report issues, track progress and help improve our community.</p>
          </div>

          <div class="civix-glass-weather-widget">
            <div class="civix-weather-header">
              <span class="glyphicon glyphicon-map-marker text-primary"></span>
              <strong>Chennai, Tamil Nadu</strong>
              <span class="glyphicon glyphicon-chevron-down" style="font-size:9px;"></span>
            </div>
            <div class="civix-weather-split">
              <div class="civix-weather-temp-info">
                <span class="civix-temp-reading">32°C</span>
                <span class="civix-weather-condition">Mostly Clear</span>
              </div>
              <div class="civix-animated-sun-icon">
                <svg width="38" height="38" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="5" fill="#F59E0B"/>
                  <path d="M12 1v3M12 20v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M1 12h3M20 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div class="civix-hero-promo-card">
          <div class="civix-promo-gradient-shade">
            <h3 class="civix-promo-headline">Cleaner Cities<br/>Happier People</h3>
            <div class="civix-promo-line-accent"></div>
          </div>
        </div>
      </section>

      <!-- 2. 4 INTERACTIVE KPI METRIC CARDS -->
      <section class="civix-kpi-deck">
        <a href="?id=civix_my_cases" class="civix-kpi-tile kpi-tile-blue">
          <div class="civix-kpi-icon-bubble bg-blue-subtle">
            <span class="glyphicon glyphicon-file text-blue"></span>
          </div>
          <div class="civix-kpi-details">
            <div class="civix-kpi-value-row">
              <span class="civix-kpi-count">{{c.data.counts.total}}</span>
              <span class="civix-kpi-arrow-cue">&rsaquo;</span>
            </div>
            <div class="civix-kpi-label-text">Total Complaints</div>
            <div class="civix-kpi-trend-badge trend-green">&uarr; 3 this month</div>
          </div>
        </a>

        <a href="?id=civix_my_cases&status=Resolved" class="civix-kpi-tile kpi-tile-green">
          <div class="civix-kpi-icon-bubble bg-green-subtle">
            <span class="glyphicon glyphicon-ok text-green"></span>
          </div>
          <div class="civix-kpi-details">
            <div class="civix-kpi-value-row">
              <span class="civix-kpi-count">{{c.data.counts.resolved}}</span>
              <span class="civix-kpi-arrow-cue">&rsaquo;</span>
            </div>
            <div class="civix-kpi-label-text">Resolved</div>
            <div class="civix-kpi-trend-badge trend-green">&uarr; 2 this month</div>
          </div>
        </a>

        <a href="?id=civix_my_cases&status=In%20Progress" class="civix-kpi-tile kpi-tile-gold">
          <div class="civix-kpi-icon-bubble bg-gold-subtle">
            <span class="glyphicon glyphicon-time text-gold"></span>
          </div>
          <div class="civix-kpi-details">
            <div class="civix-kpi-value-row">
              <span class="civix-kpi-count">{{c.data.counts.in_progress}}</span>
              <span class="civix-kpi-arrow-cue">&rsaquo;</span>
            </div>
            <div class="civix-kpi-label-text">In Progress</div>
            <div class="civix-kpi-trend-badge trend-neutral">&ndash; same as last month</div>
          </div>
        </a>

        <a href="?id=civix_my_cases&status=Awaiting%20Action" class="civix-kpi-tile kpi-tile-red">
          <div class="civix-kpi-icon-bubble bg-red-subtle">
            <span class="glyphicon glyphicon-exclamation-sign text-red"></span>
          </div>
          <div class="civix-kpi-details">
            <div class="civix-kpi-value-row">
              <span class="civix-kpi-count">{{c.data.counts.awaiting}}</span>
              <span class="civix-kpi-arrow-cue">&rsaquo;</span>
            </div>
            <div class="civix-kpi-label-text">Awaiting Action</div>
            <div class="civix-kpi-trend-badge trend-red">&darr; 1 from last month</div>
          </div>
        </a>
      </section>

      <!-- 3. TRI-PANEL WORKSPACE GRID -->
      <div class="civix-tri-panel-grid">
        <!-- COLUMN 1: Report Issue & Recent Complaints -->
        <div class="civix-column-primary">
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
                <div class="civix-entry-thumb-box">
                  <span class="glyphicon" ng-class="item.icon" style="font-size:20px; color:#0066FF;"></span>
                </div>
                <div class="civix-entry-info">
                  <span class="civix-entry-ticket-id">{{item.number}}</span>
                  <h4 class="civix-entry-headline">{{item.short_description}}</h4>
                  <div class="civix-entry-meta">
                    <span><span class="glyphicon glyphicon-map-marker text-primary"></span> {{item.location}}</span>
                    <span><span class="glyphicon glyphicon-calendar text-muted"></span> {{item.date}}</span>
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

        <!-- COLUMN 2: Map & Alerts -->
        <div class="civix-column-center">
          <div class="civix-white-box civix-map-panel">
            <div class="civix-box-header civix-flex-split">
              <h2 class="civix-box-title">Issue Map</h2>
              <a href="?id=civix_landing#services" class="civix-view-all-button">View Full Map &rarr;</a>
            </div>
            <div class="civix-map-stage">
              <svg class="civix-map-vector" viewBox="0 0 340 230" xmlns="http://www.w3.org/2000/svg">
                <rect width="340" height="230" fill="#F1F5F9"/>
                <path d="M245,0 Q260,80 235,140 Q215,190 255,230 L340,230 L340,0 Z" fill="#BAE6FD"/>
                <text x="260" y="125" font-size="16" font-weight="800" fill="#0284C7" opacity="0.7">Chennai</text>
                <path d="M0,95 L245,95" stroke="#CBD5E1" stroke-width="3"/>
                <path d="M0,165 L240,165" stroke="#CBD5E1" stroke-width="3"/>
                <path d="M125,0 L125,230" stroke="#CBD5E1" stroke-width="3"/>
                <path d="M185,0 L185,230" stroke="#CBD5E1" stroke-width="3"/>

                <text x="135" y="60" font-size="10" font-weight="700" fill="#475569">Anna Nagar</text>
                <text x="65" y="132" font-size="10" font-weight="700" fill="#475569">T. Nagar</text>
                <text x="95" y="195" font-size="10" font-weight="700" fill="#475569">Velachery</text>
                <text x="175" y="202" font-size="10" font-weight="700" fill="#475569">Adyar</text>

                <!-- Radar waves -->
                <circle cx="125" cy="130" r="24" fill="#0066FF" opacity="0.2"/>
                <circle cx="125" cy="130" r="14" fill="#0066FF" opacity="0.4"/>
                <circle cx="125" cy="130" r="6" fill="#0066FF"/>

                <!-- Markers -->
                <circle cx="120" cy="52" r="6" fill="#0284C7" stroke="#FFFFFF" stroke-width="2"/>
                <circle cx="68" cy="142" r="6" fill="#DC2626" stroke="#FFFFFF" stroke-width="2"/>
                <circle cx="145" cy="180" r="6" fill="#EAB308" stroke="#FFFFFF" stroke-width="2"/>
                <circle cx="195" cy="185" r="6" fill="#16A34A" stroke="#FFFFFF" stroke-width="2"/>
              </svg>
            </div>
          </div>

          <div class="civix-white-box" id="alerts">
            <div class="civix-box-header civix-flex-split">
              <h2 class="civix-box-title">Nearby Alerts</h2>
              <a href="?id=civix_landing#services" class="civix-view-all-button">View All &rarr;</a>
            </div>
            <div class="civix-alert-items-list">
              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-red"><span class="glyphicon glyphicon-exclamation-sign"></span></div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Road maintenance work in T. Nagar</h4>
                  <div class="civix-alert-foot-meta">500 m &bull; Today</div>
                </div>
              </div>
              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-gold"><span class="glyphicon glyphicon-flash"></span></div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Scheduled power maintenance - Anna Nagar</h4>
                  <div class="civix-alert-foot-meta">1.2 km &bull; Tomorrow</div>
                </div>
              </div>
              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-purple"><span class="glyphicon glyphicon-tint"></span></div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Possible waterlogging in Velachery</h4>
                  <div class="civix-alert-foot-meta">2.3 km &bull; Today</div>
                </div>
              </div>
              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-blue"><span class="glyphicon glyphicon-info-sign"></span></div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Low water pressure reported</h4>
                  <div class="civix-alert-foot-meta">3.1 km &bull; Today</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- COLUMN 3: AI Assistant -->
        <div class="civix-column-assistant">
          <div class="civix-white-box civix-bot-widget-frame">
            <div class="civix-bot-widget-header civix-flex-split">
              <div class="civix-bot-label-group">
                <span class="glyphicon glyphicon-user civix-bot-badge-icon"></span>
                <strong>Civic AI Assistant</strong>
              </div>
              <div class="civix-bot-actions-mini">
                <span class="glyphicon glyphicon-minus"></span>
                <span class="glyphicon glyphicon-option-horizontal"></span>
                <span class="glyphicon glyphicon-remove"></span>
              </div>
            </div>

            <div class="civix-bot-widget-body">
              <div class="civix-robot-mascot-box">
                <svg width="100" height="85" viewBox="0 0 120 98" fill="none">
                  <circle cx="60" cy="10" r="5" fill="#0066FF"/>
                  <rect x="58.5" y="14" width="3" height="10" fill="#64748B"/>
                  <rect x="28" y="22" width="64" height="42" rx="14" fill="#FFFFFF" stroke="#0066FF" stroke-width="3.5"/>
                  <rect x="34" y="28" width="52" height="28" rx="8" fill="#0F172A"/>
                  <circle cx="48" cy="42" r="5" fill="#38BDF8"/>
                  <circle cx="72" cy="42" r="5" fill="#38BDF8"/>
                  <rect x="20" y="32" width="8" height="20" rx="3" fill="#0066FF"/>
                  <rect x="92" y="32" width="8" height="20" rx="3" fill="#0066FF"/>
                  <rect x="40" y="66" width="40" height="28" rx="8" fill="#FFFFFF" stroke="#0066FF" stroke-width="3.5"/>
                  <rect x="46" y="72" width="28" height="12" rx="3" fill="#0066FF"/>
                  <text x="49" y="81" font-size="7.5" font-weight="900" fill="#FFFFFF">CIVIX</text>
                </svg>
              </div>

              <div class="civix-chat-scroll-area">
                <div class="civix-chat-bubble-agent">
                  <p class="civix-bubble-hi">Hi Priya! 👋</p>
                  <p class="civix-bubble-text">I'm your Civic AI Assistant.<br/>How can I help you today?</p>
                </div>
                <div ng-repeat="msg in c.chatHistory" class="civix-chat-msg-row">
                  <div ng-class="msg.sender === 'bot' ? 'civix-chat-bubble-agent' : 'civix-chat-bubble-user'">
                    {{msg.text}}
                  </div>
                </div>
                <div ng-if="c.isBotTyping" class="civix-chat-bubble-agent civix-typing-anim">
                  <span class="civix-type-dot"></span><span class="civix-type-dot"></span><span class="civix-type-dot"></span>
                </div>
              </div>

              <div class="civix-prompt-buttons-stack">
                <button type="button" class="civix-action-chip" ng-click="c.sendPrompt('Track my complaint')">
                  <span class="glyphicon glyphicon-file"></span> Track my complaint
                </button>
                <button type="button" class="civix-action-chip" ng-click="c.sendPrompt('Report a new issue')">
                  <span class="glyphicon glyphicon-edit"></span> Report a new issue
                </button>
                <button type="button" class="civix-action-chip" ng-click="c.sendPrompt('Check nearby issues')">
                  <span class="glyphicon glyphicon-map-marker"></span> Check nearby issues
                </button>
                <button type="button" class="civix-action-chip" ng-click="c.sendPrompt('Know service information')">
                  <span class="glyphicon glyphicon-info-sign"></span> Know service information
                </button>
              </div>

              <div class="civix-chat-input-toolbar">
                <input type="text" class="civix-chat-text-box" placeholder="Type your message..." ng-model="c.userMsgInput" ng-keydown="c.onChatEnter($event)" />
                <button type="button" class="civix-chat-send-btn" ng-click="c.submitChatMessage()">
                  <span class="glyphicon glyphicon-send"></span>
                </button>
              </div>
              <div class="civix-bot-caption-notice">I can assist you in all Indian languages</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</div>
"""

HOME_CSS = BASE_SHELL_CSS + """
/* BANNER GRID */
.civix-banner-grid {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 20px;
  margin-bottom: 22px;
}
.civix-hero-welcome-card {
  background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 50%, #F8FAFC 100%);
  border: 1px solid #BAE6FD;
  border-radius: 18px;
  padding: 28px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 102, 255, 0.05);
}
.civix-hero-skyline-overlay {
  position: absolute;
  right: 0; top: 0; bottom: 0;
  width: 320px;
  background: url('https://images.unsplash.com/photo-1477959858617-67f30bc75b82?w=800&auto=format&fit=crop&q=80') center right/cover no-repeat;
  opacity: 0.12;
  pointer-events: none;
}
.civix-hero-big-greeting {
  font-size: 28px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1.15;
  margin: 0 0 6px 0;
}
.civix-name-gradient {
  color: #0066FF;
}
.civix-hero-tagline-main { font-size: 13.5px; font-weight: 600; color: #334155; margin: 0; }
.civix-hero-tagline-sub { font-size: 12.5px; color: #64748B; margin: 2px 0 0 0; }

.civix-glass-weather-widget {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(16px);
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 12px 18px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  z-index: 2;
  min-width: 180px;
}
.civix-weather-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #0F172A;
  margin-bottom: 6px;
}
.civix-weather-split {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.civix-temp-reading { font-size: 20px; font-weight: 800; color: #0F172A; }
.civix-weather-condition { font-size: 11px; color: #64748B; }

.civix-hero-promo-card {
  border-radius: 18px;
  overflow: hidden;
  position: relative;
  background: url('https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=600&auto=format&fit=crop&q=80') center/cover no-repeat;
  border: 1px solid #CBD5E1;
  display: flex;
  align-items: flex-end;
}
.civix-promo-gradient-shade {
  width: 100%;
  background: linear-gradient(180deg, transparent 0%, rgba(15, 23, 42, 0.88) 100%);
  padding: 20px;
  color: #FFFFFF;
}
.civix-promo-headline { font-size: 16px; font-weight: 800; line-height: 1.3; margin: 0 0 6px 0; }
.civix-promo-line-accent { width: 36px; height: 4px; background: #38BDF8; border-radius: 2px; }

/* 4 KPI CARDS */
.civix-kpi-deck {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 22px;
}
.civix-kpi-tile {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 16px 18px;
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  transition: all 0.2s;
}
.civix-kpi-tile:hover {
  transform: translateY(-3px);
  text-decoration: none;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}
.civix-kpi-icon-bubble {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}
.bg-blue-subtle { background: #EFF6FF; }
.bg-green-subtle { background: #ECFDF5; }
.bg-gold-subtle { background: #FFFBEB; }
.bg-red-subtle { background: #FEF2F2; }
.text-blue { color: #0066FF; }
.text-green { color: #16A34A; }
.text-gold { color: #D97706; }
.text-red { color: #DC2626; }
.civix-kpi-details { flex-grow: 1; }
.civix-kpi-value-row { display: flex; justify-content: space-between; align-items: baseline; }
.civix-kpi-count { font-size: 24px; font-weight: 800; color: #0F172A; }
.civix-kpi-arrow-cue { font-size: 18px; color: #94A3B8; }
.civix-kpi-label-text { font-size: 13px; font-weight: 600; color: #64748B; margin: 2px 0; }
.civix-kpi-trend-badge { font-size: 11px; font-weight: 600; }
.trend-green { color: #16A34A; }
.trend-neutral { color: #B45309; }
.trend-red { color: #DC2626; }

/* TRI PANEL GRID (FLUID MINMAX TO AVOID SCROLLBARS) */
.civix-tri-panel-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.8fr) minmax(280px, 1fr) minmax(260px, 0.9fr);
  gap: 20px;
  width: 100%;
}
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
.civix-cat-pill-card {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 16px 8px;
  text-align: center;
  text-decoration: none;
  transition: all 0.2s;
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

/* COMPLAINTS LIST */
.civix-complaint-stack { display: flex; flex-direction: column; gap: 10px; }
.civix-complaint-entry {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.15s;
}
.civix-complaint-entry:hover {
  background: #F8FAFC;
  border-color: #CBD5E1;
  text-decoration: none;
}
.civix-entry-thumb-box {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: #EFF6FF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.civix-entry-info { flex-grow: 1; min-width: 0; }
.civix-entry-ticket-id { font-size: 11px; font-weight: 700; color: #0066FF; }
.civix-entry-headline {
  font-size: 13.5px;
  font-weight: 600;
  color: #0F172A;
  margin: 2px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.civix-entry-meta { display: flex; gap: 14px; font-size: 11px; color: #64748B; }
.civix-entry-badge-col { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.civix-badge-pill-status {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 14px;
}
.pill-in-progress { background: #FEF3C7; color: #B45309; }
.pill-resolved { background: #DCFCE7; color: #15803D; }
.pill-awaiting { background: #FEE2E2; color: #B91C1C; }
.civix-entry-arrow { font-size: 18px; color: #94A3B8; }

/* MAP */
.civix-map-stage { border-radius: 12px; overflow: hidden; border: 1px solid #E2E8F0; background: #F1F5F9; }
.civix-map-vector { width: 100%; height: auto; display: block; }

/* ALERTS */
.civix-alert-items-list { display: flex; flex-direction: column; gap: 12px; }
.civix-alert-item-card { display: flex; gap: 12px; padding-bottom: 10px; border-bottom: 1px solid #F1F5F9; }
.civix-alert-icon-ring {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #FFFFFF;
  flex-shrink: 0;
}
.alert-red { background: #EF4444; }
.alert-gold { background: #F59E0B; }
.alert-purple { background: #A855F7; }
.alert-blue { background: #0EA5E9; }
.civix-alert-info-side { flex-grow: 1; }
.civix-alert-item-title { font-size: 12.5px; font-weight: 600; color: #0F172A; margin: 0 0 2px 0; }
.civix-alert-foot-meta { font-size: 11px; color: #64748B; }

/* ASSISTANT */
.civix-bot-widget-frame { border-top: 4px solid #0066FF; padding: 16px 18px 20px; }
.civix-bot-widget-header { padding-bottom: 12px; border-bottom: 1px solid #F1F5F9; margin-bottom: 12px; }
.civix-bot-label-group { display: flex; align-items: center; gap: 8px; font-size: 14px; color: #0F172A; }
.civix-bot-badge-icon { color: #0066FF; font-size: 16px; }
.civix-bot-actions-mini { display: flex; gap: 8px; color: #94A3B8; font-size: 11px; }
.civix-robot-mascot-box { text-align: center; margin-bottom: 10px; }
.civix-chat-scroll-area {
  max-height: 200px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}
.civix-chat-bubble-agent {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 10px 12px;
  font-size: 12.5px;
  line-height: 1.4;
  color: #0F172A;
}
.civix-chat-bubble-user {
  background: #0066FF;
  color: #FFFFFF;
  border-radius: 12px;
  padding: 8px 12px;
  font-size: 12px;
  align-self: flex-end;
}
.civix-bubble-hi { font-weight: 700; margin: 0 0 2px 0; }
.civix-bubble-text { margin: 0; color: #475569; }
.civix-typing-anim { display: flex; gap: 4px; padding: 8px 12px; width: 50px; }
.civix-type-dot { width: 5px; height: 5px; border-radius: 50%; background: #0066FF; animation: bounceDot 1.4s infinite ease-in-out; }
.civix-type-dot:nth-child(2) { animation-delay: 0.2s; }
.civix-type-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounceDot { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }

.civix-prompt-buttons-stack { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
.civix-action-chip {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 600;
  color: #334155;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.15s;
}
.civix-action-chip:hover { background: #EFF6FF; border-color: #0066FF; color: #0066FF; }
.civix-chat-input-toolbar {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 4px 6px;
}
.civix-chat-text-box {
  flex-grow: 1;
  background: transparent;
  border: none;
  font-size: 12px;
  outline: none;
  padding: 4px;
}
.civix-chat-send-btn {
  background: #0066FF;
  border: none;
  border-radius: 6px;
  color: #FFFFFF;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  cursor: pointer;
}
.civix-bot-caption-notice { font-size: 10.5px; color: #94A3B8; text-align: center; margin-top: 8px; }

/* RESPONSIVE LAYOUT */
@media (max-width: 1400px) {
  .civix-tri-panel-grid {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  }
  .civix-column-assistant {
    grid-column: span 2;
  }
}
@media (max-width: 1024px) {
  .civix-kpi-deck { grid-template-columns: repeat(2, 1fr); }
  .civix-banner-grid { grid-template-columns: 1fr; }
  .civix-category-cards-grid { grid-template-columns: repeat(3, 1fr); }
  .civix-tri-panel-grid { grid-template-columns: 1fr; }
  .civix-column-assistant { grid-column: span 1; }
}
"""

HOME_CLIENT_SCRIPT = """
function($scope, $timeout) {
  var c = this;
  c.langOpen = false;
  c.selectedLang = 'en';
  c.currentLangDisplay = 'भारतीय भाषाएं / Language';
  c.chatHistory = [];
  c.isBotTyping = false;

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

  c.toggleLang = function() { c.langOpen = !c.langOpen; };
  c.chooseLang = function(l) {
    c.selectedLang = l.code;
    c.currentLangDisplay = l.native + ' / ' + l.name;
    c.langOpen = false;
  };

  c.sendPrompt = function(promptText) {
    c.chatHistory.push({ sender: 'user', text: promptText });
    c.isBotTyping = true;
    $timeout(function() {
      c.isBotTyping = false;
      var reply = 'I am processing your inquiry regarding "' + promptText + '". Checking Ward 12 operations in real-time...';
      if (promptText.indexOf('Track') >= 0) {
        reply = 'You have 3 complaints In Progress: CIVIX-2024-00123 (Water leakage, Adyar), CIVIX-2024-00118 (Street light, Anna Nagar), and CIVIX-2024-00102 (Drainage, Velachery).';
      } else if (promptText.indexOf('Report') >= 0) {
        reply = 'Opening quick intake form. Please select your service category above or describe the location and issue.';
      } else if (promptText.indexOf('nearby') >= 0) {
        reply = 'Nearby Alert: Road maintenance on 3rd Main Road, T. Nagar (500m away). Expect minor traffic diversions.';
      }
      c.chatHistory.push({ sender: 'bot', text: reply });
    }, 600);
  };

  c.submitChatMessage = function() {
    if (!c.userMsgInput || !c.userMsgInput.trim()) return;
    var userText = c.userMsgInput.trim();
    c.userMsgInput = '';
    c.chatHistory.push({ sender: 'user', text: userText });
    c.isBotTyping = true;
    $timeout(function() {
      c.isBotTyping = false;
      c.chatHistory.push({
        sender: 'bot',
        text: 'Thank you for your report: "' + userText + '". Our civic intelligence agent has logged this for Ward 12 inspection.'
      });
    }, 700);
  };

  c.onChatEnter = function(e) {
    if (e.keyCode === 13) c.submitChatMessage();
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
      status: 'In Progress',
      statusClass: 'in-progress',
      icon: 'glyphicon-tint'
    },
    {
      sys_id: 'c2',
      number: 'CIVIX-2024-00118',
      short_description: 'Street light not working near Anna Nagar Park',
      location: 'Anna Nagar, Chennai',
      date: '10 Nov 2024, 06:12 PM',
      status: 'Resolved',
      statusClass: 'resolved',
      icon: 'glyphicon-flash'
    },
    {
      sys_id: 'c3',
      number: 'CIVIX-2024-00110',
      short_description: 'Pothole near 100 Feet Road',
      location: 'T. Nagar, Chennai',
      date: '05 Nov 2024, 02:30 PM',
      status: 'Resolved',
      statusClass: 'resolved',
      icon: 'glyphicon-road'
    },
    {
      sys_id: 'c4',
      number: 'CIVIX-2024-00102',
      short_description: 'Drainage overflow in residential area',
      location: 'Velachery, Chennai',
      date: '28 Oct 2024, 09:15 AM',
      status: 'Awaiting Action',
      statusClass: 'awaiting',
      icon: 'glyphicon-filter'
    }
  ];
})();
"""


# ==============================================================================
# WIDGET 2: REPORT AN ISSUE (PREMIUM MULTI-STEP WITH SHELL)
# ==============================================================================
REPORT_TEMPLATE = """
<div class="civix-app-shell">
  __SIDEBAR_REPORT__

  <main class="civix-main-column">
    __TOPBAR__

    <div class="civix-content-area">
      <!-- Page Header -->
      <div class="civix-page-top-bar">
        <div>
          <h1 class="civix-page-heading-main">Report a Civic Issue</h1>
          <p class="civix-page-sub-main">Submit civic infrastructure defects directly to your municipal ward engineers.</p>
        </div>
      </div>

      <!-- Main Form Card -->
      <div class="civix-panel-card" style="max-width: 960px;">
        <!-- Step Indicator -->
        <div class="civix-step-nav-bar">
          <div class="civix-step-item" ng-class="{'active': c.step >= 1}">
            <span class="civix-step-index">1</span>
            <span class="civix-step-name">Service & Category</span>
          </div>
          <div class="civix-step-line" ng-class="{'active': c.step >= 2}"></div>
          <div class="civix-step-item" ng-class="{'active': c.step >= 2}">
            <span class="civix-step-index">2</span>
            <span class="civix-step-name">Location & Ward</span>
          </div>
          <div class="civix-step-line" ng-class="{'active': c.step >= 3}"></div>
          <div class="civix-step-item" ng-class="{'active': c.step >= 3}">
            <span class="civix-step-index">3</span>
            <span class="civix-step-name">Review & Submit</span>
          </div>
        </div>

        <!-- Success Message -->
        <div ng-if="c.successData" class="alert alert-success text-center" style="padding: 30px; border-radius: 12px;">
          <div style="font-size: 42px; color: #16A34A; margin-bottom: 12px;"><span class="glyphicon glyphicon-ok-circle"></span></div>
          <h2 style="font-weight: 800; color: #0F172A; margin: 0 0 8px 0;">Civic Complaint Successfully Logged!</h2>
          <p class="text-muted">Your complaint tracking reference is:</p>
          <div style="display:inline-block; background:#0F172A; color:#FFFFFF; font-size:22px; font-weight:800; padding:10px 24px; border-radius:10px; letter-spacing:1px; margin: 10px 0;">
            {{c.successData.number}}
          </div>
          <p style="margin-top: 14px; font-size: 13.5px;">A ward engineer has been alerted for on-site inspection.</p>
          <div style="margin-top: 24px; display: flex; justify-content: center; gap: 14px;">
            <a href="?id=civix_track_case&sys_id={{c.successData.sys_id}}" class="btn btn-primary btn-lg" style="font-weight:700;">Track This Case Now &rarr;</a>
            <a href="?id=civix_home" class="btn btn-default btn-lg">Return to Dashboard</a>
          </div>
        </div>

        <form ng-if="!c.successData">
          <!-- Step 1: Category & Details -->
          <div ng-if="c.step === 1">
            <h3 style="font-size: 17px; font-weight: 700; margin-bottom: 16px;">Select Service Category</h3>
            <div class="civix-cat-selector-grid">
              <button type="button" class="civix-cat-select-btn" ng-class="{'selected': c.form.category === 'Water'}" ng-click="c.form.category = 'Water'">
                <span class="glyphicon glyphicon-tint text-primary" style="font-size:24px; margin-bottom:6px;"></span>
                <strong>Water Supply</strong>
                <small class="text-muted">Leakage, low pressure</small>
              </button>
              <button type="button" class="civix-cat-select-btn" ng-class="{'selected': c.form.category === 'Electricity'}" ng-click="c.form.category = 'Electricity'">
                <span class="glyphicon glyphicon-flash text-warning" style="font-size:24px; margin-bottom:6px;"></span>
                <strong>Electricity</strong>
                <small class="text-muted">Streetlights, outage</small>
              </button>
              <button type="button" class="civix-cat-select-btn" ng-class="{'selected': c.form.category === 'Roads'}" ng-click="c.form.category = 'Roads'">
                <span class="glyphicon glyphicon-road" style="font-size:24px; margin-bottom:6px; color:#475569;"></span>
                <strong>Roads</strong>
                <small class="text-muted">Potholes, surface damage</small>
              </button>
              <button type="button" class="civix-cat-select-btn" ng-class="{'selected': c.form.category === 'Drainage'}" ng-click="c.form.category = 'Drainage'">
                <span class="glyphicon glyphicon-filter text-success" style="font-size:24px; margin-bottom:6px;"></span>
                <strong>Drainage</strong>
                <small class="text-muted">Blockage, overflow</small>
              </button>
              <button type="button" class="civix-cat-select-btn" ng-class="{'selected': c.form.category === 'Waterlogging'}" ng-click="c.form.category = 'Waterlogging'">
                <span class="glyphicon glyphicon-random" style="font-size:24px; margin-bottom:6px; color:#9333EA;"></span>
                <strong>Waterlogging</strong>
                <small class="text-muted">Rainwater accumulation</small>
              </button>
            </div>

            <div class="form-group" style="margin-top: 24px;">
              <label style="font-weight: 700; color:#0F172A;">Issue Title <span class="text-danger">*</span></label>
              <input type="text" class="form-control input-lg" ng-model="c.form.title" placeholder="e.g. Broken water pipe leaking near intersection" required />
            </div>

            <div class="form-group">
              <label style="font-weight: 700; color:#0F172A;">Problem Description <span class="text-danger">*</span></label>
              <textarea class="form-control" rows="4" ng-model="c.form.description" placeholder="Describe the severity, duration, and any immediate hazard..." required></textarea>
            </div>

            <div style="display:flex; justify-content:flex-end; margin-top: 24px;">
              <button type="button" class="btn btn-primary btn-lg" ng-click="c.step = 2" ng-disabled="!c.form.title || !c.form.description" style="font-weight:700;">
                Next: Location & Ward &rarr;
              </button>
            </div>
          </div>

          <!-- Step 2: Location & Ward -->
          <div ng-if="c.step === 2">
            <h3 style="font-size: 17px; font-weight: 700; margin-bottom: 16px;">Locality & Address</h3>
            <div class="form-group">
              <label style="font-weight: 700; color:#0F172A;">Municipal Ward <span class="text-danger">*</span></label>
              <select class="form-control input-lg" ng-model="c.form.ward">
                <option value="Ward 12 - T. Nagar">Ward 12 - T. Nagar</option>
                <option value="Ward 8 - Anna Nagar">Ward 8 - Anna Nagar</option>
                <option value="Ward 15 - Velachery">Ward 15 - Velachery</option>
                <option value="Ward 18 - Adyar">Ward 18 - Adyar</option>
                <option value="Ward 4 - Mylapore">Ward 4 - Mylapore</option>
              </select>
            </div>

            <div class="form-group">
              <label style="font-weight: 700; color:#0F172A;">Street Address / Landmark <span class="text-danger">*</span></label>
              <input type="text" class="form-control input-lg" ng-model="c.form.address" placeholder="e.g. Opposite Post Office, 3rd Cross Street" required />
            </div>

            <div class="form-group" style="background:#F1F5F9; padding: 16px; border-radius: 10px; margin-top: 18px;">
              <label style="font-weight: 700; color:#0F172A;">Precise GPS Geolocation</label><br/>
              <button type="button" class="btn btn-default" ng-click="c.detectGeo()" style="margin-right: 12px;">
                <span class="glyphicon glyphicon-map-marker text-primary"></span> Detect My GPS Coordinates
              </button>
              <span ng-if="c.form.geo" class="text-success" style="font-weight: 600;"><span class="glyphicon glyphicon-ok"></span> {{c.form.geo}}</span>
            </div>

            <div style="display:flex; justify-content:space-between; margin-top: 24px;">
              <button type="button" class="btn btn-default btn-lg" ng-click="c.step = 1">&larr; Back</button>
              <button type="button" class="btn btn-primary btn-lg" ng-click="c.step = 3" ng-disabled="!c.form.address" style="font-weight:700;">
                Next: Review & Submit &rarr;
              </button>
            </div>
          </div>

          <!-- Step 3: Review & Submit -->
          <div ng-if="c.step === 3">
            <h3 style="font-size: 17px; font-weight: 700; margin-bottom: 16px;">Confirm & Submit Details</h3>
            <div style="background:#F8FAFC; border: 1px solid #E2E8F0; border-radius:12px; padding: 20px; line-height: 1.8;">
              <p><strong>Category:</strong> {{c.form.category}}</p>
              <p><strong>Issue Title:</strong> {{c.form.title}}</p>
              <p><strong>Description:</strong> {{c.form.description}}</p>
              <p><strong>Ward & Locality:</strong> {{c.form.ward}}</p>
              <p><strong>Street Address:</strong> {{c.form.address}}</p>
              <p ng-if="c.form.geo"><strong>GPS:</strong> {{c.form.geo}}</p>
            </div>

            <div style="display:flex; justify-content:space-between; margin-top: 24px;">
              <button type="button" class="btn btn-default btn-lg" ng-click="c.step = 2">&larr; Back</button>
              <button type="button" class="btn btn-success btn-lg" ng-click="c.submitIssue()" ng-disabled="c.submitting" style="font-weight:800; padding:12px 28px;">
                <span ng-if="c.submitting"><span class="glyphicon glyphicon-refresh glyphicon-spin"></span> Logging Incident in ServiceNow...</span>
                <span ng-if="!c.submitting"><span class="glyphicon glyphicon-send"></span> Confirm & Submit Issue</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </main>
</div>
"""

REPORT_TEMPLATE = REPORT_TEMPLATE.replace("__SIDEBAR_REPORT__", get_sidebar_html("report")).replace("__TOPBAR__", get_topbar_html())

REPORT_CSS = BASE_SHELL_CSS + """
.civix-page-top-bar { margin-bottom: 22px; }
.civix-page-heading-main { font-size: 24px; font-weight: 800; color: #0F172A; margin: 0 0 4px 0; }
.civix-page-sub-main { font-size: 13.5px; color: #64748B; margin: 0; }

.civix-step-nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  position: relative;
}
.civix-step-item {
  display: flex;
  align-items: center;
  gap: 10px;
}
.civix-step-index {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #E2E8F0;
  color: #64748B;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
}
.civix-step-item.active .civix-step-index {
  background: #0066FF;
  color: #FFFFFF;
}
.civix-step-name {
  font-size: 13.5px;
  font-weight: 600;
  color: #64748B;
}
.civix-step-item.active .civix-step-name {
  color: #0F172A;
  font-weight: 700;
}
.civix-step-line {
  flex-grow: 1;
  height: 2px;
  background: #E2E8F0;
  margin: 0 16px;
}
.civix-step-line.active { background: #0066FF; }

.civix-cat-selector-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}
.civix-cat-select-btn {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 16px 10px;
  text-align: center;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.2s;
}
.civix-cat-select-btn:hover {
  background: #FFFFFF;
  border-color: #0066FF;
  transform: translateY(-2px);
}
.civix-cat-select-btn.selected {
  background: #EFF6FF;
  border-color: #0066FF;
  box-shadow: 0 0 0 2px rgba(0, 102, 255, 0.2);
}
.civix-cat-select-btn strong { font-size: 13px; color: #0F172A; }
.civix-cat-select-btn small { font-size: 10.5px; margin-top: 2px; }
"""

REPORT_CLIENT_SCRIPT = """
function($scope, $location) {
  var c = this;
  c.step = 1;
  c.submitting = false;
  var paramCat = $location.search().cat || 'Water';
  c.form = {
    category: paramCat,
    ward: 'Ward 12 - T. Nagar',
    title: '',
    description: '',
    address: '',
    geo: ''
  };

  c.detectGeo = function() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(pos) {
        $scope.$apply(function() {
          c.form.geo = 'Lat: ' + pos.coords.latitude.toFixed(4) + ', Long: ' + pos.coords.longitude.toFixed(4);
        });
      });
    } else {
      c.form.geo = 'Lat: 13.0418, Long: 80.2341 (Chennai Central)';
    }
  };

  c.submitIssue = function() {
    c.submitting = true;
    c.server.get({ action: 'submit_issue', form: c.form }).then(function(r) {
      c.submitting = false;
      if (r.data.status === 'success') {
        c.successData = r.data.ticket;
      }
    });
  };
}
"""

REPORT_SERVER_SCRIPT = """
(function() {
  if (input && input.action === 'submit_issue') {
    var f = input.form;
    var gr = new GlideRecord('incident');
    gr.initialize();
    gr.setValue('short_description', f.title);
    gr.setValue('description', f.description + '\n\nWard: ' + f.ward + '\nAddress: ' + f.address + (f.geo ? ('\nGPS: ' + f.geo) : ''));
    gr.setValue('category', f.category);
    gr.setValue('urgency', '2');
    gr.setValue('impact', '2');
    if (gs.isLoggedIn() && gs.getUserName() !== 'guest') {
      gr.setValue('caller_id', gs.getUserID());
    }
    var sysId = gr.insert();
    if (sysId) {
      var grRead = new GlideRecord('incident');
      grRead.get(sysId);
      data.status = 'success';
      data.ticket = {
        sys_id: sysId,
        number: grRead.getValue('number')
      };
    } else {
      data.status = 'error';
    }
  }
})();
"""


# ==============================================================================
# WIDGET 3: MY COMPLAINTS (PREMIUM INTERACTIVE WITH SHELL)
# ==============================================================================
CASES_TEMPLATE = """
<div class="civix-app-shell">
  __SIDEBAR_CASES__

  <main class="civix-main-column">
    __TOPBAR__

    <div class="civix-content-area">
      <!-- Page Header -->
      <div class="civix-page-top-bar civix-flex-split">
        <div>
          <h1 class="civix-page-heading-main">My Reported Complaints</h1>
          <p class="civix-page-sub-main">Track real-time status and municipal engineer updates across your ward.</p>
        </div>
        <a href="?id=civix_report_issue" class="btn btn-primary btn-lg" style="font-weight:700;">
          <span class="glyphicon glyphicon-plus"></span> Report New Issue
        </a>
      </div>

      <!-- 4 Status Summary Badges -->
      <div style="display:flex; gap:16px; margin-bottom: 22px; flex-wrap:wrap;">
        <button type="button" class="btn" ng-class="c.filterStatus === '' ? 'btn-primary' : 'btn-default'" ng-click="c.filterStatus = ''">
          All Cases ({{c.data.cases.length}})
        </button>
        <button type="button" class="btn" ng-class="c.filterStatus === 'In Progress' ? 'btn-warning' : 'btn-default'" ng-click="c.filterStatus = 'In Progress'">
          In Progress (3)
        </button>
        <button type="button" class="btn" ng-class="c.filterStatus === 'Resolved' ? 'btn-success' : 'btn-default'" ng-click="c.filterStatus = 'Resolved'">
          Resolved (8)
        </button>
        <button type="button" class="btn" ng-class="c.filterStatus === 'Awaiting Action' ? 'btn-danger' : 'btn-default'" ng-click="c.filterStatus = 'Awaiting Action'">
          Awaiting Action (1)
        </button>
      </div>

      <!-- Search & Category Filter Card -->
      <div class="civix-panel-card" style="padding:16px 20px; margin-bottom: 20px;">
        <div style="display:flex; gap:16px; align-items:center;">
          <div style="flex:1; position:relative;">
            <span class="glyphicon glyphicon-search" style="position:absolute; left:14px; top:12px; color:#94A3B8;"></span>
            <input type="text" class="form-control input-lg" style="padding-left:38px; border-radius:10px;" placeholder="Search complaints by case number, street or keyword..." ng-model="c.searchFilter" />
          </div>
          <div style="width:220px;">
            <select class="form-control input-lg" style="border-radius:10px;" ng-model="c.catFilter">
              <option value="">All Categories</option>
              <option value="Water">Water Supply</option>
              <option value="Electricity">Electricity</option>
              <option value="Roads">Roads</option>
              <option value="Drainage">Drainage</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Complaints List Cards -->
      <div class="civix-panel-card">
        <div class="civix-complaint-stack">
          <a ng-repeat="item in c.data.cases | filter:c.searchFilter | filter:{status: c.filterStatus, category: c.catFilter}" 
             href="?id=civix_track_case&sys_id={{item.sys_id}}" 
             class="civix-complaint-entry">
            <div class="civix-entry-thumb-box">
              <span class="glyphicon" ng-class="item.icon" style="font-size:20px; color:#0066FF;"></span>
            </div>
            <div class="civix-entry-info">
              <span class="civix-entry-ticket-id">{{item.number}}</span>
              <h4 class="civix-entry-headline">{{item.short_description}}</h4>
              <div class="civix-entry-meta">
                <span><span class="glyphicon glyphicon-map-marker text-primary"></span> {{item.location}}</span>
                <span><span class="glyphicon glyphicon-calendar text-muted"></span> {{item.date}}</span>
                <span class="label label-default" style="background:#E2E8F0; color:#334155; font-weight:600;">{{item.category}}</span>
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
  </main>
</div>
"""

CASES_TEMPLATE = CASES_TEMPLATE.replace("__SIDEBAR_CASES__", get_sidebar_html("complaints")).replace("__TOPBAR__", get_topbar_html())

CASES_CSS = BASE_SHELL_CSS + """
.civix-page-top-bar { margin-bottom: 20px; }
.civix-page-heading-main { font-size: 24px; font-weight: 800; color: #0F172A; margin: 0 0 4px 0; }
.civix-page-sub-main { font-size: 13.5px; color: #64748B; margin: 0; }
.civix-complaint-stack { display: flex; flex-direction: column; gap: 12px; }
.civix-complaint-entry {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 18px;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s;
}
.civix-complaint-entry:hover {
  background: #F8FAFC;
  border-color: #0066FF;
  transform: translateX(4px);
  text-decoration: none;
}
.civix-entry-thumb-box {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #EFF6FF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.civix-entry-info { flex-grow: 1; min-width: 0; }
.civix-entry-ticket-id { font-size: 11.5px; font-weight: 700; color: #0066FF; }
.civix-entry-headline { font-size: 14px; font-weight: 700; color: #0F172A; margin: 2px 0 4px 0; }
.civix-entry-meta { display: flex; gap: 16px; font-size: 11.5px; color: #64748B; }
.civix-entry-badge-col { display: flex; align-items: center; gap: 12px; flex-shrink: 0; }
.civix-badge-pill-status { font-size: 11.5px; font-weight: 700; padding: 5px 14px; border-radius: 16px; }
.pill-in-progress { background: #FEF3C7; color: #B45309; }
.pill-resolved { background: #DCFCE7; color: #15803D; }
.pill-awaiting { background: #FEE2E2; color: #B91C1C; }
.civix-entry-arrow { font-size: 20px; color: #94A3B8; }
"""

CASES_CLIENT_SCRIPT = """
function($scope) {
  var c = this;
  c.filterStatus = '';
  c.catFilter = '';
  c.searchFilter = '';
}
"""

CASES_SERVER_SCRIPT = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  data.citizenName = 'Priya Sharma';

  data.cases = [
    {
      sys_id: 'c1',
      number: 'CIVIX-2024-00123',
      short_description: 'Water leakage on 3rd Main Road',
      location: 'Adyar, Chennai',
      date: '15 Nov 2024, 10:24 AM',
      category: 'Water',
      status: 'In Progress',
      statusClass: 'in-progress',
      icon: 'glyphicon-tint'
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
      icon: 'glyphicon-flash'
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
      icon: 'glyphicon-road'
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
      icon: 'glyphicon-filter'
    }
  ];

  // Also query live incidents if any
  var gr = new GlideRecord('incident');
  gr.orderByDesc('sys_created_on');
  gr.setLimit(5);
  gr.query();
  while (gr.next()) {
    var st = gr.getValue('state');
    var stLabel = gr.getDisplayValue('state');
    var stClass = 'awaiting';
    if (st == '2') stClass = 'in-progress';
    else if (st == '6' || st == '7') stClass = 'resolved';
    data.cases.push({
      sys_id: gr.getUniqueValue(),
      number: gr.getValue('number'),
      short_description: gr.getValue('short_description'),
      location: 'Ward 12, Chennai',
      date: gr.getValue('sys_created_on'),
      category: gr.getDisplayValue('category') || 'Water',
      status: stLabel,
      statusClass: stClass,
      icon: 'glyphicon-folder-open'
    });
  }
})();
"""


# ==============================================================================
# WIDGET 4: CASE TRACKING (PREMIUM WITH SHELL)
# ==============================================================================
TRACK_TEMPLATE = """
<div class="civix-app-shell">
  __SIDEBAR_TRACK__

  <main class="civix-main-column">
    __TOPBAR__

    <div class="civix-content-area">
      <!-- Breadcrumb -->
      <div style="margin-bottom: 16px;">
        <a href="?id=civix_my_cases" class="text-primary" style="font-weight:700;">&larr; Back to My Complaints</a>
      </div>

      <div class="civix-panel-card" style="max-width: 980px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; padding-bottom: 20px; border-bottom: 1px solid #E2E8F0; margin-bottom: 24px;">
          <div>
            <span class="label label-primary" style="background:#0066FF; font-size:12px; padding:4px 10px;">{{c.data.case.category}}</span>
            <h1 style="font-size:24px; font-weight:800; color:#0F172A; margin:8px 0 4px 0;">{{c.data.case.number}} &bull; {{c.data.case.short_description}}</h1>
            <p class="text-muted"><span class="glyphicon glyphicon-map-marker text-primary"></span> {{c.data.case.location}} &bull; Submitted on: {{c.data.case.opened_at}}</p>
          </div>
          <div>
            <span class="civix-badge-pill-status pill-in-progress" style="font-size:14px; padding:6px 16px;">{{c.data.case.state}}</span>
          </div>
        </div>

        <!-- Lifecycle Stepper -->
        <div style="background:#F8FAFC; border: 1px solid #E2E8F0; border-radius:14px; padding: 24px; margin-bottom: 24px;">
          <h4 style="font-size: 15px; font-weight: 700; color: #0F172A; margin-top:0;">Municipal Resolution Lifecycle</h4>
          <div style="display:flex; justify-content:space-between; position:relative; margin-top: 24px;">
            <div ng-repeat="st in c.steps" style="text-align:center; flex:1;">
              <div style="width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 8px; font-weight:700; font-size:13px;"
                   ng-style="{'background': st.num <= c.data.case.stepNum ? '#0066FF' : '#E2E8F0', 'color': st.num <= c.data.case.stepNum ? '#FFFFFF' : '#64748B'}">
                {{st.num}}
              </div>
              <div style="font-size:12px; font-weight:600; color:#0F172A;">{{st.label}}</div>
            </div>
          </div>
        </div>

        <!-- Incident Details -->
        <div style="line-height: 1.8; font-size: 14px;">
          <h4 style="font-weight: 700;">Problem Description</h4>
          <p class="text-muted">{{c.data.case.description}}</p>
          <hr/>
          <h4 style="font-weight: 700;">Engineer Field Notes & Resolution Updates</h4>
          <p class="text-info" style="background:#EFF6FF; border-left:4px solid #0066FF; padding:12px; border-radius:4px;">
            {{c.data.case.resolution_notes}}
          </p>
        </div>
      </div>
    </div>
  </main>
</div>
"""

TRACK_TEMPLATE = TRACK_TEMPLATE.replace("__SIDEBAR_TRACK__", get_sidebar_html("complaints")).replace("__TOPBAR__", get_topbar_html())

TRACK_CSS = BASE_SHELL_CSS + """
.pill-in-progress { background: #FEF3C7; color: #B45309; }
.pill-resolved { background: #DCFCE7; color: #15803D; }
"""

TRACK_CLIENT_SCRIPT = """
function($scope) {
  var c = this;
  c.steps = [
    { num: 1, label: 'Submitted' },
    { num: 2, label: 'Under Review' },
    { num: 3, label: 'Assigned' },
    { num: 4, label: 'In Progress' },
    { num: 5, label: 'Resolved' },
    { num: 6, label: 'Closed' }
  ];
}
"""

TRACK_SERVER_SCRIPT = """
(function() {
  var sysId = $sp.getParameter('sys_id');
  data.case = {
    number: 'CIVIX-2024-00123',
    short_description: 'Water leakage on 3rd Main Road',
    category: 'Water Supply',
    location: 'Adyar, Ward 18, Chennai',
    opened_at: '15 Nov 2024, 10:24 AM',
    state: 'In Progress',
    stepNum: 4,
    description: 'Severe potable pipeline leak causing water accumulation near pedestrian crossway.',
    resolution_notes: 'Ward engineer and pipeline repair crew dispatched. Trenching in progress on site.'
  };

  if (sysId) {
    var gr = new GlideRecord('incident');
    if (gr.get(sysId)) {
      var st = gr.getValue('state');
      var step = 2;
      if (st == '2') step = 4;
      else if (st == '6') step = 5;
      else if (st == '7') step = 6;
      data.case = {
        sys_id: gr.getUniqueValue(),
        number: gr.getValue('number'),
        short_description: gr.getValue('short_description'),
        category: gr.getDisplayValue('category') || 'Water Supply',
        location: 'Ward 12, Chennai',
        opened_at: gr.getValue('sys_created_on'),
        state: gr.getDisplayValue('state'),
        stepNum: step,
        description: gr.getValue('description') || gr.getValue('short_description'),
        resolution_notes: gr.getValue('close_notes') || 'Assigned to field technician for resolution.'
      };
    }
  }
})();
"""


# ==============================================================================
# MAIN DEPLOYMENT ROUTINE
# ==============================================================================
if __name__ == "__main__":
    print("=== DEPLOYING FULL MULTI-PAGE PREMIUM REDESIGN ===")
    update_theme()

    print("\n--- 2. Updating Customer Home & Dashboard ---")
    update_widget("civix_home_widget", HOME_TEMPLATE, HOME_CSS, HOME_CLIENT_SCRIPT, HOME_SERVER_SCRIPT)
    update_widget("civix_dashboard_widget", HOME_TEMPLATE, HOME_CSS, HOME_CLIENT_SCRIPT, HOME_SERVER_SCRIPT)

    print("\n--- 3. Updating Report an Issue ---")
    update_widget("civix_report_issue_widget", REPORT_TEMPLATE, REPORT_CSS, REPORT_CLIENT_SCRIPT, REPORT_SERVER_SCRIPT)

    print("\n--- 4. Updating My Complaints ---")
    update_widget("civix_my_cases_widget", CASES_TEMPLATE, CASES_CSS, CASES_CLIENT_SCRIPT, CASES_SERVER_SCRIPT)

    print("\n--- 5. Updating Case Tracking ---")
    update_widget("civix_track_case_widget", TRACK_TEMPLATE, TRACK_CSS, TRACK_CLIENT_SCRIPT, TRACK_SERVER_SCRIPT)

    print("\n=== ALL PAGES FULLY UPGRADED TO PREMIUM ENTERPRISE STANDARD ===")
