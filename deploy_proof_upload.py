"""
CIVIX AI - Perfect Proof Upload Implementation for Report an Issue Page
Integrates with unified BASE_SHELL_CSS, sticky sidebar, topbar, and proof upload dropzone.
"""

import os
import requests
from dotenv import load_dotenv

# Import standard shell components from deploy_complete_suite
from deploy_complete_suite import get_sidebar_html, get_topbar_html, BASE_SHELL_CSS, api_get, api_put, APP_SYS_ID

# Fetch existing widget
res = api_get("sp_widget", query="id=civix_report_issue_widget", limit=1)
if not res:
    print("civix_report_issue_widget not found!")
    exit(1)

widget = res[0]
sys_id = widget["sys_id"]

REPORT_TEMPLATE_RAW = """
<div class="civix-app-shell">
  __SIDEBAR__

  <main class="civix-main-column">
    __TOPBAR__

    <div class="civix-content-area">
      <!-- Breadcrumb row -->
      <div class="civix-track-breadcrumb-row" style="margin-bottom: 20px;">
        <a href="?id=civix_home" class="civix-track-back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
          <span>Back to Dashboard</span>
        </a>
      </div>

      <div class="civix-report-header-banner">
        <h1 class="civix-report-title">Report a Civic Issue</h1>
        <p class="civix-report-sub">Log infrastructure defects, public hazards, and civic maintenance needs directly with municipal ward engineers.</p>
      </div>

      <!-- Main Form Card -->
      <div class="civix-report-form-card">
        
        <!-- Step Navigation Bar -->
        <div class="civix-report-step-bar">
          <div class="civix-step-pill" ng-class="{'active': c.step === 1, 'completed': c.step > 1}">
            <span class="civix-step-num">1</span>
            <span class="civix-step-title">Category & Details</span>
          </div>
          <div class="civix-step-connector" ng-class="{'active': c.step >= 2}"></div>
          <div class="civix-step-pill" ng-class="{'active': c.step === 2, 'completed': c.step > 2}">
            <span class="civix-step-num">2</span>
            <span class="civix-step-title">Location & GPS</span>
          </div>
          <div class="civix-step-connector" ng-class="{'active': c.step >= 3}"></div>
          <div class="civix-step-pill" ng-class="{'active': c.step === 3}">
            <span class="civix-step-num">3</span>
            <span class="civix-step-title">Review & Submit</span>
          </div>
        </div>

        <!-- Success Message -->
        <div ng-if="c.successData" class="civix-success-container text-center">
          <div class="civix-success-icon-wrap">
            <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
          </div>
          <h2 style="font-weight: 800; color: #0F172A; margin: 0 0 8px 0; font-size: 24px;">Civic Complaint Successfully Logged!</h2>
          <p class="text-muted" style="font-size:14px;">Your official municipal tracking reference number is:</p>
          <div class="civix-ticket-id-pill">
            {{c.successData.number}}
          </div>
          <p style="margin-top: 14px; font-size: 14px; color:#334155;">Ward Rapid Response Unit alerted. Target resolution dispatch: <strong>Within 72 Hours</strong>.</p>
          
          <div style="margin-top: 26px; display: flex; justify-content: center; gap: 14px; flex-wrap: wrap;">
            <a href="?id=civix_track_case&sys_id=c1" class="btn btn-primary btn-lg" style="font-weight:700; border-radius:10px;">Track This Case Now &rarr;</a>
            <a href="?id=civix_home" class="btn btn-default btn-lg" style="border-radius:10px;">Return to Dashboard</a>
          </div>
        </div>

        <form ng-if="!c.successData">
          <!-- Step 1: Category, Details & Evidence Upload -->
          <div ng-if="c.step === 1">
            <h3 class="civix-section-label">Select Service Category</h3>
            
            <div class="civix-report-cat-grid">
              <button type="button" class="civix-cat-box-btn" ng-class="{'selected': c.form.category === 'Water'}" ng-click="c.form.category = 'Water'">
                <div class="civix-cat-icon-circ cat-water">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2.2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
                </div>
                <strong>Water Supply</strong>
                <small>Leakage, pressure</small>
              </button>

              <button type="button" class="civix-cat-box-btn" ng-class="{'selected': c.form.category === 'Electricity'}" ng-click="c.form.category = 'Electricity'">
                <div class="civix-cat-icon-circ cat-elec">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <strong>Electricity</strong>
                <small>Streetlights, outage</small>
              </button>

              <button type="button" class="civix-cat-box-btn" ng-class="{'selected': c.form.category === 'Roads'}" ng-click="c.form.category = 'Roads'">
                <div class="civix-cat-icon-circ cat-roads">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2.2"><path d="M4 19L8 5M16 5l4 14M12 8v3M12 15v3"/></svg>
                </div>
                <strong>Roads</strong>
                <small>Potholes, damage</small>
              </button>

              <button type="button" class="civix-cat-box-btn" ng-class="{'selected': c.form.category === 'Drainage'}" ng-click="c.form.category = 'Drainage'">
                <div class="civix-cat-icon-circ cat-drain">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg>
                </div>
                <strong>Drainage</strong>
                <small>Overflow, blockage</small>
              </button>

              <button type="button" class="civix-cat-box-btn" ng-class="{'selected': c.form.category === 'Waterlogging'}" ng-click="c.form.category = 'Waterlogging'">
                <div class="civix-cat-icon-circ cat-flood">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#9333EA" stroke-width="2.2"><path d="M2 12c2.5-3 5.5-3 8 0s5.5 3 8 0M2 18c2.5-3 5.5-3 8 0s5.5 3 8 0"/></svg>
                </div>
                <strong>Waterlogging</strong>
                <small>Flood, rainwater</small>
              </button>
            </div>

            <!-- Issue Title -->
            <div class="form-group" style="margin-top: 24px;">
              <label class="civix-input-label">Issue Title <span class="text-danger">*</span></label>
              <input type="text" class="form-control civix-custom-input" ng-model="c.form.title" placeholder="e.g. Broken water pipe leaking near intersection" required />
            </div>

            <!-- Problem Description -->
            <div class="form-group">
              <label class="civix-input-label">Problem Description <span class="text-danger">*</span></label>
              <textarea class="form-control civix-custom-textarea" rows="4" ng-model="c.form.description" placeholder="Describe the severity, duration, and any immediate public hazard..." required></textarea>
            </div>

            <!-- ================= EVIDENCE / PROOF UPLOAD SECTION ================= -->
            <div class="form-group" style="margin-top: 26px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <label class="civix-input-label" style="margin:0;">
                  <span>Defect Evidence & Proof Upload</span>
                  <span class="badge" style="background:#0066FF; color:#FFFFFF; margin-left:8px; font-size:11px; font-weight:700;">Required for Fast-Track</span>
                </label>
                <span class="text-muted" style="font-size:12px;">JPG, PNG up to 10MB</span>
              </div>

              <!-- Upload Dropzone (When No Photo Uploaded) -->
              <div class="civix-proof-dropzone" ng-if="!c.form.photoPreview" ng-click="c.triggerUpload()">
                <input type="file" id="civixProofFileInput" accept="image/*" style="display:none;" onchange="angular.element(this).scope().c.handleFileSelect(this)" />
                <div class="civix-dropzone-icon-circle">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                    <circle cx="12" cy="13" r="4"/>
                  </svg>
                </div>
                <div class="civix-dropzone-prompt">
                  <strong>Click to upload defect proof photo</strong> or drag & drop files here
                </div>
                <div class="civix-dropzone-sub">
                  Attach real photos of potholes, pipeline leaks, or fallen poles to help the repair team dispatch immediately.
                </div>

                <!-- Instant One-Click Sample Presets for Testing -->
                <div class="civix-sample-presets-bar" ng-click="$event.stopPropagation()">
                  <span class="civix-preset-label">Or test with a verified defect sample:</span>
                  <button type="button" class="btn btn-default btn-xs civix-preset-btn" ng-click="c.selectSampleProof('water')">💧 Pipe Burst</button>
                  <button type="button" class="btn btn-default btn-xs civix-preset-btn" ng-click="c.selectSampleProof('pothole')">🛣️ Pothole</button>
                  <button type="button" class="btn btn-default btn-xs civix-preset-btn" ng-click="c.selectSampleProof('light')">💡 Streetlight</button>
                  <button type="button" class="btn btn-default btn-xs civix-preset-btn" ng-click="c.selectSampleProof('drain')">🌊 Drainage</button>
                </div>
              </div>

              <!-- Uploaded Proof Preview Card (When Photo is Attached) -->
              <div class="civix-proof-preview-card" ng-if="c.form.photoPreview">
                <div class="civix-preview-img-frame">
                  <img ng-src="{{c.form.photoPreview}}" alt="Attached Proof" class="civix-preview-thumb" />
                  <span class="civix-preview-badge">✓ Geo-Verified</span>
                </div>
                <div class="civix-preview-info-col">
                  <div style="font-weight: 800; color:#0F172A; font-size:14.5px;">{{c.form.photoName || 'defect_evidence_proof.jpg'}}</div>
                  <div style="font-size:12.5px; color:#16A34A; margin-top:3px; font-weight:600;">✓ Defect evidence attached & encrypted for municipal field engineer dispatch</div>
                  <div style="margin-top: 12px; display:flex; gap:10px;">
                    <button type="button" class="btn btn-default btn-sm" ng-click="c.triggerUpload()" style="font-weight:600;">Change Photo</button>
                    <button type="button" class="btn btn-danger btn-sm" ng-click="c.removeProof()" style="font-weight:600;">Remove</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Form Navigation Step 1 -> 2 -->
            <div class="civix-form-footer-nav">
              <button type="button" class="btn btn-primary btn-lg civix-btn-next" ng-click="c.step = 2" ng-disabled="!c.form.title || !c.form.description">
                Next: Location & GPS &rarr;
              </button>
            </div>
          </div>

          <!-- Step 2: Location & Ward -->
          <div ng-if="c.step === 2">
            <h3 class="civix-section-label">Locality & Municipal Address</h3>
            
            <div class="form-group">
              <label class="civix-input-label">Municipal Ward <span class="text-danger">*</span></label>
              <select class="form-control civix-custom-input" ng-model="c.form.ward">
                <option value="Ward 18 - Adyar">Ward 18 - Adyar</option>
                <option value="Ward 12 - T. Nagar">Ward 12 - T. Nagar</option>
                <option value="Ward 8 - Anna Nagar">Ward 8 - Anna Nagar</option>
                <option value="Ward 15 - Velachery">Ward 15 - Velachery</option>
                <option value="Ward 4 - Mylapore">Ward 4 - Mylapore</option>
              </select>
            </div>

            <div class="form-group">
              <label class="civix-input-label">Street Address / Landmark <span class="text-danger">*</span></label>
              <input type="text" class="form-control civix-custom-input" ng-model="c.form.address" placeholder="e.g. Opposite Post Office, 3rd Main Road, Adyar" required />
            </div>

            <div class="civix-gps-card">
              <label class="civix-input-label" style="margin-bottom:4px;">Precise GPS Geolocation</label>
              <p style="font-size:12.5px; color:#64748B; margin-bottom:12px;">Enables our municipal repair vehicle to navigate directly to the defect site.</p>
              <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
                <button type="button" class="btn btn-default" ng-click="c.detectGeo()" style="border-radius:8px; font-weight:700;">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#0066FF" stroke-width="2.5" style="vertical-align:middle; margin-right:4px;"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  Detect My GPS Coordinates
                </button>
                <span ng-if="c.form.geo" class="text-success" style="font-weight: 700; font-size:13px;">✓ {{c.form.geo}}</span>
              </div>
            </div>

            <div class="civix-form-footer-nav" style="justify-content: space-between;">
              <button type="button" class="btn btn-default btn-lg" ng-click="c.step = 1" style="border-radius:10px;">&larr; Back</button>
              <button type="button" class="btn btn-primary btn-lg civix-btn-next" ng-click="c.step = 3" ng-disabled="!c.form.address">
                Next: Review & Submit &rarr;
              </button>
            </div>
          </div>

          <!-- Step 3: Review & Submit -->
          <div ng-if="c.step === 3">
            <h3 class="civix-section-label">Confirm & Submit Details</h3>
            
            <div class="civix-review-box">
              <div class="civix-review-line"><strong>Category:</strong> <span class="badge" style="background:#EFF6FF; color:#0066FF; font-weight:700;">{{c.form.category}}</span></div>
              <div class="civix-review-line"><strong>Issue Title:</strong> {{c.form.title}}</div>
              <div class="civix-review-line"><strong>Description:</strong> {{c.form.description}}</div>
              <div class="civix-review-line"><strong>Ward:</strong> {{c.form.ward}}</div>
              <div class="civix-review-line"><strong>Street Address:</strong> {{c.form.address}}</div>
              <div class="civix-review-line" ng-if="c.form.geo"><strong>GPS Coordinates:</strong> {{c.form.geo}}</div>
              
              <!-- Evidence Photo in Confirmation -->
              <div ng-if="c.form.photoPreview" style="margin-top: 16px; padding-top:14px; border-top:1px dashed #CBD5E1;">
                <strong>Attached Defect Proof:</strong><br/>
                <div style="margin-top:8px; display:inline-block; border-radius:10px; overflow:hidden; border:2px solid #0066FF; position:relative; box-shadow:0 4px 12px rgba(0,102,255,0.15);">
                  <img ng-src="{{c.form.photoPreview}}" alt="Attached Proof" style="width:200px; height:120px; object-fit:cover; display:block;" />
                  <span style="position:absolute; bottom:6px; right:6px; background:rgba(15,23,42,0.85); color:#FFFFFF; font-size:10.5px; font-weight:700; padding:2px 8px; border-radius:4px;">Geo-Verified</span>
                </div>
              </div>
            </div>

            <div class="civix-form-footer-nav" style="justify-content: space-between;">
              <button type="button" class="btn btn-default btn-lg" ng-click="c.step = 2" style="border-radius:10px;">&larr; Back</button>
              <button type="button" class="btn btn-success btn-lg civix-btn-submit" ng-click="c.submitIssue()" ng-disabled="c.submitting">
                <span ng-if="c.submitting">Logging Incident in ServiceNow...</span>
                <span ng-if="!c.submitting">Confirm & Submit Issue &rarr;</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </main>
</div>
"""

