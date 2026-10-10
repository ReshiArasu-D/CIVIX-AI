"""
CIVIX AI - Premium Redesign of Citizen Profile & Settings Page (civix_profile)
Replaces the plain initial placeholder with the full Plus Jakarta Sans design system,
hero citizen identity card, verified credentials, ward locality, notifications, and settings tabs.
"""

import os
import requests
from dotenv import load_dotenv

from deploy_complete_suite import get_sidebar_html, get_topbar_html, BASE_SHELL_CSS, api_get, api_put, APP_SYS_ID

# Fetch widget
res = api_get("sp_widget", query="id=civix_profile_widget", limit=1)
if not res:
    print("civix_profile_widget not found!")
    exit(1)

widget = res[0]
sys_id = widget["sys_id"]

PROFILE_TEMPLATE_RAW = """
<div class="civix-app-shell">
  __SIDEBAR__

  <main class="civix-main-column">
    __TOPBAR__

    <div class="civix-content-area">
      <!-- Breadcrumb -->
      <div class="civix-track-breadcrumb-row" style="margin-bottom: 20px;">
        <a href="?id=civix_home" class="civix-track-back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
          <span>Back to Dashboard</span>
        </a>
      </div>

      <!-- HERO CITIZEN IDENTITY CARD -->
      <div class="civix-profile-hero-card">
        <div class="civix-profile-hero-bg"></div>
        <div class="civix-profile-hero-content">
          <div class="civix-profile-avatar-frame">
            <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=240&auto=format&fit=crop&q=80" alt="Priya Sharma" class="civix-profile-avatar-img" />
            <span class="civix-verified-shield" title="UIDAI Aadhaar Verified Citizen">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
            </span>
          </div>

          <div class="civix-profile-info-col">
            <div class="civix-profile-badges-row">
              <span class="civix-badge-verified">✓ UIDAI Verified Citizen</span>
              <span class="civix-badge-ward">Ward 18 (Adyar)</span>
              <span class="civix-badge-id">CIN: GCC-2024-88319</span>
            </div>
            
            <h1 class="civix-profile-name">Priya Sharma</h1>
            <p class="civix-profile-motto">Registered Citizen of Greater Chennai Corporation &bull; Adyar Ward 18 Resident</p>

            <div class="civix-profile-kpi-row">
              <div class="civix-prof-kpi">
                <span class="kpi-num">12</span>
                <span class="kpi-lbl">Total Complaints</span>
              </div>
              <div class="civix-prof-kpi">
                <span class="kpi-num" style="color:#10B981;">8</span>
                <span class="kpi-lbl">Resolved</span>
              </div>
              <div class="civix-prof-kpi">
                <span class="kpi-num" style="color:#F59E0B;">3</span>
                <span class="kpi-lbl">In Progress</span>
              </div>
              <div class="civix-prof-kpi">
                <span class="kpi-num" style="color:#0066FF;">100%</span>
                <span class="kpi-lbl">Citizen Trust Score</span>
              </div>
            </div>
          </div>

          <div class="civix-profile-hero-actions">
            <button type="button" class="btn btn-default civix-btn-outline-light" ng-click="c.showPhotoNotice()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
              <span>Change Photo</span>
            </button>
            <a href="?id=civix_landing" class="btn btn-danger civix-btn-danger-out" title="Sign out of portal">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
              <span>Sign Out</span>
            </a>
          </div>
        </div>
      </div>

      <!-- SUCCESS TOAST NOTIFICATION -->
      <div class="alert alert-success civix-save-alert" ng-if="c.savedSuccess">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
        <span>Profile & Civic Preferences updated successfully!</span>
      </div>

      <!-- 2-COLUMN SETTINGS GRID -->
      <div class="civix-profile-settings-grid">
        
        <!-- LEFT COLUMN: IDENTITY & LOCALITY -->
        <div class="civix-settings-col">
          
          <!-- SECTION 1: PERSONAL & CIVIC IDENTITY -->
          <div class="civix-white-box civix-settings-card">
            <div class="civix-card-head-row">
              <div class="civix-card-title-group">
                <div class="civix-card-icon-pill">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                </div>
                <div>
                  <h3 class="civix-card-head-title">Personal & Civic Identity</h3>
                  <p class="civix-card-head-sub">Verified against Government of India UIDAI Registry.</p>
                </div>
              </div>
            </div>

            <div class="civix-fields-stack">
              <div class="form-group">
                <label class="civix-label">Full Legal Name</label>
                <input type="text" class="form-control civix-field-input" ng-model="c.profile.name" />
              </div>

              <div class="civix-two-fields-row">
                <div class="form-group">
                  <label class="civix-label">Registered Email</label>
                  <div class="input-group">
                    <input type="email" class="form-control civix-field-input" ng-model="c.profile.email" />
                    <span class="input-group-addon civix-verified-addon">✓ Verified</span>
                  </div>
                </div>

                <div class="form-group">
                  <label class="civix-label">Registered Mobile</label>
                  <div class="input-group">
                    <input type="text" class="form-control civix-field-input" ng-model="c.profile.mobile" />
                    <span class="input-group-addon civix-verified-addon">✓ OTP</span>
                  </div>
                </div>
              </div>

              <div class="civix-two-fields-row">
                <div class="form-group">
                  <label class="civix-label">Aadhaar Verification (Masked)</label>
                  <div class="input-group">
                    <input type="text" class="form-control civix-field-input" value="XXXX-XXXX-4821" readonly style="background:#F8FAFC; color:#64748B; font-weight:700;" />
                    <span class="input-group-addon civix-verified-addon" style="background:#DCFCE7; color:#15803D;">✓ UIDAI</span>
                  </div>
                </div>

                <div class="form-group">
                  <label class="civix-label">Assigned Portal Role</label>
                  <input type="text" class="form-control civix-field-input" value="x_civic_ai_citizen (CIVIX Core)" readonly style="background:#F8FAFC; color:#64748B;" />
                </div>
              </div>
            </div>
          </div>

          <!-- SECTION 2: WARD & RESIDENTIAL LOCALITY -->
          <div class="civix-white-box civix-settings-card">
            <div class="civix-card-head-row">
              <div class="civix-card-title-group">
                <div class="civix-card-icon-pill" style="background:#EFF6FF; color:#0066FF;">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2.2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                </div>
                <div>
                  <h3 class="civix-card-head-title">Residential Locality & Ward</h3>
                  <p class="civix-card-head-sub">Used for routing complaints to your local ward engineer team.</p>
                </div>
              </div>
            </div>

            <div class="civix-fields-stack">
              <div class="civix-two-fields-row">
                <div class="form-group">
                  <label class="civix-label">Municipal Corporation</label>
                  <input type="text" class="form-control civix-field-input" value="Greater Chennai Corporation (GCC)" readonly style="background:#F8FAFC; color:#64748B;" />
                </div>

                <div class="form-group">
                  <label class="civix-label">Zone & Ward</label>
                  <select class="form-control civix-field-input" ng-model="c.profile.ward">
                    <option value="Ward 18 - Adyar (Zone XIII)">Ward 18 - Adyar (Zone XIII)</option>
                    <option value="Ward 12 - T. Nagar (Zone X)">Ward 12 - T. Nagar (Zone X)</option>
                    <option value="Ward 8 - Anna Nagar (Zone VIII)">Ward 8 - Anna Nagar (Zone VIII)</option>
                    <option value="Ward 15 - Velachery (Zone XIII)">Ward 15 - Velachery (Zone XIII)</option>
                    <option value="Ward 4 - Mylapore (Zone IX)">Ward 4 - Mylapore (Zone IX)</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="civix-label">Street Address & Door Number</label>
                <input type="text" class="form-control civix-field-input" ng-model="c.profile.address" />
              </div>

              <div class="civix-two-fields-row">
                <div class="form-group">
                  <label class="civix-label">Landmark</label>
                  <input type="text" class="form-control civix-field-input" ng-model="c.profile.landmark" />
                </div>
                <div class="form-group">
                  <label class="civix-label">Postal Pincode</label>
                  <input type="text" class="form-control civix-field-input" ng-model="c.profile.pincode" />
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- RIGHT COLUMN: PREFERENCES & SECURITY -->
        <div class="civix-settings-col">
          
          <!-- SECTION 3: NOTIFICATIONS & LANGUAGE -->
          <div class="civix-white-box civix-settings-card">
            <div class="civix-card-head-row">
              <div class="civix-card-title-group">
                <div class="civix-card-icon-pill" style="background:#FEF3C7; color:#D97706;">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                </div>
                <div>
                  <h3 class="civix-card-head-title">Notifications & Language</h3>
                  <p class="civix-card-head-sub">Control how municipal ward updates are delivered.</p>
                </div>
              </div>
            </div>

            <div class="civix-fields-stack">
              <div class="form-group">
                <label class="civix-label">Preferred Interface Language</label>
                <select class="form-control civix-field-input" ng-model="c.profile.language">
                  <option value="en">English (Official)</option>
                  <option value="ta">தமிழ் (Tamil)</option>
                  <option value="hi">हिंदी (Hindi)</option>
                  <option value="te">తెలుగు (Telugu)</option>
                  <option value="kn">ಕನ್ನಡ (Kannada)</option>
                </select>
              </div>

              <!-- Toggles Stack -->
              <div class="civix-toggle-item-row">
                <div>
                  <strong>SMS Dispatch Updates</strong>
                  <p>Receive text alerts when field engineers begin on-site repairs.</p>
                </div>
                <input type="checkbox" class="civix-switch" ng-model="c.profile.smsAlerts" />
              </div>

              <div class="civix-toggle-item-row">
                <div>
                  <strong>WhatsApp Real-time Tracking</strong>
                  <p>Receive milestone photos and resolution confirmation on WhatsApp.</p>
                </div>
                <input type="checkbox" class="civix-switch" ng-model="c.profile.whatsappAlerts" />
              </div>

              <div class="civix-toggle-item-row">
                <div>
                  <strong>Corporation Public Advisories</strong>
                  <p>Weekly bulletins regarding scheduled water and road maintenance.</p>
                </div>
                <input type="checkbox" class="civix-switch" ng-model="c.profile.emailAdvisories" />
              </div>
            </div>
          </div>

          <!-- SECTION 4: ACCOUNT SECURITY & ACTIONS -->
          <div class="civix-white-box civix-settings-card">
            <div class="civix-card-head-row">
              <div class="civix-card-title-group">
                <div class="civix-card-icon-pill" style="background:#F1F5F9; color:#475569;">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2.2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                </div>
                <div>
                  <h3 class="civix-card-head-title">Session & Security</h3>
                  <p class="civix-card-head-sub">Active login credentials and audit log.</p>
                </div>
              </div>
            </div>

            <div class="civix-session-info-box">
              <div class="civix-sess-row">
                <span class="sess-dot"></span>
                <span>Active Session: <strong>Windows 11 Chrome</strong></span>
              </div>
              <small class="text-muted">Authenticated via Aadhaar OTP &bull; IP: 157.48.21.90 (Chennai)</small>
            </div>

            <div style="margin-top: 22px; display:flex; flex-direction:column; gap:10px;">
              <button type="button" class="btn btn-primary btn-lg civix-btn-save-profile" ng-click="c.saveProfile()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                <span>Save Profile Changes</span>
              </button>

              <button type="button" class="btn btn-default civix-btn-download-card" ng-click="c.downloadCardNotice()">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                <span>Download Citizen Digital Identity Card</span>
              </button>
            </div>
          </div>

        </div>

      </div>

    </div>
  </main>
</div>
"""

