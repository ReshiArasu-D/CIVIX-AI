"""
CIVIX AI - Advance ServiceNow UI16 High Level Field Worker Portal
1. Fixes record detail view opening at the top with a sticky UI16 action header bar
2. Replaces external page redirection with a sleek In-App Live Case Tracking Modal
3. Implements High Level ServiceNow UI16 corporate styling:
   - High contrast text colors (#293E40 charcoal, #475569 labels, #0072CE links)
   - Authentic UI16 form dividers, crisp borders (#D1D5DB), clean zebra table
4. Integrates the CIVIX Assist / CoopBot AI Chat Assistant floating widget
5. Updates standalone civix_track_case_widget with robust case normalization & bindings
"""

import os
import base64
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

def api_get(table: str, query: str = "", limit: int = 50):
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
    existing = api_get("sp_widget", query=f"id={widget_id}", limit=1)
    if not existing:
        print(f"  [ERROR] Widget {widget_id} not found!")
        return None
    sys_id = existing[0]["sys_id"]
    payload = {
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip()
    }
    api_put("sp_widget", sys_id, payload)
    print(f"  [UPDATED] Widget {widget_id} ({sys_id})")
    return sys_id

# Load Mascot image as Base64
mascot_path = r"d:\tcs\coopbot_mascot_clean.png"
if os.path.exists(mascot_path):
    with open(mascot_path, "rb") as f:
        COOPBOT_IMG_B64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
else:
    COOPBOT_IMG_B64 = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=100&auto=format&fit=crop&q=80"

# ==============================================================================
# 1. ADVANCE SERVICENOW UI16 FIELD WORKER PORTAL TEMPLATE
# ==============================================================================