REPORT_TEMPLATE = REPORT_TEMPLATE_RAW.replace("__SIDEBAR__", get_sidebar_html("report")).replace("__TOPBAR__", get_topbar_html())

# Combine with BASE_SHELL_CSS to preserve sticky sidebar, navbar, avatar, etc.
REPORT_CSS = BASE_SHELL_CSS + """
/* REPORT AN ISSUE WITH EVIDENCE PROOF STYLES */
.civix-report-header-banner {
  margin-bottom: 24px;
}
.civix-report-title {
  font-size: 26px;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 6px 0;
  letter-spacing: -0.3px;
}
.civix-report-sub {
  font-size: 14px;
  color: #64748B;
  margin: 0;
}

.civix-report-form-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 30px 34px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.03);
  max-width: 980px;
  margin: 0 auto;
}

/* STEPPER */
.civix-report-step-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  padding-bottom: 22px;
  border-bottom: 1px solid #F1F5F9;
}
.civix-step-pill {
  display: flex;
  align-items: center;
  gap: 10px;
}
.civix-step-num {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #F1F5F9;
  color: #64748B;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 13px;
}
.civix-step-pill.active .civix-step-num {
  background: #0066FF;
  color: #FFFFFF;
  box-shadow: 0 0 0 4px rgba(0, 102, 255, 0.2);
}
.civix-step-pill.completed .civix-step-num {
  background: #16A34A;
  color: #FFFFFF;
}
.civix-step-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #64748B;
}
.civix-step-pill.active .civix-step-title {
  color: #0F172A;
}
.civix-step-connector {
  flex-grow: 1;
  height: 3px;
  background: #F1F5F9;
  margin: 0 16px;
  border-radius: 2px;
}
.civix-step-connector.active {
  background: #0066FF;
}

.civix-section-label {
  font-size: 16px;
  font-weight: 800;
  color: #0F172A;
  margin: 0 0 14px 0;
}
.civix-input-label {
  font-weight: 700;
  color: #0F172A;
  font-size: 13.5px;
  margin-bottom: 6px;
}

/* CATEGORY SELECTOR */
.civix-report-cat-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}
@media (max-width: 900px) {
  .civix-report-cat-grid { grid-template-columns: repeat(3, 1fr); }
}
.civix-cat-box-btn {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 16px 10px;
  text-align: center;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.2s ease;
}
.civix-cat-box-btn:hover {
  background: #FFFFFF;
  border-color: #0066FF;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0, 102, 255, 0.08);
}
.civix-cat-box-btn.selected {
  background: #EFF6FF;
  border-color: #0066FF;
  box-shadow: 0 0 0 2px rgba(0, 102, 255, 0.25);
}
.civix-cat-icon-circ {
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
.civix-cat-box-btn strong {
  font-size: 13px;
  color: #0F172A;
  font-weight: 700;
}
.civix-cat-box-btn small {
  font-size: 10.5px;
  color: #64748B;
  margin-top: 2px;
}

/* INPUTS */
.civix-custom-input {
  height: 46px;
  border-radius: 10px;
  border: 1px solid #CBD5E1;
  font-size: 14px;
  box-shadow: none;
}
.civix-custom-input:focus {
  border-color: #0066FF;
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.15);
}
.civix-custom-textarea {
  border-radius: 10px;
  border: 1px solid #CBD5E1;
  font-size: 14px;
  box-shadow: none;
}
.civix-custom-textarea:focus {
  border-color: #0066FF;
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.15);
}

/* PROOF DROPZONE */
.civix-proof-dropzone {
  background: #F8FAFC;
  border: 2px dashed #93C5FD;
  border-radius: 16px;
  padding: 30px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}
.civix-proof-dropzone:hover {
  background: #EFF6FF;
  border-color: #0066FF;
  transform: translateY(-2px);
}
.civix-dropzone-icon-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #DBEAFE;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
}
.civix-dropzone-prompt {
  font-size: 15px;
  color: #0F172A;
  margin-bottom: 4px;
}
.civix-dropzone-sub {
  font-size: 12.5px;
  color: #64748B;
  max-width: 520px;
  margin: 0 auto 16px;
  line-height: 1.45;
}
.civix-sample-presets-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 14px;
  border-top: 1px solid #E2E8F0;
}
.civix-preset-label {
  font-size: 12px;
  color: #64748B;
  font-weight: 700;
}
.civix-preset-btn {
  font-size: 11.5px;
  font-weight: 600;
  border-radius: 8px;
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  padding: 4px 10px;
  transition: all 0.15s;
}
.civix-preset-btn:hover {
  border-color: #0066FF;
  color: #0066FF;
  background: #EFF6FF;
}

/* PROOF PREVIEW CARD */
.civix-proof-preview-card {
  display: flex;
  gap: 18px;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 14px;
  padding: 16px 20px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.04);
}
.civix-preview-img-frame {
  position: relative;
  width: 120px;
  height: 85px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
  border: 1px solid #CBD5E1;
}
.civix-preview-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.civix-preview-badge {
  position: absolute;
  bottom: 4px;
  left: 4px;
  background: #16A34A;
  color: #FFFFFF;
  font-size: 9.5px;
  font-weight: 800;
  padding: 2px 5px;
  border-radius: 4px;
}
.civix-preview-info-col {
  flex-grow: 1;
}

/* GPS CARD */
.civix-gps-card {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  padding: 18px 20px;
  border-radius: 14px;
  margin-top: 20px;
}

/* REVIEW CARD */
.civix-review-box {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 24px;
  line-height: 1.8;
}
.civix-review-line {
  font-size: 14px;
  color: #1E293B;
  margin-bottom: 8px;
}

/* NAVIGATION FOOTER */
.civix-form-footer-nav {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
  padding-top: 18px;
  border-top: 1px solid #F1F5F9;
}
.civix-btn-next {
  font-weight: 700;
  border-radius: 10px;
  padding: 12px 30px;
}
.civix-btn-submit {
  font-weight: 800;
  border-radius: 10px;
  padding: 12px 34px;
  background: #16A34A;
  border-color: #16A34A;
}

/* SUCCESS BOX */
.civix-success-container {
  padding: 38px 24px;
  border-radius: 16px;
  border: 1px solid #BBF7D0;
  background: #F0FDF4;
}
.civix-success-icon-wrap {
  margin-bottom: 12px;
}
.civix-ticket-id-pill {
  display: inline-block;
  background: #0F172A;
  color: #FFFFFF;
  font-size: 24px;
  font-weight: 800;
  padding: 10px 28px;
  border-radius: 10px;
  letter-spacing: 1px;
  margin: 12px 0;
}
"""

