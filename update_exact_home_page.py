"""
CIVIX AI - Exact Customer Home Page Implementation
Replicates the exact pixel-perfect design provided in the user's reference mockup.
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
    print(f"[UPDATED WIDGET] {widget_id} ({sys_id})")
    return sys_id

# Template matching the reference mockup EXACTLY
TEMPLATE = """
<div class="civix-root-layout">
  <!-- LEFT SIDEBAR -->
  <aside class="civix-sidebar" role="navigation" aria-label="Sidebar Navigation">
    <div class="civix-sidebar-bg"></div>
    <div class="civix-sidebar-content">
      <!-- Brand -->
      <div class="civix-brand-box">
        <a href="?id=civix_home" class="civix-brand-link">
          <div class="civix-brand-logo-wrap">
            <svg class="civix-city-icon" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="2" y="16" width="7" height="22" rx="1" fill="#0066FF"/>
              <rect x="11" y="8" width="9" height="30" rx="1" fill="#2563EB"/>
              <rect x="22" y="4" width="8" height="34" rx="1" fill="#1D4ED8"/>
              <rect x="32" y="12" width="6" height="26" rx="1" fill="#3B82F6"/>
              <!-- windows -->
              <circle cx="5.5" cy="20" r="1" fill="#93C5FD"/>
              <circle cx="5.5" cy="24" r="1" fill="#93C5FD"/>
              <circle cx="15.5" cy="13" r="1" fill="#DBEAFE"/>
              <circle cx="15.5" cy="18" r="1" fill="#DBEAFE"/>
              <circle cx="15.5" cy="23" r="1" fill="#DBEAFE"/>
              <circle cx="26" cy="9" r="1" fill="#EFF6FF"/>
              <circle cx="26" cy="14" r="1" fill="#EFF6FF"/>
              <circle cx="26" cy="19" r="1" fill="#EFF6FF"/>
              <circle cx="26" cy="24" r="1" fill="#EFF6FF"/>
            </svg>
            <div class="civix-brand-text-col">
              <span class="civix-logo-name">CIVIX AI</span>
              <span class="civix-logo-tagline">Smart Cities. Safer Communities.</span>
            </div>
          </div>
        </a>
      </div>

      <!-- Navigation Menu -->
      <nav class="civix-side-nav">
        <a href="?id=civix_home" class="civix-nav-btn" ng-class="{'active': c.currentTab === 'dashboard'}" ng-click="c.setTab('dashboard')">
          <span class="civix-icon-wrap"><i class="glyphicon glyphicon-home"></i></span>
          <span class="civix-nav-label">Dashboard</span>
        </a>
        <a href="?id=civix_report_issue" class="civix-nav-btn" ng-class="{'active': c.currentTab === 'report'}" ng-click="c.setTab('report')">
          <span class="civix-icon-wrap"><i class="glyphicon glyphicon-edit"></i></span>
          <span class="civix-nav-label">Report an Issue</span>
        </a>
        <a href="?id=civix_my_cases" class="civix-nav-btn" ng-class="{'active': c.currentTab === 'complaints'}" ng-click="c.setTab('complaints')">
          <span class="civix-icon-wrap"><i class="glyphicon glyphicon-list-alt"></i></span>
          <span class="civix-nav-label">My Complaints</span>
        </a>
        <a href="?id=civix_landing#services" class="civix-nav-btn" ng-class="{'active': c.currentTab === 'services'}" ng-click="c.setTab('services')">
          <span class="civix-icon-wrap"><i class="glyphicon glyphicon-info-sign"></i></span>
          <span class="civix-nav-label">Service Information</span>
        </a>
        <a href="?id=civix_landing#trust" class="civix-nav-btn" ng-class="{'active': c.currentTab === 'help'}" ng-click="c.setTab('help')">
          <span class="civix-icon-wrap"><i class="glyphicon glyphicon-headphones"></i></span>
          <span class="civix-nav-label">Help & Support</span>
        </a>
      </nav>

      <!-- Bottom Tagline -->
      <div class="civix-side-footer">
        <div class="civix-leaf-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2">
            <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>
            <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>
          </svg>
        </div>
        <div class="civix-green-motto">
          <span>Clean Cities</span>
          <span>Green Communities</span>
          <span>Better Tomorrows</span>
        </div>
      </div>
    </div>
  </aside>

  <!-- MAIN VIEWPORT -->
  <main class="civix-main-viewport">
    <!-- TOP BAR -->
    <header class="civix-topbar">
      <!-- Search -->
      <div class="civix-search-col">
        <div class="civix-search-wrapper">
          <span class="glyphicon glyphicon-search civix-search-icon"></span>
          <input type="text" class="civix-search-input" placeholder="Search services, complaints or help..." ng-model="c.searchQuery" />
        </div>
      </div>

      <!-- Right Nav Actions -->
      <div class="civix-top-actions">
        <!-- 22 Languages Selector -->
        <div class="civix-lang-dropdown-box">
          <button type="button" class="civix-lang-pill-btn" ng-click="c.toggleLang()" aria-expanded="{{c.langOpen}}">
            <span class="glyphicon glyphicon-globe"></span>
            <span class="civix-lang-txt">भारतीय भाषाएं / Language</span>
            <span class="glyphicon glyphicon-chevron-down civix-caret-icon"></span>
          </button>
          <div class="civix-lang-menu-card" ng-show="c.langOpen">
            <div class="civix-lang-scroll-list">
              <button type="button" class="civix-lang-row" ng-class="{'active': c.selectedLang === 'en'}" ng-click="c.selectLang('en')">
                <span class="glyphicon glyphicon-globe lang-icon"></span>
                <strong>English</strong>
              </button>
              <button type="button" class="civix-lang-row" ng-class="{'active': c.selectedLang === 'hi'}" ng-click="c.selectLang('hi')">
                <span class="lang-circle hi-c">हि</span>
                <span>हिन्दी</span> <small>Hindi</small>
              </button>
              <button type="button" class="civix-lang-row" ng-class="{'active': c.selectedLang === 'ta'}" ng-click="c.selectLang('ta')">
                <span class="lang-circle ta-c">த</span>
                <span>தமிழ்</span> <small>Tamil</small>
              </button>
              <button type="button" class="civix-lang-row" ng-class="{'active': c.selectedLang === 'te'}" ng-click="c.selectLang('te')">
                <span class="lang-circle te-c">తె</span>
                <span>తెలుగు</span> <small>Telugu</small>
              </button>
              <button type="button" class="civix-lang-row" ng-class="{'active': c.selectedLang === 'kn'}" ng-click="c.selectLang('kn')">
                <span class="lang-circle kn-c">ಕ</span>
                <span>ಕನ್ನಡ</span> <small>Kannada</small>
              </button>
              <button type="button" class="civix-lang-row" ng-class="{'active': c.selectedLang === 'ml'}" ng-click="c.selectLang('ml')">
                <span class="lang-circle ml-c">മ</span>
                <span>മലയാളം</span> <small>Malayalam</small>
              </button>
              <button type="button" class="civix-lang-row" ng-class="{'active': c.selectedLang === 'bn'}" ng-click="c.selectLang('bn')">
                <span class="lang-circle bn-c">বা</span>
                <span>বাংলা</span> <small>Bengali</small>
              </button>
              <button type="button" class="civix-lang-row" ng-class="{'active': c.selectedLang === 'mr'}" ng-click="c.selectLang('mr')">
                <span class="lang-circle mr-c">म</span>
                <span>मराठी</span> <small>Marathi</small>
              </button>
              <button type="button" class="civix-lang-row" ng-class="{'active': c.selectedLang === 'gu'}" ng-click="c.selectLang('gu')">
                <span class="lang-circle gu-c">ગુ</span>
                <span>ગુજરાતી</span> <small>Gujarati</small>
              </button>
            </div>
          </div>
        </div>

        <!-- Notification Bell -->
        <a href="#alerts" class="civix-bell-btn" title="3 Notifications">
          <span class="glyphicon glyphicon-bell"></span>
          <span class="civix-bell-badge">3</span>
        </a>

        <!-- Profile Avatar & Name -->
        <div class="civix-profile-pill">
          <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100&auto=format&fit=crop&q=80" alt="Priya Sharma" class="civix-user-photo" />
          <span class="civix-user-display">{{c.data.citizenName}}</span>
        </div>
      </div>
    </header>

    <!-- CONTENT BODY -->
    <div class="civix-content-body">
      <!-- HERO BANNER ROW -->
      <section class="civix-hero-banner-row">
        <!-- Welcome Card -->
        <div class="civix-welcome-card">
          <div class="civix-welcome-text-side">
            <h1 class="civix-welcome-title">Welcome back,<br/><span class="civix-user-heading">{{c.data.citizenName}}!</span> 👋</h1>
            <p class="civix-welcome-motto-1">Together for a cleaner, safer and smarter city.</p>
            <p class="civix-welcome-motto-2">Report issues, track progress and help improve our community.</p>
          </div>
          <!-- Weather / Ward Pill -->
          <div class="civix-weather-widget">
            <div class="civix-weather-top">
              <span class="glyphicon glyphicon-map-marker text-primary"></span>
              <strong>Chennai, Tamil Nadu</strong>
              <span class="glyphicon glyphicon-chevron-down civix-loc-caret"></span>
            </div>
            <div class="civix-weather-bottom">
              <div class="civix-temp-box">
                <span class="civix-deg">32°C</span>
                <span class="civix-condition">Mostly Clear</span>
              </div>
              <div class="civix-sun-icon">
                <svg width="34" height="34" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="5" fill="#F59E0B"/>
                  <path d="M12 1v3M12 20v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M1 12h3M20 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" stroke="#F59E0B" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Cleaner Cities Promo Card -->
        <div class="civix-promo-card">
          <div class="civix-promo-bg"></div>
          <div class="civix-promo-overlay">
            <h3>Cleaner Cities<br/>Happier People</h3>
            <div class="civix-promo-bar"></div>
          </div>
        </div>
      </section>

      <!-- 4 KPI SUMMARY CARDS -->
      <section class="civix-kpi-grid">
        <!-- 1. Total Complaints -->
        <a href="?id=civix_my_cases" class="civix-stat-card">
          <div class="civix-stat-icon-wrap bg-blue-subtle">
            <span class="glyphicon glyphicon-file text-blue"></span>
          </div>
          <div class="civix-stat-content">
            <div class="civix-stat-num">{{c.data.counts.total}}</div>
            <div class="civix-stat-label">Total Complaints <span class="civix-chev">&rsaquo;</span></div>
            <div class="civix-stat-change text-success">&uarr; 3 this month</div>
          </div>
        </a>

        <!-- 2. Resolved -->
        <a href="?id=civix_my_cases&status=Resolved" class="civix-stat-card">
          <div class="civix-stat-icon-wrap bg-green-subtle">
            <span class="glyphicon glyphicon-ok-sign text-green"></span>
          </div>
          <div class="civix-stat-content">
            <div class="civix-stat-num">{{c.data.counts.resolved}}</div>
            <div class="civix-stat-label">Resolved <span class="civix-chev">&rsaquo;</span></div>
            <div class="civix-stat-change text-success">&uarr; 2 this month</div>
          </div>
        </a>

        <!-- 3. In Progress -->
        <a href="?id=civix_my_cases&status=In%20Progress" class="civix-stat-card">
          <div class="civix-stat-icon-wrap bg-gold-subtle">
            <span class="glyphicon glyphicon-time text-gold"></span>
          </div>
          <div class="civix-stat-content">
            <div class="civix-stat-num">{{c.data.counts.in_progress}}</div>
            <div class="civix-stat-label">In Progress <span class="civix-chev">&rsaquo;</span></div>
            <div class="civix-stat-change text-gold-muted">&ndash; same as last month</div>
          </div>
        </a>

        <!-- 4. Awaiting Action -->
        <a href="?id=civix_my_cases&status=Awaiting%20Action" class="civix-stat-card">
          <div class="civix-stat-icon-wrap bg-red-subtle">
            <span class="glyphicon glyphicon-exclamation-sign text-red"></span>
          </div>
          <div class="civix-stat-content">
            <div class="civix-stat-num">{{c.data.counts.awaiting}}</div>
            <div class="civix-stat-label">Awaiting Action</div>
            <div class="civix-stat-change text-red">&darr; 1 from last month</div>
          </div>
        </a>
      </section>

      <!-- 3-COLUMN MAIN DASHBOARD GRID -->
      <div class="civix-main-columns">
        <!-- COLUMN 1: Report an Issue & Recent Complaints (Left, ~50% width) -->
        <div class="civix-col-left">
          <!-- Report a New Issue Section -->
          <div class="civix-white-card">
            <div class="civix-card-title-row">
              <h2 class="civix-card-title">Report a New Issue</h2>
              <p class="civix-card-sub">Select a service category to report an issue in your area.</p>
            </div>
            <!-- 5 Service Category Cards -->
            <div class="civix-categories-row">
              <!-- Water Supply -->
              <a href="?id=civix_report_issue&cat=Water" class="civix-cat-card">
                <div class="civix-cat-icon-circle cat-bg-water">
                  <span class="glyphicon glyphicon-tint text-water"></span>
                </div>
                <div class="civix-cat-heading">Water Supply <span class="civix-cat-arr">&rsaquo;</span></div>
                <p class="civix-cat-desc">No water, leakage, low pressure</p>
              </a>

              <!-- Electricity -->
              <a href="?id=civix_report_issue&cat=Electricity" class="civix-cat-card">
                <div class="civix-cat-icon-circle cat-bg-elec">
                  <span class="glyphicon glyphicon-flash text-elec"></span>
                </div>
                <div class="civix-cat-heading">Electricity <span class="civix-cat-arr">&rsaquo;</span></div>
                <p class="civix-cat-desc">Power outage, street lights</p>
              </a>

              <!-- Roads -->
              <a href="?id=civix_report_issue&cat=Roads" class="civix-cat-card">
                <div class="civix-cat-icon-circle cat-bg-roads">
                  <span class="glyphicon glyphicon-road text-roads"></span>
                </div>
                <div class="civix-cat-heading">Roads <span class="civix-cat-arr">&rsaquo;</span></div>
                <p class="civix-cat-desc">Potholes, damage, maintenance</p>
              </a>

              <!-- Drainage -->
              <a href="?id=civix_report_issue&cat=Drainage" class="civix-cat-card">
                <div class="civix-cat-icon-circle cat-bg-drain">
                  <span class="glyphicon glyphicon-filter text-drain"></span>
                </div>
                <div class="civix-cat-heading">Drainage <span class="civix-cat-arr">&rsaquo;</span></div>
                <p class="civix-cat-desc">Blockage, overflow, maintenance</p>
              </a>

              <!-- Waterlogging -->
              <a href="?id=civix_report_issue&cat=Waterlogging" class="civix-cat-card">
                <div class="civix-cat-icon-circle cat-bg-flood">
                  <span class="glyphicon glyphicon-random text-flood"></span>
                </div>
                <div class="civix-cat-heading">Waterlogging <span class="civix-cat-arr">&rsaquo;</span></div>
                <p class="civix-cat-desc">Rainwater, flooding, stagnation</p>
              </a>
            </div>
          </div>

          <!-- Recent Complaints Section -->
          <div class="civix-white-card">
            <div class="civix-card-title-row civix-row-between">
              <div>
                <h2 class="civix-card-title">Recent Complaints</h2>
                <p class="civix-card-sub">Here are your latest reported issues</p>
              </div>
              <a href="?id=civix_my_cases" class="civix-view-link">View All &rarr;</a>
            </div>

            <!-- Complaint List Items -->
            <div class="civix-complaints-box">
              <a ng-repeat="item in c.data.recentCases" href="?id=civix_track_case&sys_id={{item.sys_id}}" class="civix-complaint-row">
                <div class="civix-complaint-img-wrap">
                  <img ng-src="{{item.thumbUrl}}" alt="{{item.short_description}}" class="civix-complaint-thumb" />
                </div>
                <div class="civix-complaint-details">
                  <span class="civix-complaint-id">{{item.number}}</span>
                  <h4 class="civix-complaint-title">{{item.short_description}}</h4>
                  <div class="civix-complaint-meta">
                    <span><span class="glyphicon glyphicon-map-marker"></span> {{item.location}}</span>
                    <span><span class="glyphicon glyphicon-calendar"></span> {{item.date}}</span>
                  </div>
                </div>
                <div class="civix-complaint-action-col">
                  <span class="civix-pill-badge" ng-class="'badge-' + item.statusClass">{{item.status}}</span>
                  <span class="civix-row-chev">&rsaquo;</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <!-- COLUMN 2: Issue Map & Nearby Alerts (Middle, ~25% width) -->
        <div class="civix-col-mid">
          <!-- Issue Map Card -->
          <div class="civix-white-card civix-map-card">
            <div class="civix-card-title-row civix-row-between">
              <h2 class="civix-card-title">Issue Map</h2>
              <a href="?id=civix_landing#services" class="civix-view-link">View Full Map &rarr;</a>
            </div>
            <!-- Custom Chennai Styled Map -->
            <div class="civix-map-frame">
              <svg class="civix-svg-map" viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg">
                <!-- Map Background Water / Land -->
                <rect width="320" height="220" fill="#E8F1F2"/>
                <!-- Bay of Bengal Coastline -->
                <path d="M230,0 Q240,60 220,120 T240,220 L320,220 L320,0 Z" fill="#BFDBFE"/>
                <text x="250" y="115" font-size="16" font-weight="700" fill="#1E40AF" opacity="0.65">Chennai</text>
                <!-- Major Roads -->
                <path d="M0,80 L220,80" stroke="#CBD5E1" stroke-width="4"/>
                <path d="M0,150 L225,150" stroke="#CBD5E1" stroke-width="3"/>
                <path d="M120,0 L120,220" stroke="#CBD5E1" stroke-width="4"/>
                <path d="M180,0 L180,220" stroke="#CBD5E1" stroke-width="3"/>
                <path d="M50,0 Q130,90 200,220" stroke="#E2E8F0" stroke-width="2"/>
                <!-- Ward Labels -->
                <text x="130" y="55" font-size="10" font-weight="600" fill="#475569">Anna Nagar</text>
                <text x="75" y="125" font-size="10" font-weight="600" fill="#475569">T. Nagar</text>
                <text x="100" y="185" font-size="10" font-weight="600" fill="#475569">Velachery</text>
                <text x="175" y="195" font-size="10" font-weight="600" fill="#475569">Adyar</text>
                <!-- Pulse radar circle at T. Nagar -->
                <circle cx="130" cy="120" r="24" fill="#3B82F6" opacity="0.18"/>
                <circle cx="130" cy="120" r="14" fill="#3B82F6" opacity="0.35"/>
                <circle cx="130" cy="120" r="6" fill="#1D4ED8"/>
                <!-- Incident Pins -->
                <!-- Pin 1 Anna Nagar: Water (Blue) -->
                <circle cx="115" cy="48" r="6" fill="#0284C7"/>
                <!-- Pin 2 T. Nagar: Red alert -->
                <circle cx="75" cy="138" r="6" fill="#DC2626"/>
                <!-- Pin 3 Adyar: Green resolved -->
                <circle cx="195" cy="178" r="6" fill="#16A34A"/>
                <!-- Pin 4 Velachery: Yellow in progress -->
                <circle cx="145" cy="170" r="6" fill="#EAB308"/>
              </svg>
              <!-- Map Controls Overlays -->
              <div class="civix-map-ctrls">
                <button type="button" class="civix-map-btn" aria-label="Layers"><span class="glyphicon glyphicon-th-large"></span></button>
                <div class="civix-zoom-group">
                  <button type="button" class="civix-map-btn" aria-label="Zoom In">+</button>
                  <button type="button" class="civix-map-btn" aria-label="Zoom Out">&minus;</button>
                </div>
                <button type="button" class="civix-map-btn" aria-label="Locate Me"><span class="glyphicon glyphicon-screenshot"></span></button>
              </div>
            </div>
          </div>

          <!-- Nearby Alerts Card -->
          <div class="civix-white-card">
            <div class="civix-card-title-row civix-row-between">
              <h2 class="civix-card-title">Nearby Alerts</h2>
              <a href="?id=civix_landing#services" class="civix-view-link">View All &rarr;</a>
            </div>
            <!-- Alert Items List -->
            <div class="civix-alerts-stack">
              <!-- Alert 1: Road maintenance -->
              <div class="civix-alert-row">
                <div class="civix-alert-badge alert-bg-red">
                  <span class="glyphicon glyphicon-exclamation-sign text-white"></span>
                </div>
                <div class="civix-alert-text-side">
                  <h5 class="civix-alert-headline">Road maintenance work in T. Nagar</h5>
                  <div class="civix-alert-dist-meta">500 m &bull; Today</div>
                </div>
              </div>

              <!-- Alert 2: Scheduled power maintenance -->
              <div class="civix-alert-row">
                <div class="civix-alert-badge alert-bg-gold">
                  <span class="glyphicon glyphicon-flash text-white"></span>
                </div>
                <div class="civix-alert-text-side">
                  <h5 class="civix-alert-headline">Scheduled power maintenance - Anna Nagar</h5>
                  <div class="civix-alert-dist-meta">1.2 km &bull; Tomorrow</div>
                </div>
              </div>

              <!-- Alert 3: Possible waterlogging -->
              <div class="civix-alert-row">
                <div class="civix-alert-badge alert-bg-purple">
                  <span class="glyphicon glyphicon-tint text-white"></span>
                </div>
                <div class="civix-alert-text-side">
                  <h5 class="civix-alert-headline">Possible waterlogging in Velachery</h5>
                  <div class="civix-alert-dist-meta">2.3 km &bull; Today</div>
                </div>
              </div>

              <!-- Alert 4: Low water pressure -->
              <div class="civix-alert-row">
                <div class="civix-alert-badge alert-bg-blue">
                  <span class="glyphicon glyphicon-info-sign text-white"></span>
                </div>
                <div class="civix-alert-text-side">
                  <h5 class="civix-alert-headline">Low water pressure reported</h5>
                  <div class="civix-alert-dist-meta">3.1 km &bull; Today</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- COLUMN 3: Civic AI Assistant (Right, ~25% width) -->
        <div class="civix-col-right">
          <div class="civix-white-card civix-assistant-card-exact">
            <!-- Header -->
            <div class="civix-bot-header civix-row-between">
              <div class="civix-bot-title-grp">
                <span class="glyphicon glyphicon-user civix-bot-head-icon"></span>
                <strong>Civic AI Assistant</strong>
              </div>
              <div class="civix-bot-window-ctrls">
                <span class="glyphicon glyphicon-minus"></span>
                <span class="glyphicon glyphicon-option-horizontal"></span>
                <span class="glyphicon glyphicon-remove"></span>
              </div>
            </div>

            <!-- Body -->
            <div class="civix-bot-body">
              <!-- Robot Illustration -->
              <div class="civix-robot-avatar-center">
                <svg width="110" height="95" viewBox="0 0 120 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <!-- Robot Antenna -->
                  <circle cx="60" cy="12" r="5" fill="#0066FF"/>
                  <rect x="58" y="16" width="4" height="12" fill="#64748B"/>
                  <!-- Robot Head -->
                  <rect x="30" y="24" width="60" height="42" rx="14" fill="#FFFFFF" stroke="#0066FF" stroke-width="3"/>
                  <!-- Robot Visor Screen -->
                  <rect x="36" y="30" width="48" height="28" rx="8" fill="#0F172A"/>
                  <!-- Robot Glowing Blue Eyes -->
                  <circle cx="50" cy="44" r="5" fill="#38BDF8"/>
                  <circle cx="70" cy="44" r="5" fill="#38BDF8"/>
                  <!-- Headphones -->
                  <rect x="22" y="34" width="8" height="20" rx="3" fill="#0066FF"/>
                  <rect x="90" y="34" width="8" height="20" rx="3" fill="#0066FF"/>
                  <!-- Body -->
                  <rect x="42" y="68" width="36" height="28" rx="8" fill="#FFFFFF" stroke="#0066FF" stroke-width="3"/>
                  <rect x="48" y="74" width="24" height="12" rx="3" fill="#0066FF"/>
                  <text x="50" y="83" font-size="7" font-weight="900" fill="#FFFFFF">CIVIX</text>
                  <!-- Arms -->
                  <rect x="28" y="72" width="12" height="6" rx="3" fill="#64748B" transform="rotate(-30 28 72)"/>
                  <rect x="80" y="72" width="12" height="6" rx="3" fill="#64748B" transform="rotate(30 80 72)"/>
                </svg>
              </div>

              <!-- Greeting Message -->
              <div class="civix-bot-bubble">
                <p class="civix-bot-msg-hi">Hi Priya! 👋</p>
                <p class="civix-bot-msg-desc">I'm your Civic AI Assistant.<br/>How can I help you today?</p>
              </div>

              <!-- Quick Action Pills -->
              <div class="civix-bot-prompt-list">
                <a href="?id=civix_my_cases" class="civix-bot-pill">
                  <span class="glyphicon glyphicon-file"></span> Track my complaint
                </a>
                <a href="?id=civix_report_issue" class="civix-bot-pill">
                  <span class="glyphicon glyphicon-edit"></span> Report a new issue
                </a>
                <a href="?id=civix_landing#services" class="civix-bot-pill">
                  <span class="glyphicon glyphicon-map-marker"></span> Check nearby issues
                </a>
                <a href="?id=civix_landing#how-it-works" class="civix-bot-pill">
                  <span class="glyphicon glyphicon-info-sign"></span> Know service information
                </a>
                <a href="tel:1913" class="civix-bot-pill">
                  <span class="glyphicon glyphicon-question-sign"></span> Ask any question
                </a>
              </div>

              <!-- Chat Input Box with Mic and Send -->
              <div class="civix-bot-input-row">
                <input type="text" class="civix-bot-input" placeholder="Type your message..." ng-model="c.chatMsg" ng-keydown="c.onChatKey($event)" />
                <button type="button" class="civix-mic-btn" aria-label="Voice input">
                  <span class="glyphicon glyphicon-bullhorn"></span>
                </button>
                <button type="button" class="civix-send-btn" ng-click="c.sendChat()" aria-label="Send message">
                  <span class="glyphicon glyphicon-send"></span>
                </button>
              </div>

              <div class="civix-bot-footer-caption">
                I can assist you in all Indian languages
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</div>
"""

CSS = """
/* ROOT LAYOUT */
.civix-root-layout {
  display: flex;
  min-height: 100vh;
  background: #F1F5F9;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: #0F172A;
  margin: -15px -15px 0 -15px; /* cancel default portal container padding */
}

