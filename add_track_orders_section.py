import re

with open('deploy_ui16_highlevel_worker_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

# ==============================================================================
# 1. ADD "TRACK ORDERS" TO THE SIDEBAR NAVIGATION
# ==============================================================================
old_sidebar_anchor = '<!-- Active Job Record removed from sidebar to keep nav clean -->'
new_sidebar_item = """      <!-- 3. Track Orders (Dedicated Section) -->
      <button type="button" class="sidebar-nav-link" ng-class="{{'active': c.currentTab === 'track'}}" ng-click="c.setTab('track')">
        <span class="nav-icon">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon>
          </svg>
        </span>
        <span class="nav-title">Track Orders</span>
        <span class="nav-badge-pill blue">Live</span>
      </button>"""

if old_sidebar_anchor in code:
    code = code.replace(old_sidebar_anchor, new_sidebar_item)
    print("Added 'Track Orders' button to sidebar!")
else:
    print("Could not find sidebar anchor, checking alternative...")

# ==============================================================================
# 2. ADD BREADCRUMB FOR TRACK ORDERS TAB
# ==============================================================================
old_crumb_profile = """<span class="crumb-current" ng-if="c.currentTab === 'profile'">Technician Profile &amp; Ward Info</span>"""
new_crumb_track = """<span class="crumb-current" ng-if="c.currentTab === 'track'">Track Orders &bull; Live Cross-Portal Lifecycle</span>
        <span class="crumb-current" ng-if="c.currentTab === 'profile'">Technician Profile &amp; Ward Info</span>"""
if old_crumb_profile in code:
    code = code.replace(old_crumb_profile, new_crumb_track)
    print("Added Track Orders breadcrumb!")

# ==============================================================================
# 3. ADD DEDICATED TRACK ORDERS VIEW TEMPLATE
# ==============================================================================
track_orders_view = """
      <!-- =====================================================================
           VIEW: TRACK ORDERS (DEDICATED FULL SECTION)
           ===================================================================== -->
      <div class="fsm-view-wrap" id="fsmTrackOrdersSection" ng-if="c.currentTab === 'track'">
        
        <!-- SECTION TITLE & SEARCH HEADER -->
        <div class="fsm-track-header-card">
          <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
            <div>
              <div class="d-flex align-items-center gap-2">
                <span class="badge-track-live">LIVE TRACKING SYSTEM</span>
                <h2 class="track-section-title">Field Work Order &amp; Citizen Case Tracker</h2>
              </div>
              <p class="track-section-subtitle">Real-time bi-directional synchronization between Citizen Complaints and Field Operations</p>
            </div>
            <div class="track-quick-actions">
              <button type="button" class="btn btn-sm btn-primary" ng-click="c.selectJob(c.getActiveTrackWo())">
                Manage Selected Order &rarr;
              </button>
            </div>
          </div>

          <!-- Quick Selector Pills for Ward 172 Work Orders -->
          <div class="track-order-selector-row mt-3">
            <span class="selector-lbl">SELECT ORDER:</span>
            <div class="selector-pills-list">
              <button type="button" class="track-select-pill" 
                      ng-repeat="wo in c.data.workOrders" 
                      ng-class="{{'active': c.getActiveTrackWo().u_number === wo.u_number}}" 
                      ng-click="c.selectTrackOrder(wo)">
                <span class="pill-wo-num">{{{{wo.u_number}}}}</span>
                <span class="pill-badge" ng-class="c.getStateClass(wo.u_state)">{{{{wo.u_state}}}}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- ACTIVE TRACKED ORDER DOSSIER -->
        <div class="fsm-card mt-3 track-dossier-card" ng-if="c.getActiveTrackWo()">
          
          <!-- Cross-Mapping Header Bar -->
          <div class="fsm-card-header bg-track-bar">
            <div class="d-flex align-items-center justify-content-between w-100 flex-wrap gap-2">
              <div class="d-flex align-items-center gap-2">
                <span class="badge-priority" ng-class="c.getPriorityClass(c.getActiveTrackWo().u_priority)">{{{{c.getActiveTrackWo().u_priority}}}}</span>
                <strong class="fsm-card-title font-mono">{{{{c.getActiveTrackWo().u_number}}}}</strong>
                <span class="text-muted">&harr;</span>
                <span class="fsm-case-pill font-mono">LINKED CASE: {{{{c.getActiveTrackWo().u_case_number}}}}</span>
              </div>
              <div class="d-flex align-items-center gap-2">
                <span class="badge-state" ng-class="c.getStateClass(c.getActiveTrackWo().u_state)">{{{{c.getActiveTrackWo().u_state}}}}</span>
                <a ng-href="https://www.google.com/maps/dir/?api=1&destination={{{{c.getActiveTrackWo().u_latitude}}}},{{{{c.getActiveTrackWo().u_longitude}}}}" target="_blank" class="btn btn-xs btn-default">
                  &#x1f9ed; GPS Map
                </a>
              </div>
            </div>
          </div>

          <div class="fsm-card-body p-4">
            
            <!-- 5-Stage Visual Stepper -->
            <div class="inapp-stepper my-3">
              <div class="step-dot-wrap" ng-class="{{'done': c.getStepNum(c.getActiveTrackWo().u_state) >= 1}}">
                <div class="step-dot">1</div>
                <span class="step-title">Submitted</span>
              </div>
              <div class="step-connector" ng-class="{{'done': c.getStepNum(c.getActiveTrackWo().u_state) >= 2}}"></div>
              <div class="step-dot-wrap" ng-class="{{'done': c.getStepNum(c.getActiveTrackWo().u_state) >= 2}}">
                <div class="step-dot">2</div>
                <span class="step-title">Dispatched</span>
              </div>
              <div class="step-connector" ng-class="{{'done': c.getStepNum(c.getActiveTrackWo().u_state) >= 3}}"></div>
              <div class="step-dot-wrap" ng-class="{{'done': c.getStepNum(c.getActiveTrackWo().u_state) >= 3}}">
                <div class="step-dot">3</div>
                <span class="step-title">Arrived</span>
              </div>
              <div class="step-connector" ng-class="{{'done': c.getStepNum(c.getActiveTrackWo().u_state) >= 4}}"></div>
              <div class="step-dot-wrap" ng-class="{{'done': c.getStepNum(c.getActiveTrackWo().u_state) >= 4}}">
                <div class="step-dot">4</div>
                <span class="step-title">In Progress</span>
              </div>
              <div class="step-connector" ng-class="{{'done': c.getStepNum(c.getActiveTrackWo().u_state) >= 5}}"></div>
              <div class="step-dot-wrap" ng-class="{{'done': c.getStepNum(c.getActiveTrackWo().u_state) >= 5}}">
                <div class="step-dot">5</div>
                <span class="step-title">Resolved</span>
              </div>
            </div>

            <!-- Two-Column Grid: Citizen Case Info + Field Execution Info -->
            <div class="row mt-4">
              
              <!-- Column 1: Citizen Complaint Details -->
              <div class="col-md-6 col-sm-12">
                <div class="track-sub-card">
                  <div class="track-sub-head">&#x1f4cb; Citizen Complaint Dossier</div>
                  <div class="track-sub-body">
                    <div class="track-field-row">
                      <span class="track-field-lbl">Issue Description:</span>
                      <strong class="track-field-val">{{{{c.getActiveTrackWo().u_short_description}}}}</strong>
                    </div>
                    <div class="track-field-row">
                      <span class="track-field-lbl">Location Address:</span>
                      <span class="track-field-val">{{{{c.getActiveTrackWo().u_location}}}} ({{{{c.getActiveTrackWo().u_ward}}}})</span>
                    </div>
                    <div class="track-field-row">
                      <span class="track-field-lbl">Registered By Citizen:</span>
                      <span class="track-field-val">S. Rajesh Kumar &bull; +91 98401 23456</span>
                    </div>
                    <div class="track-field-row">
                      <span class="track-field-lbl">Category &amp; Department:</span>
                      <span class="track-field-val">{{{{c.getActiveTrackWo().u_category}}}}</span>
                    </div>
                    <div class="track-field-row">
                      <span class="track-field-lbl">Target SLA Due:</span>
                      <span class="track-field-val font-mono font-bold">{{{{c.getActiveTrackWo().u_target_sla}}}}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Column 2: Assigned Field Crew & Verification -->
              <div class="col-md-6 col-sm-12">
                <div class="track-sub-card">
                  <div class="track-sub-head">&#x1f477; Field Execution &amp; Crew Dossier</div>
                  <div class="track-sub-body">
                    <div class="track-field-row">
                      <span class="track-field-lbl">Assigned Technician:</span>
                      <strong class="track-field-val text-success">{{{{c.getActiveTrackWo().u_assigned_name}}}}</strong>
                    </div>
                    <div class="track-field-row">
                      <span class="track-field-lbl">Worker Employee ID:</span>
                      <span class="track-field-val font-mono"><strong>{{{{c.getActiveTrackWo().u_worker_id || 'EMP-9021'}}}}</strong></span>
                    </div>
                    <div class="track-field-row">
                      <span class="track-field-lbl">Arrival Verification Code:</span>
                      <span class="track-field-val font-mono"><strong>{{{{c.getActiveTrackWo().u_arrival_otp || '4829'}}}}</strong> (On-Site Beacon)</span>
                    </div>
                    <div class="track-field-row">
                      <span class="track-field-lbl">Arrival Verified:</span>
                      <span class="track-field-val">
                        <span class="text-success" ng-if="c.getActiveTrackWo().u_arrival_verified === 'true' || c.getActiveTrackWo().u_arrival_verified === true">&#x2714; Verified ({{{{c.getActiveTrackWo().u_arrival_timestamp}}}})</span>
                        <span class="text-muted" ng-if="c.getActiveTrackWo().u_arrival_verified !== 'true' && c.getActiveTrackWo().u_arrival_verified !== true">Awaiting on-site technician beacon validation</span>
                      </span>
                    </div>
                    <div class="track-field-row">
                      <span class="track-field-lbl">Latest Field Status Note:</span>
                      <span class="track-field-val font-italic text-primary">{{{{c.getActiveTrackWo().u_completion_notes || 'Field technician actively deployed for site remediation.'}}}}</span>
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <!-- Live Field Activity Timeline -->
            <div class="inapp-activity-box mt-4">
              <strong class="text-xs text-muted font-bold text-uppercase">&#x2692; LIVE CHRONOLOGICAL FIELD AUDIT LOG</strong>
              <div class="timeline-scroll-feed mt-2">
                <div class="feed-item" ng-repeat="log in c.parseProgressLogs(c.getActiveTrackWo().u_progress_updates)">
                  <span class="feed-time">{{{{log.time}}}}</span>
                  <span class="feed-badge">{{{{log.category}}}}</span>
                  <span class="feed-text">{{{{log.text}}}}</span>
                </div>
              </div>
            </div>

          </div>

          <div class="fsm-card-footer bg-light d-flex justify-content-between align-items-center">
            <span class="text-xs text-muted">Auto-synchronized with Greater Chennai Corporation Central Dispatch</span>
            <button type="button" class="btn btn-sm btn-primary" ng-click="c.selectJob(c.getActiveTrackWo())">
              Open Work Order in Workbench &rarr;
            </button>
          </div>

        </div>

      </div>
"""

# Insert the Track Orders view before the Resolved History view
insert_marker = "<!-- VIEW 4: RESOLVED HISTORY ARCHIVE -->"
if "<!-- VIEW 4: RESOLVED HISTORY ARCHIVE -->" not in code:
    insert_marker = "ng-if=\"c.currentTab === 'history'\""

# Let's locate before history view
history_pattern = r'<div class="fsm-view-wrap" ng-if="c\.currentTab === \'history\'">'
if re.search(history_pattern, code):
    code = re.sub(history_pattern, track_orders_view + '\n      <div class="fsm-view-wrap" ng-if="c.currentTab === \'history\'">', code, count=1)
    print("Inserted Track Orders View before History View!")
else:
    print("Could not find history view pattern!")

# ==============================================================================
# 4. ALSO UPDATE RECORD DETAIL VIEW TO LINK TO TRACK SECTION DIRECTLY
# ==============================================================================
old_detail_track_btn = """              <!-- IN-APP CASE TRACKING BUTTON (NO NEW TAB!) -->
              <button type="button" class="btn btn-sm btn-info fsm-action-btn" ng-click="c.openCaseTrackingModal(c.selectedWo)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <span>Track Linked Case (In-App)</span>
              </button>"""

new_detail_track_btn = """              <!-- DEDICATED TRACK SECTION BUTTON -->
              <button type="button" class="btn btn-sm btn-info fsm-action-btn" ng-click="c.goToTrackOrder(c.selectedWo)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon></svg>
                <span>Track Order Section &rarr;</span>
              </button>"""

if old_detail_track_btn in code:
    code = code.replace(old_detail_track_btn, new_detail_track_btn)
    print("Updated detail header button to link to Track Order Section!")

# Also update the inline case link button
old_inline_link = """<button type="button" class="btn btn-xs btn-primary font-bold" ng-click="c.openCaseTrackingModal(c.selectedWo)">View In-App Tracking &rarr;</button>"""
new_inline_link = """<button type="button" class="btn btn-xs btn-primary font-bold" ng-click="c.goToTrackOrder(c.selectedWo)">Track Order &bull; Full Section &rarr;</button>"""
if old_inline_link in code:
    code = code.replace(old_inline_link, new_inline_link)
    print("Updated inline case mapping button!")

# ==============================================================================
# 5. ADD CLIENT METHODS FOR TRACK ORDERS VIEW
# ==============================================================================
old_client_anchor = "c.selectJob = function(wo) {"
new_client_methods = """  c.trackWo = null;

  c.getActiveTrackWo = function() {
    if (c.trackWo) return c.trackWo;
    if (c.selectedWo) return c.selectedWo;
    if (c.data.workOrders && c.data.workOrders.length > 0) return c.data.workOrders[0];
    return null;
  };

  c.selectTrackOrder = function(wo) {
    c.trackWo = wo;
  };

  c.goToTrackOrder = function(wo) {
    if (wo) c.trackWo = wo;
    c.setTab('track');
  };

  c.getStepNum = function(state) {
    if (!state) return 1;
    if (state === 'Assigned') return 2;
    if (state === 'Arrival Verified') return 3;
    if (state === 'In Progress' || state === 'On Hold') return 4;
    if (state === 'Completed' || state === 'Resolved') return 5;
    return 1;
  };

  c.selectJob = function(wo) {"""

if old_client_anchor in code:
    code = code.replace(old_client_anchor, new_client_methods, 1)
    print("Added Track Orders client methods!")

# ==============================================================================
# 6. ADD CSS FOR TRACK ORDERS SECTION
# ==============================================================================
track_css = """
/* ==============================================================================
   TRACK ORDERS DEDICATED SECTION CSS
   ============================================================================== */
.fsm-track-header-card {
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 18px 22px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
.badge-track-live {
  background: #e0f2fe;
  color: #0369a1;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
  letter-spacing: 0.5px;
}
.track-section-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #293e40;
}
.track-section-subtitle {
  margin: 4px 0 0 0;
  font-size: 13px;
  color: #64748b;
}
.track-order-selector-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  padding-top: 12px;
  border-top: 1px solid #f1f5f9;
}
.selector-lbl {
  font-size: 11px;
  font-weight: 700;
  color: #475569;
  letter-spacing: 0.5px;
}
.selector-pills-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.track-select-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.track-select-pill:hover {
  background: #e0f2fe;
  border-color: #0072ce;
}
.track-select-pill.active {
  background: #0072ce;
  border-color: #0072ce;
}
.track-select-pill.active .pill-wo-num {
  color: #ffffff;
}
.pill-wo-num {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 12px;
  font-weight: 600;
  color: #1e293b;
}
.pill-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
}
.track-dossier-card {
  border: 1px solid #d1d5db;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}
.bg-track-bar {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  padding: 12px 18px;
}
.track-sub-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
  height: 100%;
}
.track-sub-head {
  padding: 10px 14px;
  background: #edf2f7;
  font-size: 13px;
  font-weight: 700;
  color: #293e40;
  border-bottom: 1px solid #e2e8f0;
}
.track-sub-body {
  padding: 14px;
}
.track-field-row {
  display: flex;
  margin-bottom: 10px;
  font-size: 13px;
  line-height: 1.4;
}
.track-field-lbl {
  width: 150px;
  color: #64748b;
  flex-shrink: 0;
  font-size: 12.5px;
}
.track-field-val {
  color: #1e293b;
  flex: 1;
}
"""

old_css_anchor = "/* 1. LEFT SIDEBAR (270px) */"
if old_css_anchor in code:
    code = code.replace(old_css_anchor, track_css + "\n" + old_css_anchor)
    print("Added Track Orders CSS rules!")

with open('deploy_ui16_highlevel_worker_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved updated deploy_ui16_highlevel_worker_portal.py with dedicated Track Orders section!")
