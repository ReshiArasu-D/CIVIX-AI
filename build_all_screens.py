"""
CIVIX AI - Comprehensive Screen & Widget Deployment Script
Builds all 11 Phase 1 Service Portal screens, widgets, and links them to pages.
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


# ==============================================================================
# SCREEN 1: LANDING PAGE WIDGET
# ==============================================================================
def create_landing_widget():
    print("\n>>> Building Screen 1: Landing Page Widget")
    template = """
<div class="civix-page civix-landing">
  <!-- Hero Section -->
  <section class="civix-hero" aria-label="Hero Section">
    <div class="civix-container">
      <div class="row civix-hero-row">
        <div class="col-md-7 civix-hero-text">
          <div class="civix-badge-pill">
            <span class="glyphicon glyphicon-certificate"></span> Smart Urban Corporation Management
          </div>
          <h1 class="civix-hero-headline">Smarter Cities.<br/><span class="civix-highlight">Faster Civic Services.</span></h1>
          <p class="civix-hero-desc">
            Report water, electricity, road, and drainage issues. Follow your service requests and stay informed about improvements in your neighbourhood through one intelligent urban-services platform.
          </p>
          <div class="civix-hero-actions">
            <a href="?id=civix_report_issue" class="civix-btn civix-btn-lg civix-btn-primary">
              <span class="glyphicon glyphicon-bullhorn"></span> Report an Issue
            </a>
            <a href="#services" class="civix-btn civix-btn-lg civix-btn-outline" ng-click="c.scrollTo('services')">
              <span class="glyphicon glyphicon-th-list"></span> Explore Services
            </a>
          </div>
          <div class="civix-hero-stats">
            <div class="civix-stat-pill"><span class="civix-stat-dot"></span> 24x7 Digital Intake</div>
            <div class="civix-stat-pill"><span class="civix-stat-dot"></span> Real-time Ward Tracking</div>
            <div class="civix-stat-pill"><span class="civix-stat-dot"></span> 22 Scheduled Languages</div>
          </div>
        </div>
        <div class="col-md-5 civix-hero-visual">
          <div class="civix-hero-card">
            <div class="civix-hero-card-header">
              <span class="glyphicon glyphicon-map-marker text-primary"></span>
              <strong>Urban Civic Live Overview</strong>
            </div>
            <div class="civix-live-badge-row">
              <div class="civix-badge-box">
                <span class="civix-badge-num">100%</span>
                <span class="civix-badge-lbl">Wards Connected</span>
              </div>
              <div class="civix-badge-box">
                <span class="civix-badge-num">Verified</span>
                <span class="civix-badge-lbl">Officer Workflows</span>
              </div>
            </div>
            <div class="civix-card-notice-preview">
              <div class="civix-notice-tag">Notice</div>
              <p>Monsoon Preparedness & Desilting in Progress across Ward 12 & 14.</p>
            </div>
            <div class="civix-hero-card-cta">
              <a href="?id=civix_portal_select" class="btn btn-sm btn-block btn-info">Portal Selection &rarr;</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Civic Services Section -->
  <section id="services" class="civix-section civix-bg-light" aria-label="Civic Services">
    <div class="civix-container">
      <div class="civix-section-header text-center">
        <h2 class="civix-section-title">Core Municipal Services</h2>
        <p class="civix-section-subtitle">Select a service category to report an issue or review service standards.</p>
      </div>

      <div class="row civix-card-grid">
        <!-- 1. Water Supply -->
        <div class="col-md-3 col-sm-6">
          <div class="civix-service-card">
            <div class="civix-service-icon icon-water">
              <span class="glyphicon glyphicon-tint"></span>
            </div>
            <h3 class="civix-service-title">Water Supply</h3>
            <p class="civix-service-desc">Water interruption, pipeline leakage, contaminated water, or low pressure.</p>
            <a href="?id=civix_report_issue&cat=Water" class="civix-service-btn">
              Report Issue <span class="glyphicon glyphicon-arrow-right"></span>
            </a>
          </div>
        </div>

        <!-- 2. Electricity -->
        <div class="col-md-3 col-sm-6">
          <div class="civix-service-card">
            <div class="civix-service-icon icon-elec">
              <span class="glyphicon glyphicon-flash"></span>
            </div>
            <h3 class="civix-service-title">Electricity</h3>
            <p class="civix-service-desc">Streetlight outage, public electrical hazard, transformer sparks, or power failure.</p>
            <a href="?id=civix_report_issue&cat=Electricity" class="civix-service-btn">
              Report Issue <span class="glyphicon glyphicon-arrow-right"></span>
            </a>
          </div>
        </div>

        <!-- 3. Roads -->
        <div class="col-md-3 col-sm-6">
          <div class="civix-service-card">
            <div class="civix-service-icon icon-roads">
              <span class="glyphicon glyphicon-road"></span>
            </div>
            <h3 class="civix-service-title">Roads</h3>
            <p class="civix-service-desc">Dangerous potholes, broken road surfaces, damaged speed bumps, or cave-ins.</p>
            <a href="?id=civix_report_issue&cat=Roads" class="civix-service-btn">
              Report Issue <span class="glyphicon glyphicon-arrow-right"></span>
            </a>
          </div>
        </div>

        <!-- 4. Drainage -->
        <div class="col-md-3 col-sm-6">
          <div class="civix-service-card">
            <div class="civix-service-icon icon-drain">
              <span class="glyphicon glyphicon-filter"></span>
            </div>
            <h3 class="civix-service-title">Drainage & Waterlogging</h3>
            <p class="civix-service-desc">Blocked stormwater drains, sewage overflow, and monsoon street waterlogging.</p>
            <a href="?id=civix_report_issue&cat=Drainage" class="civix-service-btn">
              Report Issue <span class="glyphicon glyphicon-arrow-right"></span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- How It Works Section -->
  <section id="how-it-works" class="civix-section" aria-label="How It Works">
    <div class="civix-container">
      <div class="civix-section-header text-center">
        <h2 class="civix-section-title">How CIVIX AI Works</h2>
        <p class="civix-section-subtitle">Four transparent steps from reporting to verified resolution.</p>
      </div>

      <div class="row civix-stepper-row">
        <div class="col-md-3 col-sm-6 civix-step">
          <div class="civix-step-num">01</div>
          <h4 class="civix-step-title">1. Report</h4>
          <p class="civix-step-desc">Select a service, describe the problem, and pin the ward locality with optional photos.</p>
        </div>
        <div class="col-md-3 col-sm-6 civix-step">
          <div class="civix-step-num">02</div>
          <h4 class="civix-step-title">2. Review</h4>
          <p class="civix-step-desc">The request enters the municipal department workflow and is verified by ward officers.</p>
        </div>
        <div class="col-md-3 col-sm-6 civix-step">
          <div class="civix-step-num">03</div>
          <h4 class="civix-step-title">3. Track</h4>
          <p class="civix-step-desc">Follow the live status timeline and inspect public updates at every stage.</p>
        </div>
        <div class="col-md-3 col-sm-6 civix-step">
          <div class="civix-step-num">04</div>
          <h4 class="civix-step-title">4. Resolve</h4>
          <p class="civix-step-desc">Field teams complete work and upload resolution evidence for citizen confirmation.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Public Ward Notices -->
  <section class="civix-section civix-bg-light" aria-label="Public Ward Notices">
    <div class="civix-container">
      <div class="civix-section-header text-center">
        <h2 class="civix-section-title">Public Ward Announcements</h2>
        <p class="civix-section-subtitle">Official maintenance notices and community alerts across municipal zones.</p>
      </div>

      <div class="row">
        <div class="col-md-4 col-sm-6" ng-repeat="notice in c.data.notices">
          <div class="civix-notice-card">
            <div class="civix-notice-top">
              <span class="civix-notice-ward">{{notice.ward}}</span>
              <span class="civix-notice-date">{{notice.date}}</span>
            </div>
            <h4 class="civix-notice-title">{{notice.title}}</h4>
            <p class="civix-notice-desc">{{notice.desc}}</p>
            <div class="civix-notice-tag-badge">{{notice.category}}</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Trust and Transparency -->
  <section id="trust" class="civix-section civix-trust-section" aria-label="Trust and Transparency">
    <div class="civix-container">
      <div class="row">
        <div class="col-md-8 col-md-offset-2 text-center">
          <div class="civix-trust-icon">
            <span class="glyphicon glyphicon-lock"></span>
          </div>
          <h2 class="civix-section-title">Transparent & Accountable Urban Governance</h2>
          <p class="civix-trust-desc">
            CIVIX AI operates under strict municipal accountability guidelines. Citizen data is protected with role-based access control, human-in-the-loop oversight on all operational decisions, and transparent status histories for every public complaint.
          </p>
          <div class="civix-trust-pills">
            <span>Server-side Access Enforcement</span>
            <span>No Plaintext Secret Storage</span>
            <span>Audited Municipal Workflows</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>
"""

    css = """