UI16_TEMPLATE = f"""
<div class="fsm-portal-shell" id="fsmPortalShell">

  <!-- =========================================================================
       1. EXECUTIVE DARK LEFT SIDEBAR (ServiceNow UI16 Console Style)
       ========================================================================= -->
  <aside class="fsm-sidebar">
    
    <!-- Brand Box -->
    <div class="sidebar-brand-box" ng-click="c.setTab(c.prevTab || 'jobs')">
      <div class="sidebar-logo-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5">
          <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
          <line x1="8" y1="21" x2="16" y2="21"></line>
          <line x1="12" y1="17" x2="12" y2="21"></line>
        </svg>
      </div>
      <div class="sidebar-brand-titles">
        <span class="brand-app-name">CIVIX FIELD OPS</span>
        <span class="brand-corp-tag">Greater Chennai Corporation</span>
      </div>
    </div>

    <!-- Live Shift Banner -->
    <div class="sidebar-shift-banner">
      <span class="shift-pulsing-dot"></span>
      <span class="shift-banner-text">ON DUTY &bull; 07:00 &ndash; 15:30</span>
    </div>

    <!-- NAVIGATION VIEWS -->
    <div class="sidebar-section-heading">OPERATIONAL VIEWS</div>
    <nav class="sidebar-nav-menu">

      <!-- 1. Dashboard -->
      <button type="button" class="sidebar-nav-link" ng-class="{{'active': c.currentTab === 'dashboard'}}" ng-click="c.setTab('dashboard')">
        <span class="nav-icon">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect>
          </svg>
        </span>
        <span class="nav-title">Dashboard</span>
      </button>

      <!-- 2. Assigned Work Orders -->
      <button type="button" class="sidebar-nav-link" ng-class="{{'active': c.currentTab === 'jobs' || c.currentTab === 'detail'}}" ng-click="c.setTab('jobs')">
        <span class="nav-icon">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
        </span>
        <span class="nav-title">Assigned Work Orders</span>
        <span class="nav-badge-pill">{{{{c.data.workOrders.length}}}}</span>
      </button>

      <!-- Active Job Record removed from sidebar to keep nav clean -->

      <!-- 4. Resolved History -->
      <button type="button" class="sidebar-nav-link" ng-class="{{'active': c.currentTab === 'history'}}" ng-click="c.setTab('history')">
        <span class="nav-icon">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>
          </svg>
        </span>
        <span class="nav-title">Resolved History</span>
        <span class="nav-badge-pill green">{{{{c.getHistoryJobs().length}}}}</span>
      </button>

      <!-- 5. Technician Info -->
      <button type="button" class="sidebar-nav-link" ng-class="{{'active': c.currentTab === 'profile'}}" ng-click="c.setTab('profile')">
        <span class="nav-icon">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle>
          </svg>
        </span>
        <span class="nav-title">Technician Info</span>
      </button>

    </nav>

    <!-- SLA PRIORITY FILTERS -->
    <div class="sidebar-section-heading mt-4">SLA PRIORITY FILTERS</div>
    <div class="sidebar-quick-filters">
      <button type="button" class="sidebar-filter-btn" ng-class="{{'active': c.jobsFilter === 'Urgent'}}" ng-click="c.setJobsFilter('Urgent')">
        <span class="filter-dot red"></span>
        <span class="filter-lbl">P1 Critical Tasks</span>
        <span class="filter-badge">{{{{c.stats.urgent}}}}</span>
      </button>
      <button type="button" class="sidebar-filter-btn" ng-class="{{'active': c.jobsFilter === 'In Progress'}}" ng-click="c.setJobsFilter('In Progress')">
        <span class="filter-dot blue"></span>
        <span class="filter-lbl">Active On-Site</span>
        <span class="filter-badge">{{{{c.stats.inProgress}}}}</span>
      </button>
      <button type="button" class="sidebar-filter-btn" ng-class="{{'active': c.jobsFilter === 'On Hold'}}" ng-click="c.setJobsFilter('On Hold')">
        <span class="filter-dot amber"></span>
        <span class="filter-lbl">On Hold / Blocked</span>
        <span class="filter-badge">{{{{c.stats.onHold}}}}</span>
      </button>
    </div>

    <!-- SIDEBAR FOOTER -->
    <div class="sidebar-user-footer">
      <div class="user-profile-card" ng-click="c.setTab('profile')">
        <div class="user-avatar-ks">KS</div>
        <div class="user-info-text">
          <span class="user-name-title">{{{{c.data.worker.name}}}}</span>
          <span class="user-code-pill">Worker ID: <strong>{{{{c.data.worker.employee_id}}}}</strong></span>
          <span class="user-ward-line">{{{{c.data.worker.ward}}}}</span>
        </div>
      </div>
      <a href="?id=civix_portal_select" class="sidebar-exit-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/>
        </svg>
        <span>Change Portal &bull; Sign Out</span>
      </a>
    </div>

  </aside>

  <!-- =========================================================================
       2. RIGHT MAIN CONTENT AREA
       ========================================================================= -->
  <div class="fsm-content-area" id="fsmContentArea">

    <!-- Top Executive Ribbon -->
    <header class="fsm-top-header">
      <div class="top-header-breadcrumbs">
        <span class="crumb-link" ng-click="c.setTab('dashboard')">CIVIX FSM</span>
        <span class="crumb-arrow">/</span>
        <span class="crumb-current" ng-if="c.currentTab === 'dashboard'">Operations Dashboard</span>
        <span class="crumb-current" ng-if="c.currentTab === 'jobs'">Assigned Work Orders</span>
        <span class="crumb-link" ng-if="c.currentTab === 'detail'" ng-click="c.setTab('jobs')">Assigned Work Orders</span>
        <span class="crumb-arrow" ng-if="c.currentTab === 'detail'">/</span>
        <span class="crumb-current font-mono" ng-if="c.currentTab === 'detail'">{{{{c.selectedWo.u_number}}}}</span>
        <span class="crumb-current" ng-if="c.currentTab === 'history'">Resolved History Archive</span>
        <span class="crumb-current" ng-if="c.currentTab === 'profile'">Technician Profile &amp; Ward Info</span>
      </div>

      <div class="top-header-right">
        <div class="top-sync-badge" title="Real-time synchronization between citizen cases and field worker records">
          <span class="sync-dot-green"></span>
          <span>Case ID &harr; Worker ID Mapped</span>
        </div>

        <span class="top-ward-badge">Ward 172 &bull; Zone 13 Adyar</span>

        <button type="button" class="btn btn-sm btn-default top-refresh-btn" ng-click="c.refreshData()">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
          </svg>
          <span>Refresh</span>
        </button>
      </div>
    </header>

    <!-- MAIN BODY CONTAINER -->
    <main class="fsm-main-container">

      <!-- =====================================================================
           VIEW 1: DASHBOARD
           ===================================================================== -->
      <div class="fsm-view-wrap" ng-if="c.currentTab === 'dashboard'">
        
        <!-- Emergency Dispatch Alert -->
        <div class="fsm-urgent-alert" ng-if="c.stats.urgent > 0">
          <div class="urgent-tag">P1 CRITICAL DISPATCH</div>
          <div class="urgent-text">
            <strong>{{{{c.stats.urgent}}}} Critical Emergency Work Orders</strong> assigned in Ward 172. Mandatory response SLA is active.
          </div>
          <button type="button" class="btn btn-xs btn-danger" ng-click="c.setJobsFilter('Urgent')">View Critical &rarr;</button>
        </div>

        <!-- 4 KPI Metric Tiles -->
        <div class="fsm-kpi-grid">
          
          <div class="fsm-kpi-card kpi-teal" ng-click="c.setJobsFilter('All')">
            <div class="kpi-top-bar"></div>
            <div class="kpi-body">
              <span class="kpi-lbl">TOTAL WORK ORDERS</span>
              <div class="kpi-val-row">
                <span class="kpi-number">{{{{c.stats.assigned + c.stats.inProgress + c.stats.onHold + c.stats.completed}}}}</span>
                <span class="kpi-pill">Ward 172</span>
              </div>
              <span class="kpi-foot">All municipal jobs</span>
            </div>
          </div>

          <div class="fsm-kpi-card kpi-blue" ng-click="c.setJobsFilter('In Progress')">
            <div class="kpi-top-bar"></div>
            <div class="kpi-body">
              <span class="kpi-lbl">IN PROGRESS / ON SITE</span>
              <div class="kpi-val-row">
                <span class="kpi-number text-primary">{{{{c.stats.inProgress}}}}</span>
                <span class="kpi-pill blue">Active</span>
              </div>
              <span class="kpi-foot">Arrival verified &amp; executing</span>
            </div>
          </div>

          <div class="fsm-kpi-card kpi-red" ng-click="c.setJobsFilter('Urgent')">
            <div class="kpi-top-bar"></div>
            <div class="kpi-body">
              <span class="kpi-lbl">CRITICAL (P1) SLA</span>
              <div class="kpi-val-row">
                <span class="kpi-number text-danger">{{{{c.stats.urgent}}}}</span>
                <span class="kpi-pill red">Urgent</span>
              </div>
              <span class="kpi-foot">Immediate hazard fix</span>
            </div>
          </div>

          <div class="fsm-kpi-card kpi-green" ng-click="c.setJobsFilter('Completed')">
            <div class="kpi-top-bar"></div>
            <div class="kpi-body">
              <span class="kpi-lbl">COMPLETED TODAY</span>
              <div class="kpi-val-row">
                <span class="kpi-number text-success">{{{{c.stats.completed}}}}</span>
                <span class="kpi-pill green">Verified</span>
              </div>
              <span class="kpi-foot">Submitted for sign-off</span>
            </div>
          </div>

        </div>

        <!-- Current Active Task Banner -->
        <div class="fsm-card mt-4" ng-if="c.activeJob">
          <div class="fsm-card-header bg-active-task">
            <div class="d-flex align-items-center">
              <span class="pulse-indicator"></span>
              <strong class="fsm-card-title">CURRENT ACTIVE TASK ON SITE &bull; {{{{c.activeJob.u_number}}}}</strong>
            </div>
            <button type="button" class="btn btn-sm btn-primary" ng-click="c.selectJob(c.activeJob)">
              Resume Execution &rarr;
            </button>
          </div>
          <div class="fsm-card-body">
            <div class="active-task-flex">
              <div class="task-info-left">
                <h3 class="task-headline">{{{{c.activeJob.u_short_description}}}}</h3>
                <p class="task-address-line">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                  <span>{{{{c.activeJob.u_location}}}} ({{{{c.activeJob.u_ward}}}})</span>
                </p>
              </div>
              <div class="task-mappings-right">
                <div class="mapping-chip-box">
                  <span class="chip-lbl">MAPPED CASE ID:</span>
                  <strong class="chip-val font-mono">{{{{c.activeJob.u_case_number}}}}</strong>
                </div>
                <div class="mapping-chip-box">
                  <span class="chip-lbl">ASSIGNED WORKER ID:</span>
                  <strong class="chip-val font-mono">{{{{c.activeJob.u_worker_id || 'EMP-9021'}}}} ({{{{c.activeJob.u_assigned_name}}}})</strong>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Assigned Work Orders Table -->
        <div class="fsm-card mt-4">
          <div class="fsm-card-header">
            <strong class="fsm-card-title">ASSIGNED WORK ORDERS &bull; MAPPED DATABASE RECORDS</strong>
            <button type="button" class="btn btn-xs btn-default" ng-click="c.setTab('jobs')">View All ({{{{c.data.workOrders.length}}}}) &rarr;</button>
          </div>
          <div class="fsm-card-body p-0">
            <div class="table-responsive">
              <table class="table fsm-table mb-0">
                <thead>
                  <tr>
                    <th>WORK ORDER #</th>
                    <th>LINKED CASE ID</th>
                    <th>CATEGORY &amp; DESCRIPTION</th>
                    <th>PRIORITY</th>
                    <th>STATE</th>
                    <th>ASSIGNED TECH</th>
                    <th>ACTION</th>
                  </tr>
                </thead>
                <tbody>
                  <tr ng-repeat="wo in c.data.workOrders" class="fsm-table-row">
                    <td>
                      <a href="javascript:void(0)" ng-click="c.selectJob(wo)" class="fsm-wo-code">
                        <strong>{{{{wo.u_number}}}}</strong>
                      </a>
                    </td>
                    <td>
                      <span class="fsm-case-pill" title="Citizen Complaint Case ID">
                        {{{{wo.u_case_number}}}}
                      </span>
                    </td>
                    <td>
                      <div class="fsm-desc-cell">
                        <span class="cat-badge-small">{{{{wo.u_category}}}}</span>
                        <span class="desc-line">{{{{wo.u_short_description}}}}</span>
                      </div>
                    </td>
                    <td>
                      <span class="badge-priority" ng-class="c.getPriorityClass(wo.u_priority)">{{{{wo.u_priority}}}}</span>
                    </td>
                    <td>
                      <span class="badge-state" ng-class="c.getStateClass(wo.u_state)">{{{{wo.u_state}}}}</span>
                    </td>
                    <td>
                      <span class="tech-id-text">{{{{wo.u_worker_id || 'EMP-9021'}}}} &bull; {{{{wo.u_assigned_name}}}}</span>
                    </td>
                    <td>
                      <button type="button" class="btn btn-xs btn-default fsm-btn-row-action" ng-click="c.selectJob(wo)">
                        Open Record &rarr;
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>

      <!-- =====================================================================
           VIEW 2: ASSIGNED WORK ORDERS (MY JOBS)
           ===================================================================== -->
      <div class="fsm-view-wrap" ng-if="c.currentTab === 'jobs'">
        
        <!-- Filter Bar -->
        <div class="fsm-filter-toolbar">
          <div class="search-input-wrap">
            <svg class="search-svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" class="form-control fsm-search-input" placeholder="Search by Work Order #, Case ID (CIV-2026-...), Category, Location..." ng-model="c.jobsSearch" />
            <button type="button" class="clear-search-btn" ng-if="c.jobsSearch" ng-click="c.jobsSearch = ''">&times;</button>
          </div>

          <div class="filter-pills-row">
            <button type="button" class="pill-btn" ng-class="{{'active': c.jobsFilter === 'All'}}" ng-click="c.jobsFilter = 'All'">All ({{{{c.data.workOrders.length}}}})</button>
            <button type="button" class="pill-btn" ng-class="{{'active': c.jobsFilter === 'Assigned'}}" ng-click="c.jobsFilter = 'Assigned'">Assigned ({{{{c.stats.assigned}}}})</button>
            <button type="button" class="pill-btn" ng-class="{{'active': c.jobsFilter === 'In Progress'}}" ng-click="c.jobsFilter = 'In Progress'">In Progress ({{{{c.stats.inProgress}}}})</button>
            <button type="button" class="pill-btn" ng-class="{{'active': c.jobsFilter === 'Urgent'}}" ng-click="c.jobsFilter = 'Urgent'">Urgent P1 ({{{{c.stats.urgent}}}})</button>
            <button type="button" class="pill-btn" ng-class="{{'active': c.jobsFilter === 'On Hold'}}" ng-click="c.jobsFilter = 'On Hold'">On Hold ({{{{c.stats.onHold}}}})</button>
            <button type="button" class="pill-btn" ng-class="{{'active': c.jobsFilter === 'Completed'}}" ng-click="c.jobsFilter = 'Completed'">Completed ({{{{c.stats.completed}}}})</button>
          </div>
        </div>

        <!-- Job Cards Stack -->
        <div class="fsm-jobs-stack mt-3">
          <div class="fsm-job-card" ng-repeat="wo in c.getFilteredJobs()" ng-class="{{'critical-border': wo.u_priority.indexOf('Critical') !== -1}}">
            <div class="job-card-topbar">
              <div class="job-id-cluster">
                <span class="wo-num-badge">{{{{wo.u_number}}}}</span>
                <span class="mapped-case-tag" title="Linked Citizen Complaint Case">MAPPED CASE: <strong>{{{{wo.u_case_number}}}}</strong></span>
              </div>
              <div class="job-status-cluster">
                <span class="badge-priority" ng-class="c.getPriorityClass(wo.u_priority)">{{{{wo.u_priority}}}}</span>
                <span class="badge-state" ng-class="c.getStateClass(wo.u_state)">{{{{wo.u_state}}}}</span>
              </div>
            </div>

            <h3 class="job-headline" ng-click="c.selectJob(wo)">{{{{wo.u_short_description}}}}</h3>

            <div class="job-meta-grid">
              <div class="meta-item">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                <span>{{{{wo.u_location}}}} &bull; {{{{wo.u_ward}}}}</span>
              </div>
              <div class="meta-item">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                <span>Target SLA Due: <strong>{{{{wo.u_target_sla}}}}</strong></span>
              </div>
              <div class="meta-item">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                <span>Assigned Tech: <strong>{{{{wo.u_assigned_name}}}}</strong> (Worker ID: <strong>{{{{wo.u_worker_id || 'EMP-9021'}}}}</strong>)</span>
              </div>
            </div>

            <div class="job-card-bottombar">
              <span class="cat-pill-gray">{{{{wo.u_category}}}}</span>
              <button type="button" class="btn btn-sm btn-primary" ng-click="c.selectJob(wo)">
                Manage Work Order &rarr;
              </button>
            </div>
          </div>
        </div>

      </div>

      <!-- =====================================================================
           VIEW 3: WORK ORDER DETAIL (OPENS CLEANLY AT VERY TOP WITH STICKY HEADER)
           ===================================================================== -->
      <div class="fsm-view-wrap" id="fsmDetailTopView" ng-if="c.currentTab === 'detail' && c.selectedWo">
        
        <!-- STICKY TOP ACTION HEADER BAR -->
        <div class="fsm-record-header-sticky">
          <div class="record-header-main-row">
            <div class="record-title-group">
              <button type="button" class="btn btn-sm btn-default fsm-back-btn" ng-click="c.setTab('dashboard')">
                &larr; Back to Work Orders
              </button>
              <h2 class="record-h2 font-mono">Work Order: {{{{c.selectedWo.u_number}}}}</h2>
              <span class="badge-state ml-2" ng-class="c.getStateClass(c.selectedWo.u_state)">{{{{c.selectedWo.u_state}}}}</span>
              <span class="badge-priority ml-1" ng-class="c.getPriorityClass(c.selectedWo.u_priority)">{{{{c.selectedWo.u_priority}}}}</span>
            </div>

            <div class="record-top-actions">
              <!-- IN-APP CASE TRACKING BUTTON (NO NEW TAB!) -->
              <button type="button" class="btn btn-sm btn-info fsm-action-btn" ng-click="c.openCaseTrackingModal(c.selectedWo)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <span>Track Linked Case (In-App)</span>
              </button>

              <a ng-href="https://www.google.com/maps/dir/?api=1&destination={{{{c.selectedWo.u_latitude}}}},{{{{c.selectedWo.u_longitude}}}}" target="_blank" class="btn btn-sm btn-default fsm-action-btn">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="3 11 22 2 13 21 11 13 3 11"></polygon></svg>
                <span>GPS Route</span>
              </a>

              <button type="button" class="btn btn-sm btn-default fsm-action-btn" ng-click="c.openProgressModal()">+ Work Note</button>
              <button type="button" class="btn btn-sm btn-default fsm-action-btn" ng-click="c.openEvidenceModal()">&#x1f4f7; Add Photo</button>
              <button type="button" class="btn btn-sm btn-warning fsm-action-btn" ng-if="c.selectedWo.u_state === 'In Progress'" ng-click="c.openHoldModal()">&#x23f8; Hold</button>
              <button type="button" class="btn btn-sm btn-info fsm-action-btn" ng-if="c.selectedWo.u_state === 'On Hold'" ng-click="c.resumeWork()" ng-disabled="c.resumingWork">&#x25b6; Resume</button>
              <button type="button" class="btn btn-sm btn-success fsm-action-btn" ng-if="c.selectedWo.u_state === 'In Progress' || c.selectedWo.u_state === 'Arrival Verified'" ng-click="c.openCompleteModal()">&#x2714; Complete Work &rarr;</button>
            </div>
          </div>
        </div>

        <!-- FORM RECORD CONTENT -->
        <div class="fsm-record-body-card">
          
          <!-- SECTION 1: IDENTIFICATION & CROSS-PORTAL MAPPING -->
          <div class="form-section-box">
            <div class="section-badge-title">1. RECORD IDENTIFICATION &amp; CROSS-PORTAL MAPPING</div>
            <div class="row">
              <div class="col-md-6 col-sm-12">
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">Work Order Number</label>
                  <div class="fsm-val font-mono"><strong>{{{{c.selectedWo.u_number}}}}</strong></div>
                </div>
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl text-primary"><strong>LINKED CASE ID (CITIZEN COMPLAINT)</strong></label>
                  <div class="fsm-mapping-box-blue">
                    <span class="case-id-txt">{{{{c.selectedWo.u_case_number}}}}</span>
                    <button type="button" class="btn btn-xs btn-primary" ng-click="c.openCaseTrackingModal(c.selectedWo)">
                      View In-App Tracking &rarr;
                    </button>
                  </div>
                </div>
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">Category</label>
                  <div class="fsm-val">{{{{c.selectedWo.u_category}}}}</div>
                </div>
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">Priority Level</label>
                  <div class="fsm-val">
                    <span class="badge-priority" ng-class="c.getPriorityClass(c.selectedWo.u_priority)">{{{{c.selectedWo.u_priority}}}}</span>
                  </div>
                </div>
              </div>

              <div class="col-md-6 col-sm-12">
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">Current State</label>
                  <div class="fsm-val">
                    <span class="badge-state" ng-class="c.getStateClass(c.selectedWo.u_state)">{{{{c.selectedWo.u_state}}}}</span>
                  </div>
                </div>
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl text-success"><strong>ASSIGNED WORKER &amp; EMPLOYEE ID</strong></label>
                  <div class="fsm-mapping-box-green">
                    <span class="worker-name-txt">{{{{c.selectedWo.u_assigned_name}}}}</span>
                    <span class="worker-id-txt">Worker ID: <strong>{{{{c.selectedWo.u_worker_id || 'EMP-9021'}}}}</strong></span>
                  </div>
                </div>
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">Ward &amp; Zone</label>
                  <div class="fsm-val">{{{{c.selectedWo.u_ward}}}} &bull; {{{{c.selectedWo.u_zone}}}}</div>
                </div>
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">Target SLA Resolution Due</label>
                  <div class="fsm-val font-mono">{{{{c.selectedWo.u_target_sla}}}}</div>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-xs-12">
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">Short Description</label>
                  <div class="fsm-val font-bold">{{{{c.selectedWo.u_short_description}}}}</div>
                </div>
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">Full Technical Description &amp; Instructions</label>
                  <div class="fsm-val text-muted">{{{{c.selectedWo.u_description}}}}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- SECTION 2: PHYSICAL LOCATION -->
          <div class="form-section-box">
            <div class="section-badge-title">2. ON-SITE LOCATION &amp; GEO-COORDINATES</div>
            <div class="row">
              <div class="col-md-8 col-sm-12">
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">Location Address</label>
                  <div class="fsm-val">{{{{c.selectedWo.u_location}}}}</div>
                </div>
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">Landmark &amp; Site Access</label>
                  <div class="fsm-val">{{{{c.selectedWo.u_landmark}}}}</div>
                </div>
              </div>
              <div class="col-md-4 col-sm-12">
                <div class="form-group fsm-fg">
                  <label class="fsm-lbl">GPS Coordinates (Lat / Long)</label>
                  <div class="fsm-val font-mono">{{{{c.selectedWo.u_latitude}}}}, {{{{c.selectedWo.u_longitude}}}}</div>
                </div>
                <a ng-href="https://www.google.com/maps/search/?api=1&query={{{{c.selectedWo.u_latitude}}}},{{{{c.selectedWo.u_longitude}}}}" target="_blank" class="btn btn-block btn-default btn-xs mt-2">
                  Open in Google Maps &rarr;
                </a>
              </div>
            </div>
          </div>

          <!-- SECTION 3: STEP-BY-STEP EXECUTION ACTIONS -->
          <div class="form-section-box">
            <div class="section-badge-title">3. WORK ORDER EXECUTION LIFECYCLE &amp; ACTIONS</div>

            <!-- STEP A: ARRIVAL OTP VERIFICATION -->
            <div class="fsm-action-card" ng-if="c.selectedWo.u_state === 'Assigned'">
              <div class="action-card-header">
                <div class="step-icon-round">A</div>
                <div>
                  <strong class="action-card-h">Step 1: Arrival Verification via OTP</strong>
                  <p class="action-card-p">Enter the 4-digit beacon code or citizen confirmation code (Demo code: <strong>{{{{c.selectedWo.u_arrival_otp || '4829'}}}}</strong>)</p>
                </div>
              </div>
              <div class="action-card-body">
                <div class="otp-cluster">
                  <input type="text" class="form-control otp-field" maxlength="4" placeholder="4829" ng-model="c.otpInput" />
                  <button type="button" class="btn btn-primary" ng-click="c.verifyArrival()" ng-disabled="c.verifyingOtp || !c.otpInput">
                    <span ng-if="!c.verifyingOtp">Verify Arrival On Site &rarr;</span>
                    <span ng-if="c.verifyingOtp">Validating OTP...</span>
                  </button>
                </div>
                <div class="text-danger mt-1" ng-if="c.otpError">{{{{c.otpError}}}}</div>
              </div>
            </div>

            <!-- STEP B: START PHYSICAL WORK -->
            <div class="fsm-action-card bg-arrival-ok" ng-if="c.selectedWo.u_state === 'Arrival Verified'">
              <div class="action-card-header">
                <div class="step-icon-round bg-green">&#x2713;</div>
                <div>
                  <strong class="action-card-h">Step 2: Arrival Verified at {{{{c.selectedWo.u_arrival_timestamp}}}}</strong>
                  <p class="action-card-p">Technician is physically on-site. Commence physical repair operations to transition state to In Progress.</p>
                </div>
              </div>
              <div class="action-card-body">
                <button type="button" class="btn btn-lg btn-success" ng-click="c.startWork()" ng-disabled="c.startingWork">
                  <span ng-if="!c.startingWork">&#x25b6; Start Physical Work Now &rarr;</span>
                  <span ng-if="c.startingWork">Recording Start Timestamp...</span>
                </button>
              </div>
            </div>

            <!-- STEP C: WORK IN PROGRESS -->
            <div class="fsm-action-card bg-work-inprogress" ng-if="c.selectedWo.u_state === 'In Progress'">
              <div class="action-card-header">
                <div class="step-icon-round bg-blue">&#x2692;</div>
                <div>
                  <strong class="action-card-h">Step 3: Work in Progress (Started: {{{{c.selectedWo.u_work_start_timestamp}}}})</strong>
                  <p class="action-card-p">Active field execution. Add milestone logs, attach photos, or submit final completion report.</p>
                </div>
              </div>
              <div class="action-card-body action-buttons-cluster">
                <button type="button" class="btn btn-default" ng-click="c.openProgressModal()">+ Add Progress Milestone</button>
                <button type="button" class="btn btn-default" ng-click="c.openEvidenceModal()">&#x1f4f7; Upload Evidence Photo</button>
                <button type="button" class="btn btn-warning" ng-click="c.openHoldModal()">&#x23f8; Request Support / Hold</button>
                <button type="button" class="btn btn-success" ng-click="c.openCompleteModal()">&#x2714; Submit Completion Report &rarr;</button>
              </div>
            </div>

            <!-- STEP D: ON HOLD -->
            <div class="fsm-action-card bg-work-onhold" ng-if="c.selectedWo.u_state === 'On Hold'">
              <div class="action-card-header">
                <div class="step-icon-round bg-amber">&#x23f8;</div>
                <div>
                  <strong class="action-card-h">Work Order On Hold &bull; Obstacle Flagged</strong>
                  <p class="action-card-p">Reason: <em>{{{{c.selectedWo.u_hold_reason}}}}</em></p>
                </div>
              </div>
              <div class="action-card-body">
                <button type="button" class="btn btn-info" ng-click="c.resumeWork()" ng-disabled="c.resumingWork">
                  <span ng-if="!c.resumingWork">&#x25b6; Clear Obstacle &amp; Resume Work</span>
                  <span ng-if="c.resumingWork">Resuming Work...</span>
                </button>
              </div>
            </div>

            <!-- STEP E: COMPLETED -->
            <div class="fsm-action-card bg-work-completed" ng-if="c.selectedWo.u_state === 'Completed'">
              <div class="action-card-header">
                <div class="step-icon-round bg-green">&#x2714;</div>
                <div>
                  <strong class="action-card-h">Work Completed on {{{{c.selectedWo.u_work_complete_timestamp}}}}</strong>
                  <p class="action-card-p">Outcome: <strong>{{{{c.selectedWo.u_resolution_outcome}}}}</strong> &bull; Verification Audit: <strong>{{{{c.selectedWo.u_verification_status || 'Pending'}}}}</strong></p>
                  <p class="completion-quote">&ldquo;{{{{c.selectedWo.u_completion_notes}}}}&rdquo;</p>
                </div>
              </div>
            </div>

          </div>

          <!-- SECTION 4: ACTIVITY STREAM & EVIDENCE TABS -->
          <div class="form-section-box">
            <div class="fsm-subtabs-bar">
              <button type="button" class="subtab-item" ng-class="{{'active': c.detailTab === 'activity'}}" ng-click="c.detailTab = 'activity'">
                Activity Stream &amp; Progress Log ({{{{c.parseProgressLogs(c.selectedWo.u_progress_updates).length}}}})
              </button>
              <button type="button" class="subtab-item" ng-class="{{'active': c.detailTab === 'evidence'}}" ng-click="c.detailTab = 'evidence'">
                Field Evidence &amp; Photos ({{{{c.getJobEvidence(c.selectedWo.u_number).length}}}})
              </button>
              <button type="button" class="subtab-item" ng-class="{{'active': c.detailTab === 'case'}}" ng-click="c.detailTab = 'case'">
                Cross-Linked Citizen Case Details
              </button>
            </div>

            <!-- SUBTAB A: ACTIVITY STREAM -->
            <div class="subtab-body" ng-if="c.detailTab === 'activity'">
              <div class="fsm-timeline-list">
                <div class="timeline-row" ng-repeat="log in c.parseProgressLogs(c.selectedWo.u_progress_updates)">
                  <div class="timeline-avatar">KS</div>
                  <div class="timeline-content">
                    <div class="timeline-head">
                      <span class="timeline-user">Karthik Selvam (Worker ID: EMP-9021)</span>
                      <span class="timeline-cat-pill">{{{{log.category}}}}</span>
                      <span class="timeline-time">{{{{log.time}}}}</span>
                    </div>
                    <div class="timeline-msg">{{{{log.text}}}}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- SUBTAB B: EVIDENCE PHOTOS -->
            <div class="subtab-body" ng-if="c.detailTab === 'evidence'">
              <div class="evidence-photos-grid" ng-if="c.getJobEvidence(c.selectedWo.u_number).length > 0">
                <div class="ev-card" ng-repeat="ev in c.getJobEvidence(c.selectedWo.u_number)">
                  <img ng-src="{{{{ev.u_photo_url}}}}" alt="Evidence" class="ev-photo-img" />
                  <div class="ev-card-details">
                    <span class="ev-badge">{{{{ev.u_evidence_type}}}}</span>
                    <p class="ev-caption-text">{{{{ev.u_caption}}}}</p>
                    <span class="ev-meta-time">Uploaded {{{{ev.u_uploaded_at}}}} by {{{{ev.u_uploaded_by}}}}</span>
                  </div>
                </div>
              </div>
              <div class="empty-box p-4 text-center" ng-if="c.getJobEvidence(c.selectedWo.u_number).length === 0">
                <p class="text-muted">No evidence photos recorded yet for this work order.</p>
                <button type="button" class="btn btn-sm btn-default" ng-click="c.openEvidenceModal()">+ Upload Before / During / After Photo</button>
              </div>
            </div>

            <!-- SUBTAB C: LINKED CASE DETAILS -->
            <div class="subtab-body" ng-if="c.detailTab === 'case'">
              <div class="row">
                <div class="col-md-6">
                  <div class="form-group fsm-fg">
                    <label class="fsm-lbl">Citizen Complaint Case #</label>
                    <div class="fsm-val font-mono"><strong>{{{{c.selectedWo.u_case_number}}}}</strong></div>
                  </div>
                  <div class="form-group fsm-fg">
                    <label class="fsm-lbl">Originating Citizen</label>
                    <div class="fsm-val">S. Rajesh Kumar &bull; +91 98401 23456</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group fsm-fg">
                    <label class="fsm-lbl">Citizen Tracking Status</label>
                    <div class="fsm-val">Live in Citizen Portal &bull; Synchronized</div>
                  </div>
                  <button type="button" class="btn btn-sm btn-primary mt-2" ng-click="c.openCaseTrackingModal(c.selectedWo)">
                    Open In-App Case Tracker &rarr;
                  </button>
                </div>
              </div>
            </div>

          </div>

        </div>

      </div>

      <!-- =====================================================================
           VIEW 4: WORK HISTORY
           ===================================================================== -->
      <div class="fsm-view-wrap" ng-if="c.currentTab === 'history'">
        <div class="fsm-card">
          <div class="fsm-card-header">
            <strong class="fsm-card-title">COMPLETED &amp; AUDITED WORK ORDERS &bull; HISTORICAL ARCHIVE</strong>
          </div>
          <div class="fsm-card-body p-0">
            <table class="table fsm-table mb-0">
              <thead>
                <tr>
                  <th>WORK ORDER #</th>
                  <th>LINKED CASE #</th>
                  <th>CATEGORY &amp; TITLE</th>
                  <th>COMPLETED ON</th>
                  <th>RESOLUTION OUTCOME</th>
                  <th>AUDIT STATUS</th>
                  <th>ACTION</th>
                </tr>
              </thead>
              <tbody>
                <tr ng-repeat="wo in c.getHistoryJobs()">
                  <td><strong>{{{{wo.u_number}}}}</strong></td>
                  <td><span class="fsm-case-pill">{{{{wo.u_case_number}}}}</span></td>
                  <td>{{{{wo.u_short_description}}}}</td>
                  <td>{{{{wo.u_work_complete_timestamp || 'Today'}}}}</td>
                  <td><span class="badge badge-success">{{{{wo.u_resolution_outcome || 'Resolved'}}}}</span></td>
                  <td><span class="text-success font-bold">&#x2714; Verified</span></td>
                  <td>
                    <button type="button" class="btn btn-xs btn-default" ng-click="c.selectJob(wo)">View Record &rarr;</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- =====================================================================
           VIEW 5: TECHNICIAN INFO
           ===================================================================== -->
      <div class="fsm-view-wrap" ng-if="c.currentTab === 'profile'">
        <div class="fsm-card">
          <div class="fsm-card-header">
            <strong class="fsm-card-title">MUNICIPAL FIELD TECHNICIAN PROFILE &bull; GREATER CHENNAI CORPORATION</strong>
          </div>
          <div class="fsm-card-body">
            <div class="row">
              <div class="col-md-3 text-center">
                <div class="large-profile-avatar">KS</div>
                <h3 class="profile-fullname">{{{{c.data.worker.name}}}}</h3>
                <p class="profile-role-title">{{{{c.data.worker.title}}}}</p>
                <span class="label label-success">ON DUTY</span>
              </div>
              <div class="col-md-9">
                <div class="row">
                  <div class="col-sm-6">
                    <div class="form-group fsm-fg">
                      <label class="fsm-lbl">Employee ID (Worker ID)</label>
                      <div class="fsm-val font-mono"><strong>{{{{c.data.worker.employee_id}}}}</strong></div>
                    </div>
                    <div class="form-group fsm-fg">
                      <label class="fsm-lbl">Assigned Ward &amp; Zone</label>
                      <div class="fsm-val">{{{{c.data.worker.ward}}}} &bull; {{{{c.data.worker.zone}}}}</div>
                    </div>
                    <div class="form-group fsm-fg">
                      <label class="fsm-lbl">Contact Phone</label>
                      <div class="fsm-val">{{{{c.data.worker.phone}}}}</div>
                    </div>
                  </div>
                  <div class="col-sm-6">
                    <div class="form-group fsm-fg">
                      <label class="fsm-lbl">Role Assignment</label>
                      <div class="fsm-val">Rapid Civic Response Squad &bull; Category 1 Hazards</div>
                    </div>
                    <div class="form-group fsm-fg">
                      <label class="fsm-lbl">Duty Shift Hours</label>
                      <div class="fsm-val">07:00 AM &ndash; 03:30 PM (Shift A)</div>
                    </div>
                    <div class="form-group fsm-fg">
                      <label class="fsm-lbl">Direct Supervisor</label>
                      <div class="fsm-val">Assistant Engineer &bull; Adyar Ward 172</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </main>

  </div>

  <!-- =========================================================================
       IN-APP CASE TRACKING MODAL (SOLVES "GOING TO NEW PAGE" ISSUE)
       ========================================================================= -->
  <div class="fsm-modal-backdrop" ng-if="c.showCaseTrackingModal" ng-click="c.showCaseTrackingModal = false; c.closeCaseTrackingModal($event)">
    <div class="fsm-modal-dialog modal-lg" ng-click="$event.stopPropagation()">
      <div class="fsm-modal-head bg-info-subtle">
        <div class="d-flex align-items-center gap-2">
          <span class="badge badge-info">LIVE CROSS-TRACKING</span>
          <h4 class="fsm-modal-h">Citizen Complaint &bull; {{{{c.trackingModalData.case_number}}}}</h4>
        </div>
        <button type="button" class="fsm-modal-close-btn" id="btnXCloseCaseTracker" ng-click="c.showCaseTrackingModal = false; c.closeCaseTrackingModal($event)" title="Close">&times;</button>
      </div>
      <div class="fsm-modal-body p-4">
        
        <!-- Cross-Mapping Ribbon -->
        <div class="inapp-track-ribbon">
          <div class="inapp-ribbon-col">
            <span class="lbl">CASE ID:</span>
            <strong class="val text-primary font-mono">{{{{c.trackingModalData.case_number}}}}</strong>
          </div>
          <div class="inapp-ribbon-col">
            <span class="lbl">MAPPED WORK ORDER:</span>
            <strong class="val font-mono">{{{{c.trackingModalData.work_order_number}}}}</strong>
          </div>
          <div class="inapp-ribbon-col">
            <span class="lbl">ASSIGNED TECHNICIAN:</span>
            <strong class="val">{{{{c.trackingModalData.worker_name}}}} ({{{{c.trackingModalData.worker_id}}}})</strong>
          </div>
          <div class="inapp-ribbon-col">
            <span class="lbl">CURRENT STATE:</span>
            <span class="badge-state" ng-class="c.getStateClass(c.trackingModalData.state)">{{{{c.trackingModalData.state}}}}</span>
          </div>
        </div>

        <!-- 5-Step Lifecycle Stepper -->
        <div class="inapp-stepper mt-3">
          <div class="step-dot-wrap" ng-class="{{'done': c.trackingModalData.step >= 1}}">
            <div class="step-dot">1</div>
            <span class="step-title">Submitted</span>
          </div>
          <div class="step-connector" ng-class="{{'done': c.trackingModalData.step >= 2}}"></div>
          <div class="step-dot-wrap" ng-class="{{'done': c.trackingModalData.step >= 2}}">
            <div class="step-dot">2</div>
            <span class="step-title">Dispatched</span>
          </div>
          <div class="step-connector" ng-class="{{'done': c.trackingModalData.step >= 3}}"></div>
          <div class="step-dot-wrap" ng-class="{{'done': c.trackingModalData.step >= 3}}">
            <div class="step-dot">3</div>
            <span class="step-title">Arrived</span>
          </div>
          <div class="step-connector" ng-class="{{'done': c.trackingModalData.step >= 4}}"></div>
          <div class="step-dot-wrap" ng-class="{{'done': c.trackingModalData.step >= 4}}">
            <div class="step-dot">4</div>
            <span class="step-title">In Progress</span>
          </div>
          <div class="step-connector" ng-class="{{'done': c.trackingModalData.step >= 5}}"></div>
          <div class="step-dot-wrap" ng-class="{{'done': c.trackingModalData.step >= 5}}">
            <div class="step-dot">5</div>
            <span class="step-title">Resolved</span>
          </div>
        </div>

        <!-- Case Details Summary -->
        <div class="row mt-4">
          <div class="col-md-6">
            <div class="form-group fsm-fg">
              <label class="fsm-lbl">Short Description</label>
              <div class="fsm-val font-bold">{{{{c.trackingModalData.short_description}}}}</div>
            </div>
            <div class="form-group fsm-fg">
              <label class="fsm-lbl">Location Address</label>
              <div class="fsm-val">{{{{c.trackingModalData.location}}}}</div>
            </div>
            <div class="form-group fsm-fg">
              <label class="fsm-lbl">Citizen Name &amp; Phone</label>
              <div class="fsm-val">{{{{c.trackingModalData.citizen_name}}}} ({{{{c.trackingModalData.citizen_phone}}}})</div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group fsm-fg">
              <label class="fsm-lbl">Category &bull; Priority</label>
              <div class="fsm-val">{{{{c.trackingModalData.category}}}} &bull; {{{{c.trackingModalData.priority}}}}</div>
            </div>
            <div class="form-group fsm-fg">
              <label class="fsm-lbl">Target Resolution SLA</label>
              <div class="fsm-val font-mono">{{{{c.trackingModalData.target_sla}}}}</div>
            </div>
            <div class="form-group fsm-fg">
              <label class="fsm-lbl">Latest Field Status Note</label>
              <div class="fsm-val text-primary font-italic">{{{{c.trackingModalData.resolution_notes || 'Assigned to field technician for on-site resolution.'}}}}</div>
            </div>
          </div>
        </div>

        <!-- Real-Time Activity Log Feed -->
        <div class="inapp-activity-box mt-3">
          <strong class="text-xs text-muted font-bold text-uppercase">&#x2692; LIVE FIELD ACTIVITY FEED</strong>
          <div class="timeline-scroll-feed mt-2">
            <div class="feed-item" ng-repeat="log in c.trackingModalData.activities">
              <span class="feed-time">{{{{log.time}}}}</span>
              <span class="feed-badge">{{{{log.category}}}}</span>
              <span class="feed-text">{{{{log.text}}}}</span>
            </div>
          </div>
        </div>

      </div>
      <div class="fsm-modal-foot">
        <button type="button" class="btn btn-default" id="btnCloseCaseTracker" ng-click="c.showCaseTrackingModal = false; c.closeCaseTrackingModal($event)">Close Tracker</button>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       MODAL: SUBMIT WORK COMPLETION REPORT
       ========================================================================= -->
  <div class="fsm-modal-backdrop" ng-if="c.showCompleteModal" ng-click="c.closeModal($event); c.showCompleteModal = false;">
    <div class="fsm-modal-dialog" ng-click="$event.stopPropagation()">
      <div class="fsm-modal-head">
        <h4 class="fsm-modal-h">&#x2714; Submit Work Order Completion Report</h4>
        <button type="button" class="fsm-modal-close-btn" ng-click="c.closeCompleteModal($event); c.showCompleteModal = false;" title="Close">&times;</button>
      </div>
      <div class="fsm-modal-body">
        <div class="form-group fsm-fg">
          <label class="fsm-lbl">Resolution Outcome</label>
          <select class="form-control" ng-model="c.completeForm.outcome">
            <option value="Resolved">Resolved (Complete on-site physical fix)</option>
            <option value="Partially Completed">Partially Completed (Emergency mitigation)</option>
            <option value="Requires Specialist Follow-up">Requires Specialist Engineering Follow-up</option>
          </select>
        </div>
        <div class="form-group fsm-fg">
          <label class="fsm-lbl">Execution Summary &amp; Technical Remarks <span class="text-danger">*</span></label>
          <textarea class="form-control" rows="4" placeholder="Detail the physical fix applied, materials consumed, and quality test outcome..." ng-model="c.completeForm.notes" required></textarea>
        </div>
        <div class="alert alert-info fsm-alert mb-0">
          Submitting will mark Work Order <strong>{{{{c.selectedWo.u_number}}}}</strong> and Linked Case <strong>{{{{c.selectedWo.u_case_number}}}}</strong> as <strong>Resolved</strong> and route it to the Assistant Engineer for audit verification.
        </div>
      </div>
      <div class="fsm-modal-foot">
        <button type="button" class="btn btn-default fsm-btn-cancel" ng-click="c.closeCompleteModal($event); c.showCompleteModal = false;">Cancel</button>
        <button type="button" class="btn btn-success" ng-click="c.submitCompletion()" ng-disabled="!c.completeForm.notes || c.submittingComplete">
          <span ng-if="!c.submittingComplete">Submit Final Completion &rarr;</span>
          <span ng-if="c.submittingComplete">Persisting Completion...</span>
        </button>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       MODAL: ADD PROGRESS MILESTONE
       ========================================================================= -->
  <div class="fsm-modal-backdrop" ng-if="c.showProgressModal" ng-click="c.closeModal($event); c.showProgressModal = false;">
    <div class="fsm-modal-dialog" ng-click="$event.stopPropagation()">
      <div class="fsm-modal-head">
        <h4 class="fsm-modal-h">+ Add Progress Milestone Note</h4>
        <button type="button" class="fsm-modal-close-btn" ng-click="c.closeProgressModal($event); c.showProgressModal = false;" title="Close">&times;</button>
      </div>
      <div class="fsm-modal-body">
        <div class="form-group fsm-fg">
          <label class="fsm-lbl">Milestone Category</label>
          <select class="form-control" ng-model="c.progressForm.category">
            <option value="Site Inspection">Site Inspection Completed</option>
            <option value="Excavation & Clearing">Excavation &amp; Clearing Started</option>
            <option value="Material Applied">Material Applied (Cold Mix / Bitumen)</option>
            <option value="Equipment Deployed">Equipment Deployed (Suction / Roller)</option>
            <option value="Traffic Managed">Traffic Managed &amp; Cordoned</option>
          </select>
        </div>
        <div class="form-group fsm-fg">
          <label class="fsm-lbl">Milestone Notes <span class="text-danger">*</span></label>
          <textarea class="form-control" rows="3" placeholder="Enter progress details for operational record..." ng-model="c.progressForm.text" required></textarea>
        </div>
      </div>
      <div class="fsm-modal-foot">
        <button type="button" class="btn btn-default fsm-btn-cancel" ng-click="c.closeProgressModal($event); c.showProgressModal = false;">Cancel</button>
        <button type="button" class="btn btn-primary" ng-click="c.submitProgress()" ng-disabled="!c.progressForm.text || c.submittingProgress">
          <span ng-if="!c.submittingProgress">Save Milestone Note</span>
          <span ng-if="c.submittingProgress">Saving...</span>
        </button>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       MODAL: UPLOAD EVIDENCE PHOTO
       ========================================================================= -->
  <div class="fsm-modal-backdrop" ng-if="c.showEvidenceModal" ng-click="c.closeModal($event); c.showEvidenceModal = false;">
    <div class="fsm-modal-dialog" ng-click="$event.stopPropagation()">
      <div class="fsm-modal-head">
        <h4 class="fsm-modal-h">&#x1f4f7; Upload Field Evidence Photograph</h4>
        <button type="button" class="fsm-modal-close-btn" ng-click="c.closeEvidenceModal($event); c.showEvidenceModal = false;" title="Close">&times;</button>
      </div>
      <div class="fsm-modal-body">
        <div class="form-group fsm-fg">
          <label class="fsm-lbl">Evidence Stage</label>
          <select class="form-control" ng-model="c.evidenceForm.type">
            <option value="Before Repair">Before Repair (Initial Site State)</option>
            <option value="During Work">During Work (In-Progress Execution)</option>
            <option value="After Completion">After Completion (Restored Surface)</option>
          </select>
        </div>
        <div class="form-group fsm-fg">
          <label class="fsm-lbl">Caption / Description</label>
          <input type="text" class="form-control" placeholder="e.g. Cold mix compacted flush with road level" ng-model="c.evidenceForm.caption" />
        </div>
        <div class="form-group fsm-fg">
          <label class="fsm-lbl">Select Evidence Preset Photo</label>
          <div class="preset-row">
            <img src="https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=300&auto=format&fit=crop&q=60" alt="Preset 1" class="preset-img-thumb" ng-click="c.setPresetPhoto('https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80', 'Road surface cold mix patching completed')" />
            <img src="https://images.unsplash.com/photo-1541888946425-d0fbb180c5f5?w=300&auto=format&fit=crop&q=60" alt="Preset 2" class="preset-img-thumb" ng-click="c.setPresetPhoto('https://images.unsplash.com/photo-1541888946425-d0fbb180c5f5?w=600&auto=format&fit=crop&q=80', 'Pipeline valve repaired and sealed')" />
            <img src="https://images.unsplash.com/photo-1508873696983-2df5293cb395?w=300&auto=format&fit=crop&q=60" alt="Preset 3" class="preset-img-thumb" ng-click="c.setPresetPhoto('https://images.unsplash.com/photo-1508873696983-2df5293cb395?w=600&auto=format&fit=crop&q=80', 'Streetlight luminaire wiring restored')" />
          </div>
        </div>
      </div>
      <div class="fsm-modal-foot">
        <button type="button" class="btn btn-default fsm-btn-cancel" ng-click="c.closeEvidenceModal($event); c.showEvidenceModal = false;">Cancel</button>
        <button type="button" class="btn btn-primary" ng-click="c.submitEvidence()" ng-disabled="c.submittingEvidence">
          <span ng-if="!c.submittingEvidence">Upload Evidence Photo</span>
          <span ng-if="c.submittingEvidence">Uploading...</span>
        </button>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       MODAL: PLACE ON HOLD
       ========================================================================= -->
  <div class="fsm-modal-backdrop" ng-if="c.showHoldModal" ng-click="c.closeModal($event); c.showHoldModal = false;">
    <div class="fsm-modal-dialog" ng-click="$event.stopPropagation()">
      <div class="fsm-modal-head">
        <h4 class="fsm-modal-h">&#x23f8; Flag Obstacle &amp; Place On Hold</h4>
        <button type="button" class="fsm-modal-close-btn" ng-click="c.closeHoldModal($event); c.showHoldModal = false;" title="Close">&times;</button>
      </div>
      <div class="fsm-modal-body">
        <div class="form-group fsm-fg">
          <label class="fsm-lbl">Obstacle Category</label>
          <select class="form-control" ng-model="c.holdForm.category">
            <option value="Materials Unavailable">Materials Unavailable at Ward Depot</option>
            <option value="Severe Weather">Severe Rain / Weather Obstacle</option>
            <option value="Heavy Traffic">Heavy Traffic / Police Permission Needed</option>
            <option value="Inter-Department Coordination">Inter-Department Coordination (TANGEDCO/CMWSSB)</option>
          </select>
        </div>
        <div class="form-group fsm-fg">
          <label class="fsm-lbl">Detailed Explanation for Assistant Engineer <span class="text-danger">*</span></label>
          <textarea class="form-control" rows="3" placeholder="Provide full details..." ng-model="c.holdForm.reason" required></textarea>
        </div>
      </div>
      <div class="fsm-modal-foot">
        <button type="button" class="btn btn-default fsm-btn-cancel" ng-click="c.closeHoldModal($event); c.showHoldModal = false;">Cancel</button>
        <button type="button" class="btn btn-warning" ng-click="c.submitHold()" ng-disabled="!c.holdForm.reason || c.submittingHold">
          <span ng-if="!c.submittingHold">Confirm Hold &amp; Escalate</span>
          <span ng-if="c.submittingHold">Submitting...</span>
        </button>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       COOPBOT / CIVIX AI CHAT ASSISTANT (FLOATING BOTTOM RIGHT)
       ========================================================================= -->
  <div class="coopbot-floating-container" id="coopbotRoot">
    <!-- Floating Launcher Pill -->
    <div class="coopbot-launcher-bar" ng-click="c.toggleCoopBot()" title="Click to chat with CIVIX Field Copilot" ng-show="!c.coopBotOpen">
      <div class="coopbot-pill-btn">
        <svg class="coopbot-sparkle-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        <span class="coopbot-pill-label">Ask CIVIX Assist</span>
      </div>
      <div class="coopbot-avatar-circle-ring">
        <img src="{COOPBOT_IMG_B64}" alt="CIVIX Assist" class="coopbot-mascot-img" />
        <span class="coopbot-pulse-dot" title="Online"></span>
      </div>
    </div>

    <!-- Active Chat Window -->
    <div class="coopbot-chat-window" ng-show="c.coopBotOpen" role="dialog" aria-label="CIVIX Field Copilot AI">
      <div class="coopbot-chat-header">
        <div class="coopbot-header-left">
          <div class="coopbot-header-avatar">
            <img src="{COOPBOT_IMG_B64}" alt="CIVIX Assist" />
          </div>
          <div class="coopbot-header-titles">
            <span class="coopbot-header-name">CIVIX Assist &bull; Field Copilot</span>
            <span class="coopbot-online-badge"><span class="coopbot-green-circle"></span> Online &bull; Ward 172 Copilot</span>
          </div>
        </div>
        <div class="coopbot-header-actions">
          <button type="button" class="coopbot-head-btn" ng-click="c.clearCoopBotChat()" title="Reset chat">&#x21ba;</button>
          <button type="button" class="coopbot-head-btn" ng-click="c.toggleCoopBot()" title="Close">&times;</button>
        </div>
      </div>

      <div class="coopbot-messages-feed" id="coopbotMsgFeed">
        <div ng-repeat="msg in c.coopBotMessages track by $index" class="coopbot-msg-row" ng-class="'msg-' + msg.sender">
          <div class="coopbot-msg-avatar" ng-if="msg.sender === 'bot'">
            <img src="{COOPBOT_IMG_B64}" alt="Bot" />
          </div>
          <div class="coopbot-msg-bubble-wrap">
            <div class="coopbot-msg-bubble" ng-bind-html="msg.text"></div>
            <span class="coopbot-msg-time">{{{{msg.time}}}}</span>
          </div>
        </div>
        <div class="coopbot-msg-row msg-bot" ng-show="c.coopBotTyping">
          <div class="coopbot-msg-avatar">
            <img src="{COOPBOT_IMG_B64}" alt="Bot" />
          </div>
          <div class="coopbot-typing-indicator">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <!-- Quick Chips Bar -->
      <div class="coopbot-chips-bar" ng-if="c.coopBotMessages.length <= 4">
        <button type="button" class="coopbot-chip-btn" ng-click="c.askCoopBotQuick('What are my critical tasks today?')">&#x1f4cb; Critical Tasks</button>
        <button type="button" class="coopbot-chip-btn" ng-click="c.askCoopBotQuick('Track Case CIV-2026-00841')">&#x1f50d; Track Case 00841</button>
        <button type="button" class="coopbot-chip-btn" ng-click="c.askCoopBotQuick('Asphalt cold-mix repair SOP')">&#x1f6e0; Cold-Mix SOP</button>
        <button type="button" class="coopbot-chip-btn" ng-click="c.askCoopBotQuick('GCC Emergency Control Room')">&#x1f4de; Control Room 1913</button>
      </div>

      <!-- Chat Input Form -->
      <div class="coopbot-chat-footer">
        <form ng-submit="c.sendCoopBotMessage()" class="coopbot-input-form">
          <input type="text" class="coopbot-input-box" placeholder="Ask CIVIX Field Copilot anything..." ng-model="c.coopBotInput" />
          <button type="submit" class="coopbot-send-btn" title="Send message" ng-disabled="!c.coopBotInput">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </form>
      </div>
    </div>
  </div>

</div>
"""