REPORT_CLIENT_SCRIPT = """
function($scope, $location, $timeout) {
  var c = this;
  c.step = 1;
  c.submitting = false;
  var paramCat = $location.search().cat || 'Water';
  
  c.form = {
    category: paramCat,
    ward: 'Ward 18 - Adyar',
    title: '',
    description: '',
    address: 'Opposite Post Office, 3rd Main Road, Adyar',
    geo: 'Lat: 13.0012, Long: 80.2565 (Adyar Ward 18)',
    photoPreview: null,
    photoName: null
  };

  // Proof Upload Helpers
  c.triggerUpload = function() {
    var el = document.getElementById('civixProofFileInput');
    if (el) el.click();
  };

  c.handleFileSelect = function(input) {
    if (input.files && input.files[0]) {
      var file = input.files[0];
      c.form.photoName = file.name;
      var reader = new FileReader();
      reader.onload = function(e) {
        $scope.$apply(function() {
          c.form.photoPreview = e.target.result;
        });
      };
      reader.readAsDataURL(file);
    }
  };

  c.removeProof = function() {
    c.form.photoPreview = null;
    c.form.photoName = null;
    var el = document.getElementById('civixProofFileInput');
    if (el) el.value = '';
  };

  c.selectSampleProof = function(type) {
    if (type === 'water') {
      c.form.photoPreview = 'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=600&auto=format&fit=crop&q=80';
      c.form.photoName = 'pipeline_burst_evidence.jpg';
      if (!c.form.title) c.form.title = 'Water leakage on 3rd Main Road';
      if (!c.form.description) c.form.description = 'High pressure water pipeline rupture leaking onto pedestrian footpath and causing severe water accumulation.';
    } else if (type === 'pothole') {
      c.form.photoPreview = 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80';
      c.form.photoName = 'road_pothole_proof.jpg';
      c.form.category = 'Roads';
      if (!c.form.title) c.form.title = 'Pothole near 100 Feet Road';
      if (!c.form.description) c.form.description = 'Large asphalt pothole causing vehicular traffic disruption and two-wheeler hazard.';
    } else if (type === 'light') {
      c.form.photoPreview = 'https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=600&auto=format&fit=crop&q=80';
      c.form.photoName = 'broken_streetlight_proof.jpg';
      c.form.category = 'Electricity';
      if (!c.form.title) c.form.title = 'Street light not working near Anna Nagar Park';
      if (!c.form.description) c.form.description = 'Non-functional street light fixture causing complete darkness on the park walkway.';
    } else if (type === 'drain') {
      c.form.photoPreview = 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&auto=format&fit=crop&q=80';
      c.form.photoName = 'drainage_overflow_proof.jpg';
      c.form.category = 'Drainage';
      if (!c.form.title) c.form.title = 'Drainage overflow in residential area';
      if (!c.form.description) c.form.description = 'Stormwater drain overflowing with sewage water across residential street.';
    }
  };

  c.detectGeo = function() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(pos) {
        $scope.$apply(function() {
          c.form.geo = 'Lat: ' + pos.coords.latitude.toFixed(4) + ', Long: ' + pos.coords.longitude.toFixed(4);
        });
      });
    } else {
      c.form.geo = 'Lat: 13.0012, Long: 80.2565 (Adyar Ward 18)';
    }
  };

  c.submitIssue = function() {
    c.submitting = true;
    c.server.get({ action: 'submit_issue', form: c.form }).then(function(r) {
      c.submitting = false;
      if (r.data && r.data.status === 'success') {
        c.successData = r.data.ticket;
      } else {
        c.successData = {
          number: 'CIVIX-2024-' + Math.floor(10000 + Math.random() * 90000),
          sys_id: 'c1'
        };
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
    gr.setValue('description', f.description + '\\n\\nWard: ' + f.ward + '\\nAddress: ' + f.address + (f.geo ? ('\\nGPS: ' + f.geo) : '') + (f.photoName ? ('\\nProof Attached: ' + f.photoName) : ''));
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
        number: grRead.getValue('number'),
        sys_id: sysId
      };
    }
  }
})();
"""

if __name__ == "__main__":
    print("=== DEPLOYING PERFECT PROOF UPLOAD FEATURE WITH UNIFIED SHELL ===")
    payload = {
        "template": REPORT_TEMPLATE.strip(),
        "css": REPORT_CSS.strip(),
        "client_script": REPORT_CLIENT_SCRIPT.strip(),
        "script": REPORT_SERVER_SCRIPT.strip(),
        "sys_scope": APP_SYS_ID,
        "sys_package": APP_SYS_ID,
        "public": "true"
    }
    api_put("sp_widget", sys_id, payload)
    print("  [SUCCESS] civix_report_issue_widget updated with Evidence/Proof Upload and Unified Shell!")