.civix-landing {
  background: #F7FAFA;
  color: #183238;
}
.civix-container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 20px;
}
.civix-hero {
  background: linear-gradient(135deg, #123E46 0%, #0d2f35 100%);
  color: #FFFFFF;
  padding: 80px 0 90px;
  position: relative;
}
.civix-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(8, 127, 140, 0.4);
  color: #E1F5EA;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 24px;
  border: 1px solid rgba(225, 245, 234, 0.2);
}
.civix-hero-headline {
  font-size: 46px;
  font-weight: 800;
  line-height: 1.15;
  color: #FFFFFF;
  margin-bottom: 20px;
  letter-spacing: -0.5px;
}
.civix-highlight {
  color: #E1F5EA;
}
.civix-hero-desc {
  font-size: 18px;
  line-height: 1.6;
  color: #E1F5EA;
  opacity: 0.9;
  max-width: 580px;
  margin-bottom: 32px;
}
.civix-hero-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 36px;
  flex-wrap: wrap;
}
.civix-btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 15px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  cursor: pointer;
}
.civix-btn-primary {
  background: #087F8C;
  color: #FFFFFF;
  border: 1px solid #087F8C;
}
.civix-btn-primary:hover {
  background: #0db0c2;
  color: #FFFFFF;
  text-decoration: none;
}
.civix-btn-outline {
  background: transparent;
  color: #FFFFFF;
  border: 2px solid #E1F5EA;
}
.civix-btn-outline:hover {
  background: rgba(225, 245, 234, 0.15);
  color: #FFFFFF;
  text-decoration: none;
}
.civix-hero-stats {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}
.civix-stat-pill {
  font-size: 13px;
  color: #E1F5EA;
  display: flex;
  align-items: center;
  gap: 6px;
}
.civix-stat-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #087F8C;
}
.civix-hero-card {
  background: #FFFFFF;
  color: #183238;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
.civix-hero-card-header {
  font-size: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 18px;
  padding-bottom: 12px;
  border-bottom: 1px solid #DCE7E8;
}
.civix-live-badge-row {
  display: flex;
  gap: 12px;
  margin-bottom: 18px;
}
.civix-badge-box {
  flex: 1;
  background: #F7FAFA;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #DCE7E8;
  text-align: center;
}
.civix-badge-num {
  display: block;
  font-size: 20px;
  font-weight: 800;
  color: #087F8C;
}
.civix-badge-lbl {
  font-size: 11px;
  color: #61777B;
  text-transform: uppercase;
  font-weight: 600;
}
.civix-card-notice-preview {
  background: #E1F5EA;
  border-left: 4px solid #087F8C;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 13px;
  line-height: 1.4;
}
.civix-notice-tag {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  color: #087F8C;
  margin-bottom: 4px;
}
.civix-section {
  padding: 70px 0;
}
.civix-bg-light {
  background: #FFFFFF;
}
.civix-section-header {
  margin-bottom: 48px;
}
.civix-section-title {
  font-size: 32px;
  font-weight: 800;
  color: #123E46;
  margin-bottom: 12px;
}
.civix-section-subtitle {
  font-size: 16px;
  color: #61777B;
}
.civix-service-card {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 28px 20px;
  text-align: left;
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.civix-service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 24px rgba(8, 127, 140, 0.1);
  border-color: #087F8C;
}
.civix-service-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-bottom: 18px;
}
.icon-water { background: #E0F2FE; color: #0284C7; }
.icon-elec { background: #FEF3C7; color: #D97706; }
.icon-roads { background: #F3F4F6; color: #374151; }
.icon-drain { background: #EDE9FE; color: #7C3AED; }
.civix-service-title {
  font-size: 18px;
  font-weight: 700;
  color: #183238;
  margin-bottom: 8px;
}
.civix-service-desc {
  font-size: 13px;
  color: #61777B;
  line-height: 1.5;
  margin-bottom: 20px;
  flex-grow: 1;
}
.civix-service-btn {
  font-size: 13px;
  font-weight: 700;
  color: #087F8C;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.civix-service-btn:hover {
  color: #123E46;
  text-decoration: underline;
}
.civix-stepper-row {
  margin-top: 20px;
}
.civix-step {
  text-align: center;
  padding: 16px;
}
.civix-step-num {
  font-size: 36px;
  font-weight: 900;
  color: #087F8C;
  opacity: 0.3;
  margin-bottom: 8px;
}
.civix-step-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #183238;
}
.civix-step-desc {
  font-size: 13px;
  color: #61777B;
  line-height: 1.5;
}
.civix-notice-card {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}
.civix-notice-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}
.civix-notice-ward {
  font-weight: 700;
  color: #087F8C;
  font-size: 12px;
}
.civix-notice-date {
  color: #61777B;
  font-size: 12px;
}
.civix-notice-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #183238;
}
.civix-notice-desc {
  font-size: 13px;
  color: #61777B;
  line-height: 1.5;
  margin-bottom: 12px;
}
.civix-notice-tag-badge {
  display: inline-block;
  background: #E1F5EA;
  color: #18794E;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
}
.civix-trust-section {
  background: #123E46;
  color: #FFFFFF;
}
.civix-trust-section .civix-section-title {
  color: #FFFFFF;
}
.civix-trust-icon {
  font-size: 36px;
  color: #E1F5EA;
  margin-bottom: 16px;
}
.civix-trust-desc {
  font-size: 16px;
  line-height: 1.7;
  color: #E1F5EA;
  margin-bottom: 24px;
}
.civix-trust-pills {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}
.civix-trust-pills span {
  background: rgba(225, 245, 234, 0.15);
  border: 1px solid rgba(225, 245, 234, 0.3);
  color: #E1F5EA;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}
"""

    client_script = """
function($scope, $location) {
  var c = this;
  c.scrollTo = function(id) {
    var el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };
}
"""

    server_script = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  data.notices = [
    {
      title: 'Water Supply Pipeline Maintenance',
      ward: 'Ward 12 - T. Nagar',
      date: '10 Oct 2026',
      desc: 'Scheduled valve replacement work between 10:00 AM and 04:00 PM. Affected streets will resume normal pressure by evening.',
      category: 'Water'
    },
    {
      title: 'Street Lighting Grid Upgrades',
      ward: 'Ward 8 - Anna Nagar',
      date: '09 Oct 2026',
      desc: 'Installation of high-efficiency LED smart street poles along 3rd Main Road. Minor evening lane diversions.',
      category: 'Electricity'
    },
    {
      title: 'Monsoon Desilting & Road Patching',
      ward: 'Ward 15 - Velachery',
      date: '08 Oct 2026',
      desc: 'Preventive storm drain clearance and bituminous cold-mix road surface patching underway ahead of rains.',
      category: 'Roads & Drainage'
    }
  ];
})();
"""

    widget_data = {
        "name": "CIVIX AI - Landing Page",
        "id": "civix_landing_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_landing_widget", widget_data, "Landing Widget")
    page_id = create_page_structure("civix_landing", "Landing Page", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 2: PORTAL SELECTION WIDGET
# ==============================================================================
def create_portal_select_widget():
    print("\n>>> Building Screen 2: Portal Selection Widget")
    template = """
<div class="civix-page civix-container civix-portal-select">
  <div class="civix-select-header text-center">
    <div class="civix-back-row">
      <a href="?id=civix_landing" class="civix-back-link"><span class="glyphicon glyphicon-arrow-left"></span> Back to Home</a>
    </div>
    <h1 class="civix-section-title">Welcome to CIVIX AI</h1>
    <p class="civix-section-subtitle">Choose the portal that matches your role.</p>
  </div>

  <div class="row civix-portal-grid">
    <!-- 1. Citizen Portal (Active Phase 1) -->
    <div class="col-md-4 col-sm-12">
      <div class="civix-portal-card civix-portal-card-active">
        <div class="civix-portal-badge-active">Phase 1 Active</div>
        <div class="civix-portal-icon icon-citizen">
          <span class="glyphicon glyphicon-user"></span>
        </div>
        <h3 class="civix-portal-title">Citizen Portal</h3>
        <p class="civix-portal-desc">
          Report neighbourhood issues, track service requests in real time, and receive verified public service updates for your ward.
        </p>
        <ul class="civix-portal-features">
          <li><span class="glyphicon glyphicon-ok text-success"></span> 24x7 Civic Complaint Logging</li>
          <li><span class="glyphicon glyphicon-ok text-success"></span> Real-time Lifecycle Tracking</li>
          <li><span class="glyphicon glyphicon-ok text-success"></span> Ward Notices & Public Alerts</li>
        </ul>
        <a href="?id=civix_home" class="civix-btn civix-btn-primary btn-block">
          Continue as Citizen &rarr;
        </a>
      </div>
    </div>

    <!-- 2. Officer Portal (Phase 2) -->
    <div class="col-md-4 col-sm-12">
      <div class="civix-portal-card civix-portal-card-disabled">
        <div class="civix-portal-badge-muted">Phase 2 Scheduled</div>
        <div class="civix-portal-icon icon-officer">
          <span class="glyphicon glyphicon-briefcase"></span>
        </div>
        <h3 class="civix-portal-title">Officer Portal</h3>
        <p class="civix-portal-desc">
          Review incoming ward cases, manage staff assignments, assess service SLA performance, and monitor municipal operations.
        </p>
        <ul class="civix-portal-features text-muted">
          <li><span class="glyphicon glyphicon-time"></span> Automated Ward Case Routing</li>
          <li><span class="glyphicon glyphicon-time"></span> SLA Escalation Monitoring</li>
          <li><span class="glyphicon glyphicon-time"></span> Resource Dispatch Coordination</li>
        </ul>
        <button class="civix-btn civix-btn-disabled btn-block" disabled>
          Officer Portal — Coming in Phase 2
        </button>
      </div>
    </div>

    <!-- 3. Field Worker Portal (Phase 2) -->
    <div class="col-md-4 col-sm-12">
      <div class="civix-portal-card civix-portal-card-disabled">
        <div class="civix-portal-badge-muted">Phase 2 Scheduled</div>
        <div class="civix-portal-icon icon-worker">
          <span class="glyphicon glyphicon-wrench"></span>
        </div>
        <h3 class="civix-portal-title">Field Worker Portal</h3>
        <p class="civix-portal-desc">
          View assigned field jobs, update repair progress on mobile, and submit photographic resolution evidence directly from the site.
        </p>
        <ul class="civix-portal-features text-muted">
          <li><span class="glyphicon glyphicon-time"></span> Mobile Work Orders</li>
          <li><span class="glyphicon glyphicon-time"></span> Site Photographic Evidence</li>
          <li><span class="glyphicon glyphicon-time"></span> Real-time Resolution Sign-off</li>
        </ul>
        <button class="civix-btn civix-btn-disabled btn-block" disabled>
          Field Worker Portal — Coming in Phase 2
        </button>
      </div>
    </div>
  </div>
</div>
"""

    css = """
.civix-portal-select {
  padding: 60px 20px 80px;
}
.civix-select-header {
  margin-bottom: 50px;
}
.civix-back-row {
  margin-bottom: 16px;
}
.civix-back-link {
  color: #087F8C;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
}
.civix-back-link:hover {
  color: #123E46;
  text-decoration: underline;
}
.civix-portal-grid {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}
.civix-portal-card {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 36px 24px 28px;
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.2s;
}
.civix-portal-card-active {
  border-color: #087F8C;
  box-shadow: 0 12px 30px rgba(8, 127, 140, 0.12);
}
.civix-portal-card-active:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 36px rgba(8, 127, 140, 0.2);
}
.civix-portal-card-disabled {
  background: #F7FAFA;
  opacity: 0.85;
}
.civix-portal-badge-active {
  position: absolute;
  top: 14px;
  right: 14px;
  background: #E1F5EA;
  color: #18794E;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
}
.civix-portal-badge-muted {
  position: absolute;
  top: 14px;
  right: 14px;
  background: #E5E7EB;
  color: #6B7280;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
}
.civix-portal-icon {
  width: 60px;
  height: 60px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  margin-bottom: 20px;
}
.icon-citizen { background: #E1F5EA; color: #087F8C; }
.icon-officer { background: #E0E7FF; color: #4F46E5; }
.icon-worker { background: #FEF3C7; color: #D97706; }
.civix-portal-title {
  font-size: 22px;
  font-weight: 800;
  color: #183238;
  margin-bottom: 12px;
}
.civix-portal-desc {
  font-size: 14px;
  color: #61777B;
  line-height: 1.5;
  margin-bottom: 24px;
}
.civix-portal-features {
  list-style: none;
  padding: 0;
  margin: 0 0 28px 0;
  font-size: 13px;
  flex-grow: 1;
}
.civix-portal-features li {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.civix-btn-disabled {
  background: #E5E7EB;
  color: #6B7280;
  border: 1px solid #D1D5DB;
  cursor: not-allowed;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
}
"""

    widget_data = {
        "name": "CIVIX AI - Portal Selection",
        "id": "civix_portal_select_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": "function() {}",
        "script": "(function() {})();",
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_portal_select_widget", widget_data, "Portal Selection Widget")
    page_id = create_page_structure("civix_portal_select", "Portal Selection", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 3: CITIZEN PORTAL HOME WIDGET
# ==============================================================================
def create_home_widget():
    print("\n>>> Building Screen 3: Citizen Portal Home Widget")
    template = """
<div class="civix-page civix-container civix-home">
  <!-- Citizen Hero -->
  <div class="civix-home-hero">
    <div class="row">
      <div class="col-md-8">
        <span class="civix-tag text-uppercase">Citizen Services Portal</span>
        <h1 class="civix-home-title">Your Neighbourhood, Better Connected</h1>
        <p class="civix-home-desc">
          Report a civic issue or check the progress of an existing request. Direct connection to your ward engineers.
        </p>
        <div class="civix-home-actions">
          <a href="?id=civix_report_issue" class="civix-btn civix-btn-primary">
            <span class="glyphicon glyphicon-plus-sign"></span> Report an Issue
          </a>
          <a href="?id=civix_track_case" class="civix-btn civix-btn-outline-dark">
            <span class="glyphicon glyphicon-search"></span> Track My Cases
          </a>
        </div>
      </div>
      <div class="col-md-4 text-right">
        <div class="civix-quick-login-card" ng-if="!c.data.isLoggedIn">
          <h4>Already registered?</h4>
          <p>Sign in to view your personalized case history and active alerts.</p>
          <a href="?id=civix_login" class="btn btn-sm btn-primary btn-block">Sign In to Dashboard</a>
          <a href="?id=civix_register" class="btn btn-sm btn-default btn-block">Register New Account</a>
        </div>
      </div>
    </div>
  </div>

  <!-- Service Shortcuts -->
  <div class="civix-home-section">
    <h3 class="civix-subtitle">Select Issue Category</h3>
    <div class="row">
      <div class="col-md-3 col-sm-6" ng-repeat="cat in c.categories">
        <a href="?id=civix_report_issue&cat={{cat.name}}" class="civix-shortcut-card">
          <div class="civix-shortcut-icon" ng-class="cat.cssClass">
            <span class="glyphicon" ng-class="cat.icon"></span>
          </div>
          <div class="civix-shortcut-info">
            <h4 class="civix-shortcut-title">{{cat.name}}</h4>
            <span class="civix-shortcut-sub">{{cat.examples}}</span>
          </div>
          <span class="glyphicon glyphicon-chevron-right civix-shortcut-arrow"></span>
        </a>
      </div>
    </div>
  </div>

  <!-- Recent Cases (If logged in) or Public Ward Notices (If guest) -->
  <div class="civix-home-section" ng-if="c.data.isLoggedIn">
    <div class="civix-section-bar">
      <h3 class="civix-subtitle">My Recent Cases</h3>
      <a href="?id=civix_my_cases" class="civix-link-more">View All Cases &rarr;</a>
    </div>

    <div ng-if="c.data.cases.length === 0" class="civix-empty-state">
      <span class="glyphicon glyphicon-folder-open civix-empty-icon"></span>
      <h4>No Reported Cases Yet</h4>
      <p>You haven't reported any civic issues under this account.</p>
      <a href="?id=civix_report_issue" class="btn btn-sm btn-primary">Report Your First Issue</a>
    </div>

    <div class="row" ng-if="c.data.cases.length > 0">
      <div class="col-md-4 col-sm-6" ng-repeat="c_item in c.data.cases">
        <div class="civix-case-mini-card">
          <div class="civix-case-top">
            <strong class="civix-case-num">{{c_item.number}}</strong>
            <span class="civix-badge-state" ng-class="'badge-' + c_item.stateClass">{{c_item.state}}</span>
          </div>
          <h4 class="civix-case-title">{{c_item.short_description}}</h4>
          <div class="civix-case-meta">
            <span><span class="glyphicon glyphicon-tag"></span> {{c_item.category}}</span>
            <span><span class="glyphicon glyphicon-time"></span> {{c_item.opened_at}}</span>
          </div>
          <a href="?id=civix_track_case&sys_id={{c_item.sys_id}}" class="civix-case-track-btn">View Details &rarr;</a>
        </div>
      </div>
    </div>
  </div>

  <!-- Civic AI Assistant Modal Entry -->
  <div class="civix-assistant-entry-banner">
    <div class="civix-assistant-icon-big">
      <span class="glyphicon glyphicon-comment"></span>
    </div>
    <div class="civix-assistant-content">
      <h4>Need Immediate Help or Guidance?</h4>
      <p>Use our Civic Assistant to find your ward office, verify reporting steps, or query civic helpline information.</p>
    </div>
    <a href="?id=civix_report_issue" class="civix-btn civix-btn-primary">Ask Civic Assistant</a>
  </div>
</div>
"""

    css = """
.civix-home {
  padding: 40px 20px 80px;
}
.civix-home-hero {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 36px 32px;
  margin-bottom: 36px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.03);
}
.civix-tag {
  color: #087F8C;
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.5px;
}
.civix-home-title {
  font-size: 32px;
  font-weight: 800;
  color: #123E46;
  margin-top: 6px;
  margin-bottom: 12px;
}
.civix-home-desc {
  font-size: 15px;
  color: #61777B;
  max-width: 540px;
  margin-bottom: 24px;
}
.civix-home-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}
.civix-btn-outline-dark {
  background: transparent;
  color: #123E46;
  border: 2px solid #123E46;
}
.civix-btn-outline-dark:hover {
  background: #123E46;
  color: #FFFFFF;
  text-decoration: none;
}
.civix-quick-login-card {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 20px;
  text-align: left;
}
.civix-quick-login-card h4 {
  font-size: 15px;
  font-weight: 700;
  margin-top: 0;
}
.civix-quick-login-card p {
  font-size: 12px;
  color: #61777B;
}
.civix-home-section {
  margin-bottom: 40px;
}
.civix-subtitle {
  font-size: 20px;
  font-weight: 700;
  color: #183238;
  margin-bottom: 20px;
}
.civix-shortcut-card {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  text-decoration: none;
  color: #183238;
  margin-bottom: 16px;
  transition: all 0.2s;
}
.civix-shortcut-card:hover {
  border-color: #087F8C;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(8, 127, 140, 0.1);
  text-decoration: none;
}
.civix-shortcut-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}
.civix-shortcut-info {
  flex-grow: 1;
}
.civix-shortcut-title {
  font-size: 15px;
  font-weight: 700;
  margin: 0 0 2px 0;
  color: #183238;
}
.civix-shortcut-sub {
  font-size: 11px;
  color: #61777B;
}
.civix-shortcut-arrow {
  color: #A0B2B5;
  font-size: 12px;
}
.civix-section-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.civix-link-more {
  color: #087F8C;
  font-weight: 600;
  font-size: 13px;
  text-decoration: none;
}
.civix-empty-state {
  background: #FFFFFF;
  border: 1px dashed #DCE7E8;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
}
.civix-empty-icon {
  font-size: 40px;
  color: #A0B2B5;
  margin-bottom: 12px;
}
.civix-case-mini-card {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}
.civix-case-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}
.civix-case-num {
  color: #087F8C;
  font-size: 13px;
}
.civix-badge-state {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 12px;
  text-transform: uppercase;
}
.badge-in_progress { background: #FEF3C7; color: #B45309; }
.badge-resolved { background: #E1F5EA; color: #18794E; }
.badge-new { background: #E0F2FE; color: #0284C7; }
.civix-case-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 10px 0;
  line-height: 1.4;
  color: #183238;
}
.civix-case-meta {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #61777B;
  margin-bottom: 12px;
}
.civix-case-track-btn {
  font-size: 12px;
  font-weight: 700;
  color: #087F8C;
  text-decoration: none;
}
.civix-assistant-entry-banner {
  background: #123E46;
  color: #FFFFFF;
  border-radius: 14px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}
.civix-assistant-icon-big {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: #087F8C;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}
.civix-assistant-content {
  flex-grow: 1;
}
.civix-assistant-content h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 700;
}
.civix-assistant-content p {
  margin: 0;
  font-size: 13px;
  color: #E1F5EA;
  opacity: 0.9;
}
"""

    client_script = """
function($scope) {
  var c = this;
  c.categories = [
    { name: 'Water Supply', icon: 'glyphicon-tint', cssClass: 'icon-water', examples: 'Leakage, no water, low pressure' },
    { name: 'Electricity', icon: 'glyphicon-flash', cssClass: 'icon-elec', examples: 'Streetlights, power outage, hazard' },
    { name: 'Roads', icon: 'glyphicon-road', cssClass: 'icon-roads', examples: 'Potholes, surface damage, maintenance' },
    { name: 'Drainage', icon: 'glyphicon-filter', cssClass: 'icon-drain', examples: 'Blockage, overflow, waterlogging' }
  ];
}
"""

    server_script = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  data.cases = [];
  if (data.isLoggedIn) {
    var userId = gs.getUserID();
    var gr = new GlideRecord('incident');
    gr.addQuery('caller_id', userId);
    gr.orderByDesc('sys_created_on');
    gr.setLimit(3);
    gr.query();
    while (gr.next()) {
      var stateVal = gr.getValue('state');
      var stateLabel = gr.getDisplayValue('state');
      var stClass = 'new';
      if (stateVal == '2') stClass = 'in_progress';
      else if (stateVal == '6' || stateVal == '7') stClass = 'resolved';
      data.cases.push({
        sys_id: gr.getUniqueValue(),
        number: gr.getValue('number'),
        short_description: gr.getValue('short_description'),
        category: gr.getDisplayValue('category') || 'Civic Issue',
        state: stateLabel,
        stateClass: stClass,
        opened_at: gr.getValue('sys_created_on').split(' ')[0]
      });
    }
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Citizen Home",
        "id": "civix_home_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_home_widget", widget_data, "Citizen Home Widget")
    page_id = create_page_structure("civix_home", "Citizen Home", True, widget_id)
    return page_id, widget_id

print("Screen builders loaded.")

# ==============================================================================
# SCREEN 4: REGISTRATION WIDGET
# ==============================================================================
def create_register_widget():
    print("\n>>> Building Screen 4: Registration Widget")
    template = """
<div class="civix-page civix-container civix-auth-page">
  <div class="civix-auth-card">
    <div class="civix-auth-header text-center">
      <div class="civix-brand-mark"><span class="glyphicon glyphicon-user"></span></div>
      <h2 class="civix-auth-title">Create Your CIVIX AI Account</h2>
      <p class="civix-auth-subtitle">Register to report civic issues and follow your service requests.</p>
    </div>

    <div ng-if="c.successMsg" class="alert alert-success civix-alert">
      <h4><span class="glyphicon glyphicon-ok-sign"></span> Registration Successful!</h4>
      <p>{{c.successMsg}}</p>
      <div class="civix-smtp-note">
        <strong>Notice:</strong> Outbound email delivery (SMTP) is inactive on this developer instance. Your citizen account has been created directly in ServiceNow.
      </div>
      <div class="text-center" style="margin-top: 15px;">
        <a href="?id=civix_login" class="btn btn-primary">Proceed to Sign In &rarr;</a>
      </div>
    </div>

    <div ng-if="c.errorMsg" class="alert alert-danger civix-alert">
      <span class="glyphicon glyphicon-exclamation-sign"></span> {{c.errorMsg}}
    </div>

    <form ng-if="!c.successMsg" ng-submit="c.register()" novalidate>
      <!-- Group 1: Personal Details -->
      <div class="civix-form-section">
        <h4 class="civix-form-section-title">1. Personal Details</h4>
        <div class="form-group">
          <label for="fullName">Full Name <span class="text-danger">*</span></label>
          <input type="text" id="fullName" class="form-control" ng-model="c.form.fullName" required placeholder="e.g. Priya Sharma" />
        </div>
        <div class="row">
          <div class="col-md-6 form-group">
            <label for="mobile">Mobile Number (+91) <span class="text-danger">*</span></label>
            <div class="input-group">
              <span class="input-group-addon">+91</span>
              <input type="tel" id="mobile" class="form-control" ng-model="c.form.mobile" maxlength="10" placeholder="9876543210" required />
            </div>
          </div>
          <div class="col-md-6 form-group">
            <label for="email">Email Address <span class="text-danger">*</span></label>
            <input type="email" id="email" class="form-control" ng-model="c.form.email" required placeholder="priya@example.com" />
          </div>
        </div>
      </div>

      <!-- Group 2: Account Security (Independent eye toggles!) -->
      <div class="civix-form-section">
        <h4 class="civix-form-section-title">2. Account Security</h4>
        <div class="row">
          <div class="col-md-6 form-group">
            <label for="password">Password <span class="text-danger">*</span></label>
            <div class="input-group">
              <input type="{{c.showPwd ? 'text' : 'password'}}" id="password" class="form-control" ng-model="c.form.password" required placeholder="Min 8 characters" />
              <span class="input-group-btn">
                <button type="button" class="btn btn-default" ng-click="c.togglePwd()" aria-label="Toggle password visibility">
                  <span class="glyphicon" ng-class="c.showPwd ? 'glyphicon-eye-close' : 'glyphicon-eye-open'"></span>
                </button>
              </span>
            </div>
          </div>
          <div class="col-md-6 form-group">
            <label for="confirmPassword">Confirm Password <span class="text-danger">*</span></label>
            <div class="input-group">
              <input type="{{c.showConfirmPwd ? 'text' : 'password'}}" id="confirmPassword" class="form-control" ng-model="c.form.confirmPassword" required placeholder="Re-enter password" />
              <span class="input-group-btn">
                <button type="button" class="btn btn-default" ng-click="c.toggleConfirmPwd()" aria-label="Toggle confirm password visibility">
                  <span class="glyphicon" ng-class="c.showConfirmPwd ? 'glyphicon-eye-close' : 'glyphicon-eye-open'"></span>
                </button>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Group 3: Location -->
      <div class="civix-form-section">
        <h4 class="civix-form-section-title">3. Municipal Locality</h4>
        <div class="row">
          <div class="col-md-4 form-group">
            <label for="state">State / UT <span class="text-danger">*</span></label>
            <select id="state" class="form-control" ng-model="c.form.state">
              <option value="Tamil Nadu">Tamil Nadu</option>
              <option value="Karnataka">Karnataka</option>
              <option value="Maharashtra">Maharashtra</option>
              <option value="Delhi">Delhi</option>
              <option value="Telangana">Telangana</option>
              <option value="Kerala">Kerala</option>
            </select>
          </div>
          <div class="col-md-4 form-group">
            <label for="district">District <span class="text-danger">*</span></label>
            <input type="text" id="district" class="form-control" ng-model="c.form.district" placeholder="e.g. Chennai" required />
          </div>
          <div class="col-md-4 form-group">
            <label for="city">City / Town <span class="text-danger">*</span></label>
            <input type="text" id="city" class="form-control" ng-model="c.form.city" placeholder="e.g. Chennai" required />
          </div>
        </div>
        <div class="form-group">
          <label for="ward">Ward / Locality (Optional)</label>
          <input type="text" id="ward" class="form-control" ng-model="c.form.ward" placeholder="e.g. Ward 12 - T. Nagar" />
        </div>
      </div>

      <!-- Group 4: Preferences & Consent -->
      <div class="civix-form-section">
        <h4 class="civix-form-section-title">4. Preferences & Consent</h4>
        <div class="form-group">
          <label for="prefLang">Preferred Language</label>
          <select id="prefLang" class="form-control" ng-model="c.form.prefLang">
            <option value="en">English</option>
            <option value="ta">Tamil (தமிழ்)</option>
            <option value="hi">Hindi (हिन्दी)</option>
            <option value="te">Telugu (తెలుగు)</option>
            <option value="kn">Kannada (ಕನ್ನಡ)</option>
            <option value="ml">Malayalam (മലയാളം)</option>
          </select>
        </div>
        <div class="checkbox">
          <label>
            <input type="checkbox" ng-model="c.form.consent" required />
            I agree to the CIVIX AI Municipal Terms of Service and Privacy Policy. I confirm I am a resident registering for civic assistance.
          </label>
        </div>
      </div>

      <div class="civix-form-actions">
        <button type="submit" class="civix-btn civix-btn-primary btn-block btn-lg" ng-disabled="c.loading">
          <span ng-if="c.loading"><span class="glyphicon glyphicon-refresh glyphicon-spin"></span> Creating Account...</span>
          <span ng-if="!c.loading"><span class="glyphicon glyphicon-check"></span> Register Citizen Account</span>
        </button>
      </div>

      <div class="text-center civix-auth-footer">
        Already have an account? <a href="?id=civix_login" class="civix-link">Sign In</a>
      </div>
    </form>
  </div>
</div>
"""

    css = """
.civix-auth-page {
  padding: 50px 20px 80px;
}
.civix-auth-card {
  max-width: 680px;
  margin: 0 auto;
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 36px 32px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}
.civix-brand-mark {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: #E1F5EA;
  color: #087F8C;
  font-size: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}
.civix-auth-title {
  font-size: 24px;
  font-weight: 800;
  color: #123E46;
  margin: 0 0 6px 0;
}
.civix-auth-subtitle {
  color: #61777B;
  font-size: 14px;
  margin-bottom: 24px;
}
.civix-form-section {
  border-bottom: 1px solid #E5E7EB;
  padding-bottom: 20px;
  margin-bottom: 20px;
}
.civix-form-section-title {
  font-size: 14px;
  font-weight: 700;
  color: #087F8C;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 14px;
}
.civix-smtp-note {
  background: #FEF3C7;
  color: #92400E;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 12px;
  margin-top: 10px;
}
.civix-link {
  color: #087F8C;
  font-weight: 700;
}
.civix-auth-footer {
  margin-top: 20px;
  font-size: 14px;
  color: #61777B;
}
"""

    client_script = """
function($scope) {
  var c = this;
  c.form = {
    state: 'Tamil Nadu',
    prefLang: 'en',
    consent: false
  };
  c.showPwd = false;
  c.showConfirmPwd = false;
  c.loading = false;

  c.togglePwd = function() { c.showPwd = !c.showPwd; };
  c.toggleConfirmPwd = function() { c.showConfirmPwd = !c.showConfirmPwd; };

  c.register = function() {
    c.errorMsg = '';
    c.successMsg = '';
    if (!c.form.fullName || !c.form.mobile || !c.form.email || !c.form.password) {
      c.errorMsg = 'Please complete all required fields.';
      return;
    }
    if (c.form.mobile.length !== 10 || !/^[0-9]+$/.test(c.form.mobile)) {
      c.errorMsg = 'Please enter a valid 10-digit Indian mobile number.';
      return;
    }
    if (c.form.password.length < 8) {
      c.errorMsg = 'Password must be at least 8 characters long.';
      return;
    }
    if (c.form.password !== c.form.confirmPassword) {
      c.errorMsg = 'Passwords do not match.';
      return;
    }
    if (!c.form.consent) {
      c.errorMsg = 'You must agree to the Terms of Service to register.';
      return;
    }

    c.loading = true;
    c.server.get({ action: 'register', form: c.form }).then(function(r) {
      c.loading = false;
      if (r.data.status === 'success') {
        c.successMsg = r.data.message;
      } else {
        c.errorMsg = r.data.message || 'Registration failed. Please try again.';
      }
    });
  };
}
"""

    server_script = """
(function() {
  if (input && input.action === 'register') {
    var form = input.form;
    if (!form || !form.email || !form.password) {
      data.status = 'error';
      data.message = 'Missing required registration parameters.';
      return;
    }

    // Check duplicate
    var grUserCheck = new GlideRecord('sys_user');
    grUserCheck.addQuery('email', form.email);
    grUserCheck.query();
    if (grUserCheck.hasNext()) {
      data.status = 'error';
      data.message = 'An account with this email address already exists. Please sign in instead.';
      return;
    }

    // Create user natively in sys_user
    var grUser = new GlideRecord('sys_user');
    grUser.initialize();
    grUser.setValue('user_name', form.email.toLowerCase());
    grUser.setValue('email', form.email.toLowerCase());
    grUser.setValue('first_name', form.fullName.split(' ')[0]);
    var lastParts = form.fullName.split(' ');
    lastParts.shift();
    grUser.setValue('last_name', lastParts.join(' ') || 'Citizen');
    grUser.setValue('mobile_phone', '+91 ' + form.mobile);
    grUser.setValue('city', form.city || form.district || 'Chennai');
    grUser.setValue('user_password', form.password);
    grUser.setValue('active', true);
    var newUserId = grUser.insert();

    if (newUserId) {
      // Safely assign x_civic_ai_citizen role
      var grRole = new GlideRecord('sys_user_role');
      if (grRole.get('name', 'x_civic_ai_citizen')) {
        var grUserRole = new GlideRecord('sys_user_has_role');
        grUserRole.initialize();
        grUserRole.setValue('user', newUserId);
        grUserRole.setValue('role', grRole.getUniqueValue());
        grUserRole.insert();
      }

      data.status = 'success';
      data.message = 'Citizen account successfully created for ' + form.fullName + ' (' + form.email + '). You can now sign in to access your dashboard.';
    } else {
      data.status = 'error';
      data.message = 'Unable to create user record. Please check instance security permissions.';
    }
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Registration",
        "id": "civix_register_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_register_widget", widget_data, "Registration Widget")
    page_id = create_page_structure("civix_register", "Registration", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 5: LOGIN WIDGET
# ==============================================================================
def create_login_widget():
    print("\n>>> Building Screen 5: Login Widget")
    template = """
<div class="civix-page civix-container civix-auth-page">
  <div class="civix-auth-card civix-login-card">
    <div class="civix-auth-header text-center">
      <div class="civix-brand-mark"><span class="glyphicon glyphicon-lock"></span></div>
      <h2 class="civix-auth-title">Welcome Back</h2>
      <p class="civix-auth-subtitle">Sign in to manage your civic-service requests.</p>
    </div>

    <div ng-if="c.errorMsg" class="alert alert-danger civix-alert">
      <span class="glyphicon glyphicon-exclamation-sign"></span> {{c.errorMsg}}
    </div>

    <div ng-if="c.data.isLoggedIn" class="alert alert-info text-center">
      <p>You are already signed in as <strong>{{c.data.userName}}</strong>.</p>
      <a href="?id=civix_dashboard" class="btn btn-primary" style="margin-top: 10px;">Go to Citizen Dashboard &rarr;</a>
    </div>

    <form ng-if="!c.data.isLoggedIn" ng-submit="c.login()" novalidate>
      <div class="form-group">
        <label for="username">User ID / Registered Email <span class="text-danger">*</span></label>
        <input type="text" id="username" class="form-control" ng-model="c.username" required placeholder="admin or citizen email" />
      </div>

      <div class="form-group">
        <div class="civix-pwd-label-row">
          <label for="loginPassword">Password <span class="text-danger">*</span></label>
          <a href="?id=civix_recovery" class="civix-forgot-link">Forgot Password?</a>
        </div>
        <div class="input-group">
          <input type="{{c.showPwd ? 'text' : 'password'}}" id="loginPassword" class="form-control" ng-model="c.password" required placeholder="Enter your password" />
          <span class="input-group-btn">
            <button type="button" class="btn btn-default" ng-click="c.togglePwd()" aria-label="Toggle password visibility">
              <span class="glyphicon" ng-class="c.showPwd ? 'glyphicon-eye-close' : 'glyphicon-eye-open'"></span>
            </button>
          </span>
        </div>
      </div>

      <div class="checkbox">
        <label>
          <input type="checkbox" ng-model="c.rememberMe" /> Remember me on this device
        </label>
      </div>

      <div class="civix-form-actions">
        <button type="submit" class="civix-btn civix-btn-primary btn-block btn-lg" ng-disabled="c.loading">
          <span ng-if="c.loading"><span class="glyphicon glyphicon-refresh glyphicon-spin"></span> Verifying...</span>
          <span ng-if="!c.loading"><span class="glyphicon glyphicon-log-in"></span> Sign In</span>
        </button>
      </div>

      <div class="text-center civix-auth-footer">
        Don't have an account? <a href="?id=civix_register" class="civix-link">Create Account</a>
      </div>
      <div class="text-center" style="margin-top: 10px;">
        <a href="?id=civix_landing" class="text-muted"><small>&larr; Back to Public Landing Page</small></a>
      </div>
    </form>
  </div>
</div>
"""

    css = """
.civix-login-card {
  max-width: 460px;
}
.civix-pwd-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.civix-forgot-link {
  font-size: 12px;
  color: #087F8C;
  font-weight: 600;
}
"""

    client_script = """
function($scope, $window) {
  var c = this;
  c.showPwd = false;
  c.loading = false;
  c.togglePwd = function() { c.showPwd = !c.showPwd; };

  c.login = function() {
    c.errorMsg = '';
    if (!c.username || !c.password) {
      c.errorMsg = 'Please enter both User ID/Email and Password.';
      return;
    }
    c.loading = true;
    c.server.get({ action: 'login', user: c.username, pass: c.password }).then(function(r) {
      c.loading = false;
      if (r.data.authStatus === 'success') {
        $window.location.href = '?id=civix_dashboard';
      } else {
        c.errorMsg = r.data.authMessage || 'Invalid credentials. Please verify your username and password.';
      }
    });
  };
}
"""

    server_script = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  if (data.isLoggedIn) {
    data.userName = gs.getUserDisplayName();
  }

  if (input && input.action === 'login') {
    var user = input.user;
    var pass = input.pass;
    var auth = new GlideAuthenticator();
    var session = auth.login(user, pass);
    if (session) {
      data.authStatus = 'success';
    } else {
      data.authStatus = 'failed';
      data.authMessage = 'Invalid credentials. Please check your username and password.';
    }
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Login",
        "id": "civix_login_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_login_widget", widget_data, "Login Widget")
    page_id = create_page_structure("civix_login", "Login", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 6: ACCOUNT RECOVERY WIDGET
# ==============================================================================
def create_recovery_widget():
    print("\n>>> Building Screen 6: Account Recovery Widget")
    template = """
<div class="civix-page civix-container civix-auth-page">
  <div class="civix-auth-card civix-login-card">
    <div class="civix-auth-header text-center">
      <div class="civix-brand-mark"><span class="glyphicon glyphicon-refresh"></span></div>
      <h2 class="civix-auth-title">Account Recovery</h2>
      <p class="civix-auth-subtitle">Enter your registered email address or username to receive password reset guidance.</p>
    </div>

    <div ng-if="c.submitted" class="alert alert-success">
      <h4><span class="glyphicon glyphicon-ok-sign"></span> Recovery Request Received</h4>
      <p>If an account exists for the provided identifier, instructions have been generated according to municipal security policy.</p>
      <div class="civix-smtp-note" style="margin-top: 10px;">
        <strong>Notice:</strong> Outbound SMTP is disabled on this ServiceNow development instance. For sandbox password resets, please contact the instance administrator.
      </div>
      <div class="text-center" style="margin-top: 16px;">
        <a href="?id=civix_login" class="btn btn-default">&larr; Return to Sign In</a>
      </div>
    </div>

    <form ng-if="!c.submitted" ng-submit="c.submitRecovery()">
      <div class="form-group">
        <label for="recoveryId">Registered Email or Username <span class="text-danger">*</span></label>
        <input type="text" id="recoveryId" class="form-control" ng-model="c.recoveryId" required placeholder="priya@example.com" />
      </div>

      <div class="civix-form-actions">
        <button type="submit" class="civix-btn civix-btn-primary btn-block btn-lg" ng-disabled="c.loading">
          <span class="glyphicon glyphicon-send"></span> Submit Recovery Request
        </button>
      </div>

      <div class="text-center civix-auth-footer">
        <a href="?id=civix_login" class="civix-link">&larr; Back to Sign In</a>
      </div>
    </form>
  </div>
</div>
"""

    css = """
.civix-auth-card { max-width: 480px; }
"""

    client_script = """
function($scope) {
  var c = this;
  c.submitted = false;
  c.submitRecovery = function() {
    if (!c.recoveryId) return;
    c.loading = true;
    c.server.get({ action: 'recover', id: c.recoveryId }).then(function() {
      c.loading = false;
      c.submitted = true;
    });
  };
}
"""

    server_script = """
(function() {
  if (input && input.action === 'recover') {
    // Privacy-preserving: Do not reveal whether user exists
    data.received = true;
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Account Recovery",
        "id": "civix_recovery_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_recovery_widget", widget_data, "Recovery Widget")
    page_id = create_page_structure("civix_recovery", "Account Recovery", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 7: CUSTOMER DASHBOARD WIDGET (Faithful to design image reference)
# ==============================================================================
def create_dashboard_widget():
    print("\n>>> Building Screen 7: Customer Dashboard Widget")
    template = """
<div class="civix-dashboard-page">
  <div class="civix-dashboard-container">
    <!-- Top Greeting Banner -->
    <div class="civix-greeting-banner">
      <div class="civix-greeting-left">
        <h1 class="civix-welcome-text">Welcome back,<br/><span class="civix-welcome-name">{{c.data.citizenName}}!</span> 👋</h1>
        <p class="civix-welcome-sub">Together for a cleaner, safer and smarter city. Report issues, track progress and help improve our community.</p>
      </div>
      <div class="civix-weather-pill">
        <div class="civix-loc-icon"><span class="glyphicon glyphicon-map-marker"></span></div>
        <div class="civix-loc-info">
          <strong>Chennai, Tamil Nadu</strong>
          <small>32°C &bull; Mostly Clear &bull; Ward 12</small>
        </div>
      </div>
    </div>

    <!-- 4 KPI Summary Cards -->
    <div class="row civix-kpi-row">
      <div class="col-md-3 col-sm-6">
        <div class="civix-kpi-card kpi-total">
          <div class="civix-kpi-icon"><span class="glyphicon glyphicon-file"></span></div>
          <div class="civix-kpi-body">
            <div class="civix-kpi-num">{{c.data.counts.total}}</div>
            <div class="civix-kpi-title">Total Complaints</div>
            <div class="civix-kpi-trend text-success">&uarr; 3 this month</div>
          </div>
        </div>
      </div>
      <div class="col-md-3 col-sm-6">
        <div class="civix-kpi-card kpi-resolved">
          <div class="civix-kpi-icon"><span class="glyphicon glyphicon-ok-sign"></span></div>
          <div class="civix-kpi-body">
            <div class="civix-kpi-num">{{c.data.counts.resolved}}</div>
            <div class="civix-kpi-title">Resolved</div>
            <div class="civix-kpi-trend text-success">&uarr; 2 this month</div>
          </div>
        </div>
      </div>
      <div class="col-md-3 col-sm-6">
        <div class="civix-kpi-card kpi-progress">
          <div class="civix-kpi-icon"><span class="glyphicon glyphicon-time"></span></div>
          <div class="civix-kpi-body">
            <div class="civix-kpi-num">{{c.data.counts.in_progress}}</div>
            <div class="civix-kpi-title">In Progress</div>
            <div class="civix-kpi-trend text-warning">&ndash; same as last month</div>
          </div>
        </div>
      </div>
      <div class="col-md-3 col-sm-6">
        <div class="civix-kpi-card kpi-action">
          <div class="civix-kpi-icon"><span class="glyphicon glyphicon-exclamation-sign"></span></div>
          <div class="civix-kpi-body">
            <div class="civix-kpi-num">{{c.data.counts.awaiting}}</div>
            <div class="civix-kpi-title">Awaiting Action</div>
            <div class="civix-kpi-trend text-danger">&darr; 1 from last month</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="row civix-dash-main-row">
      <!-- Left Column: Report Shortcuts & Recent Complaints -->
      <div class="col-md-8 civix-dash-left">
        <!-- Report a New Issue Category Picker -->
        <div class="civix-panel">
          <div class="civix-panel-header">
            <h3>Report a New Issue</h3>
            <p>Select a service category to report an issue in your area.</p>
          </div>
          <div class="row civix-cat-pill-row">
            <div class="col-xs-6 col-md-2-4" ng-repeat="cat in c.categories">
              <a href="?id=civix_report_issue&cat={{cat.name}}" class="civix-category-box">
                <div class="civix-cat-icon" ng-class="cat.css">
                  <span class="glyphicon" ng-class="cat.icon"></span>
                </div>
                <div class="civix-cat-name">{{cat.name}} &gt;</div>
                <div class="civix-cat-desc">{{cat.sub}}</div>
              </a>
            </div>
          </div>
        </div>

        <!-- Recent Complaints Table -->
        <div class="civix-panel">
          <div class="civix-panel-header civix-flex-between">
            <div>
              <h3>Recent Complaints</h3>
              <p>Here are your latest reported civic issues</p>
            </div>
            <a href="?id=civix_my_cases" class="civix-view-all-link">View All &rarr;</a>
          </div>

          <div ng-if="c.data.recentCases.length === 0" class="civix-empty-dash text-center">
            <p>No recent complaints found for this citizen account.</p>
            <a href="?id=civix_report_issue" class="btn btn-sm btn-primary">Report an Issue Now</a>
          </div>

          <div class="civix-complaints-list" ng-if="c.data.recentCases.length > 0">
            <div class="civix-complaint-item" ng-repeat="item in c.data.recentCases">
              <div class="civix-complaint-thumb" ng-class="'thumb-' + item.categoryClass">
                <span class="glyphicon" ng-class="item.icon"></span>
              </div>
              <div class="civix-complaint-info">
                <div class="civix-comp-id">{{item.number}}</div>
                <div class="civix-comp-title">{{item.short_description}}</div>
                <div class="civix-comp-loc">
                  <span class="glyphicon glyphicon-map-marker"></span> {{item.location}} &bull; 
                  <span class="glyphicon glyphicon-calendar"></span> {{item.date}}
                </div>
              </div>
              <div class="civix-complaint-status">
                <span class="civix-status-badge" ng-class="'status-' + item.statusClass">{{item.status}}</span>
              </div>
              <a href="?id=civix_track_case&sys_id={{item.sys_id}}" class="civix-complaint-arrow">&rsaquo;</a>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Nearby Alerts & Civic AI Assistant -->
      <div class="col-md-4 civix-dash-right">
        <!-- Nearby Alerts -->
        <div class="civix-panel">
          <div class="civix-panel-header civix-flex-between">
            <h3>Nearby Alerts</h3>
            <span class="badge badge-info">Chennai</span>
          </div>
          <div class="civix-alerts-list">
            <div class="civix-alert-item" ng-repeat="alert in c.alerts">
              <div class="civix-alert-icon" ng-class="alert.css"><span class="glyphicon" ng-class="alert.icon"></span></div>
              <div class="civix-alert-text">
                <div class="civix-alert-title">{{alert.title}}</div>
                <div class="civix-alert-dist">{{alert.dist}} &bull; {{alert.time}}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Civic AI Assistant Panel (Matches Reference) -->
        <div class="civix-panel civix-assistant-card">
          <div class="civix-assistant-head">
            <div class="civix-assistant-bot-icon">
              <span class="glyphicon glyphicon-cog"></span>
            </div>
            <strong>Civic AI Assistant</strong>
          </div>
          <div class="civix-assistant-body">
            <div class="civix-chat-bubble">
              Hi {{c.data.citizenName}}! 👋<br/>
              I'm your Civic AI Assistant. How can I help you today?
            </div>
            <div class="civix-chat-prompts">
              <a href="?id=civix_my_cases" class="civix-prompt-pill"><span class="glyphicon glyphicon-file"></span> Track my complaint</a>
              <a href="?id=civix_report_issue" class="civix-prompt-pill"><span class="glyphicon glyphicon-plus"></span> Report a new issue</a>
              <a href="?id=civix_landing#services" class="civix-prompt-pill"><span class="glyphicon glyphicon-info-sign"></span> Know service information</a>
              <a href="tel:1913" class="civix-prompt-pill"><span class="glyphicon glyphicon-earphone"></span> Call 1913 Helpline</a>
            </div>
            <div class="civix-chat-input-bar">
              <input type="text" placeholder="Type your message..." class="civix-chat-input" />
              <button class="civix-chat-send-btn" type="button"><span class="glyphicon glyphicon-send"></span></button>
            </div>
            <small class="text-muted text-center" style="display:block; margin-top: 8px;">Supports 22 scheduled Indian languages</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

    css = """
.civix-dashboard-page {
  background: #F7FAFA;
  padding: 30px 20px 80px;
}
.civix-dashboard-container {
  max-width: 1360px;
  margin: 0 auto;
}
.civix-greeting-banner {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 28px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.civix-welcome-text {
  font-size: 28px;
  font-weight: 800;
  color: #123E46;
  margin: 0 0 6px 0;
}
.civix-welcome-name { color: #087F8C; }
.civix-welcome-sub {
  color: #61777B;
  font-size: 14px;
  margin: 0;
}
.civix-weather-pill {
  background: #E1F5EA;
  border: 1px solid #B7E4C7;
  padding: 10px 18px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.civix-loc-icon { font-size: 20px; color: #087F8C; }
.civix-loc-info strong { display: block; font-size: 13px; color: #183238; }
.civix-loc-info small { color: #61777B; font-size: 11px; }

.civix-kpi-row { margin-bottom: 24px; }
.civix-kpi-card {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 14px;
  padding: 20px 18px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.civix-kpi-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}
.kpi-total .civix-kpi-icon { background: #E0F2FE; color: #0284C7; }
.kpi-resolved .civix-kpi-icon { background: #E1F5EA; color: #18794E; }
.kpi-progress .civix-kpi-icon { background: #FEF3C7; color: #D97706; }
.kpi-action .civix-kpi-icon { background: #FEE2E2; color: #DC2626; }
.civix-kpi-num { font-size: 26px; font-weight: 800; color: #183238; line-height: 1; }
.civix-kpi-title { font-size: 13px; font-weight: 600; color: #61777B; margin: 4px 0 2px; }
.civix-kpi-trend { font-size: 11px; font-weight: 600; }

.civix-panel {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 14px;
  padding: 24px;
  margin-bottom: 24px;
}
.civix-panel-header { margin-bottom: 18px; }
.civix-panel-header h3 { font-size: 18px; font-weight: 700; color: #183238; margin: 0 0 4px 0; }
.civix-panel-header p { font-size: 13px; color: #61777B; margin: 0; }
.civix-flex-between { display: flex; justify-content: space-between; align-items: center; }
.civix-view-all-link { font-size: 13px; font-weight: 700; color: #087F8C; text-decoration: none; }

.col-md-2-4 { width: 20%; float: left; padding: 0 6px; }
@media (max-width: 991px) { .col-md-2-4 { width: 50%; margin-bottom: 12px; } }
.civix-category-box {
  display: block;
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 16px 10px;
  text-align: center;
  text-decoration: none;
  transition: all 0.2s;
}
.civix-category-box:hover {
  border-color: #087F8C;
  transform: translateY(-2px);
  text-decoration: none;
}
.civix-cat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  margin: 0 auto 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}
.cat-water { background: #E0F2FE; color: #0284C7; }
.cat-elec { background: #FEF3C7; color: #D97706; }
.cat-roads { background: #F3F4F6; color: #374151; }
.cat-drain { background: #EDE9FE; color: #7C3AED; }
.cat-flood { background: #E0E7FF; color: #4F46E5; }
.civix-cat-name { font-size: 13px; font-weight: 700; color: #183238; }
.civix-cat-desc { font-size: 10px; color: #61777B; }

.civix-complaint-item {
  display: flex;
  align-items: center;
  padding: 14px;
  border: 1px solid #DCE7E8;
  border-radius: 10px;
  margin-bottom: 12px;
  gap: 14px;
}
.civix-complaint-thumb {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.thumb-water { background: #E0F2FE; color: #0284C7; }
.thumb-elec { background: #FEF3C7; color: #D97706; }
.thumb-roads { background: #F3F4F6; color: #374151; }
.thumb-drain { background: #EDE9FE; color: #7C3AED; }
.civix-complaint-info { flex-grow: 1; }
.civix-comp-id { font-size: 11px; font-weight: 700; color: #087F8C; }
.civix-comp-title { font-size: 14px; font-weight: 600; color: #183238; }
.civix-comp-loc { font-size: 11px; color: #61777B; }
.civix-status-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 12px;
}
.status-progress { background: #FEF3C7; color: #B45309; }
.status-resolved { background: #E1F5EA; color: #18794E; }
.status-awaiting { background: #FEE2E2; color: #DC2626; }
.civix-complaint-arrow { font-size: 22px; color: #A0B2B5; text-decoration: none; }

.civix-alert-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #F0F4F4;
}
.civix-alert-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}
.alert-red { background: #FEE2E2; color: #DC2626; }
.alert-yellow { background: #FEF3C7; color: #D97706; }
.alert-purple { background: #EDE9FE; color: #7C3AED; }
.alert-blue { background: #E0F2FE; color: #0284C7; }
.civix-alert-title { font-size: 13px; font-weight: 600; color: #183238; }
.civix-alert-dist { font-size: 11px; color: #61777B; }

.civix-assistant-card { border-top: 4px solid #087F8C; }
.civix-assistant-head {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  margin-bottom: 14px;
}
.civix-assistant-bot-icon {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: #087F8C;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}
.civix-chat-bubble {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 10px;
  padding: 12px 14px;
  font-size: 13px;
  line-height: 1.5;
  margin-bottom: 14px;
}
.civix-chat-prompts { display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px; }
.civix-prompt-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 600;
  color: #183238;
  text-decoration: none;
  transition: all 0.15s;
}
.civix-prompt-pill:hover { border-color: #087F8C; background: #E1F5EA; color: #087F8C; text-decoration: none; }
.civix-chat-input-bar { display: flex; gap: 6px; }
.civix-chat-input {
  flex-grow: 1;
  border: 1px solid #DCE7E8;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 12px;
  outline: none;
}
.civix-chat-send-btn {
  background: #087F8C;
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  padding: 0 12px;
  cursor: pointer;
}
"""

    client_script = """
function($scope) {
  var c = this;
  c.categories = [
    { name: 'Water Supply', css: 'cat-water', icon: 'glyphicon-tint', sub: 'Leakage, pressure' },
    { name: 'Electricity', css: 'cat-elec', icon: 'glyphicon-flash', sub: 'Streetlights, power' },
    { name: 'Roads', css: 'cat-roads', icon: 'glyphicon-road', sub: 'Potholes, surface' },
    { name: 'Drainage', css: 'cat-drain', icon: 'glyphicon-filter', sub: 'Blockage, overflow' },
    { name: 'Waterlogging', css: 'cat-flood', icon: 'glyphicon-tint', sub: 'Monsoon flooding' }
  ];
  c.alerts = [
    { title: 'Road maintenance work in T. Nagar', dist: '500 m', time: 'Today', css: 'alert-red', icon: 'glyphicon-exclamation-sign' },
    { title: 'Scheduled power maintenance - Anna Nagar', dist: '1.2 km', time: 'Tomorrow', css: 'alert-yellow', icon: 'glyphicon-flash' },
    { title: 'Possible waterlogging in Velachery', dist: '2.3 km', time: 'Today', css: 'alert-purple', icon: 'glyphicon-tint' },
    { title: 'Low water pressure reported', dist: '3.1 km', time: 'Today', css: 'alert-blue', icon: 'glyphicon-info-sign' }
  ];
}
"""

    server_script = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  data.citizenName = data.isLoggedIn ? (gs.getUser().getFirstName() || gs.getUserDisplayName()) : 'Priya Sharma';

  data.counts = { total: 0, resolved: 0, in_progress: 0, awaiting: 0 };
  data.recentCases = [];

  var userId = gs.getUserID();
  var gr = new GlideRecord('incident');
  if (data.isLoggedIn) {
    gr.addQuery('caller_id', userId);
  }
  gr.orderByDesc('sys_created_on');
  gr.setLimit(5);
  gr.query();

  while (gr.next()) {
    data.counts.total++;
    var st = gr.getValue('state');
    var stLabel = gr.getDisplayValue('state');
    var stClass = 'awaiting';
    if (st == '2') {
      data.counts.in_progress++;
      stClass = 'progress';
    } else if (st == '6' || st == '7') {
      data.counts.resolved++;
      stClass = 'resolved';
    } else {
      data.counts.awaiting++;
    }

    var cat = gr.getDisplayValue('category') || 'Water';
    var icon = 'glyphicon-tint';
    var catClass = 'water';
    if (cat.toLowerCase().indexOf('elec') >= 0) { icon = 'glyphicon-flash'; catClass = 'elec'; }
    else if (cat.toLowerCase().indexOf('road') >= 0) { icon = 'glyphicon-road'; catClass = 'roads'; }
    else if (cat.toLowerCase().indexOf('drain') >= 0) { icon = 'glyphicon-filter'; catClass = 'drain'; }

    data.recentCases.push({
      sys_id: gr.getUniqueValue(),
      number: gr.getValue('number'),
      short_description: gr.getValue('short_description'),
      location: 'Ward 12, Chennai',
      date: gr.getValue('sys_created_on').split(' ')[0],
      status: stLabel,
      statusClass: stClass,
      icon: icon,
      categoryClass: catClass
    });
  }

  // If no records in incident yet for demo citizen, provide baseline demo counts
  if (data.counts.total === 0) {
    data.counts = { total: 12, resolved: 8, in_progress: 3, awaiting: 1 };
    data.recentCases = [
      { sys_id: 'demo1', number: 'CIVIX-2026-00123', short_description: 'Water leakage on 3rd Main Road', location: 'Adyar, Chennai', date: 'Today', status: 'In Progress', statusClass: 'progress', icon: 'glyphicon-tint', categoryClass: 'water' },
      { sys_id: 'demo2', number: 'CIVIX-2026-00118', short_description: 'Street light not working near Anna Nagar Park', location: 'Anna Nagar, Chennai', date: 'Yesterday', status: 'Resolved', statusClass: 'resolved', icon: 'glyphicon-flash', categoryClass: 'elec' },
      { sys_id: 'demo3', number: 'CIVIX-2026-00110', short_description: 'Pothole near 100 Feet Road', location: 'T. Nagar, Chennai', date: '08 Oct 2026', status: 'Resolved', statusClass: 'resolved', icon: 'glyphicon-road', categoryClass: 'roads' },
      { sys_id: 'demo4', number: 'CIVIX-2026-00102', short_description: 'Drainage overflow in residential area', location: 'Velachery, Chennai', date: '05 Oct 2026', status: 'Awaiting Action', statusClass: 'awaiting', icon: 'glyphicon-filter', categoryClass: 'drain' }
    ];
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Customer Dashboard",
        "id": "civix_dashboard_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_dashboard_widget", widget_data, "Dashboard Widget")
    page_id = create_page_structure("civix_dashboard", "Customer Dashboard", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 8: MY CASES WIDGET
# ==============================================================================
def create_my_cases_widget():
    print("\n>>> Building Screen 8: My Cases Foundation Widget")
    template = """
<div class="civix-page civix-container civix-cases-page">
  <div class="civix-section-bar">
    <div>
      <h2 class="civix-section-title">My Reported Cases</h2>
      <p class="civix-section-subtitle">Track status and review municipal responses for your submitted civic issues.</p>
    </div>
    <a href="?id=civix_report_issue" class="civix-btn civix-btn-primary">
      <span class="glyphicon glyphicon-plus"></span> Report New Issue
    </a>
  </div>

  <div class="civix-cases-filter-bar">
    <div class="row">
      <div class="col-md-6 form-group">
        <input type="text" class="form-control" ng-model="c.searchQuery" placeholder="Search by case number or keyword..." />
      </div>
      <div class="col-md-3 form-group">
        <select class="form-control" ng-model="c.statusFilter">
          <option value="">All Statuses</option>
          <option value="In Progress">In Progress</option>
          <option value="Resolved">Resolved</option>
          <option value="Awaiting Action">Awaiting Action</option>
        </select>
      </div>
      <div class="col-md-3 form-group">
        <select class="form-control" ng-model="c.catFilter">
          <option value="">All Categories</option>
          <option value="Water">Water Supply</option>
          <option value="Electricity">Electricity</option>
          <option value="Roads">Roads</option>
          <option value="Drainage">Drainage</option>
        </select>
      </div>
    </div>
  </div>

  <div class="civix-cases-table-wrap">
    <table class="table civix-table">
      <thead>
        <tr>
          <th>Case Number</th>
          <th>Category</th>
          <th>Subject / Description</th>
          <th>Location</th>
          <th>Date Logged</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr ng-repeat="item in c.data.cases | filter:c.searchQuery | filter:{status: c.statusFilter, category: c.catFilter}">
          <td><strong>{{item.number}}</strong></td>
          <td><span class="label label-default">{{item.category}}</span></td>
          <td>{{item.short_description}}</td>
          <td>{{item.location}}</td>
          <td>{{item.date}}</td>
          <td><span class="civix-status-badge" ng-class="'status-' + item.statusClass">{{item.status}}</span></td>
          <td><a href="?id=civix_track_case&sys_id={{item.sys_id}}" class="btn btn-xs btn-info">Track Case &rarr;</a></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""

    css = """
.civix-cases-page { padding: 40px 20px 80px; }
.civix-cases-filter-bar {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 16px 16px 0;
  margin-bottom: 24px;
}
.civix-cases-table-wrap {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  overflow: hidden;
}
.civix-table th { background: #F7FAFA; color: #183238; border-bottom: 2px solid #DCE7E8; }
.civix-table td { vertical-align: middle !important; }
"""

    client_script = """
function($scope) {
  var c = this;
  c.searchQuery = '';
  c.statusFilter = '';
  c.catFilter = '';
}
"""

    server_script = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  data.cases = [];
  var userId = gs.getUserID();
  var gr = new GlideRecord('incident');
  if (data.isLoggedIn) {
    gr.addQuery('caller_id', userId);
  }
  gr.orderByDesc('sys_created_on');
  gr.setLimit(20);
  gr.query();

  while (gr.next()) {
    var st = gr.getValue('state');
    var stLabel = gr.getDisplayValue('state');
    var stClass = 'awaiting';
    if (st == '2') stClass = 'progress';
    else if (st == '6' || st == '7') stClass = 'resolved';

    data.cases.push({
      sys_id: gr.getUniqueValue(),
      number: gr.getValue('number'),
      short_description: gr.getValue('short_description'),
      category: gr.getDisplayValue('category') || 'Water',
      location: 'Ward 12, Chennai',
      date: gr.getValue('sys_created_on').split(' ')[0],
      status: stLabel,
      statusClass: stClass
    });
  }

  if (data.cases.length === 0) {
    data.cases = [
      { sys_id: 'c1', number: 'CIVIX-2026-00123', category: 'Water', short_description: 'Water leakage on 3rd Main Road', location: 'Adyar, Chennai', date: '10 Oct 2026', status: 'In Progress', statusClass: 'progress' },
      { sys_id: 'c2', number: 'CIVIX-2026-00118', category: 'Electricity', short_description: 'Street light not working near Anna Nagar Park', location: 'Anna Nagar, Chennai', date: '09 Oct 2026', status: 'Resolved', statusClass: 'resolved' },
      { sys_id: 'c3', number: 'CIVIX-2026-00110', category: 'Roads', short_description: 'Pothole near 100 Feet Road', location: 'T. Nagar, Chennai', date: '08 Oct 2026', status: 'Resolved', statusClass: 'resolved' },
      { sys_id: 'c4', number: 'CIVIX-2026-00102', category: 'Drainage', short_description: 'Drainage overflow in residential area', location: 'Velachery, Chennai', date: '05 Oct 2026', status: 'Awaiting Action', statusClass: 'awaiting' }
    ];
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - My Cases",
        "id": "civix_my_cases_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_my_cases_widget", widget_data, "My Cases Widget")
    page_id = create_page_structure("civix_my_cases", "My Cases", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 9: REPORT AN ISSUE WIDGET
# ==============================================================================
def create_report_issue_widget():
    print("\n>>> Building Screen 9: Report an Issue Foundation Widget")
    template = """
<div class="civix-page civix-container civix-report-page">
  <div class="civix-report-card">
    <div class="civix-report-header text-center">
      <h2 class="civix-auth-title">Report a Civic Issue</h2>
      <p class="civix-auth-subtitle">Submit details directly to your municipal ward operations department.</p>
    </div>

    <!-- Stepper indicator -->
    <div class="civix-report-stepper">
      <div class="civix-step-pill" ng-class="{'active': c.step >= 1}">1. Service & Category</div>
      <div class="civix-step-pill" ng-class="{'active': c.step >= 2}">2. Location & Ward</div>
      <div class="civix-step-pill" ng-class="{'active': c.step >= 3}">3. Review & Submit</div>
    </div>

    <!-- Success Message -->
    <div ng-if="c.successData" class="alert alert-success civix-alert text-center">
      <div style="font-size: 36px; margin-bottom: 10px;"><span class="glyphicon glyphicon-ok-circle"></span></div>
      <h3>Issue Successfully Logged!</h3>
      <p>Your case tracking number is:</p>
      <div class="civix-ticket-badge">{{c.successData.number}}</div>
      <p style="margin-top: 15px;">A ward engineer has been alerted to review and schedule field inspection.</p>
      <div style="margin-top: 20px;">
        <a href="?id=civix_track_case&sys_id={{c.successData.sys_id}}" class="btn btn-primary">Track This Case Now &rarr;</a>
        <a href="?id=civix_dashboard" class="btn btn-default">Return to Dashboard</a>
      </div>
    </div>

    <form ng-if="!c.successData" ng-submit="c.nextStep()">
      <!-- Step 1: Category & Description -->
      <div ng-if="c.step === 1" class="civix-step-box">
        <div class="form-group">
          <label>Service Category <span class="text-danger">*</span></label>
          <select class="form-control" ng-model="c.form.category" required>
            <option value="Water">Water Supply (Leakage, Interruption)</option>
            <option value="Electricity">Electricity (Streetlights, Hazards)</option>
            <option value="Roads">Roads (Potholes, Damage)</option>
            <option value="Drainage">Drainage & Waterlogging (Blockage, Overflow)</option>
          </select>
        </div>

        <div class="form-group">
          <label>Issue Title <span class="text-danger">*</span></label>
          <input type="text" class="form-control" ng-model="c.form.title" placeholder="e.g. Broken water pipe leaking near intersection" required />
        </div>

        <div class="form-group">
          <label>Detailed Description <span class="text-danger">*</span></label>
          <textarea class="form-control" rows="4" ng-model="c.form.description" placeholder="Describe the severity, duration, and any immediate hazard..." required></textarea>
        </div>

        <div class="civix-step-actions">
          <button type="button" class="btn btn-primary" ng-click="c.step = 2">Next: Location Details &rarr;</button>
        </div>
      </div>

      <!-- Step 2: Location -->
      <div ng-if="c.step === 2" class="civix-step-box">
        <div class="form-group">
          <label>Municipal Ward <span class="text-danger">*</span></label>
          <select class="form-control" ng-model="c.form.ward" required>
            <option value="Ward 12 - T. Nagar">Ward 12 - T. Nagar</option>
            <option value="Ward 8 - Anna Nagar">Ward 8 - Anna Nagar</option>
            <option value="Ward 15 - Velachery">Ward 15 - Velachery</option>
            <option value="Ward 18 - Adyar">Ward 18 - Adyar</option>
            <option value="Ward 4 - Mylapore">Ward 4 - Mylapore</option>
          </select>
        </div>

        <div class="form-group">
          <label>Street Address / Landmark <span class="text-danger">*</span></label>
          <input type="text" class="form-control" ng-model="c.form.address" placeholder="e.g. Opposite Post Office, 3rd Cross Street" required />
        </div>

        <div class="form-group">
          <label>Use Geolocation</label><br/>
          <button type="button" class="btn btn-default btn-sm" ng-click="c.getGeo()">
            <span class="glyphicon glyphicon-map-marker"></span> Detect My Current Coordinates
          </button>
          <span ng-if="c.geoCoords" class="text-success" style="margin-left: 10px;">{{c.geoCoords}}</span>
        </div>

        <div class="civix-step-actions">
          <button type="button" class="btn btn-default" ng-click="c.step = 1">&larr; Back</button>
          <button type="button" class="btn btn-primary" ng-click="c.step = 3">Next: Review & Submit &rarr;</button>
        </div>
      </div>

      <!-- Step 3: Review & Submit -->
      <div ng-if="c.step === 3" class="civix-step-box">
        <div class="civix-review-panel">
          <h4>Review Civic Issue Details</h4>
          <p><strong>Category:</strong> {{c.form.category}}</p>
          <p><strong>Issue:</strong> {{c.form.title}}</p>
          <p><strong>Description:</strong> {{c.form.description}}</p>
          <p><strong>Ward & Locality:</strong> {{c.form.ward}}, {{c.form.address}}</p>
        </div>

        <div class="civix-step-actions">
          <button type="button" class="btn btn-default" ng-click="c.step = 2">&larr; Back</button>
          <button type="button" class="btn btn-success btn-lg" ng-click="c.submitIssue()" ng-disabled="c.loading">
            <span ng-if="c.loading"><span class="glyphicon glyphicon-refresh glyphicon-spin"></span> Submitting to ServiceNow...</span>
            <span ng-if="!c.loading"><span class="glyphicon glyphicon-send"></span> Confirm & Submit Issue</span>
          </button>
        </div>
      </div>
    </form>
  </div>
</div>
"""

    css = """
.civix-report-page { padding: 40px 20px 80px; }
.civix-report-card {
  max-width: 720px;
  margin: 0 auto;
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 36px 32px;
}
.civix-report-stepper {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}
.civix-step-pill {
  flex: 1;
  text-align: center;
  padding: 8px;
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #61777B;
}
.civix-step-pill.active {
  background: #E1F5EA;
  color: #087F8C;
  border-color: #087F8C;
}
.civix-ticket-badge {
  display: inline-block;
  background: #123E46;
  color: #FFFFFF;
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 1px;
}
.civix-review-panel {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 20px;
}
.civix-step-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 24px;
}
"""

    client_script = """
function($scope, $location) {
  var c = this;
  c.step = 1;
  var paramCat = $location.search().cat || 'Water';
  c.form = {
    category: paramCat,
    ward: 'Ward 12 - T. Nagar'
  };

  c.getGeo = function() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(pos) {
        $scope.$apply(function() {
          c.geoCoords = 'Lat: ' + pos.coords.latitude.toFixed(4) + ', Long: ' + pos.coords.longitude.toFixed(4);
          c.form.geo = c.geoCoords;
        });
      });
    } else {
      c.geoCoords = 'Geolocation not supported by browser.';
    }
  };

  c.submitIssue = function() {
    c.loading = true;
    c.server.get({ action: 'submit_issue', form: c.form }).then(function(r) {
      c.loading = false;
      if (r.data.status === 'success') {
        c.successData = r.data.ticket;
      }
    });
  };
}
"""

    server_script = """
(function() {
  if (input && input.action === 'submit_issue') {
    var f = input.form;
    var gr = new GlideRecord('incident');
    gr.initialize();
    gr.setValue('short_description', f.title);
    gr.setValue('description', f.description + '\n\nWard: ' + f.ward + '\nAddress: ' + f.address + (f.geo ? ('\nGeo: ' + f.geo) : ''));
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

    widget_data = {
        "name": "CIVIX AI - Report an Issue",
        "id": "civix_report_issue_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_report_issue_widget", widget_data, "Report Issue Widget")
    page_id = create_page_structure("civix_report_issue", "Report an Issue", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 10: CASE TRACKING WIDGET
# ==============================================================================
def create_track_case_widget():
    print("\n>>> Building Screen 10: Case Tracking Foundation Widget")
    template = """
<div class="civix-page civix-container civix-track-page">
  <div class="civix-track-card">
    <div class="civix-section-bar">
      <div>
        <h2 class="civix-section-title">Case Status & Timeline</h2>
        <p class="civix-section-subtitle">Real-time municipal resolution progress for this reported civic complaint.</p>
      </div>
      <a href="?id=civix_my_cases" class="btn btn-default">&larr; Back to My Cases</a>
    </div>

    <!-- Case Lookup Header -->
    <div class="civix-case-detail-header">
      <div class="civix-case-main-info">
        <span class="civix-badge-pill"><span class="glyphicon glyphicon-tag"></span> {{c.data.case.category}}</span>
        <h3>{{c.data.case.number}} &bull; {{c.data.case.short_description}}</h3>
        <p class="text-muted"><span class="glyphicon glyphicon-map-marker"></span> {{c.data.case.location}} &bull; Logged on: {{c.data.case.opened_at}}</p>
      </div>
      <div class="civix-case-curr-status">
        <span class="civix-status-badge status-progress" style="font-size: 14px; padding: 6px 14px;">{{c.data.case.state}}</span>
      </div>
    </div>

    <!-- Approved Lifecycle Timeline -->
    <div class="civix-timeline-card">
      <h4 class="civix-form-section-title">Approved Resolution Lifecycle</h4>
      <div class="civix-lifecycle-bar">
        <div class="civix-lifecycle-step" ng-repeat="st in c.steps" ng-class="{'completed': st.num <= c.data.case.stepNum, 'active': st.num === c.data.case.stepNum}">
          <div class="civix-step-circle">{{st.num}}</div>
          <div class="civix-step-label">{{st.label}}</div>
        </div>
      </div>
    </div>

    <!-- Case Details Details -->
    <div class="civix-case-meta-box">
      <h4>Description Logged</h4>
      <p>{{c.data.case.description}}</p>
      <hr/>
      <h4>Public Resolution Information</h4>
      <p class="text-info">{{c.data.case.resolution_notes}}</p>
    </div>
  </div>
</div>
"""

    css = """
.civix-track-page { padding: 40px 20px 80px; }
.civix-track-card {
  max-width: 900px;
  margin: 0 auto;
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 32px;
}
.civix-case-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 20px;
  border-bottom: 1px solid #DCE7E8;
  margin-bottom: 24px;
}
.civix-case-main-info h3 { margin: 8px 0; font-size: 20px; font-weight: 700; color: #183238; }
.civix-timeline-card {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}
.civix-lifecycle-bar {
  display: flex;
  justify-content: space-between;
  position: relative;
  margin-top: 20px;
}
.civix-lifecycle-step {
  text-align: center;
  position: relative;
  flex: 1;
}
.civix-step-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #DCE7E8;
  color: #61777B;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  margin: 0 auto 8px;
}
.civix-lifecycle-step.completed .civix-step-circle {
  background: #087F8C;
  color: #FFFFFF;
}
.civix-lifecycle-step.active .civix-step-circle {
  background: #18794E;
  color: #FFFFFF;
  box-shadow: 0 0 0 4px #E1F5EA;
}
.civix-step-label { font-size: 11px; font-weight: 600; color: #183238; }
.civix-case-meta-box {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 20px;
}
"""

    client_script = """
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

    server_script = """
(function() {
  var sysId = $sp.getParameter('sys_id');
  data.case = {
    number: 'CIVIX-2026-00123',
    short_description: 'Water leakage on 3rd Main Road',
    category: 'Water Supply',
    location: 'Adyar, Ward 18, Chennai',
    opened_at: '10 Oct 2026 10:24 AM',
    state: 'In Progress',
    stepNum: 4,
    description: 'Severe potable pipeline leak causing water accumulation near pedestrian crossway.',
    resolution_notes: 'Ward engineer and pipeline repair crew dispatched. Repair parts staged on site.'
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
        category: gr.getDisplayValue('category') || 'Civic Issue',
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

    widget_data = {
        "name": "CIVIX AI - Case Tracking",
        "id": "civix_track_case_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_track_case_widget", widget_data, "Case Tracking Widget")
    page_id = create_page_structure("civix_track_case", "Case Tracking", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 11: CITIZEN PROFILE & SETTINGS WIDGET
# ==============================================================================
def create_profile_widget():
    print("\n>>> Building Screen 11: Citizen Profile and Settings Foundation Widget")
    template = """
<div class="civix-page civix-container civix-profile-page">
  <div class="civix-profile-card">
    <div class="civix-section-bar">
      <div>
        <h2 class="civix-section-title">Citizen Profile & Settings</h2>
        <p class="civix-section-subtitle">Manage your contact details, locality, and preferred interface language.</p>
      </div>
      <a href="/logout.do" class="btn btn-danger btn-sm"><span class="glyphicon glyphicon-log-out"></span> Sign Out</a>
    </div>

    <div class="row">
      <div class="col-md-4 text-center">
        <div class="civix-avatar-large">{{c.data.userInitials}}</div>
        <h3>{{c.data.userName}}</h3>
        <span class="label label-success">Verified Citizen</span>
      </div>
      <div class="col-md-8">
        <div class="civix-profile-details">
          <div class="form-group">
            <label>Registered Email</label>
            <input type="text" class="form-control" value="{{c.data.userEmail}}" readonly />
          </div>
          <div class="form-group">
            <label>Registered Mobile</label>
            <input type="text" class="form-control" value="{{c.data.mobile}}" readonly />
          </div>
          <div class="form-group">
            <label>City & Locality</label>
            <input type="text" class="form-control" value="{{c.data.city}}" readonly />
          </div>
          <div class="form-group">
            <label>Assigned Role</label>
            <input type="text" class="form-control" value="x_civic_ai_citizen (CIVIX AI Citizen Access)" readonly />
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

    css = """
.civix-profile-page { padding: 40px 20px 80px; }
.civix-profile-card {
  max-width: 800px;
  margin: 0 auto;
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 32px;
}
.civix-avatar-large {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: #087F8C;
  color: #FFFFFF;
  font-size: 32px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px auto 14px;
}
"""

    client_script = "function() {}"

    server_script = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  if (data.isLoggedIn) {
    var u = gs.getUser();
    data.userName = u.getDisplayName();
    data.userEmail = u.getEmail();
    data.mobile = u.getRecord().getValue('mobile_phone') || '+91 9876543210';
    data.city = u.getRecord().getValue('city') || 'Chennai, Tamil Nadu';
    var names = data.userName.split(' ');
    data.userInitials = names.length > 1 ? (names[0][0] + names[names.length-1][0]).toUpperCase() : data.userName.substring(0, 2).toUpperCase();
  } else {
    data.userName = 'Priya Sharma';
    data.userEmail = 'priya.sharma@example.com';
    data.mobile = '+91 9876543210';
    data.city = 'Chennai, Tamil Nadu';
    data.userInitials = 'PS';
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Profile and Settings",
        "id": "civix_profile_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_profile_widget", widget_data, "Profile Widget")
    page_id = create_page_structure("civix_profile", "Profile and Settings", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# CONFIGURE MAIN PORTAL (sp_portal)
# ==============================================================================
def configure_portal(landing_page_sys_id: str):
    print("\n>>> Configuring Main Service Portal Record (/civix)")
    portal_data = {
        "title": "CIVIX AI - Citizen Portal",
        "url_suffix": "civix",
        "homepage": landing_page_sys_id,
        "theme": THEME_SYS_ID,
        "header": HEADER_WIDGET_SYS_ID,
        "footer": FOOTER_WIDGET_SYS_ID,
        "default": "false",
        "css_variables": "$navbar-height: 0px !important;\n$grid-gutter-width: 0px !default;"
    }
    portal_id = upsert("sp_portal", "url_suffix=civix", portal_data, "CIVIX AI Portal")
    return portal_id


if __name__ == "__main__":
    print("=== DEPLOYING ALL CIVIX AI PHASE 1 SCREENS & WIDGETS ===")
    p1, w1 = create_landing_widget()
    p2, w2 = create_portal_select_widget()
    p3, w3 = create_home_widget()
    p4, w4 = create_register_widget()
    p5, w5 = create_login_widget()
    p6, w6 = create_recovery_widget()
    p7, w7 = create_dashboard_widget()
    p8, w8 = create_my_cases_widget()
    p9, w9 = create_report_issue_widget()
    p10, w10 = create_track_case_widget()
    p11, w11 = create_profile_widget()

    portal_sys_id = configure_portal(p1)
    print(f"\n=======================================================")
    print(f"CIVIX AI Portal successfully deployed with url_suffix: civix")
    print(f"Landing page ID: {p1}")
    print(f"Portal Sys ID: {portal_sys_id}")
    print(f"URL: {INSTANCE_URL}/civix")
    print(f"=======================================================")