/* SIDEBAR */
.civix-sidebar {
  width: 240px;
  min-width: 240px;
  background: #0B192C;
  color: #FFFFFF;
  position: relative;
  display: flex;
  flex-direction: column;
  z-index: 50;
  box-shadow: 2px 0 10px rgba(0,0,0,0.2);
}
.civix-sidebar-bg {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(180deg, #0A192F 0%, #0F284E 50%, #0A192F 100%);
  opacity: 0.98;
}
.civix-sidebar-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 24px 16px;
}
.civix-brand-box {
  margin-bottom: 32px;
  padding-left: 4px;
}
.civix-brand-logo-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}
.civix-city-icon {
  width: 38px;
  height: 38px;
  flex-shrink: 0;
}
.civix-brand-text-col {
  display: flex;
  flex-direction: column;
}
.civix-logo-name {
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #FFFFFF;
  line-height: 1.1;
}
.civix-logo-tagline {
  font-size: 9.5px;
  color: #94A3B8;
  font-weight: 500;
}
.civix-side-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-grow: 1;
}
.civix-nav-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 16px;
  border-radius: 10px;
  color: #CBD5E1;
  font-size: 13.5px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.18s ease;
}
.civix-nav-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #FFFFFF;
  text-decoration: none;
}
.civix-nav-btn.active {
  background: #0066FF;
  color: #FFFFFF;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 102, 255, 0.35);
}
.civix-icon-wrap {
  font-size: 16px;
  width: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.civix-side-footer {
  margin-top: auto;
  padding-top: 24px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.civix-green-motto {
  display: flex;
  flex-direction: column;
  font-size: 10.5px;
  font-weight: 600;
  color: #22C55E;
  line-height: 1.35;
}

/* MAIN VIEWPORT */
.civix-main-viewport {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: #F8FAFC;
}

/* TOPBAR */
.civix-topbar {
  height: 68px;
  background: #FFFFFF;
  border-bottom: 1px solid #E2E8F0;
  padding: 0 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.civix-search-col {
  flex: 1;
  max-width: 480px;
}
.civix-search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.civix-search-icon {
  position: absolute;
  left: 14px;
  color: #94A3B8;
  font-size: 14px;
}
.civix-search-input {
  width: 100%;
  height: 40px;
  background: #F1F5F9;
  border: 1px solid transparent;
  border-radius: 20px;
  padding: 0 16px 0 38px;
  font-size: 13px;
  color: #0F172A;
  outline: none;
  transition: all 0.2s;
}
.civix-search-input:focus {
  background: #FFFFFF;
  border-color: #0066FF;
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}
.civix-top-actions {
  display: flex;
  align-items: center;
  gap: 18px;
}
.civix-lang-dropdown-box {
  position: relative;
}
.civix-lang-pill-btn {
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 12.5px;
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.civix-lang-pill-btn:hover {
  background: #E2E8F0;
}
.civix-caret-icon { font-size: 9px; opacity: 0.7; }
.civix-lang-menu-card {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 220px;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(0,0,0,0.12);
  z-index: 100;
  overflow: hidden;
}
.civix-lang-scroll-list {
  max-height: 280px;
  overflow-y: auto;
}
.civix-lang-row {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 14px;
  border: none;
  background: none;
  text-align: left;
  font-size: 13px;
  color: #1E293B;
  cursor: pointer;
}
.civix-lang-row:hover, .civix-lang-row.active {
  background: #EFF6FF;
  color: #0066FF;
}
.lang-circle {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: #FFFFFF;
}
.hi-c { background: #EA580C; }
.ta-c { background: #0284C7; }
.te-c { background: #16A34A; }
.kn-c { background: #9333EA; }
.ml-c { background: #0D9488; }
.bn-c { background: #DC2626; }
.mr-c { background: #E11D48; }
.gu-c { background: #D97706; }

.civix-bell-btn {
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
.civix-bell-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: #EF4444;
  color: #FFFFFF;
  font-size: 10px;
  font-weight: 700;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.civix-profile-pill {
  display: flex;
  align-items: center;
  gap: 10px;
}
.civix-user-photo {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #E2E8F0;
}
.civix-user-display {
  font-size: 13.5px;
  font-weight: 600;
  color: #0F172A;
}

/* CONTENT BODY */
.civix-content-body {
  padding: 24px 28px 60px;
  max-width: 1480px;
}

/* HERO BANNER ROW */
.civix-hero-banner-row {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 20px;
  margin-bottom: 22px;
}
.civix-welcome-card {
  background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%), url('https://images.unsplash.com/photo-1477959858617-67f30bc75b82?w=1200&auto=format&fit=crop&q=80') center/cover no-repeat;
  background-blend-mode: overlay;
  border-radius: 16px;
  padding: 28px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #CBD5E1;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.03);
}
.civix-welcome-title {
  font-size: 28px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1.15;
  margin: 0 0 8px 0;
}
.civix-user-heading {
  color: #0066FF;
}
.civix-welcome-motto-1 {
  font-size: 13.5px;
  font-weight: 600;
  color: #334155;
  margin: 0;
}
.civix-welcome-motto-2 {
  font-size: 12.5px;
  color: #64748B;
  margin: 2px 0 0 0;
}
.civix-weather-widget {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 12px 18px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}
.civix-weather-top {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #0F172A;
  margin-bottom: 6px;
}
.civix-weather-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.civix-deg {
  display: block;
  font-size: 20px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1;
}
.civix-condition {
  font-size: 11px;
  color: #64748B;
}

.civix-promo-card {
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  background: url('https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=600&auto=format&fit=crop&q=80') center/cover no-repeat;
  border: 1px solid #CBD5E1;
  display: flex;
  align-items: flex-end;
}
.civix-promo-overlay {
  width: 100%;
  background: linear-gradient(180deg, transparent 0%, rgba(15, 23, 42, 0.85) 100%);
  padding: 20px;
  color: #FFFFFF;
}
.civix-promo-overlay h3 {
  font-size: 16px;
  font-weight: 800;
  line-height: 1.3;
  margin: 0 0 8px 0;
}
.civix-promo-bar {
  width: 36px;
  height: 4px;
  background: #38BDF8;
  border-radius: 2px;
}

/* 4 KPI SUMMARY CARDS */
.civix-kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 22px;
}
.civix-stat-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 16px 18px;
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  transition: all 0.2s;
  box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}
.civix-stat-card:hover {
  transform: translateY(-2px);
  border-color: #0066FF;
  box-shadow: 0 6px 16px rgba(0, 102, 255, 0.08);
  text-decoration: none;
}
.civix-stat-icon-wrap {
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
.text-gold-muted { color: #B45309; }
.text-red { color: #DC2626; }
.civix-stat-num {
  font-size: 24px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1;
}
.civix-stat-label {
  font-size: 13px;
  font-weight: 600;
  color: #64748B;
  margin: 3px 0 2px 0;
}
.civix-chev { font-size: 15px; color: #94A3B8; }
.civix-stat-change {
  font-size: 11px;
  font-weight: 600;
}

/* 3-COLUMN MAIN DASHBOARD GRID */
.civix-main-columns {
  display: grid;
  grid-template-columns: 1fr 340px 300px;
  gap: 20px;
}
.civix-white-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 20px 22px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.civix-card-title-row {
  margin-bottom: 16px;
}
.civix-card-title {
  font-size: 16.5px;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 3px 0;
}
.civix-card-sub {
  font-size: 12.5px;
  color: #64748B;
  margin: 0;
}
.civix-row-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.civix-view-link {
  font-size: 12.5px;
  font-weight: 700;
  color: #0066FF;
  text-decoration: none;
}
.civix-view-link:hover { text-decoration: underline; }

/* 5 CATEGORY CARDS */
.civix-categories-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}
.civix-cat-card {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 16px 10px;
  text-align: center;
  text-decoration: none;
  transition: all 0.18s;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.civix-cat-card:hover {
  background: #FFFFFF;
  border-color: #0066FF;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 102, 255, 0.08);
  text-decoration: none;
}
.civix-cat-icon-circle {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-bottom: 10px;
}
.cat-bg-water { background: #E0F2FE; }
.cat-bg-elec { background: #FEF3C7; }
.cat-bg-roads { background: #F1F5F9; }
.cat-bg-drain { background: #DCFCE7; }
.cat-bg-flood { background: #F3E8FF; }
.text-water { color: #0284C7; }
.text-elec { color: #D97706; }
.text-roads { color: #334155; }
.text-drain { color: #16A34A; }
.text-flood { color: #9333EA; }
.civix-cat-heading {
  font-size: 13px;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 4px;
}
.civix-cat-arr { color: #94A3B8; font-weight: 700; }
.civix-cat-desc {
  font-size: 10.5px;
  color: #64748B;
  line-height: 1.35;
  margin: 0;
}

/* RECENT COMPLAINTS */
.civix-complaints-box {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.civix-complaint-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.15s;
}
.civix-complaint-row:hover {
  background: #F8FAFC;
  border-color: #CBD5E1;
  text-decoration: none;
}
.civix-complaint-img-wrap {
  width: 58px;
  height: 52px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background: #E2E8F0;
}
.civix-complaint-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.civix-complaint-details {
  flex-grow: 1;
  min-width: 0;
}
.civix-complaint-id {
  font-size: 11px;
  font-weight: 700;
  color: #0066FF;
}
.civix-complaint-title {
  font-size: 13.5px;
  font-weight: 600;
  color: #0F172A;
  margin: 2px 0 4px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.civix-complaint-meta {
  display: flex;
  gap: 14px;
  font-size: 11px;
  color: #64748B;
}
.civix-complaint-action-col {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}
.civix-pill-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 14px;
}
.badge-progress { background: #FEF3C7; color: #B45309; }
.badge-resolved { background: #DCFCE7; color: #15803D; }
.badge-awaiting { background: #FEE2E2; color: #B91C1C; }
.civix-row-chev { font-size: 18px; color: #94A3B8; }

/* MAP */
.civix-map-card { padding-bottom: 16px; }
.civix-map-frame {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #E2E8F0;
  background: #E8F1F2;
}
.civix-svg-map {
  width: 100%;
  height: auto;
  display: block;
}
.civix-map-ctrls {
  position: absolute;
  right: 10px;
  bottom: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.civix-map-btn {
  width: 26px;
  height: 26px;
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #334155;
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
  cursor: pointer;
}
.civix-zoom-group {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

/* NEARBY ALERTS */
.civix-alerts-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.civix-alert-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}
.civix-alert-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
  margin-top: 2px;
}
.alert-bg-red { background: #EF4444; }
.alert-bg-gold { background: #F59E0B; }
.alert-bg-purple { background: #A855F7; }
.alert-bg-blue { background: #0EA5E9; }
.civix-alert-text-side {
  flex-grow: 1;
}
.civix-alert-headline {
  font-size: 12.5px;
  font-weight: 600;
  color: #0F172A;
  margin: 0 0 2px 0;
  line-height: 1.35;
}
.civix-alert-dist-meta {
  font-size: 11px;
  color: #64748B;
}

/* CIVIC AI ASSISTANT PANEL */
.civix-assistant-card-exact {
  border-top: 4px solid #0066FF;
  padding: 16px 18px 20px;
}
.civix-bot-header {
  padding-bottom: 12px;
  border-bottom: 1px solid #F1F5F9;
  margin-bottom: 14px;
}
.civix-bot-title-grp {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #0F172A;
}
.civix-bot-head-icon {
  color: #0066FF;
  font-size: 16px;
}
.civix-bot-window-ctrls {
  display: flex;
  gap: 8px;
  color: #94A3B8;
  font-size: 11px;
}
.civix-robot-avatar-center {
  text-align: center;
  margin-bottom: 12px;
}
.civix-bot-bubble {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 14px;
  font-size: 12.5px;
  line-height: 1.45;
}
.civix-bot-msg-hi {
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 2px 0;
}
.civix-bot-msg-desc {
  color: #475569;
  margin: 0;
}
.civix-bot-prompt-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}
.civix-bot-pill {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 600;
  color: #334155;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.15s;
}
.civix-bot-pill:hover {
  background: #EFF6FF;
  border-color: #0066FF;
  color: #0066FF;
  text-decoration: none;
}
.civix-bot-input-row {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 4px 6px;
}
.civix-bot-input {
  flex-grow: 1;
  background: transparent;
  border: none;
  font-size: 12px;
  outline: none;
  padding: 4px 6px;
  color: #0F172A;
}
.civix-mic-btn {
  background: transparent;
  border: none;
  color: #64748B;
  font-size: 13px;
  cursor: pointer;
  padding: 4px;
}
.civix-send-btn {
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
.civix-bot-footer-caption {
  font-size: 10.5px;
  color: #94A3B8;
  text-align: center;
  margin-top: 10px;
}

@media (max-width: 1200px) {
  .civix-main-columns {
    grid-template-columns: 1fr;
  }
  .civix-hero-banner-row {
    grid-template-columns: 1fr;
  }
  .civix-kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .civix-categories-row {
    grid-template-columns: repeat(2, 1fr);
  }
}
"""

CLIENT_SCRIPT = """
function($scope, $window) {
  var c = this;
  c.currentTab = 'dashboard';
  c.langOpen = false;
  c.selectedLang = 'en';

  c.setTab = function(tab) {
    c.currentTab = tab;
  };

  c.toggleLang = function() {
    c.langOpen = !c.langOpen;
  };

  c.selectLang = function(code) {
    c.selectedLang = code;
    c.langOpen = false;
  };

  c.sendChat = function() {
    if (!c.chatMsg) return;
    $window.alert("Civic AI Assistant: Received query: '" + c.chatMsg + "'. Connecting to municipal knowledge agent...");
    c.chatMsg = '';
  };

  c.onChatKey = function(e) {
    if (e.keyCode === 13) {
      c.sendChat();
    }
  };
}
"""

SERVER_SCRIPT = """
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
      statusClass: 'progress',
      thumbUrl: 'https://images.unsplash.com/photo-1541888946425-d0fbb186c5f9?w=160&auto=format&fit=crop&q=80'
    },
    {
      sys_id: 'c2',
      number: 'CIVIX-2024-00118',
      short_description: 'Street light not working near Anna Nagar Park',
      location: 'Anna Nagar, Chennai',
      date: '10 Nov 2024, 06:12 PM',
      status: 'Resolved',
      statusClass: 'resolved',
      thumbUrl: 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=160&auto=format&fit=crop&q=80'
    },
    {
      sys_id: 'c3',
      number: 'CIVIX-2024-00110',
      short_description: 'Pothole near 100 Feet Road',
      location: 'T. Nagar, Chennai',
      date: '05 Nov 2024, 02:30 PM',
      status: 'Resolved',
      statusClass: 'resolved',
      thumbUrl: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=160&auto=format&fit=crop&q=80'
    },
    {
      sys_id: 'c4',
      number: 'CIVIX-2024-00102',
      short_description: 'Drainage overflow in residential area',
      location: 'Velachery, Chennai',
      date: '28 Oct 2024, 09:15 AM',
      status: 'Awaiting Action',
      statusClass: 'awaiting',
      thumbUrl: 'https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?w=160&auto=format&fit=crop&q=80'
    }
  ];
})();
"""

if __name__ == "__main__":
    print("=== Updating civix_home_widget and civix_dashboard_widget ===")
    update_widget("civix_home_widget", TEMPLATE, CSS, CLIENT_SCRIPT, SERVER_SCRIPT)
    update_widget("civix_dashboard_widget", TEMPLATE, CSS, CLIENT_SCRIPT, SERVER_SCRIPT)
    print("Completed!")