PROFILE_TEMPLATE = PROFILE_TEMPLATE_RAW.replace("__SIDEBAR__", get_sidebar_html("")).replace("__TOPBAR__", get_topbar_html())

PROFILE_CSS = BASE_SHELL_CSS + """
/* HERO IDENTITY CARD */
.civix-profile-hero-card {
  position: relative;
  background: linear-gradient(135deg, #0B192C 0%, #1E3A8A 55%, #0284C7 100%);
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 26px;
  box-shadow: 0 10px 30px rgba(11, 25, 44, 0.12);
  color: #FFFFFF;
}
.civix-profile-hero-bg {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 50%;
  background: url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1000&auto=format&fit=crop&q=80') center right/cover no-repeat;
  opacity: 0.12;
  pointer-events: none;
}
.civix-profile-hero-content {
  position: relative;
  z-index: 2;
  padding: 32px 36px;
  display: flex;
  align-items: center;
  gap: 28px;
  flex-wrap: wrap;
}

.civix-profile-avatar-frame {
  position: relative;
  width: 104px;
  height: 104px;
  border-radius: 50%;
  border: 4px solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
  flex-shrink: 0;
}
.civix-profile-avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  display: block;
}
.civix-verified-shield {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #10B981;
  border: 2px solid #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.civix-profile-info-col {
  flex-grow: 1;
  min-width: 280px;
}
.civix-profile-badges-row {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
}
.civix-badge-verified {
  background: #10B981;
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 6px;
  letter-spacing: 0.3px;
}
.civix-badge-ward {
  background: rgba(255, 255, 255, 0.18);
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 6px;
  backdrop-filter: blur(4px);
}
.civix-badge-id {
  background: rgba(255, 255, 255, 0.1);
  color: #CBD5E1;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 6px;
}

.civix-profile-name {
  font-size: 28px;
  font-weight: 800;
  color: #FFFFFF;
  margin: 0 0 4px 0;
  letter-spacing: -0.4px;
}
.civix-profile-motto {
  font-size: 13.5px;
  color: #E2E8F0;
  margin: 0 0 18px 0;
}

.civix-profile-kpi-row {
  display: flex;
  gap: 24px;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  flex-wrap: wrap;
}
.civix-prof-kpi {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.civix-prof-kpi .kpi-num {
  font-size: 20px;
  font-weight: 800;
  color: #FFFFFF;
}
.civix-prof-kpi .kpi-lbl {
  font-size: 11.5px;
  color: #CBD5E1;
  font-weight: 600;
}

.civix-profile-hero-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: stretch;
  flex-shrink: 0;
}
.civix-btn-outline-light {
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #FFFFFF !important;
  font-weight: 700;
  border-radius: 10px;
  padding: 9px 18px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}
.civix-btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: #FFFFFF;
}
.civix-btn-danger-out {
  background: rgba(220, 38, 38, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #FECACA !important;
  font-weight: 700;
  border-radius: 10px;
  padding: 9px 18px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  text-decoration: none !important;
}
.civix-btn-danger-out:hover {
  background: #DC2626;
  color: #FFFFFF !important;
  border-color: #DC2626;
}

/* SETTINGS GRID */
.civix-profile-settings-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr);
  gap: 24px;
}
@media (max-width: 960px) {
  .civix-profile-settings-grid { grid-template-columns: 1fr; }
}
.civix-settings-col {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.civix-settings-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 18px;
  padding: 24px 28px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}
.civix-card-head-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid #F1F5F9;
}
.civix-card-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}
.civix-card-icon-pill {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #EFF6FF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.civix-card-head-title {
  font-size: 16.5px;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 2px 0;
}
.civix-card-head-sub {
  font-size: 12.5px;
  color: #64748B;
  margin: 0;
}

.civix-fields-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.civix-two-fields-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
@media (max-width: 600px) {
  .civix-two-fields-row { grid-template-columns: 1fr; }
}

.civix-label {
  font-size: 13px;
  font-weight: 700;
  color: #1E293B;
  margin-bottom: 6px;
}
.civix-field-input {
  height: 44px;
  border-radius: 10px;
  border: 1px solid #CBD5E1;
  font-size: 13.5px;
  box-shadow: none;
}
.civix-field-input:focus {
  border-color: #0066FF;
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.15);
}
.civix-verified-addon {
  background: #EFF6FF;
  color: #0066FF;
  font-weight: 700;
  font-size: 11.5px;
  border: 1px solid #CBD5E1;
  border-left: none;
  border-radius: 0 10px 10px 0;
}

/* TOGGLES */
.civix-toggle-item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  background: #F8FAFC;
  border: 1px solid #F1F5F9;
  border-radius: 12px;
}
.civix-toggle-item-row strong {
  font-size: 13.5px;
  color: #0F172A;
  display: block;
  margin-bottom: 2px;
}
.civix-toggle-item-row p {
  font-size: 11.5px;
  color: #64748B;
  margin: 0;
}
.civix-switch {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #0066FF;
}

/* SESSION & SAVE */
.civix-session-info-box {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 14px 16px;
}
.civix-sess-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #0F172A;
  margin-bottom: 4px;
}
.sess-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10B981;
}

.civix-btn-save-profile {
  font-weight: 800;
  border-radius: 12px;
  padding: 13px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: #0066FF;
  border-color: #0066FF;
  box-shadow: 0 4px 14px rgba(0, 102, 255, 0.25);
}
.civix-btn-save-profile:hover {
  background: #0052CC;
}
.civix-btn-download-card {
  font-weight: 700;
  border-radius: 12px;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-color: #CBD5E1;
  color: #0066FF;
}

.civix-save-alert {
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  padding: 14px 18px;
  margin-bottom: 24px;
  border: 1px solid #BBF7D0;
  background: #F0FDF4;
  color: #15803D;
  animation: fadeIn 0.3s;
}
"""

