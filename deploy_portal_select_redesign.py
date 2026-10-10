"""
Deploy Premium Portal Selection Redesign (civix_portal_select)
Matches Reference Image 1 exactly:
- Dark high-tech theme with glowing radial lighting
- Top bar with CIVIX AI brand and Language selector pill
- Ambient floating worker/ward status pills in background corners
- Centered hero headline with 'UNIFIED CIVIC SERVICE ECOSYSTEM' badge
- 3 Elevated Glowing Cards:
    1. Civic Citizen (Orange glow, Citizen Login, Register)
    2. Field Officer (Blue glow, Officer Login, Register Partner)
    3. Corporation Admin (Emerald/Amber glow, Admin Login, Internal only badge)
- Footer: '© 2026 CIVIX AI • Connect | Serve | Empower. All rights reserved.'
- Floating CIVIX Assist chatbot
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

INSTANCE_URL = os.getenv("SERVICENOW_INSTANCE_URL", "https://dev187180.service-now.com").rstrip("/")
USERNAME = os.getenv("SERVICENOW_USERNAME", "admin")
PASSWORD = os.getenv("SERVICENOW_PASSWORD", "mn%XC1^ScdA4")

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

TEMPLATE = """
<div class="civix-portal-select-root">

  <!-- Ambient Floating Background Badges (Matches Reference Image 1) -->
  <div class="civix-ambient-pill civix-amb-tl">
    <div class="amb-icon-wrap">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F97316" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
    </div>
    <div class="amb-text">
      <span class="amb-title">Adyar Ward 18</span>
      <span class="amb-sub">DISPATCH CREW ACTIVE</span>
    </div>
  </div>

  <div class="civix-ambient-pill civix-amb-tr">
    <div class="amb-icon-wrap">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
    </div>
    <div class="amb-text">
      <span class="amb-title">TANGEDCO Power Grid</span>
      <span class="amb-sub">RAPID RESPONSE UNIT</span>
    </div>
  </div>

  <div class="civix-ambient-pill civix-amb-bl">
    <div class="amb-icon-wrap">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
    </div>
    <div class="amb-text">
      <span class="amb-title">CMWSSB Water Works</span>
      <span class="amb-sub">MONITORED LINE</span>
    </div>
  </div>

  <div class="civix-ambient-pill civix-amb-br">
    <div class="amb-icon-wrap">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
    </div>
    <div class="amb-text">
      <span class="amb-title">Stormwater Desilting</span>
      <span class="amb-sub">ON SITE TECHNICIAN</span>
    </div>
  </div>

  <!-- Top Navigation Bar -->
  <header class="civix-portal-header">
    <div class="civix-portal-header-inner">
      <a href="?id=civix_landing" class="civix-portal-brand">
        <div class="civix-portal-brand-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M3 21h18M5 21V7l8-4v18M13 21V3l6 4v14"/></svg>
        </div>
        <div class="civix-portal-brand-info">
          <span class="brand-title">CIVIX AI</span>
          <span class="brand-sub">Greater Chennai Corporation</span>
        </div>
      </a>

      <!-- Language Selector Dropdown (Reference Image 1) -->
      <div class="civix-lang-dropdown" ng-class="{'open': c.langMenuOpen}">
        <button class="civix-lang-btn" type="button" ng-click="c.toggleLangMenu()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span>{{c.selectedLang}}</span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="civix-lang-menu" ng-if="c.langMenuOpen">
          <a href="javascript:void(0)" ng-click="c.selectLang('English')">English</a>
          <a href="javascript:void(0)" ng-click="c.selectLang('தமிழ் (Tamil)')">தமிழ் (Tamil)</a>
          <a href="javascript:void(0)" ng-click="c.selectLang('हिन्दी (Hindi)')">हिन्दी (Hindi)</a>
          <a href="javascript:void(0)" ng-click="c.selectLang('తెలుగు (Telugu)')">తెలుగు (Telugu)</a>
        </div>
      </div>
    </div>
  </header>

  <!-- Center Main Container -->
  <main class="civix-portal-main">
    <div class="civix-portal-hero">
      <!-- Pill Badge -->
      <div class="civix-badge-pill">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        <span>UNIFIED CIVIC SERVICE ECOSYSTEM</span>
      </div>

      <!-- Main Headline -->
      <h1 class="civix-portal-headline">Select Your Portal to Get Started</h1>

      <!-- Subtitle -->
      <p class="civix-portal-subtext">
        Dedicated authenticated portals designed for Citizens, Certified Field Technicians, and Municipal Administrators.
      </p>
    </div>

    <!-- 3 Glowing Dedicated Portal Cards (Reference Image 1) -->
    <div class="civix-cards-grid">

      <!-- CARD 1: CITIZEN (Orange Glow) -->
      <div class="civix-card civix-card-citizen">
        <div class="civix-card-icon-box">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#FB923C" stroke-width="2.2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>

        <span class="civix-card-tag">CITIZENS</span>
        <h2 class="civix-card-title">Civic Citizen</h2>
        <p class="civix-card-desc">
          Report civic issues with real-time GPS tracking, photo proof, automated AI triage, and live ward repair notifications.
        </p>

        <div class="civix-card-actions">
          <a href="?id=civix_home" class="btn btn-block civix-btn-primary-orange">
            <span>Customer Login (Email / Mobile)</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
          <a href="?id=civix_profile" class="btn btn-block civix-btn-secondary-glass">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
            <span>New Citizen? Register</span>
          </a>
        </div>
      </div>

      <!-- CARD 2: FIELD OFFICER / SERVICE PARTNER (Blue Glow) -->
      <div class="civix-card civix-card-officer">
        <div class="civix-card-icon-box">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2.2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
        </div>

        <span class="civix-card-tag">SERVICE PARTNERS</span>
        <h2 class="civix-card-title">Ward Field Officer</h2>
        <p class="civix-card-desc">
          Manage incoming ward bookings, verify on-site photographic evidence, request extra parts, and track repair SLA completion.
        </p>

        <div class="civix-card-actions">
          <a href="?id=civix_dashboard" class="btn btn-block civix-btn-primary-blue">
            <span>Officer Login (ID + OTP)</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
          <button type="button" class="btn btn-block civix-btn-secondary-glass" ng-click="c.showPartnerNotice()">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span>Register as Field Partner</span>
          </button>
        </div>
      </div>

      <!-- CARD 3: CORPORATION ADMIN (Emerald / Amber Glow) -->
      <div class="civix-card civix-card-admin">
        <div class="civix-card-icon-box">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2.2"><line x1="3" y1="21" x2="21" y2="21"/><line x1="4" y1="10" x2="20" y2="10"/><polyline points="12 3 2 10 22 10 12 3"/><line x1="6" y1="10" x2="6" y2="21"/><line x1="10" y1="10" x2="10" y2="21"/><line x1="14" y1="10" x2="14" y2="21"/><line x1="18" y1="10" x2="18" y2="21"/></svg>
        </div>

        <span class="civix-card-tag">COOPERATIVE AUTHORITY</span>
        <h2 class="civix-card-title">Corporation Admin</h2>
        <p class="civix-card-desc">
          Platform administration, verify and approve pillars, manage service catalogue, audit live orders, and inspect welfare finance.
        </p>

        <div class="civix-card-actions">
          <a href="/now/nav/ui/classic/params/target/incident_list.do" class="btn btn-block civix-btn-primary-amber">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            <span>Admin Login (ID + OTP)</span>
          </a>
          <div class="civix-card-restricted-pill">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            <span>Internal access only (No registration)</span>
          </div>
        </div>
      </div>

    </div>
  </main>

  <!-- Footer (Reference Image 1) -->
  <footer class="civix-portal-footer">
    <p>&copy; 2026 CIVIX AI &bull; Connect | Serve | Empower. All rights reserved.</p>
  </footer>

