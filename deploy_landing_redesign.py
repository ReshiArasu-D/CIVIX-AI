"""
CIVIX AI - Premium Public Landing Page Redesign (civix_landing)
Deploys a modern, full-width, responsive civic portal landing page with:
- Glassmorphic top navigation bar
- Cinematic hero section with city skyline overlay & live GCC command widget
- 5 Vibrant Service Category Cards with direct links
- 3-Step Municipal Resolution Workflow
- Impact Metrics Bar & Emergency Helplines
- Public civic footer & floating CIVIX Assist
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

res = api_get("sp_widget", query="id=civix_landing_widget", limit=1)
if not res:
    print("civix_landing_widget not found!")
    exit(1)

widget = res[0]
sys_id = widget["sys_id"]

LANDING_TEMPLATE = """
<div class="civix-public-root">
  
  <!-- 1. STICKY TOP NAVIGATION BAR -->
  <header class="civix-land-nav-bar">
    <div class="civix-land-nav-inner">
      <a href="?id=civix_landing" class="civix-land-brand">
        <div class="civix-land-logo-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M3 21h18M5 21V7l8-4v18M13 21V3l6 4v14"/></svg>
        </div>
        <div class="civix-land-brand-text">
          <span class="civix-brand-main">CIVIX AI</span>
          <span class="civix-brand-tagline">Greater Chennai Corporation</span>
        </div>
      </a>

      <nav class="civix-land-menu-links">
        <a href="#services" class="civix-land-nav-item">Municipal Services</a>
        <a href="#workflow" class="civix-land-nav-item">How It Works</a>
        <a href="#metrics" class="civix-land-nav-item">Live Operations</a>
        <a href="#contacts" class="civix-land-nav-item">Emergency Desks</a>
      </nav>

      <div class="civix-land-nav-ctas">
        <a href="?id=civix_portal_select" class="btn btn-default civix-btn-portal-select">Portal Selection</a>
        <a href="?id=civix_home" class="btn btn-default civix-btn-citizen-login">Citizen Login</a>
        <a href="?id=civix_report_issue" class="btn btn-primary civix-btn-report-cta">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          <span>Report an Issue</span>
        </a>
      </div>
    </div>
  </header>

  <!-- 2. HERO SECTION WITH SKYLINE & COMMAND CARD -->
  <section class="civix-land-hero-section">
    <div class="civix-hero-overlay-city"></div>
    <div class="civix-land-hero-container">
      
      <!-- Left Hero Column -->
      <div class="civix-hero-copy-col">
        <div class="civix-hero-badge-pill">
          <span class="pulse-indicator-dot"></span>
          <span>ServiceNow Agentic Intelligence &bull; Urban Public Services</span>
        </div>

        <h1 class="civix-hero-heading">
          Smarter Cities.<br/>
          <span class="civix-text-gradient">Faster Civic Services.</span>
        </h1>

        <p class="civix-hero-lead">
          Empowering citizens across Greater Chennai to report water, road, electricity, and drainage defects in 60 seconds. Track real-time repair progress verified by municipal engineers.
        </p>

        <div class="civix-hero-actions-row">
          <a href="?id=civix_report_issue" class="btn btn-primary btn-lg civix-hero-primary-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            <span>Report a Civic Issue Now</span>
          </a>
          <a href="?id=civix_track_case&sys_id=c1" class="btn btn-default btn-lg civix-hero-secondary-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <span>Track Existing Complaint</span>
          </a>
        </div>

        <div class="civix-hero-trust-bar">
          <div class="trust-pill"><span>✓</span> 24/7 Digital Intake</div>
          <div class="trust-pill"><span>✓</span> Real-Time Ward Tracking</div>
          <div class="trust-pill"><span>✓</span> 22 Scheduled Indian Languages</div>
        </div>
      </div>

      <!-- Right Hero Live Command Card -->
      <div class="civix-hero-card-col">
        <div class="civix-hero-live-card">
          <div class="civix-live-card-header">
            <div class="civix-live-status-pill">
              <span class="green-live-dot"></span>
              <strong>Live Municipal Operations</strong>
            </div>
            <span class="civix-live-zone-tag">15 Wards Connected</span>
          </div>

          <div class="civix-live-metrics-3col">
            <div class="civix-card-kpi">
              <span class="card-kpi-val">14,820+</span>
              <span class="card-kpi-lbl">Issues Resolved</span>
            </div>
            <div class="civix-card-kpi">
              <span class="card-kpi-val">&lt; 48h</span>
              <span class="card-kpi-lbl">Avg Resolution</span>
            </div>
            <div class="civix-card-kpi">
              <span class="card-kpi-val">99.4%</span>
              <span class="card-kpi-lbl">Citizen Trust</span>
            </div>
          </div>

          <!-- Live Feed Ticker -->
          <div class="civix-live-feed-box">
            <div class="civix-feed-item">
              <span class="feed-badge in-progress">In Progress</span>
              <div class="feed-details">
                <strong>CIVIX-2024-00123 &bull; Water Leakage</strong>
                <small>Adyar Ward 18 &bull; Field crew excavating pipe</small>
              </div>
            </div>
            <div class="civix-feed-item">
              <span class="feed-badge resolved">Resolved</span>
              <div class="feed-details">
                <strong>CIVIX-2024-00118 &bull; Streetlight Repaired</strong>
                <small>Anna Nagar Ward 8 &bull; Fixture replaced</small>
              </div>
            </div>
            <div class="civix-feed-item">
              <span class="feed-badge resolved">Resolved</span>
              <div class="feed-details">
                <strong>CIVIX-2024-00110 &bull; Pothole Restored</strong>
                <small>T. Nagar 100 Ft Rd &bull; Bitumen repaved</small>
              </div>
            </div>
          </div>

          <a href="?id=civix_home" class="btn btn-default civix-btn-card-access">
            <span>Access Citizen Dashboard</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </a>
        </div>
      </div>

    </div>
  </section>

  <!-- 3. CORE MUNICIPAL SERVICES SECTION -->
  <section class="civix-land-services-section" id="services">
    <div class="civix-land-content-wrap">
      <div class="civix-section-heading-center">
        <span class="civix-sub-badge">Municipal Services</span>
        <h2 class="civix-section-main-title">Direct Service Intake Portals</h2>
        <p class="civix-section-main-desc">Select a category below to submit geo-tagged complaints directly to the responsible municipal engineering division.</p>
      </div>

      <div class="civix-services-cards-grid">
        <!-- 1. Water Supply -->
        <a href="?id=civix_report_issue&cat=Water" class="civix-service-card">
          <div class="civix-card-icon-bubble cat-water">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2.2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
          </div>
          <h3 class="civix-card-name">Water Supply</h3>
          <p class="civix-card-desc">Pipe bursts, low water pressure, contaminated supply, valve leakage, and water tanker requests.</p>
          <div class="civix-card-action-link">
            <span>Report Water Issue</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </div>
        </a>

        <!-- 2. Electricity -->
        <a href="?id=civix_report_issue&cat=Electricity" class="civix-service-card">
          <div class="civix-card-icon-bubble cat-elec">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          </div>
          <h3 class="civix-card-name">Electricity & Lights</h3>
          <p class="civix-card-desc">Non-functional streetlights, dangling live wires, damaged electrical poles, and park illumination.</p>
          <div class="civix-card-action-link">
            <span>Report Electrical Issue</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </div>
        </a>

        <!-- 3. Roads & Potholes -->
        <a href="?id=civix_report_issue&cat=Roads" class="civix-service-card">
          <div class="civix-card-icon-bubble cat-roads">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2.2"><path d="M4 19L8 5M16 5l4 14M12 8v3M12 15v3"/></svg>
          </div>
          <h3 class="civix-card-name">Roads & Potholes</h3>
          <p class="civix-card-desc">Asphalt potholes, crater hazards, broken pedestrian sidewalks, and illegal road cuts.</p>
          <div class="civix-card-action-link">
            <span>Report Road Defect</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </div>
        </a>

        <!-- 4. Drainage & Sewage -->
        <a href="?id=civix_report_issue&cat=Drainage" class="civix-service-card">
          <div class="civix-card-icon-bubble cat-drain">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg>
          </div>
          <h3 class="civix-card-name">Drainage & Overflow</h3>
          <p class="civix-card-desc">Stormwater drain blockages, open manholes, sewage overflow, and urgent desilting requirements.</p>
          <div class="civix-card-action-link">
            <span>Report Drainage Issue</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </div>
        </a>

        <!-- 5. Waterlogging & Floods -->
        <a href="?id=civix_report_issue&cat=Waterlogging" class="civix-service-card">
          <div class="civix-card-icon-bubble cat-flood">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#9333EA" stroke-width="2.2"><path d="M2 12c2.5-3 5.5-3 8 0s5.5 3 8 0M2 18c2.5-3 5.5-3 8 0s5.5 3 8 0"/></svg>
          </div>
          <h3 class="civix-card-name">Waterlogging & Floods</h3>
          <p class="civix-card-desc">Rainwater stagnation, flooded intersections, submerged subways, and emergency water extraction.</p>
          <div class="civix-card-action-link">
            <span>Report Waterlogging</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </div>
        </a>
      </div>
    </div>
  </section>

  <!-- 4. HOW IT WORKS WORKFLOW SECTION -->
  <section class="civix-land-workflow-section" id="workflow">
    <div class="civix-land-content-wrap">
      <div class="civix-section-heading-center">
        <span class="civix-sub-badge" style="background:#EFF6FF; color:#0066FF;">Transparent Lifecycle</span>
        <h2 class="civix-section-main-title">How CIVIX AI Resolves Issues</h2>
        <p class="civix-section-main-desc">From initial citizen submission to verified on-site field engineering closure.</p>
      </div>

      <div class="civix-workflow-3steps-grid">
        <div class="civix-step-card">
          <div class="civix-step-number-tag">01</div>
          <div class="civix-step-icon-wrap">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2.2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
          </div>
          <h3 class="civix-step-title">1. Report & Attach Proof</h3>
          <p class="civix-step-desc">Select your issue category, detect GPS coordinates, and attach clear photo proof in under 60 seconds.</p>
        </div>

        <div class="civix-step-card">
          <div class="civix-step-number-tag">02</div>
          <div class="civix-step-icon-wrap" style="background:#FEF3C7; color:#D97706;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          </div>
          <h3 class="civix-step-title">2. AI Triage & Crew Dispatch</h3>
          <p class="civix-step-desc">ServiceNow Agentic AI categorizes urgency and dispatches the nearest Ward Rapid Response Unit with parts.</p>
        </div>

        <div class="civix-step-card">
          <div class="civix-step-number-tag">03</div>
          <div class="civix-step-icon-wrap" style="background:#DCFCE7; color:#16A34A;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          </div>
          <h3 class="civix-step-title">3. Verified Milestone Closure</h3>
          <p class="civix-step-desc">Follow live 6-stage repair milestones. Inspect final engineer resolution photos before case closure.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 5. COMMUNITY OPERATIONS & IMPACT METRICS -->
  <section class="civix-land-metrics-section" id="metrics">
    <div class="civix-land-content-wrap">
      <div class="civix-metrics-strip-card">
        <div class="civix-stat-block">
          <span class="stat-number">15</span>
          <span class="stat-label">Municipal Zones</span>
        </div>
        <div class="civix-stat-divider"></div>
        <div class="civix-stat-block">
          <span class="stat-number">200</span>
          <span class="stat-label">Wards Connected</span>
        </div>
        <div class="civix-stat-divider"></div>
        <div class="civix-stat-block">
          <span class="stat-number">2,450+</span>
          <span class="stat-label">Field Technicians</span>
        </div>
        <div class="civix-stat-divider"></div>
        <div class="civix-stat-block">
          <span class="stat-number">100%</span>
          <span class="stat-label">Open Public Audit</span>
        </div>
      </div>
    </div>
  </section>

  <!-- 6. EMERGENCY HELPLINES BANNER -->
  <section class="civix-land-emergency-section" id="contacts">
    <div class="civix-land-content-wrap">
      <div class="civix-emergency-banner-box">
        <div class="civix-em-left">
          <div class="civix-em-badge">24/7 Rapid Helplines</div>
          <h3 class="civix-em-title">Immediate Municipal Assistance</h3>
          <p class="civix-em-sub">For life-threatening road hazards, severe flooding, or electrical fires, contact our emergency desks directly.</p>
        </div>
        <div class="civix-em-hotlines-row">
          <div class="civix-em-hotline-card">
            <span class="em-name">Corporation Control Room</span>
            <strong class="em-phone">1913</strong>
          </div>
          <div class="civix-em-hotline-card">
            <span class="em-name">Ward Rapid Desk (Toll-Free)</span>
            <strong class="em-phone">1800-425-0018</strong>
          </div>
          <div class="civix-em-hotline-card">
            <span class="em-name">Power Emergency (TANGEDCO)</span>
            <strong class="em-phone">1912</strong>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 7. MODERN PUBLIC CIVIC FOOTER -->
  <footer class="civix-land-footer">
    <div class="civix-land-content-wrap">
      <div class="civix-footer-top-row">
        <div class="civix-footer-brand-side">
          <div class="civix-land-logo-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M3 21h18M5 21V7l8-4v18M13 21V3l6 4v14"/></svg>
          </div>
          <span style="font-size:20px; font-weight:800; color:#FFFFFF; margin-left:10px;">CIVIX AI</span>
          <p style="font-size:13px; color:#94A3B8; margin-top:10px; max-width:380px;">
            Digital urban services transformation platform built for Greater Chennai Corporation. Transparent, accountable, and responsive citizen governance.
          </p>
        </div>

        <div class="civix-footer-nav-col">
          <strong>Citizen Portals</strong>
          <a href="?id=civix_home">Dashboard</a>
          <a href="?id=civix_report_issue">Report an Issue</a>
          <a href="?id=civix_my_cases">Track Complaints</a>
          <a href="?id=civix_profile">Citizen Profile</a>
        </div>

        <div class="civix-footer-nav-col">
          <strong>Corporation Info</strong>
          <a href="#services">Municipal Services</a>
          <a href="#workflow">Resolution Workflow</a>
          <a href="#contacts">Emergency Desks</a>
          <a href="?id=civix_portal_select">Officer Operations Portal</a>
        </div>
      </div>

      <div class="civix-footer-bottom-bar">
        <span>© 2026 Greater Chennai Corporation &bull; CIVIX AI Platform. All rights reserved.</span>
        <div class="civix-footer-sub-links">
          <span>Clean Cities &bull; Green Communities &bull; Better Tomorrows</span>
        </div>
      </div>
    </div>
  </footer>