PROFILE_CLIENT_SCRIPT = """
function($scope, $timeout) {
  var c = this;
  c.savedSuccess = false;

  c.profile = {
    name: 'Priya Sharma',
    email: 'priya.sharma@example.com',
    mobile: '+91 98765 43210',
    ward: 'Ward 18 - Adyar (Zone XIII)',
    address: 'Opposite Post Office, 3rd Main Road',
    landmark: 'Near Gandhi Nagar Club',
    pincode: '600020',
    language: 'en',
    smsAlerts: true,
    whatsappAlerts: true,
    emailAdvisories: true
  };

  c.saveProfile = function() {
    c.savedSuccess = true;
    $timeout(function() {
      c.savedSuccess = false;
    }, 4000);
  };

  c.showPhotoNotice = function() {
    alert('UIDAI citizen verification photo is synchronized with your Corporation Identity Record. To update, please submit a municipal change request.');
  };

  c.downloadCardNotice = function() {
    alert('Generating encrypted CIVIX Digital Identity Card for Priya Sharma (CIN: GCC-2024-88319)... File ready for download.');
  };
}
"""

PROFILE_SERVER_SCRIPT = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  data.userName = gs.getUserDisplayName();
})();
"""

if __name__ == "__main__":
    print("=== DEPLOYING COMPLETE PREMIUM CITIZEN PROFILE & SETTINGS PAGE ===")
    payload = {
        "template": PROFILE_TEMPLATE.strip(),
        "css": PROFILE_CSS.strip(),
        "client_script": PROFILE_CLIENT_SCRIPT.strip(),
        "script": PROFILE_SERVER_SCRIPT.strip(),
        "sys_scope": APP_SYS_ID,
        "sys_package": APP_SYS_ID,
        "public": "true"
    }
    api_put("sp_widget", sys_id, payload)
    print(f"  [SUCCESS] civix_profile_widget ({sys_id}) updated with Premium Design!")