</div>
"""

CSS = """
/* Full-viewport dark override for ServiceNow Service Portal */
#page_root, .sp-page-root, body {
  background-color: #080C14 !important;
  color: #F8FAFC !important;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow-x: hidden !important;
}

.civix-portal-select-root {
  min-height: 100vh;
  width: 100%;
  background: radial-gradient(circle at 50% 15%, rgba(245, 158, 11, 0.05) 0%, transparent 45%),
              radial-gradient(circle at 80% 35%, rgba(59, 130, 246, 0.05) 0%, transparent 40%),
              radial-gradient(circle at 20% 70%, rgba(16, 185, 129, 0.04) 0%, transparent 40%),
              #080C14;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
}

/* Ambient Floating Background Badges (Reference Image 1) */
.civix-ambient-pill {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(8px);
  padding: 8px 16px;
  border-radius: 9999px;
  pointer-events: none;
  opacity: 0.65;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.civix-amb-tl { top: 90px; left: 40px; }
.civix-amb-tr { top: 90px; right: 40px; }
.civix-amb-bl { bottom: 60px; left: 40px; }
.civix-amb-br { bottom: 60px; right: 40px; }

.amb-icon-wrap {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
}

.amb-text {
  display: flex;
  flex-direction: column;
}

.amb-title {
  font-size: 11px;
  font-weight: 700;
  color: #CBD5E1;
  line-height: 1.2;
}

.amb-sub {
  font-size: 9px;
  font-weight: 600;
  color: #64748B;
  letter-spacing: 0.5px;
}

/* Top Navigation Bar */
.civix-portal-header {
  width: 100%;
  padding: 24px 48px;
  position: relative;
  z-index: 10;
}

.civix-portal-header-inner {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.civix-portal-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none !important;
}

.civix-portal-brand-logo {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
}

.civix-portal-brand-info {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-size: 18px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.brand-sub {
  font-size: 11px;
  font-weight: 500;
  color: #94A3B8;
  letter-spacing: 0.2px;
}

/* Language Selector Pill */
.civix-lang-dropdown {
  position: relative;
}

.civix-lang-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #E2E8F0;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 18px;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.civix-lang-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.25);
  color: #FFFFFF;
}

.civix-lang-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: #0F172A;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  min-width: 170px;
  padding: 6px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.5);
  z-index: 50;
}