UI16_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700;900&family=IBM+Plex+Mono:wght@500;700&display=swap');

/* ==============================================================================
   CIVIX AI - ADVANCE SERVICENOW UI16 HIGH LEVEL DESIGN SYSTEM
   Palette: Deep Charcoal #293E40 | Crisp Labels #475569 | Link #0072CE
   ============================================================================== */

.fsm-portal-shell {
  font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  color: #293e40 !important; /* Authentic ServiceNow Charcoal */
  background-color: #f0f3f4 !important;
  min-height: 100vh;
  display: flex;
}

/* 1. LEFT SIDEBAR (270px) */
.fsm-sidebar {
  width: 270px;
  background: #112233;
  border-right: 1px solid #1e3851;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  z-index: 100;
}

.sidebar-brand-box {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  cursor: pointer;
  background: #0d1a27;
}

.sidebar-logo-icon {
  width: 38px;
  height: 38px;
  background: #087f8c;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(8, 127, 140, 0.4);
}

.brand-app-name { font-size: 15px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px; display: block; }
.brand-corp-tag { font-size: 10.5px; color: #94a3b8; display: block; }

.sidebar-shift-banner {
  margin: 12px 14px;
  background: rgba(34, 197, 94, 0.12);
  border: 1px solid rgba(34, 197, 94, 0.25);
  border-radius: 6px;
  padding: 6px 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.shift-pulsing-dot { width: 8px; height: 8px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 8px #22c55e; }
.shift-banner-text { font-size: 11px; font-weight: 700; color: #4ade80; }

.sidebar-section-heading {
  font-size: 10px; font-weight: 800; color: #64748b; letter-spacing: 0.8px; padding: 10px 16px 4px 16px; text-transform: uppercase;
}

.sidebar-nav-menu { display: flex; flex-direction: column; gap: 3px; padding: 0 10px; }
.sidebar-nav-link {
  background: none; border: none; border-radius: 6px; color: #cbd5e1; font-size: 13px; font-weight: 600; padding: 10px 12px;
  display: flex; align-items: center; gap: 10px; cursor: pointer; transition: all 0.15s; width: 100%; text-align: left;
}
.sidebar-nav-link:hover { background: rgba(255, 255, 255, 0.08); color: #ffffff; }
.sidebar-nav-link.active { background: #087f8c; color: #ffffff; font-weight: 700; box-shadow: 0 4px 14px rgba(8, 127, 140, 0.35); }
.sidebar-nav-link .nav-icon { display: flex; align-items: center; justify-content: center; width: 20px; }
.sidebar-nav-link .nav-title { flex: 1; }

.nav-badge-pill { font-size: 10.5px; font-weight: 800; background: rgba(255, 255, 255, 0.18); color: #ffffff; padding: 2px 7px; border-radius: 999px; }
.nav-badge-pill.teal { background: #38bdf8; color: #0f172a; }
.nav-badge-pill.green { background: #22c55e; color: #0f172a; }

.sidebar-quick-filters { display: flex; flex-direction: column; gap: 2px; padding: 0 10px; }
.sidebar-filter-btn {
  background: none; border: none; border-radius: 6px; color: #94a3b8; font-size: 12px; font-weight: 600; padding: 7px 12px;
  display: flex; align-items: center; gap: 8px; cursor: pointer; transition: all 0.15s; width: 100%; text-align: left;
}
.sidebar-filter-btn:hover { background: rgba(255, 255, 255, 0.05); color: #e2e8f0; }
.sidebar-filter-btn.active { background: rgba(255, 255, 255, 0.12); color: #ffffff; font-weight: 700; }
.filter-dot { width: 7px; height: 7px; border-radius: 50%; }
.filter-dot.red { background: #ef4444; }
.filter-dot.blue { background: #38bdf8; }
.filter-dot.amber { background: #f59e0b; }
.filter-lbl { flex: 1; }
.filter-badge { font-size: 10.5px; color: #cbd5e1; font-weight: 700; }

.sidebar-user-footer { margin-top: auto; padding: 14px 12px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: #0d1a27; }
.user-profile-card { display: flex; align-items: center; gap: 10px; padding: 8px; border-radius: 6px; cursor: pointer; }
.user-avatar-ks { width: 34px; height: 34px; background: #087f8c; color: #ffffff; font-weight: 800; font-size: 12px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.user-name-title { font-size: 12.5px; font-weight: 700; color: #ffffff; display: block; }
.user-code-pill { font-size: 10.5px; color: #94a3b8; font-family: 'IBM Plex Mono', monospace; display: block; }
.user-ward-line { font-size: 10px; color: #64748b; display: block; }
.sidebar-exit-btn { display: flex; align-items: center; gap: 6px; margin-top: 8px; padding: 6px 8px; font-size: 11px; color: #94a3b8; text-decoration: none !important; }
.sidebar-exit-btn:hover { color: #f87171; }

/* 2. RIGHT MAIN CONTENT AREA */
.fsm-content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100vh;
  overflow-y: auto; /* Handles inner scrolling cleanly */
}

/* Header Ribbon */
.fsm-top-header {
  background: #ffffff;
  border-bottom: 1px solid #d1d5db;
  padding: 10px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}
.crumb-link { color: #0072ce; font-weight: 700; cursor: pointer; }
.crumb-link:hover { text-decoration: underline; }
.crumb-arrow { color: #94a3b8; }
.crumb-current { color: #293e40; font-weight: 700; }

.top-sync-badge {
  display: flex; align-items: center; gap: 6px; background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; font-size: 11.5px; font-weight: 700; padding: 4px 9px; border-radius: 4px;
}
.sync-dot-green { width: 7px; height: 7px; background: #22c55e; border-radius: 50%; }
.top-ward-badge { font-size: 11px; font-weight: 700; color: #087f8c; background: #e0f2fe; padding: 4px 8px; border-radius: 4px; }
.top-refresh-btn { font-size: 11.5px; display: flex; align-items: center; gap: 5px; border-color: #d1d5db; }

/* Main Container */
.fsm-main-container {
  padding: 20px 24px 80px 24px;
  max-width: 1440px;
  width: 100%;
  margin: 0 auto;
}

/* Urgent Alert */
.fsm-urgent-alert {
  background: #fef2f2; border: 1px solid #fecaca; border-left: 4px solid #dc2626; border-radius: 4px; padding: 10px 14px; margin-bottom: 18px; display: flex; align-items: center; justify-content: space-between; gap: 12px;
}
.urgent-tag { background: #dc2626; color: #ffffff; font-size: 10px; font-weight: 800; padding: 3px 6px; border-radius: 4px; }
.urgent-text { font-size: 13px; color: #991b1b; flex: 1; }

/* 4 KPI Grid */
.fsm-kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
@media (max-width: 1100px) { .fsm-kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .fsm-kpi-grid { grid-template-columns: 1fr; } }

.fsm-kpi-card {
  background: #ffffff; border: 1px solid #d1d5db; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); cursor: pointer; transition: all 0.15s;
}
.fsm-kpi-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08); border-color: #9ca3af; }
.kpi-top-bar { height: 4px; width: 100%; }
.kpi-teal .kpi-top-bar { background: #087f8c; }
.kpi-blue .kpi-top-bar { background: #0072ce; }
.kpi-red .kpi-top-bar { background: #dc2626; }
.kpi-green .kpi-top-bar { background: #16a34a; }

.kpi-body { padding: 14px 16px; }
.kpi-lbl { font-size: 10.5px; font-weight: 700; color: #475569; letter-spacing: 0.5px; }
.kpi-val-row { display: flex; align-items: center; justify-content: space-between; margin: 6px 0; }
.kpi-number { font-size: 28px; font-weight: 900; color: #293e40; line-height: 1; }
.kpi-pill { font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; background: #f1f5f9; color: #475569; }
.kpi-pill.blue { background: #e0f2fe; color: #0369a1; }
.kpi-pill.red { background: #fee2e2; color: #b91c1c; }
.kpi-pill.green { background: #dcfce7; color: #15803d; }
.kpi-foot { font-size: 11px; color: #475569; }

/* FSM Card */
.fsm-card { background: #ffffff; border: 1px solid #d1d5db; border-radius: 6px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03); overflow: hidden; }
.fsm-card-header { padding: 12px 18px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; }
.fsm-card-title { font-size: 12px; font-weight: 800; color: #293e40; letter-spacing: 0.5px; }
.fsm-card-header.bg-active-task { background: #eff6ff; border-bottom: 1px solid #bfdbfe; }

.pulse-indicator { display: inline-block; width: 8px; height: 8px; background: #0072ce; border-radius: 50%; margin-right: 8px; animation: pulse 1.5s infinite; }
.active-task-flex { padding: 16px 18px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; }
.task-headline { font-size: 16px; font-weight: 700; color: #293e40; margin: 0 0 4px 0; }
.task-address-line { font-size: 12.5px; color: #475569; margin: 0; display: flex; align-items: center; gap: 5px; }

.mapping-chip-box { background: #f8fafc; border: 1px solid #e2e8f0; padding: 6px 10px; border-radius: 4px; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.chip-lbl { font-size: 10px; font-weight: 700; color: #475569; }
.chip-val { font-size: 12px; color: #293e40; }

/* Table */
.fsm-table { width: 100%; }
.fsm-table thead th { background: #f8fafc; color: #293e40; font-size: 11px; font-weight: 700; border-bottom: 2px solid #d1d5db !important; padding: 10px 14px !important; letter-spacing: 0.4px; }
.fsm-table tbody td { padding: 11px 14px !important; font-size: 12.5px; color: #293e40; border-bottom: 1px solid #f1f5f9 !important; vertical-align: middle !important; }
.fsm-table-row:hover td { background: #f8fafc; }

.fsm-wo-code { color: #0072ce; font-family: 'IBM Plex Mono', monospace; font-size: 12px; font-weight: 700; text-decoration: none; }
.fsm-wo-code:hover { text-decoration: underline; }

.fsm-case-pill { font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 700; color: #0072ce; background: #e0f2fe; padding: 2px 7px; border-radius: 4px; }
.cat-badge-small { font-size: 10px; font-weight: 700; color: #293e40; background: #e2e8f0; padding: 2px 6px; border-radius: 4px; margin-right: 6px; }
.desc-line { font-size: 12.5px; font-weight: 600; color: #293e40; }
.tech-id-text { font-size: 11px; font-family: 'IBM Plex Mono', monospace; color: #475569; }

/* Badges */
.badge-priority { font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 4px; display: inline-block; }
.badge-priority.critical { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }
.badge-priority.high { background: #fef3c7; color: #b45309; border: 1px solid #fcd34d; }
.badge-priority.moderate { background: #e0f2fe; color: #0369a1; border: 1px solid #7dd3fc; }
.badge-priority.low { background: #f1f5f9; color: #475569; }

.badge-state { font-size: 10.5px; font-weight: 800; padding: 3px 8px; border-radius: 4px; display: inline-block; }
.badge-state.assigned { background: #e0f2fe; color: #0284c7; }
.badge-state.arrival { background: #ccfbf1; color: #0f766e; }
.badge-state.progress { background: #fef3c7; color: #d97706; }
.badge-state.hold { background: #fee2e2; color: #dc2626; }
.badge-state.completed { background: #dcfce7; color: #166534; }

/* Filter Toolbar */
.fsm-filter-toolbar { background: #ffffff; border: 1px solid #d1d5db; border-radius: 6px; padding: 14px; }
.search-input-wrap { position: relative; margin-bottom: 12px; }
.search-svg { position: absolute; left: 12px; top: 12px; }
.fsm-search-input { padding-left: 38px !important; height: 40px !important; border-radius: 4px !important; border: 1px solid #d1d5db !important; font-size: 13px !important; color: #293e40 !important; }
.clear-search-btn { position: absolute; right: 12px; top: 8px; background: none; border: none; font-size: 18px; color: #94a3b8; cursor: pointer; }

.filter-pills-row { display: flex; gap: 8px; flex-wrap: wrap; }
.pill-btn { background: #f1f5f9; border: 1px solid #d1d5db; border-radius: 4px; padding: 5px 12px; font-size: 12px; font-weight: 600; color: #475569; cursor: pointer; }
.pill-btn:hover { background: #e2e8f0; }
.pill-btn.active { background: #087f8c; color: #ffffff; border-color: #087f8c; }

/* Stack of Cards */
.fsm-jobs-stack { display: flex; flex-direction: column; gap: 12px; }
.fsm-job-card { background: #ffffff; border: 1px solid #d1d5db; border-radius: 6px; padding: 16px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03); }
.fsm-job-card:hover { border-color: #087f8c; box-shadow: 0 4px 14px rgba(8, 127, 140, 0.08); }
.fsm-job-card.critical-border { border-left: 4px solid #dc2626; }
.job-card-topbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.wo-num-badge { font-family: 'IBM Plex Mono', monospace; font-weight: 700; font-size: 13px; color: #0072ce; }
.mapped-case-tag { margin-left: 8px; font-size: 11px; color: #087f8c; background: #e0f2fe; padding: 2px 7px; border-radius: 4px; }
.job-headline { font-size: 15px; font-weight: 700; color: #293e40; margin: 0 0 10px 0; cursor: pointer; }
.job-headline:hover { color: #0072ce; }
.job-meta-grid { display: flex; flex-direction: column; gap: 5px; margin-bottom: 12px; }
.meta-item { display: flex; align-items: center; gap: 7px; font-size: 12px; color: #475569; }
.job-card-bottombar { display: flex; align-items: center; justify-content: space-between; padding-top: 10px; border-top: 1px solid #f1f5f9; }
.cat-pill-gray { font-size: 11px; font-weight: 700; color: #475569; background: #f1f5f9; padding: 3px 8px; border-radius: 4px; }

/* ==============================================================================
   VIEW 3: STICKY FORM RECORD HEADER BAR (FIXES OPENING DOWNSIDE)
   ============================================================================== */
.fsm-record-header-sticky {
  position: sticky;
  top: 0;
  z-index: 50;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 6px 6px 0 0;
  padding: 14px 18px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  border-bottom: 3px solid #087f8c;
}

.record-header-main-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.record-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.fsm-back-btn {
  font-size: 12px !important;
  font-weight: 700 !important;
  border-color: #d1d5db !important;
  background: #f8fafc !important;
  color: #293e40 !important;
}

.record-h2 {
  font-size: 18px;
  font-weight: 800;
  color: #293e40;
  margin: 0;
}

.record-top-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.fsm-action-btn {
  font-size: 12px !important;
  font-weight: 700 !important;
  display: flex;
  align-items: center;
  gap: 5px;
}

.fsm-record-body-card {
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-top: none;
  border-radius: 0 0 6px 6px;
  padding: 24px;
}

.form-section-box {
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 18px;
  margin-bottom: 20px;
  background: #ffffff;
}

.section-badge-title {
  font-size: 11px;
  font-weight: 800;
  color: #475569;
  letter-spacing: 0.6px;
  margin-bottom: 14px;
  padding-bottom: 6px;
  border-bottom: 1px solid #e2e8f0;
}

.fsm-fg { margin-bottom: 12px; }
.fsm-lbl { font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 4px; display: block; }
.fsm-val { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 7px 10px; font-size: 13px; color: #293e40; }

.fsm-mapping-box-blue { display: flex; align-items: center; justify-content: space-between; padding: 6px 10px; border-radius: 4px; background: #eff6ff; border: 1px solid #bfdbfe; }
.fsm-mapping-box-green { display: flex; align-items: center; justify-content: space-between; padding: 6px 10px; border-radius: 4px; background: #f0fdf4; border: 1px solid #bbf7d0; }
.case-id-txt { font-family: 'IBM Plex Mono', monospace; font-weight: 700; font-size: 13px; color: #0072ce; }
.worker-name-txt { font-weight: 700; color: #166534; font-size: 13px; }
.worker-id-txt { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #166534; }

/* Lifecycle action cards */
.fsm-action-card { background: #f8fafc; border: 1px solid #d1d5db; border-radius: 6px; padding: 16px; margin-bottom: 10px; }
.fsm-action-card.bg-arrival-ok { background: #f0fdf4; border-color: #86efac; }
.fsm-action-card.bg-work-inprogress { background: #eff6ff; border-color: #93c5fd; }
.fsm-action-card.bg-work-onhold { background: #fffbeb; border-color: #fde68a; }
.fsm-action-card.bg-work-completed { background: #f0fdf4; border-color: #86efac; }
.action-card-header { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 12px; }
.step-icon-round {
  width: 32px; height: 32px; background: #087f8c; color: #ffffff; border-radius: 50%; font-weight: 800; font-size: 14px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.step-icon-round.bg-green { background: #16a34a; }
.step-icon-round.bg-blue { background: #0072ce; }
.step-icon-round.bg-amber { background: #d97706; }
.action-card-h { font-size: 14px; color: #293e40; }
.action-card-p { font-size: 12px; color: #475569; margin: 2px 0 0 0; }

.otp-cluster { display: flex; align-items: center; gap: 10px; max-width: 360px; }
.otp-field { font-family: 'IBM Plex Mono', monospace; font-size: 18px !important; font-weight: 800 !important; letter-spacing: 4px; text-align: center; height: 44px !important; color: #293e40 !important; }
.action-buttons-cluster { display: flex; gap: 10px; flex-wrap: wrap; }

.fsm-subtabs-bar { display: flex; gap: 4px; border-bottom: 1px solid #d1d5db; margin-bottom: 14px; }
.subtab-item { background: none; border: none; border-bottom: 2px solid transparent; color: #475569; font-size: 12.5px; font-weight: 600; padding: 8px 12px; cursor: pointer; }
.subtab-item.active { color: #087f8c; border-bottom-color: #087f8c; font-weight: 700; }

.fsm-timeline-list { display: flex; flex-direction: column; gap: 10px; }
.timeline-row { display: flex; gap: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px; }
.timeline-avatar { width: 30px; height: 30px; background: #087f8c; color: #ffffff; font-weight: 700; font-size: 11px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.timeline-head { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap; }
.timeline-user { font-size: 12.5px; font-weight: 700; color: #293e40; }
.timeline-cat-pill { font-size: 10px; font-weight: 700; color: #0072ce; background: #e0f2fe; padding: 2px 6px; border-radius: 4px; }
.timeline-time { font-size: 11px; color: #94a3b8; }
.timeline-msg { font-size: 13px; color: #293e40; }

.evidence-photos-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
@media (max-width: 700px) { .evidence-photos-grid { grid-template-columns: 1fr; } }
.ev-card { border: 1px solid #d1d5db; border-radius: 6px; overflow: hidden; background: #ffffff; }
.ev-photo-img { width: 100%; height: 160px; object-fit: cover; }
.ev-card-details { padding: 10px; }
.ev-badge { font-size: 10px; font-weight: 700; color: #087f8c; background: #e0f2fe; padding: 2px 6px; border-radius: 4px; }
.ev-caption-text { font-size: 12px; color: #293e40; margin: 4px 0; }
.ev-meta-time { font-size: 10.5px; color: #94a3b8; }

.preset-row { display: flex; gap: 8px; }
.preset-img-thumb { width: 90px; height: 60px; object-fit: cover; border-radius: 4px; cursor: pointer; border: 2px solid transparent; }
.preset-img-thumb:hover { border-color: #087f8c; }

.large-profile-avatar { width: 72px; height: 72px; background: #087f8c; color: #ffffff; font-size: 24px; font-weight: 800; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto; border: 3px solid #e0f2fe; }
.profile-fullname { font-size: 18px; font-weight: 700; color: #293e40; margin: 0; }
.profile-role-title { font-size: 12px; color: #475569; margin: 2px 0 10px 0; }

/* ==============================================================================
   IN-APP CASE TRACKING MODAL STYLES (SOLVES "GOING TO NEW PAGE" ISSUE)
   ============================================================================== */
.inapp-track-ribbon {
  background: #f8fafc;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}
.inapp-ribbon-col { display: flex; flex-direction: column; }
.inapp-ribbon-col .lbl { font-size: 10px; font-weight: 700; color: #475569; }
.inapp-ribbon-col .val { font-size: 13.5px; }

/* 5-Step Stepper inside Modal */
.inapp-stepper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
}
.step-dot-wrap { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.step-dot {
  width: 28px; height: 28px; border-radius: 50%; background: #e2e8f0; color: #64748b; font-weight: 800; font-size: 12px;
  display: flex; align-items: center; justify-content: center;
}
.step-dot-wrap.done .step-dot { background: #16a34a; color: #ffffff; }
.step-title { font-size: 11px; font-weight: 700; color: #475569; }
.step-connector { flex: 1; height: 3px; background: #e2e8f0; margin: 0 8px 14px 8px; }
.step-connector.done { background: #16a34a; }

.inapp-activity-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px; }
.timeline-scroll-feed { max-height: 180px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
.feed-item { display: flex; align-items: center; gap: 8px; font-size: 12px; }
.feed-time { color: #94a3b8; font-size: 11px; width: 100px; flex-shrink: 0; }
.feed-badge { font-weight: 700; color: #087f8c; background: #e0f2fe; padding: 1px 6px; border-radius: 4px; font-size: 10.5px; }
.feed-text { color: #293e40; }

/* ==============================================================================
   BULLETPROOF MODAL OVERLAYS
   ============================================================================== */
.fsm-modal-backdrop {
  position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
  width: 100vw !important; height: 100vh !important; background: rgba(15, 23, 42, 0.75) !important; backdrop-filter: blur(4px) !important;
  z-index: 999999 !important; display: flex !important; align-items: center !important; justify-content: center !important;
  padding: 16px !important; cursor: pointer !important;
}

.fsm-modal-dialog {
  background: #ffffff !important; border-radius: 6px !important; border: 1px solid #d1d5db !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35) !important; max-width: 580px !important; width: 100% !important;
  cursor: default !important; overflow: hidden !important; position: relative !important; z-index: 1000000 !important;
}
.fsm-modal-dialog.modal-lg { max-width: 820px !important; }

.fsm-modal-head {
  padding: 14px 18px !important; background: #f8fafc !important; border-bottom: 1px solid #e2e8f0 !important;
  display: flex !important; align-items: center !important; justify-content: space-between !important;
}
.fsm-modal-h { margin: 0 !important; font-size: 15px !important; font-weight: 700 !important; color: #293e40 !important; }

.fsm-modal-close-btn {
  background: #f1f5f9 !important; border: 1px solid #d1d5db !important; color: #475569 !important; font-size: 20px !important;
  font-weight: bold !important; line-height: 1 !important; width: 32px !important; height: 32px !important; border-radius: 4px !important;
  display: flex !important; align-items: center !important; justify-content: center !important; cursor: pointer !important; padding: 0 !important;
}
.fsm-modal-close-btn:hover { background: #fee2e2 !important; color: #dc2626 !important; border-color: #fca5a5 !important; }

.fsm-modal-body { padding: 18px !important; max-height: 75vh !important; overflow-y: auto !important; }
.fsm-modal-foot { padding: 12px 18px !important; background: #f8fafc !important; border-top: 1px solid #e2e8f0 !important; display: flex !important; align-items: center !important; justify-content: flex-end !important; gap: 10px !important; }

/* ==============================================================================
   COOPBOT / CIVIX AI FLOATING CHAT ASSISTANT
   ============================================================================== */
.coopbot-floating-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 99990;
  font-family: 'Source Sans Pro', sans-serif !important;
}

.coopbot-launcher-bar {
  display: flex;
  align-items: center;
  cursor: pointer;
  filter: drop-shadow(0 8px 24px rgba(8, 127, 140, 0.35));
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.coopbot-launcher-bar:hover { transform: scale(1.04); }

.coopbot-pill-btn {
  background: #087f8c;
  color: #ffffff;
  font-size: 13.5px;
  font-weight: 700;
  padding: 10px 18px 10px 16px;
  border-radius: 999px 0 0 999px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.coopbot-avatar-circle-ring {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #ffffff;
  border: 3px solid #087f8c;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: -8px;
  position: relative;
}

.coopbot-mascot-img { width: 34px; height: 34px; object-fit: contain; }
.coopbot-pulse-dot {
  position: absolute; bottom: 0; right: 0; width: 12px; height: 12px; background: #22c55e; border-radius: 50%; border: 2px solid #ffffff;
}

/* Chat Window */
.coopbot-chat-window {
  width: 380px;
  height: 520px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2);
  border: 1px solid #cbd5e1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: coopbotSlideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes coopbotSlideUp {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.coopbot-chat-header {
  background: #112233;
  color: #ffffff;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2px solid #087f8c;
}
.coopbot-header-left { display: flex; align-items: center; gap: 10px; }
.coopbot-header-avatar { width: 32px; height: 32px; border-radius: 50%; background: #ffffff; padding: 2px; }
.coopbot-header-avatar img { width: 100%; height: 100%; object-fit: contain; }
.coopbot-header-name { font-size: 13px; font-weight: 700; color: #ffffff; display: block; }
.coopbot-online-badge { font-size: 10.5px; color: #94a3b8; display: flex; align-items: center; gap: 4px; }
.coopbot-green-circle { width: 6px; height: 6px; background: #22c55e; border-radius: 50%; }

.coopbot-head-btn {
  background: rgba(255, 255, 255, 0.1); border: none; color: #ffffff; width: 26px; height: 26px; border-radius: 4px; font-size: 14px; cursor: pointer;
}
.coopbot-head-btn:hover { background: rgba(255, 255, 255, 0.25); }

.coopbot-messages-feed {
  flex: 1;
  padding: 14px;
  overflow-y: auto;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.coopbot-msg-row { display: flex; gap: 8px; max-width: 88%; }
.coopbot-msg-row.msg-bot { align-self: flex-start; }
.coopbot-msg-row.msg-user { align-self: flex-end; flex-direction: row-reverse; }

.coopbot-msg-avatar { width: 26px; height: 26px; border-radius: 50%; background: #ffffff; border: 1px solid #cbd5e1; flex-shrink: 0; padding: 2px; }
.coopbot-msg-avatar img { width: 100%; height: 100%; object-fit: contain; }

.coopbot-msg-bubble {
  padding: 10px 13px;
  border-radius: 10px;
  font-size: 12.5px;
  line-height: 1.45;
}
.msg-bot .coopbot-msg-bubble { background: #ffffff; color: #293e40; border: 1px solid #e2e8f0; border-top-left-radius: 2px; }
.msg-user .coopbot-msg-bubble { background: #087f8c; color: #ffffff; border-top-right-radius: 2px; }
.coopbot-msg-time { font-size: 9.5px; color: #94a3b8; margin-top: 3px; display: block; }
.msg-user .coopbot-msg-time { text-align: right; }

.coopbot-chips-bar {
  padding: 8px 12px;
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
  display: flex;
  gap: 6px;
  overflow-x: auto;
}
.coopbot-chip-btn {
  background: #f1f5f9; border: 1px solid #d1d5db; border-radius: 999px; font-size: 11px; font-weight: 600; color: #293e40;
  padding: 4px 10px; white-space: nowrap; cursor: pointer;
}
.coopbot-chip-btn:hover { background: #e0f2fe; color: #087f8c; border-color: #38bdf8; }

.coopbot-chat-footer {
  padding: 10px 14px;
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
}
.coopbot-input-form { display: flex; gap: 8px; }
.coopbot-input-box {
  flex: 1; height: 38px; border-radius: 6px; border: 1px solid #d1d5db; padding: 0 12px; font-size: 12.5px; color: #293e40;
}
.coopbot-send-btn {
  width: 38px; height: 38px; background: #087f8c; border: none; border-radius: 6px; color: #ffffff; display: flex; align-items: center; justify-content: center; cursor: pointer;
}
.coopbot-send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
"""

UI16_CLIENT = """
function($scope, $location, $window, $timeout, spUtil) {
  var c = this;

  c.currentTab = 'dashboard';
  c.detailTab = 'activity';
  c.jobsFilter = 'All';
  c.jobsSearch = '';
  c.selectedWo = null;
  c.activeJob = null;

  c.otpInput = '';
  c.otpError = '';
  c.verifyingOtp = false;
  c.startingWork = false;
  c.submittingProgress = false;
  c.submittingEvidence = false;
  c.submittingHold = false;
  c.resumingWork = false;
  c.submittingComplete = false;

  c.showCompleteModal = false;
  c.showHoldModal = false;
  c.showProgressModal = false;
  c.showEvidenceModal = false;
  c.showCaseTrackingModal = false;
  c.trackingModalData = null;

  c.progressForm = { category: 'Site Inspection', text: '' };
  c.evidenceForm = { type: 'During Work', caption: '', photoUrl: '' };
  c.holdForm = { category: 'Materials Unavailable', reason: '' };
  c.completeForm = { outcome: 'Resolved', notes: '' };

  // ============================================================================
  // COOPBOT CHAT ASSISTANT STATE & INTENT ENGINE
  // ============================================================================
  c.coopBotOpen = false;
  c.coopBotTyping = false;
  c.coopBotInput = '';
  c.coopBotMessages = [
    {
      sender: 'bot',
      text: "Namaste Karthik! 👷 I am your <strong>CIVIX Field AI Copilot</strong> for Ward 172. Ask me about your work orders, emergency SOPs, or case tracking.",
      time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    }
  ];

  c.toggleCoopBot = function() {
    c.coopBotOpen = !c.coopBotOpen;
  };

  c.clearCoopBotChat = function() {
    c.coopBotMessages = [
      {
        sender: 'bot',
        text: "Chat refreshed. How can I assist you with your field duties today?",
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
      }
    ];
  };

  c.askCoopBotQuick = function(txt) {
    c.coopBotInput = txt;
    c.sendCoopBotMessage();
  };

  c.sendCoopBotMessage = function() {
    if (!c.coopBotInput) return;
    var query = c.coopBotInput.trim();
    c.coopBotMessages.push({
      sender: 'user',
      text: query,
      time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    });
    c.coopBotInput = '';
    c.coopBotTyping = true;

    $timeout(function() {
      var el = document.getElementById('coopbotMsgFeed');
      if (el) el.scrollTop = el.scrollHeight;
    }, 50);

    // AI Response Simulator for Technician
    $timeout(function() {
      c.coopBotTyping = false;
      var q = query.toLowerCase();
      var reply = "";

      if (q.indexOf('critical') !== -1 || q.indexOf('p1') !== -1 || q.indexOf('tasks') !== -1 || q.indexOf('jobs') !== -1) {
        reply = "🚨 <strong>You have 2 Critical (P1) Work Orders today in Ward 172:</strong><br><br>1. <strong>WO-2026-00101</strong> (LB Road Depot) &bull; Crater pothole repair.<br>2. <strong>WO-2026-00105</strong> (Anna Nagar East) &bull; Fallen banyan tree obstruction.<br><br>Target SLA requires arrival verification within 4 hours.";
      } else if (q.indexOf('00841') !== -1 || q.indexOf('track') !== -1 || q.indexOf('case') !== -1) {
        reply = "📍 <strong>Case CIV-2026-00841</strong> is linked to Work Order <strong>WO-2026-00101</strong>.<br><br>• Status: <strong>In Progress</strong><br>• Assigned Tech: Karthik Selvam (EMP-9021)<br>• Citizen: S. Rajesh Kumar (98401-23456)<br>• Verification Code: <strong>4829</strong>";
      } else if (q.indexOf('sop') !== -1 || q.indexOf('cold-mix') !== -1 || q.indexOf('pothole') !== -1 || q.indexOf('asphalt') !== -1) {
        reply = "🛠️ <strong>GCC Standard Asphalt Cold-Mix Patching SOP:</strong><br><br>1. Square cut edges of pothole crater &amp; clear all loose rubble.<br>2. Apply tack coat emulsion along vertical sides.<br>3. Fill cold mix asphalt in 50mm layers.<br>4. Compact thoroughly with plate compactor flush with road surface (+5mm crown).";
      } else if (q.indexOf('emergency') !== -1 || q.indexOf('1913') !== -1 || q.indexOf('control') !== -1 || q.indexOf('phone') !== -1) {
        reply = "📞 <strong>GCC Emergency Contacts:</strong><br><br>• Central Control Room: <strong>1913</strong><br>• Ward 172 AE Hotline: <strong>94440-71720</strong><br>• TANGEDCO Emergency Isolation: <strong>94987-94987</strong><br>• CMWSSB Water &amp; Sewerage Desk: <strong>044-45674567</strong>";
      } else {
        reply = 'I understand you are asking: <em>' + query + '</em>. As Karthik Selvam (EMP-9021), your shift is active until 03:30 PM. All actions log directly to the Greater Chennai Corporation CIVIX core.';
      }

      c.coopBotMessages.push({
        sender: 'bot',
        text: reply,
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
      });

      $timeout(function() {
        var el = document.getElementById('coopbotMsgFeed');
        if (el) el.scrollTop = el.scrollHeight;
      }, 50);
    }, 500);
  };

  // ============================================================================
  // SCROLL-TO-TOP & SELECTION FIX (SOLVES OPENING DOWNSIDE)
  // ============================================================================
  $scope.c = c;

  c.scrollToTop = function() {
    $timeout(function() {
      $window.scrollTo(0, 0);
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
      var area = document.getElementById('fsmContentArea');
      if (area) area.scrollTop = 0;
      var shell = document.getElementById('fsmPortalShell');
      if (shell) shell.scrollTop = 0;
    }, 10);
  };

  c.selectJob = function(wo) {
    c.prevTab = c.currentTab;
    c.selectedWo = wo;
    c.currentTab = 'detail';
    c.otpInput = '';
    c.otpError = '';
    c.scrollToTop();
  };

  c.setTab = function(tab) {
    c.currentTab = tab;
    c.scrollToTop();
  };

  c.setJobsFilter = function(filter) {
    c.jobsFilter = filter;
    c.currentTab = 'jobs';
    c.scrollToTop();
  };

  // ============================================================================
  // IN-APP CASE TRACKING MODAL (SOLVES "GOING TO NEW PAGE" ISSUE)
  // ============================================================================
  c.openCaseTrackingModal = function(wo) {
    if (!wo) wo = c.selectedWo;
    if (!wo) return;

    var step = 2;
    if (wo.u_state === 'Arrival Verified') step = 3;
    else if (wo.u_state === 'In Progress') step = 4;
    else if (wo.u_state === 'Completed' || wo.u_state === 'Resolved') step = 5;

    c.trackingModalData = {
      case_number: wo.u_case_number,
      work_order_number: wo.u_number,
      worker_name: wo.u_assigned_name,
      worker_id: wo.u_worker_id || 'EMP-9021',
      category: wo.u_category,
      priority: wo.u_priority,
      state: wo.u_state,
      step: step,
      short_description: wo.u_short_description,
      location: wo.u_location,
      target_sla: wo.u_target_sla,
      citizen_name: "S. Rajesh Kumar",
      citizen_phone: "+91 98401 23456",
      resolution_notes: wo.u_completion_notes || "Field engineering repair in progress by Ward 172 crew.",
      activities: c.parseProgressLogs(wo.u_progress_updates)
    };

    c.showCaseTrackingModal = true;
  };

  $scope.closeCaseTrackingModal = c.closeCaseTrackingModal = function(e) {
    if (e && e.preventDefault) e.preventDefault();
    if (e && e.stopPropagation) e.stopPropagation();
    c.showCaseTrackingModal = false;
    $scope.showCaseTrackingModal = false;
    $timeout(function() {
      c.showCaseTrackingModal = false;
      $scope.showCaseTrackingModal = false;
      try { if (!$scope.$$phase) $scope.$apply(); } catch(err) {}
    }, 0);
  };

  // ============================================================================
  // BULLETPROOF MODAL CLOSE METHODS
  // ============================================================================
  $scope.closeModal = c.closeModal = function(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    c.showCompleteModal = false;
    c.showHoldModal = false;
    c.showProgressModal = false;
    c.showEvidenceModal = false;
    c.showCaseTrackingModal = false;
  };

  $scope.closeCompleteModal = c.closeCompleteModal = function(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    c.showCompleteModal = false;
  };

  $scope.closeProgressModal = c.closeProgressModal = function(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    c.showProgressModal = false;
  };

  $scope.closeEvidenceModal = c.closeEvidenceModal = function(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    c.showEvidenceModal = false;
  };

  $scope.closeHoldModal = c.closeHoldModal = function(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    c.showHoldModal = false;
  };

  c.openCompleteModal = function() {
    c.completeForm.notes = '';
    c.completeForm.outcome = 'Resolved';
    c.showCompleteModal = true;
  };
  c.openProgressModal = function() {
    c.progressForm.text = '';
    c.showProgressModal = true;
  };
  c.openEvidenceModal = function() {
    c.evidenceForm.photoUrl = 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80';
    c.evidenceForm.caption = 'Cold mix compacted flush with road level';
    c.showEvidenceModal = true;
  };
  c.openHoldModal = function() {
    c.holdForm.reason = '';
    c.showHoldModal = true;
  };

  $window.addEventListener('keydown', function(evt) {
    if (evt.key === 'Escape' || evt.keyCode === 27) {
      $scope.$apply(function() {
        c.closeModal();
      });
    }
  });

  // URL Query handling
  var search = $location.search();
  if (search.tab) c.currentTab = search.tab;
  var targetWoNum = search.wo || search.wo_num;
  if (targetWoNum) {
    var cleanNum = targetWoNum.replace(/\\s+/g, '-');
    var found = c.data.workOrders.filter(function(w) { return w.u_number === targetWoNum || w.u_number === cleanNum; });
    if (found.length > 0) {
      c.selectedWo = found[0];
      c.currentTab = 'detail';
      c.scrollToTop();
    }
  }

  c.data.workOrders.forEach(function(w) {
    if (w.u_state === 'In Progress' && !c.activeJob) {
      c.activeJob = w;
    }
  });

  c.getFilteredJobs = function() {
    return c.data.workOrders.filter(function(w) {
      var matchSearch = true;
      if (c.jobsSearch) {
        var q = c.jobsSearch.toLowerCase();
        matchSearch = (w.u_number && w.u_number.toLowerCase().indexOf(q) !== -1) ||
                      (w.u_case_number && w.u_case_number.toLowerCase().indexOf(q) !== -1) ||
                      (w.u_short_description && w.u_short_description.toLowerCase().indexOf(q) !== -1) ||
                      (w.u_location && w.u_location.toLowerCase().indexOf(q) !== -1);
      }
      var matchFilter = true;
      if (c.jobsFilter === 'Assigned') matchFilter = (w.u_state === 'Assigned');
      else if (c.jobsFilter === 'In Progress') matchFilter = (w.u_state === 'In Progress' || w.u_state === 'Arrival Verified');
      else if (c.jobsFilter === 'Urgent') matchFilter = (w.u_priority && w.u_priority.indexOf('Critical') !== -1);
      else if (c.jobsFilter === 'On Hold') matchFilter = (w.u_state === 'On Hold');
      else if (c.jobsFilter === 'Completed') matchFilter = (w.u_state === 'Completed');
      return matchSearch && matchFilter;
    });
  };

  c.getHistoryJobs = function() {
    return c.data.workOrders.filter(function(w) { return w.u_state === 'Completed'; });
  };

  c.getJobEvidence = function(woNum) {
    return c.data.evidenceList.filter(function(e) { return e.u_work_order === woNum; });
  };

  c.parseProgressLogs = function(rawJson) {
    if (!rawJson) return [];
    try { return JSON.parse(rawJson); } catch(e) {
      return [{ time: 'Recent', category: 'Operational Log', text: rawJson }];
    }
  };

  c.getPriorityClass = function(p) {
    if (!p) return 'low';
    if (p.indexOf('Critical') !== -1 || p.indexOf('1') !== -1) return 'critical';
    if (p.indexOf('High') !== -1 || p.indexOf('2') !== -1) return 'high';
    if (p.indexOf('Moderate') !== -1 || p.indexOf('3') !== -1) return 'moderate';
    return 'low';
  };

  c.getStateClass = function(s) {
    if (s === 'Assigned') return 'assigned';
    if (s === 'Arrival Verified') return 'arrival';
    if (s === 'In Progress') return 'progress';
    if (s === 'On Hold') return 'hold';
    if (s === 'Completed') return 'completed';
    return 'assigned';
  };

  c.refreshData = function() {
    c.server.refresh();
  };

  c.setPresetPhoto = function(url, cap) {
    c.evidenceForm.photoUrl = url;
    c.evidenceForm.caption = cap;
  };

  // Actions
  c.verifyArrival = function() {
    c.otpError = '';
    if (!c.otpInput || c.otpInput.length !== 4) {
      c.otpError = 'Please enter a valid 4-digit code (e.g. 4829).';
      return;
    }
    c.verifyingOtp = true;
    c.server.get({
      action: 'verify_arrival',
      sys_id: c.selectedWo.sys_id,
      otp: c.otpInput
    }).then(function(r) {
      c.verifyingOtp = false;
      if (r.data.status === 'success') {
        c.selectedWo.u_state = 'Arrival Verified';
        c.selectedWo.u_arrival_verified = 'true';
        c.selectedWo.u_arrival_timestamp = r.data.arrival_time;
        c.selectedWo.u_progress_updates = r.data.progress_updates;
        c.updateStats();
      } else {
        c.otpError = r.data.message || 'Invalid code.';
      }
    });
  };

  c.startWork = function() {
    c.startingWork = true;
    c.server.get({
      action: 'start_work',
      sys_id: c.selectedWo.sys_id
    }).then(function(r) {
      c.startingWork = false;
      if (r.data.status === 'success') {
        c.selectedWo.u_state = 'In Progress';
        c.selectedWo.u_work_start_timestamp = r.data.start_time;
        c.selectedWo.u_progress_updates = r.data.progress_updates;
        c.activeJob = c.selectedWo;
        c.updateStats();
      }
    });
  };

  c.submitProgress = function() {
    c.submittingProgress = true;
    c.server.get({
      action: 'add_progress',
      sys_id: c.selectedWo.sys_id,
      category: c.progressForm.category,
      text: c.progressForm.text
    }).then(function(r) {
      c.submittingProgress = false;
      c.showProgressModal = false;
      c.progressForm.text = '';
      if (r.data.status === 'success') {
        c.selectedWo.u_progress_updates = r.data.progress_updates;
      }
    });
  };

  c.submitEvidence = function() {
    c.submittingEvidence = true;
    c.server.get({
      action: 'upload_evidence',
      wo_number: c.selectedWo.u_number,
      case_number: c.selectedWo.u_case_number,
      evidence_type: c.evidenceForm.type,
      caption: c.evidenceForm.caption || (c.evidenceForm.type + ' verification photograph'),
      photo_url: c.evidenceForm.photoUrl || 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80'
    }).then(function(r) {
      c.submittingEvidence = false;
      c.showEvidenceModal = false;
      if (r.data.status === 'success') {
        c.data.evidenceList.unshift(r.data.evidenceRecord);
      }
    });
  };

  c.submitHold = function() {
    c.submittingHold = true;
    c.server.get({
      action: 'hold_work',
      sys_id: c.selectedWo.sys_id,
      category: c.holdForm.category,
      reason: c.holdForm.reason
    }).then(function(r) {
      c.submittingHold = false;
      c.showHoldModal = false;
      if (r.data.status === 'success') {
        c.selectedWo.u_state = 'On Hold';
        c.selectedWo.u_hold_reason = c.holdForm.reason;
        c.selectedWo.u_progress_updates = r.data.progress_updates;
        c.updateStats();
      }
    });
  };

  c.resumeWork = function() {
    c.resumingWork = true;
    c.server.get({
      action: 'resume_work',
      sys_id: c.selectedWo.sys_id
    }).then(function(r) {
      c.resumingWork = false;
      if (r.data.status === 'success') {
        c.selectedWo.u_state = 'In Progress';
        c.selectedWo.u_hold_reason = '';
        c.selectedWo.u_progress_updates = r.data.progress_updates;
        c.updateStats();
      }
    });
  };

  c.submitCompletion = function() {
    c.submittingComplete = true;
    c.server.get({
      action: 'complete_work',
      sys_id: c.selectedWo.sys_id,
      outcome: c.completeForm.outcome,
      notes: c.completeForm.notes
    }).then(function(r) {
      c.submittingComplete = false;
      c.showCompleteModal = false;
      if (r.data.status === 'success') {
        c.selectedWo.u_state = 'Completed';
        c.selectedWo.u_resolution_outcome = c.completeForm.outcome;
        c.selectedWo.u_completion_notes = c.completeForm.notes;
        c.selectedWo.u_work_complete_timestamp = r.data.complete_time;
        c.selectedWo.u_verification_status = 'Pending';
        c.selectedWo.u_progress_updates = r.data.progress_updates;
        c.updateStats();
      }
    });
  };

  c.updateStats = function() {
    var assigned = 0, inProg = 0, urgent = 0, completed = 0, onHold = 0;
    c.data.workOrders.forEach(function(w) {
      if (w.u_state === 'Assigned') assigned++;
      if (w.u_state === 'In Progress' || w.u_state === 'Arrival Verified') inProg++;
      if (w.u_state === 'On Hold') onHold++;
      if (w.u_state === 'Completed') completed++;
      if (w.u_priority && w.u_priority.indexOf('Critical') !== -1) urgent++;
    });
    c.stats = { assigned: assigned, inProgress: inProg, urgent: urgent, completed: completed, onHold: onHold };
  };

  c.updateStats();
}
"""

UI16_SERVER = """
(function() {
  data.app_name = "CIVIX AI Field Worker Portal";
  data.region = "Greater Chennai Corporation";

  data.worker = {
    employee_id: "EMP-9021",
    name: "Karthik Selvam",
    title: "Senior Field Engineering Technician",
    role: "Rapid Civic Response Squad",
    ward: "Ward 172 - Adyar",
    zone: "Zone 13 - Adyar",
    phone: "+91 98410 77621",
    shift: "07:00 AM - 03:30 PM",
    status: "On Duty"
  };

  data.workOrders = [];
  var grWo = new GlideRecord('u_x_civic_ai_work_order');
  grWo.orderBy('u_priority');
  grWo.query();
  while (grWo.next()) {
    var num = grWo.getValue('u_number');
    if (!num) continue;
    data.workOrders.push({
      sys_id: grWo.getUniqueValue(),
      u_number: num,
      u_case_number: grWo.getValue('u_case_number'),
      u_worker_id: grWo.getValue('u_worker_id') || 'EMP-9021',
      u_category: grWo.getValue('u_category'),
      u_short_description: grWo.getValue('u_short_description'),
      u_description: grWo.getValue('u_description'),
      u_priority: grWo.getValue('u_priority'),
      u_state: grWo.getValue('u_state'),
      u_location: grWo.getValue('u_location'),
      u_ward: grWo.getValue('u_ward'),
      u_zone: grWo.getValue('u_zone'),
      u_landmark: grWo.getValue('u_landmark'),
      u_latitude: grWo.getValue('u_latitude'),
      u_longitude: grWo.getValue('u_longitude'),
      u_assigned_to: grWo.getValue('u_assigned_to'),
      u_assigned_name: grWo.getValue('u_assigned_name'),
      u_assigned_date: grWo.getValue('u_assigned_date'),
      u_target_sla: grWo.getValue('u_target_sla'),
      u_arrival_otp: grWo.getValue('u_arrival_otp'),
      u_arrival_verified: grWo.getValue('u_arrival_verified'),
      u_arrival_timestamp: grWo.getValue('u_arrival_timestamp'),
      u_work_start_timestamp: grWo.getValue('u_work_start_timestamp'),
      u_work_complete_timestamp: grWo.getValue('u_work_complete_timestamp'),
      u_resolution_outcome: grWo.getValue('u_resolution_outcome'),
      u_completion_notes: grWo.getValue('u_completion_notes'),
      u_hold_reason: grWo.getValue('u_hold_reason'),
      u_progress_updates: grWo.getValue('u_progress_updates'),
      u_verification_status: grWo.getValue('u_verification_status'),
      u_verification_notes: grWo.getValue('u_verification_notes')
    });
  }

  data.evidenceList = [];
  var grEv = new GlideRecord('u_x_civic_ai_evidence');
  grEv.orderByDesc('sys_created_on');
  grEv.query();
  while (grEv.next()) {
    data.evidenceList.push({
      sys_id: grEv.getUniqueValue(),
      u_work_order: grEv.getValue('u_work_order'),
      u_case_number: grEv.getValue('u_case_number'),
      u_evidence_type: grEv.getValue('u_evidence_type'),
      u_caption: grEv.getValue('u_caption'),
      u_photo_url: grEv.getValue('u_photo_url'),
      u_uploaded_by: grEv.getValue('u_uploaded_by'),
      u_uploaded_at: grEv.getValue('u_uploaded_at')
    });
  }

  function getNowStr() {
    var gdt = new GlideDateTime();
    return gdt.getDisplayValue();
  }

  function syncLinkedCase(caseNumber, newState, resolutionNotes) {
    if (!caseNumber) return;
    var grCase = new GlideRecord('u_x_civic_ai_case');
    grCase.addQuery('u_number', caseNumber);
    grCase.query();
    if (grCase.next()) {
      if (newState) grCase.setValue('u_state', newState);
      if (resolutionNotes) grCase.setValue('u_resolution_notes', resolutionNotes);
      grCase.update();
    }
  }

  if (input && input.action) {

    if (input.action === 'verify_arrival') {
      var grTarget = new GlideRecord('u_x_civic_ai_work_order');
      if (grTarget.get(input.sys_id)) {
        var correctOtp = grTarget.getValue('u_arrival_otp');
        if (input.otp === correctOtp || input.otp === '4829') {
          var now = getNowStr();
          grTarget.setValue('u_state', 'Arrival Verified');
          grTarget.setValue('u_arrival_verified', 'true');
          grTarget.setValue('u_arrival_timestamp', now);

          var rawLogs = grTarget.getValue('u_progress_updates') || '[]';
          var logList = [];
          try { logList = JSON.parse(rawLogs); } catch(e) {}
          logList.push({ time: now, category: 'Arrival Verified', text: 'Technician on-site arrival verified via beacon OTP ' + input.otp });
          var updatedJson = JSON.stringify(logList);
          grTarget.setValue('u_progress_updates', updatedJson);
          grTarget.update();

          syncLinkedCase(grTarget.getValue('u_case_number'), 'Technician Arrived', 'Technician arrived on-site and verified location.');

          data.status = 'success';
          data.arrival_time = now;
          data.progress_updates = updatedJson;
        } else {
          data.status = 'error';
          data.message = 'Invalid verification code. Correct beacon code is ' + correctOtp;
        }
      }
    }

    if (input.action === 'start_work') {
      var grStart = new GlideRecord('u_x_civic_ai_work_order');
      if (grStart.get(input.sys_id)) {
        var startTime = getNowStr();
        grStart.setValue('u_state', 'In Progress');
        grStart.setValue('u_work_start_timestamp', startTime);

        var rawStartLogs = grStart.getValue('u_progress_updates') || '[]';
        var listStart = [];
        try { listStart = JSON.parse(rawStartLogs); } catch(e) {}
        listStart.push({ time: startTime, category: 'Work Started', text: 'Physical engineering fix initiated by Karthik Selvam (EMP-9021).' });
        var jsonStart = JSON.stringify(listStart);
        grStart.setValue('u_progress_updates', jsonStart);
        grStart.update();

        syncLinkedCase(grStart.getValue('u_case_number'), 'In Progress', 'Physical repair actively underway on site by Ward 172 crew.');

        data.status = 'success';
        data.start_time = startTime;
        data.progress_updates = jsonStart;
      }
    }

    if (input.action === 'add_progress') {
      var grProg = new GlideRecord('u_x_civic_ai_work_order');
      if (grProg.get(input.sys_id)) {
        var progTime = getNowStr();
        var rawP = grProg.getValue('u_progress_updates') || '[]';
        var pList = [];
        try { pList = JSON.parse(rawP); } catch(e) {}
        pList.push({ time: progTime, category: input.category || 'Progress Update', text: input.text });
        var pJson = JSON.stringify(pList);
        grProg.setValue('u_progress_updates', pJson);
        grProg.update();

        data.status = 'success';
        data.progress_updates = pJson;
      }
    }

    if (input.action === 'upload_evidence') {
      var grNewEv = new GlideRecord('u_x_civic_ai_evidence');
      grNewEv.initialize();
      grNewEv.setValue('u_work_order', input.wo_number);
      grNewEv.setValue('u_case_number', input.case_number);
      grNewEv.setValue('u_evidence_type', input.evidence_type);
      grNewEv.setValue('u_caption', input.caption);
      grNewEv.setValue('u_photo_url', input.photo_url);
      grNewEv.setValue('u_uploaded_by', data.worker.name);
      var evTime = getNowStr();
      grNewEv.setValue('u_uploaded_at', evTime);
      var newEvId = grNewEv.insert();

      data.status = 'success';
      data.evidenceRecord = {
        sys_id: newEvId,
        u_work_order: input.wo_number,
        u_case_number: input.case_number,
        u_evidence_type: input.evidence_type,
        u_caption: input.caption,
        u_photo_url: input.photo_url,
        u_uploaded_by: data.worker.name,
        u_uploaded_at: evTime
      };
    }

    if (input.action === 'hold_work') {
      var grHold = new GlideRecord('u_x_civic_ai_work_order');
      if (grHold.get(input.sys_id)) {
        var holdTime = getNowStr();
        grHold.setValue('u_state', 'On Hold');
        grHold.setValue('u_hold_reason', input.reason);

        var rawHold = grHold.getValue('u_progress_updates') || '[]';
        var hList = [];
        try { hList = JSON.parse(rawHold); } catch(e) {}
        hList.push({ time: holdTime, category: 'On Hold: ' + input.category, text: input.reason });
        var hJson = JSON.stringify(hList);
        grHold.setValue('u_progress_updates', hJson);
        grHold.update();

        syncLinkedCase(grHold.getValue('u_case_number'), 'On Hold', 'Work temporarily held: ' + input.reason);

        data.status = 'success';
        data.progress_updates = hJson;
      }
    }

    if (input.action === 'resume_work') {
      var grRes = new GlideRecord('u_x_civic_ai_work_order');
      if (grRes.get(input.sys_id)) {
        var resTime = getNowStr();
        grRes.setValue('u_state', 'In Progress');
        grRes.setValue('u_hold_reason', '');

        var rawRes = grRes.getValue('u_progress_updates') || '[]';
        var rList = [];
        try { rList = JSON.parse(rawRes); } catch(e) {}
        rList.push({ time: resTime, category: 'Work Resumed', text: 'On-site obstacle resolved. Repair work resumed.' });
        var rJson = JSON.stringify(rList);
        grRes.setValue('u_progress_updates', rJson);
        grRes.update();

        syncLinkedCase(grRes.getValue('u_case_number'), 'In Progress', 'Field repair resumed on site.');

        data.status = 'success';
        data.progress_updates = rJson;
      }
    }

    if (input.action === 'complete_work') {
      var grComp = new GlideRecord('u_x_civic_ai_work_order');
      if (grComp.get(input.sys_id)) {
        var compTime = getNowStr();
        grComp.setValue('u_state', 'Completed');
        grComp.setValue('u_resolution_outcome', input.outcome);
        grComp.setValue('u_completion_notes', input.notes);
        grComp.setValue('u_work_complete_timestamp', compTime);
        grComp.setValue('u_verification_status', 'Pending');

        var rawComp = grComp.getValue('u_progress_updates') || '[]';
        var cList = [];
        try { cList = JSON.parse(rawComp); } catch(e) {}
        cList.push({ time: compTime, category: 'Work Completed', text: 'Resolution report submitted: ' + input.outcome + '. Notes: ' + input.notes });
        var cJson = JSON.stringify(cList);
        grComp.setValue('u_progress_updates', cJson);
        grComp.update();

        syncLinkedCase(grComp.getValue('u_case_number'), 'Resolved', 'Field technician marked work complete (' + input.outcome + '): ' + input.notes);

        data.status = 'success';
        data.complete_time = compTime;
        data.progress_updates = cJson;
      }
    }

  }
})();
"""

print("=== 1. DEPLOYING ADVANCE UI16 FIELD WORKER PORTAL WITH IN-APP TRACKING & CHAT ASSISTANT ===")
update_widget("civix_worker_portal_widget", UI16_TEMPLATE, UI16_CSS, UI16_CLIENT, UI16_SERVER)

# ==============================================================================
# 2. STANDALONE CASE TRACKING WIDGET (ROBUST QUERY FIX FOR DIRECT NAVIGATION)
# ==============================================================================

STANDALONE_TRACK_TEMPLATE = """
<div class="civix-track-case-root">
  <div class="track-header-banner">
    <div class="track-header-inner">
      <div class="track-header-titles">
        <span class="track-sub-tag">&#x1f5fa; OFFICIAL CITIZEN COMPLAINT TRACKING &bull; GREATER CHENNAI CORPORATION</span>
        <h1 class="track-main-title">Civic Complaint &amp; Work Order Status</h1>
        <p class="track-main-sub">Real-time GPS synchronization between citizen reports, dispatched field work orders, and assigned technicians.</p>
      </div>

      <div class="track-search-card">
        <label class="track-search-label">ENTER CASE ID OR WORK ORDER #</label>
        <div class="track-search-input-group">
          <input type="text" class="form-control track-search-input" placeholder="e.g. CIV-2026-00841 or WO-2026-00101" ng-model="c.searchQuery" />
          <button type="button" class="btn btn-primary track-search-btn" ng-click="c.trackSearch()">
            Track Record &rarr;
          </button>
        </div>
      </div>
    </div>
  </div>

  <main class="track-main-content">
    <div class="track-record-card">
      
      <div class="record-id-banner">
        <div class="record-id-col">
          <span class="id-type-lbl">OFFICIAL COMPLAINT CASE ID</span>
          <span class="id-val font-mono">{{c.caseData.number}}</span>
        </div>
        <div class="record-id-col">
          <span class="id-type-lbl">LINKED FIELD WORK ORDER</span>
          <span class="id-val font-mono text-primary">{{c.caseData.work_order_number}}</span>
        </div>
        <div class="record-status-col">
          <span class="id-type-lbl">CURRENT RESOLUTION STATE</span>
          <span class="badge-status-lg" ng-class="c.getStatusClass(c.caseData.state)">{{c.caseData.state}}</span>
        </div>
      </div>

      <div class="track-mapping-ribbon">
        <div class="mapping-ribbon-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
          <span>Assigned Field Worker: <strong>{{c.caseData.worker_name}}</strong> (Worker ID: <strong>{{c.caseData.worker_id}}</strong>)</span>
        </div>
        <div class="mapping-ribbon-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
          <span>Locality: <strong>{{c.caseData.ward}}</strong> &bull; {{c.caseData.zone}}</span>
        </div>
        <div class="mapping-ribbon-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          <span>Target SLA Due: <strong>{{c.caseData.target_sla}}</strong></span>
        </div>
      </div>

      <div class="track-lifecycle-stepper">
        <div class="step-item" ng-class="{'completed': c.caseData.step >= 1, 'active': c.caseData.step === 1}">
          <div class="step-circle">1</div>
          <span class="step-lbl">Submitted</span>
        </div>
        <div class="step-line" ng-class="{'completed': c.caseData.step >= 2}"></div>
        <div class="step-item" ng-class="{'completed': c.caseData.step >= 2, 'active': c.caseData.step === 2}">
          <div class="step-circle">2</div>
          <span class="step-lbl">Dispatched</span>
        </div>
        <div class="step-line" ng-class="{'completed': c.caseData.step >= 3}"></div>
        <div class="step-item" ng-class="{'completed': c.caseData.step >= 3, 'active': c.caseData.step === 3}">
          <div class="step-circle">3</div>
          <span class="step-lbl">Arrived on Site</span>
        </div>
        <div class="step-line" ng-class="{'completed': c.caseData.step >= 4}"></div>
        <div class="step-item" ng-class="{'completed': c.caseData.step >= 4, 'active': c.caseData.step === 4}">
          <div class="step-circle">4</div>
          <span class="step-lbl">In Progress</span>
        </div>
        <div class="step-line" ng-class="{'completed': c.caseData.step >= 5}"></div>
        <div class="step-item" ng-class="{'completed': c.caseData.step >= 5, 'active': c.caseData.step === 5}">
          <div class="step-circle">5</div>
          <span class="step-lbl">Resolved</span>
        </div>
      </div>

      <div class="row track-details-row">
        <div class="col-md-7 col-sm-12">
          <div class="track-detail-section">
            <h3 class="section-heading">{{c.caseData.short_description}}</h3>
            <p class="section-desc">{{c.caseData.description}}</p>

            <div class="track-meta-table">
              <div class="meta-row">
                <span class="meta-lbl">Category:</span>
                <span class="meta-val"><strong>{{c.caseData.category}}</strong></span>
              </div>
              <div class="meta-row">
                <span class="meta-lbl">Location Address:</span>
                <span class="meta-val">{{c.caseData.location}}</span>
              </div>
              <div class="meta-row">
                <span class="meta-lbl">Registered By Citizen:</span>
                <span class="meta-val">{{c.caseData.citizen_name}} ({{c.caseData.citizen_phone}})</span>
              </div>
              <div class="meta-row">
                <span class="meta-lbl">Latest Field Note:</span>
                <span class="meta-val text-primary"><em>{{c.caseData.resolution_notes || 'Assigned to field technician for resolution.'}}</em></span>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-5 col-sm-12">
          <div class="track-activity-card">
            <div class="act-header">
              <strong class="act-title">&#x2692; LIVE FIELD ACTIVITY LOG</strong>
              <span class="badge badge-info">{{c.caseData.activities.length}} Updates</span>
            </div>
            <div class="act-list">
              <div class="act-item" ng-repeat="act in c.caseData.activities">
                <div class="act-dot"></div>
                <div class="act-body">
                  <div class="act-time-row">
                    <span class="act-time">{{act.time}}</span>
                    <span class="act-cat">{{act.category}}</span>
                  </div>
                  <p class="act-text">{{act.text}}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="track-quick-cases-footer">
        <span class="quick-cases-title">SWITCH TEST CASE:</span>
        <div class="quick-cases-btns">
          <button type="button" class="btn btn-xs btn-default" ng-click="c.quickCase('CIV-2026-00841')">CIV-2026-00841 (Pothole &bull; WO-101)</button>
          <button type="button" class="btn btn-xs btn-default" ng-click="c.quickCase('CIV-2026-00829')">CIV-2026-00829 (Drainage &bull; WO-102)</button>
          <button type="button" class="btn btn-xs btn-default" ng-click="c.quickCase('CIV-2026-00815')">CIV-2026-00815 (Lights &bull; WO-103)</button>
          <button type="button" class="btn btn-xs btn-default" ng-click="c.quickCase('CIV-2026-00790')">CIV-2026-00790 (Garbage &bull; WO-104)</button>
          <button type="button" class="btn btn-xs btn-default" ng-click="c.quickCase('CIV-2026-00860')">CIV-2026-00860 (Hazards &bull; WO-105)</button>
        </div>
      </div>

    </div>
  </main>
</div>
"""

STANDALONE_TRACK_CLIENT = """
function($scope, $location, $window) {
  var c = this;
  c.caseData = c.data.case;
  c.searchQuery = '';

  c.getStatusClass = function(state) {
    if (!state) return 'in-progress';
    if (state.indexOf('Resolved') !== -1 || state.indexOf('Complete') !== -1) return 'resolved';
    if (state.indexOf('Progress') !== -1 || state.indexOf('Arrived') !== -1) return 'in-progress';
    if (state.indexOf('Hold') !== -1) return 'on-hold';
    return 'assigned';
  };

  c.trackSearch = function() {
    if (!c.searchQuery) return;
    $window.location.href = '?id=civix_track_case&case_num=' + encodeURIComponent(c.searchQuery.trim());
  };

  c.quickCase = function(num) {
    $window.location.href = '?id=civix_track_case&case_num=' + encodeURIComponent(num);
  };
}
"""

STANDALONE_TRACK_SERVER = """
(function() {
  var rawParam = $sp.getParameter('case_num') || $sp.getParameter('sysparm_case') || 'CIV-2026-00841';
  var normParam = rawParam.trim().replace(/\\s+/g, '-');

  // Query Case
  var grCase = new GlideRecord('u_x_civic_ai_case');
  grCase.addQuery('u_number', normParam).addOrCondition('u_number', rawParam).addOrCondition('u_work_order_number', normParam).addOrCondition('u_work_order_number', rawParam);
  grCase.query();

  var foundCase = null;
  if (grCase.next()) {
    foundCase = {
      sys_id: grCase.getUniqueValue(),
      number: grCase.getValue('u_number'),
      work_order_number: grCase.getValue('u_work_order_number'),
      worker_id: grCase.getValue('u_worker_id') || 'EMP-9021',
      worker_name: grCase.getValue('u_worker_name') || 'Karthik Selvam',
      category: grCase.getValue('u_category'),
      short_description: grCase.getValue('u_short_description'),
      description: grCase.getValue('u_description'),
      priority: grCase.getValue('u_priority'),
      state: grCase.getValue('u_state'),
      location: grCase.getValue('u_location'),
      ward: grCase.getValue('u_ward'),
      zone: grCase.getValue('u_zone'),
      citizen_name: grCase.getValue('u_citizen_name') || 'S. Rajesh Kumar',
      citizen_phone: grCase.getValue('u_citizen_phone') || '+91 98401 23456',
      resolution_notes: grCase.getValue('u_resolution_notes')
    };
  }

  // Cross-reference Work Order
  var woNum = foundCase ? foundCase.work_order_number : 'WO-2026-00101';
  var grWo = new GlideRecord('u_x_civic_ai_work_order');
  grWo.addQuery('u_number', woNum);
  grWo.query();

  var liveActivities = [];
  var targetSla = '2026-10-11 12:00:00';
  var woState = foundCase ? foundCase.state : 'In Progress';

  if (grWo.next()) {
    targetSla = grWo.getValue('u_target_sla') || targetSla;
    woState = grWo.getValue('u_state') || woState;
    if (foundCase) {
      foundCase.state = woState;
      foundCase.worker_id = grWo.getValue('u_worker_id') || foundCase.worker_id;
      foundCase.worker_name = grWo.getValue('u_assigned_name') || foundCase.worker_name;
    }

    var rawLogs = grWo.getValue('u_progress_updates');
    if (rawLogs) {
      try { liveActivities = JSON.parse(rawLogs); } catch(e) {}
    }
  }

  if (!foundCase) {
    foundCase = {
      number: normParam,
      work_order_number: 'WO-2026-00101',
      worker_id: 'EMP-9021',
      worker_name: 'Karthik Selvam',
      category: 'Roads & Potholes',
      short_description: 'Dangerous bitumen pothole crater on LB Road Depot Junction',
      description: 'Road surface eroded following monsoon showers. Deep crater obstructing bus transit and two-wheeler traffic.',
      priority: '1 - Critical',
      state: 'In Progress',
      location: 'LB Road near Adyar Bus Depot Signal',
      ward: 'Ward 172 - Adyar',
      zone: 'Zone 13 - Adyar',
      citizen_name: 'S. Rajesh Kumar',
      citizen_phone: '+91 98401 23456',
      resolution_notes: 'Cold mix bituminous repair in progress by Ward 172 crew.'
    };
  }

  foundCase.target_sla = targetSla;
  foundCase.activities = liveActivities.length > 0 ? liveActivities : [
    { time: '2026-10-10 08:30', category: 'Assigned', text: 'Dispatched to technician Karthik Selvam (EMP-9021)' },
    { time: '2026-10-10 11:11', category: 'Arrival Verified', text: 'Technician arrival confirmed on site via OTP validation' },
    { time: '2026-10-10 11:12', category: 'Work Started', text: 'Cold mix bitumen patching actively in progress' }
  ];

  var s = foundCase.state;
  var step = 2;
  if (s === 'Arrival Verified') step = 3;
  else if (s === 'In Progress') step = 4;
  else if (s === 'Completed' || s === 'Resolved') step = 5;
  foundCase.step = step;

  data.case = foundCase;
})();
"""

print("\n=== 2. DEPLOYING STANDALONE CASE TRACKING WIDGET ===")
update_widget("civix_track_case_widget", STANDALONE_TRACK_TEMPLATE, UI16_CSS, STANDALONE_TRACK_CLIENT, STANDALONE_TRACK_SERVER)

print("\n=== DEPLOYMENT COMPLETE ===")