</div>
"""

LANDING_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

* {
  box-sizing: border-box !important;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  background-color: #0B192C !important;
  overflow-x: hidden !important;
}

.sp-page-root, #page_root, .page, .container, .container-fluid, .row, .col-xs-12, .col-sm-12, .col-md-12 {
  padding: 0 !important;
  margin: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
}

header.sp-header, nav.navbar-inverse, .navbar, footer.civix-footer {
  display: none !important;
}

.civix-public-root {
  width: 100%;
  background: #0B192C;
  color: #0F172A;
  overflow-x: hidden;
}

/* 1. TOP NAVBAR */
.civix-land-nav-bar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(11, 25, 44, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 14px 0;
}
.civix-land-nav-inner {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.civix-land-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none !important;
}
.civix-land-logo-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, #0066FF, #0284C7);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(0, 102, 255, 0.4);
}
.civix-land-brand-text {
  display: flex;
  flex-direction: column;
}
.civix-brand-main {
  font-size: 19px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: -0.2px;
}
.civix-brand-tagline {
  font-size: 10.5px;
  color: #94A3B8;
  font-weight: 600;
}

.civix-land-menu-links {
  display: flex;
  align-items: center;
  gap: 28px;
}
@media (max-width: 960px) {
  .civix-land-menu-links { display: none; }
}
.civix-land-nav-item {
  color: #E2E8F0 !important;
  font-size: 13.5px;
  font-weight: 600;
  text-decoration: none !important;
  transition: color 0.15s;
}
.civix-land-nav-item:hover {
  color: #38BDF8 !important;
}

.civix-land-nav-ctas {
  display: flex;
  align-items: center;
  gap: 12px;
}
.civix-btn-portal-select {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #E2E8F0 !important;
  font-weight: 600;
  font-size: 12.5px;
  border-radius: 8px;
  padding: 8px 14px;
}
.civix-btn-citizen-login {
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #FFFFFF !important;
  font-weight: 700;
  font-size: 13px;
  border-radius: 8px;
  padding: 8px 16px;
  transition: all 0.2s;
}
.civix-btn-citizen-login:hover {
  background: rgba(255, 255, 255, 0.22);
}
.civix-btn-report-cta {
  background: #0066FF;
  border-color: #0066FF;
  color: #FFFFFF !important;
  font-weight: 700;
  font-size: 13px;
  border-radius: 8px;
  padding: 8px 18px;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 4px 14px rgba(0, 102, 255, 0.35);
  transition: all 0.2s;
}
.civix-btn-report-cta:hover {
  background: #0052CC;
  transform: translateY(-1px);
}

/* 2. HERO SECTION */
.civix-land-hero-section {
  position: relative;
  background: linear-gradient(135deg, #0B192C 0%, #0F284E 50%, #1E3A8A 100%);
  color: #FFFFFF;
  padding: 80px 0 100px;
  overflow: hidden;
}
.civix-hero-overlay-city {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1600&auto=format&fit=crop&q=80') center center/cover no-repeat;
  opacity: 0.16;
  pointer-events: none;
}
.civix-land-hero-container {
  position: relative;
  z-index: 2;
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: minmax(0, 1.3fr) minmax(0, 1fr);
  gap: 50px;
  align-items: center;
}
@media (max-width: 960px) {
  .civix-land-hero-container { grid-template-columns: 1fr; }
}

.civix-hero-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.22);
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 700;
  color: #38BDF8;
  margin-bottom: 20px;
  backdrop-filter: blur(6px);
}
.pulse-indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #38BDF8;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.4);
}

.civix-hero-heading {
  font-size: 48px;
  font-weight: 800;
  line-height: 1.15;
  color: #FFFFFF;
  margin: 0 0 18px 0;
  letter-spacing: -0.8px;
}
@media (max-width: 768px) {
  .civix-hero-heading { font-size: 36px; }
}
.civix-text-gradient {
  background: linear-gradient(135deg, #38BDF8 0%, #60A5FA 50%, #93C5FD 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.civix-hero-lead {
  font-size: 16.5px;
  line-height: 1.6;
  color: #CBD5E1;
  margin: 0 0 32px 0;
  max-width: 600px;
}

.civix-hero-actions-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}
.civix-hero-primary-btn {
  background: #0066FF;
  border-color: #0066FF;
  color: #FFFFFF !important;
  font-weight: 800;
  font-size: 15px;
  border-radius: 12px;
  padding: 14px 28px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 6px 20px rgba(0, 102, 255, 0.4);
  transition: all 0.25s;
}
.civix-hero-primary-btn:hover {
  background: #0052CC;
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(0, 102, 255, 0.5);
}
.civix-hero-secondary-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #FFFFFF !important;
  font-weight: 700;
  font-size: 15px;
  border-radius: 12px;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  backdrop-filter: blur(8px);
  transition: all 0.2s;
}
.civix-hero-secondary-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #FFFFFF;
}

.civix-hero-trust-bar {
  display: flex;
  gap: 20px;
  align-items: center;
  flex-wrap: wrap;
}
.trust-pill {
  font-size: 12.5px;
  color: #94A3B8;
  font-weight: 600;
}
.trust-pill span {
  color: #10B981;
  font-weight: 800;
  margin-right: 4px;
}

/* LIVE COMMAND CARD */
.civix-hero-live-card {
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(14px);
}
.civix-live-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.civix-live-status-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13.5px;
  color: #FFFFFF;
}
.green-live-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #10B981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.35);
}
.civix-live-zone-tag {
  background: rgba(56, 189, 248, 0.15);
  color: #38BDF8;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.civix-live-metrics-3col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
.civix-card-kpi {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 12px 10px;
  text-align: center;
}
.card-kpi-val {
  font-size: 20px;
  font-weight: 800;
  color: #38BDF8;
  display: block;
}
.card-kpi-lbl {
  font-size: 10.5px;
  color: #94A3B8;
  font-weight: 600;
  margin-top: 2px;
  display: block;
}

.civix-live-feed-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}
.civix-feed-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  padding: 10px 12px;
}
.feed-badge {
  font-size: 10px;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 4px;
  text-transform: uppercase;
  flex-shrink: 0;
}
.feed-badge.in-progress { background: rgba(245, 158, 11, 0.2); color: #FBBF24; }
.feed-badge.resolved { background: rgba(16, 185, 129, 0.2); color: #34D399; }
.feed-details strong {
  font-size: 12px;
  color: #F8FAFC;
  display: block;
}
.feed-details small {
  font-size: 11px;
  color: #94A3B8;
}

.civix-btn-card-access {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #FFFFFF !important;
  font-weight: 700;
  font-size: 13.5px;
  border-radius: 10px;
  padding: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  text-decoration: none !important;
}
.civix-btn-card-access:hover {
  background: #0066FF;
  border-color: #0066FF;
}

/* 3. CORE SERVICES SECTION */
.civix-land-services-section {
  background: #F8FAFC;
  padding: 90px 0;
}
.civix-land-content-wrap {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 24px;
}
.civix-section-heading-center {
  text-align: center;
  max-width: 680px;
  margin: 0 auto 54px;
}
.civix-sub-badge {
  display: inline-block;
  background: #EFF6FF;
  color: #0066FF;
  font-size: 11.5px;
  font-weight: 800;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  padding: 5px 12px;
  border-radius: 9999px;
  margin-bottom: 12px;
}
.civix-section-main-title {
  font-size: 34px;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 12px 0;
  letter-spacing: -0.5px;
}
.civix-section-main-desc {
  font-size: 15px;
  color: #64748B;
  margin: 0;
  line-height: 1.6;
}

.civix-services-cards-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 18px;
}
@media (max-width: 1100px) {
  .civix-services-cards-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 700px) {
  .civix-services-cards-grid { grid-template-columns: 1fr; }
}

.civix-service-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 18px;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  text-decoration: none !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.civix-service-card:hover {
  transform: translateY(-5px);
  border-color: #0066FF;
  box-shadow: 0 14px 30px rgba(0, 102, 255, 0.12);
}
.civix-card-icon-bubble {
  width: 54px;
  height: 54px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}
.cat-water { background: #E0F2FE; }
.cat-elec { background: #FEF3C7; }
.cat-roads { background: #F1F5F9; }
.cat-drain { background: #DCFCE7; }
.cat-flood { background: #F3E8FF; }

.civix-card-name {
  font-size: 17px;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 8px 0;
}
.civix-card-desc {
  font-size: 13px;
  color: #64748B;
  line-height: 1.5;
  margin: 0 0 20px 0;
  flex-grow: 1;
}
.civix-card-action-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: #0066FF;
}

/* 4. HOW IT WORKS WORKFLOW */
.civix-land-workflow-section {
  background: #FFFFFF;
  padding: 90px 0;
  border-top: 1px solid #E2E8F0;
}
.civix-workflow-3steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}
@media (max-width: 860px) {
  .civix-workflow-3steps-grid { grid-template-columns: 1fr; }
}

.civix-step-card {
  position: relative;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 18px;
  padding: 32px 28px;
}
.civix-step-number-tag {
  position: absolute;
  top: 24px;
  right: 24px;
  font-size: 26px;
  font-weight: 900;
  color: #CBD5E1;
}
.civix-step-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: #EFF6FF;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}
.civix-step-title {
  font-size: 18px;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 10px 0;
}
.civix-step-desc {
  font-size: 14px;
  color: #64748B;
  line-height: 1.55;
  margin: 0;
}

/* 5. METRICS STRIP */
.civix-land-metrics-section {
  background: #F8FAFC;
  padding: 40px 0;
}
.civix-metrics-strip-card {
  background: #0B192C;
  border-radius: 20px;
  padding: 36px 40px;
  display: flex;
  align-items: center;
  justify-content: space-around;
  color: #FFFFFF;
  box-shadow: 0 10px 30px rgba(11, 25, 44, 0.2);
  flex-wrap: wrap;
  gap: 20px;
}
.civix-stat-block {
  text-align: center;
}
.stat-number {
  font-size: 34px;
  font-weight: 900;
  color: #38BDF8;
  display: block;
}
.stat-label {
  font-size: 13px;
  font-weight: 600;
  color: #CBD5E1;
  margin-top: 4px;
  display: block;
}
.civix-stat-divider {
  width: 1px;
  height: 48px;
  background: rgba(255, 255, 255, 0.15);
}
@media (max-width: 768px) {
  .civix-stat-divider { display: none; }
}

/* 6. EMERGENCY BANNER */
.civix-land-emergency-section {
  background: #F8FAFC;
  padding: 40px 0 90px;
}
.civix-emergency-banner-box {
  background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
  border-radius: 20px;
  padding: 36px 40px;
  color: #FFFFFF;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
  flex-wrap: wrap;
}
.civix-em-left {
  max-width: 500px;
}
.civix-em-badge {
  display: inline-block;
  background: #EF4444;
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 6px;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.civix-em-title {
  font-size: 24px;
  font-weight: 800;
  color: #FFFFFF;
  margin: 0 0 8px 0;
}
.civix-em-sub {
  font-size: 13.5px;
  color: #CBD5E1;
  line-height: 1.5;
  margin: 0;
}
.civix-em-hotlines-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.civix-em-hotline-card {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 14px 20px;
  text-align: center;
}
.em-name {
  font-size: 11.5px;
  color: #94A3B8;
  display: block;
  font-weight: 600;
}
.em-phone {
  font-size: 20px;
  font-weight: 900;
  color: #F87171;
  display: block;
  margin-top: 4px;
}

/* 7. FOOTER */
.civix-land-footer {
  background: #070F1E;
  color: #94A3B8;
  padding: 60px 0 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.civix-footer-top-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 40px;
  margin-bottom: 50px;
}
@media (max-width: 768px) {
  .civix-footer-top-row { grid-template-columns: 1fr; }
}
.civix-footer-brand-side {
  display: flex;
  flex-direction: column;
}
.civix-footer-nav-col {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.civix-footer-nav-col strong {
  color: #FFFFFF;
  font-size: 14px;
  margin-bottom: 6px;
}
.civix-footer-nav-col a {
  color: #94A3B8 !important;
  font-size: 13px;
  text-decoration: none !important;
  transition: color 0.15s;
}
.civix-footer-nav-col a:hover {
  color: #38BDF8 !important;
}
.civix-footer-bottom-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 12px;
  color: #64748B;
  flex-wrap: wrap;
  gap: 12px;
}
"""

LANDING_CLIENT_SCRIPT = """
function($scope, $timeout) {
  var c = this;
}
"""

LANDING_SERVER_SCRIPT = """
(function() {
  data.portalTitle = 'CIVIX AI';
})();
"""

if __name__ == "__main__":
    print("=== DEPLOYING COMPLETE PREMIUM PUBLIC LANDING PAGE ===")
    payload = {
        "template": LANDING_TEMPLATE.strip(),
        "css": LANDING_CSS.strip(),
        "client_script": LANDING_CLIENT_SCRIPT.strip(),
        "script": LANDING_SERVER_SCRIPT.strip(),
        "sys_scope": APP_SYS_ID,
        "sys_package": APP_SYS_ID,
        "public": "true"
    }
    api_put("sp_widget", sys_id, payload)
    print(f"  [SUCCESS] civix_landing_widget ({sys_id}) updated with Premium Design!")