.civix-lang-menu a {
  display: block;
  padding: 8px 14px;
  color: #CBD5E1;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.15s;
}

.civix-lang-menu a:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #FFFFFF;
}

/* Main Section */
.civix-portal-main {
  width: 100%;
  max-width: 1240px;
  margin: 0 auto;
  padding: 20px 24px 60px 24px;
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Hero Title Block */
.civix-portal-hero {
  text-align: center;
  max-width: 780px;
  margin-bottom: 48px;
}

.civix-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.35);
  color: #F59E0B;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 6px 16px;
  border-radius: 9999px;
  margin-bottom: 22px;
}

.civix-portal-headline {
  font-size: 44px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: -0.03em;
  line-height: 1.15;
  margin: 0 0 16px 0;
}

.civix-portal-subtext {
  font-size: 16px;
  font-weight: 400;
  color: #94A3B8;
  line-height: 1.6;
  margin: 0 auto;
  max-width: 660px;
}

/* 3 Cards Grid (Reference Image 1) */
.civix-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
  width: 100%;
}

@media (max-width: 992px) {
  .civix-cards-grid {
    grid-template-columns: 1fr;
    max-width: 480px;
  }
  .civix-ambient-pill {
    display: none !important;
  }
  .civix-portal-headline {
    font-size: 32px;
  }
}

/* Base Card Styling */
.civix-card {
  background: #0E1526;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 34px 28px;
  display: flex;
  flex-direction: column;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
}

.civix-card:hover {
  transform: translateY(-6px);
}

/* Card 1: Citizen (Orange Theme) */
.civix-card-citizen:hover {
  border-color: rgba(249, 115, 22, 0.4);
  box-shadow: 0 16px 40px rgba(249, 115, 22, 0.15), 0 0 20px rgba(249, 115, 22, 0.08);
}

.civix-card-citizen .civix-card-icon-box {
  background: rgba(249, 115, 22, 0.12);
  border: 1px solid rgba(249, 115, 22, 0.3);
  box-shadow: 0 0 20px rgba(249, 115, 22, 0.2);
}

.civix-card-citizen .civix-card-tag {
  color: #FB923C;
}

/* Card 2: Officer (Blue Theme) */
.civix-card-officer:hover {
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 16px 40px rgba(59, 130, 246, 0.15), 0 0 20px rgba(59, 130, 246, 0.08);
}

.civix-card-officer .civix-card-icon-box {
  background: rgba(59, 130, 246, 0.12);
  border: 1px solid rgba(59, 130, 246, 0.3);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
}

.civix-card-officer .civix-card-tag {
  color: #60A5FA;
}

/* Card 3: Admin (Green / Amber Theme) */
.civix-card-admin:hover {
  border-color: rgba(16, 185, 129, 0.4);
  box-shadow: 0 16px 40px rgba(16, 185, 129, 0.15), 0 0 20px rgba(16, 185, 129, 0.08);
}

.civix-card-admin .civix-card-icon-box {
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.3);
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
}

.civix-card-admin .civix-card-tag {
  color: #34D399;
}

/* Card Inner Elements */
.civix-card-icon-box {
  width: 58px;
  height: 58px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.civix-card-tag {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.4px;
  margin-bottom: 6px;
  display: block;
}

.civix-card-title {
  font-size: 24px;
  font-weight: 700;
  color: #FFFFFF;
  margin: 0 0 12px 0;
  letter-spacing: -0.02em;
}

.civix-card-desc {
  font-size: 13.5px;
  color: #94A3B8;
  line-height: 1.6;
  margin-bottom: 28px;
  min-height: 66px;
}

.civix-card-actions {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Buttons */
.civix-btn-primary-orange {
  background: linear-gradient(135deg, #F97316 0%, #EA580C 100%) !important;
  color: #FFFFFF !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  padding: 13px 20px !important;
  border-radius: 10px !important;
  border: none !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  box-shadow: 0 4px 16px rgba(249, 115, 22, 0.35) !important;
  transition: all 0.2s ease !important;
  text-decoration: none !important;
}

.civix-btn-primary-orange:hover {
  background: linear-gradient(135deg, #FB923C 0%, #F97316 100%) !important;
  box-shadow: 0 6px 20px rgba(249, 115, 22, 0.45) !important;
  transform: translateY(-1px);
}

.civix-btn-primary-blue {
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
  color: #FFFFFF !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  padding: 13px 20px !important;
  border-radius: 10px !important;
  border: none !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.35) !important;
  transition: all 0.2s ease !important;
  text-decoration: none !important;
}

.civix-btn-primary-blue:hover {
  background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%) !important;
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.45) !important;
  transform: translateY(-1px);
}

.civix-btn-primary-amber {
  background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
  color: #0F172A !important;
  font-weight: 800 !important;
  font-size: 14px !important;
  padding: 13px 20px !important;
  border-radius: 10px !important;
  border: none !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  box-shadow: 0 4px 16px rgba(245, 158, 11, 0.35) !important;
  transition: all 0.2s ease !important;
  text-decoration: none !important;
}

.civix-btn-primary-amber:hover {
  background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%) !important;
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.45) !important;
  transform: translateY(-1px);
}

.civix-btn-secondary-glass {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  color: #CBD5E1 !important;
  font-weight: 600 !important;
  font-size: 13.5px !important;
  padding: 11px 20px !important;
  border-radius: 10px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  transition: all 0.2s ease !important;
  text-decoration: none !important;
}

.civix-btn-secondary-glass:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(255, 255, 255, 0.22) !important;
  color: #FFFFFF !important;
}

.civix-card-restricted-pill {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.07);
  color: #94A3B8;
  font-size: 12px;
  font-weight: 500;
  padding: 11px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

/* Footer (Reference Image 1) */
.civix-portal-footer {
  width: 100%;
  padding: 24px;
  text-align: center;
  position: relative;
  z-index: 10;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
}

.civix-portal-footer p {
  margin: 0;
  font-size: 12px;
  color: #64748B;
  font-weight: 500;
}
"""

CLIENT_SCRIPT = """
function($scope, $window) {
  var c = this;

  c.selectedLang = 'English';
  c.langMenuOpen = false;

  c.toggleLangMenu = function() {
    c.langMenuOpen = !c.langMenuOpen;
  };

  c.selectLang = function(lang) {
    c.selectedLang = lang;
    c.langMenuOpen = false;
  };

  c.showPartnerNotice = function() {
    alert('Field Partner & Contractor Registration requires verified Greater Chennai Corporation (GCC) Department Authorization. Contact the Civic Operations Desk at 1800-425-0018.');
  };
}
"""

SERVER_SCRIPT = """
(function() {
  data.app_name = "CIVIX AI";
  data.region = "Greater Chennai Corporation";
})();
"""

print("=== DEPLOYING PORTAL SELECTION REDESIGN ===")
widget_res = api_get("sp_widget", query="id=civix_portal_select_widget", limit=1)
if not widget_res:
    print("Error: civix_portal_select_widget not found!")
    exit(1)

widget_sys_id = widget_res[0]["sys_id"]
api_put("sp_widget", widget_sys_id, {
    "template": TEMPLATE.strip(),
    "css": CSS.strip(),
    "client_script": CLIENT_SCRIPT.strip(),
    "script": SERVER_SCRIPT.strip()
})
print(f"  [SUCCESS] civix_portal_select_widget ({widget_sys_id}) updated with Reference Image 1 Design!")

# Update container to container-fluid for full-width layout
page_res = api_get("sp_page", query="id=civix_portal_select", limit=1)
if page_res:
    page_sys_id = page_res[0]["sys_id"]
    containers = api_get("sp_container", query=f"sp_page={page_sys_id}", limit=5)
    for cont in containers:
        cont_sys_id = cont["sys_id"]
        api_put("sp_container", cont_sys_id, {
            "width": "container-fluid",
            "bootstrap_alt": "true"
        })
        print(f"  [CONTAINER UPDATED] {cont_sys_id} set to container-fluid")

print("=== PORTAL SELECTION UPGRADE COMPLETE ===")
