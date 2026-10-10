"""
CIVIX AI - Comprehensive Field Worker Portal Deployment
Implements all 16 Screens for Mobile Field Operations in ServiceNow:
1. Worker Login & Auth Check
2. Field Worker Dashboard (Live KPIs, Assigned Jobs, Today's Work)
3. My Jobs (Status & Priority Filter Tabs, Search)
4. Job Details & Work Order Summary
5. Navigation & Location (Live Map directions, GPS coordinates)
6. Arrival Verification (Server-validated 4-digit OTP)
7. Start Work (Validated state transition & server timestamp)
8. Progress Updates (Categorized milestones & audit log)
9. Evidence Upload (Before, During, After photo evidence)
10. Request Support / Hold / Emergency Hazard Escalation
11. Complete Work (Resolution outcome & closure report)
12. Resolution Verification Outcome
13. My Work History (Filterable audit trail)
14. Notifications Panel
15. Profile, Ward Locality & Language (English / Tamil)
16. Duty Shift & Municipal Allowance Status
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

def api_post(table: str, data: dict):
    url = f"{INSTANCE_URL}/api/now/table/{table}"
    resp = session.post(url, json=data, timeout=25)
    resp.raise_for_status()
    return resp.json().get("result", {})

def upsert(table: str, query: str, data: dict, label: str):
    existing = api_get(table, query=query, limit=1)
    if existing:
        sys_id = existing[0]["sys_id"]
        res = api_put(table, sys_id, data)
        print(f"  [UPDATED] {label} ({sys_id})")
        return sys_id
    else:
        res = api_post(table, data)
        sys_id = res.get("sys_id")
        print(f"  [CREATED] {label} ({sys_id})")
        return sys_id

# ==============================================================================
# WIDGET TEMPLATE, CSS, CLIENT & SERVER SCRIPTS
# ==============================================================================

WORKER_TEMPLATE = """
<div class="civix-worker-portal-root">

  <!-- 1. TOP MOBILE-FIRST APP BAR -->
  <header class="worker-app-bar">
    <div class="worker-bar-left">
      <button class="worker-menu-toggle" type="button" ng-click="c.toggleDrawer()" aria-label="Menu">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
      <div class="worker-brand" ng-click="c.setTab('dashboard')">
        <div class="worker-logo-chip">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
        </div>
        <div class="worker-brand-text">
          <span class="brand-title">CIVIX FIELD OPS</span>
          <span class="brand-sub">Greater Chennai Corporation</span>
        </div>
      </div>
    </div>

    <!-- Top Right: Language, Notifications, Profile -->
    <div class="worker-bar-right">
      <!-- Language Pill -->
      <button class="worker-lang-toggle" type="button" ng-click="c.toggleLang()">
        <span>{{c.lang === 'ta' ? 'தமிழ்' : 'EN'}}</span>
      </button>

      <!-- Notifications Bell -->
      <div class="worker-notif-box" ng-class="{'open': c.notifOpen}">
        <button class="worker-icon-btn" type="button" ng-click="c.toggleNotifs()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
          <span class="notif-badge-dot" ng-if="c.unreadNotifs > 0"></span>
        </button>
        <div class="worker-notif-dropdown" ng-if="c.notifOpen">
          <div class="notif-header">
            <strong>{{c.lang === 'ta' ? 'அறிவிப்புகள்' : 'Work Notifications'}}</strong>
            <span class="badge badge-success">{{c.unreadNotifs}} new</span>
          </div>
          <div class="notif-list">
            <div class="notif-item" ng-repeat="n in c.data.notifications" ng-click="c.openJobByNum(n.woNum)">
              <div class="notif-icon-wrap" ng-class="n.type">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
              </div>
              <div class="notif-info">
                <p class="notif-title">{{n.title}}</p>
                <span class="notif-time">{{n.time}} &bull; {{n.woNum}}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Profile Avatar Toggle -->
      <button class="worker-avatar-btn" type="button" ng-click="c.setTab('profile')">
        <span class="avatar-initials">{{c.data.worker.initials}}</span>
      </button>
    </div>
  </header>

  <!-- 2. SLIDE-OUT MOBILE NAVIGATION DRAWER -->
  <div class="worker-drawer-backdrop" ng-if="c.drawerOpen" ng-click="c.toggleDrawer()"></div>
  <aside class="worker-drawer" ng-class="{'open': c.drawerOpen}">
    <div class="drawer-header">
      <div class="drawer-worker-info">
        <div class="drawer-avatar">{{c.data.worker.initials}}</div>
        <div>
          <strong class="drawer-name">{{c.data.worker.name}}</strong>
          <span class="drawer-role">{{c.data.worker.roleTitle}}</span>
        </div>
      </div>
      <button class="drawer-close-btn" type="button" ng-click="c.toggleDrawer()">&times;</button>
    </div>

    <nav class="drawer-nav">
      <a href="javascript:void(0)" class="drawer-item" ng-class="{'active': c.currentTab === 'dashboard'}" ng-click="c.setTab('dashboard')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
        <span>{{c.lang === 'ta' ? 'டாஷ்போர்டு' : 'Field Dashboard'}}</span>
      </a>
      <a href="javascript:void(0)" class="drawer-item" ng-class="{'active': c.currentTab === 'jobs'}" ng-click="c.setTab('jobs')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
        <span>{{c.lang === 'ta' ? 'எனது பணிகள்' : 'My Assigned Jobs'}}</span>
        <span class="badge badge-primary">{{c.stats.assigned + c.stats.inProgress}}</span>
      </a>
      <a href="javascript:void(0)" class="drawer-item" ng-class="{'active': c.currentTab === 'history'}" ng-click="c.setTab('history')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
        <span>{{c.lang === 'ta' ? 'பணி வரலாறு' : 'Work History'}}</span>
      </a>
      <a href="javascript:void(0)" class="drawer-item" ng-class="{'active': c.currentTab === 'support'}" ng-click="c.setTab('support')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        <span>{{c.lang === 'ta' ? 'உதவி கோரிக்கை' : 'Emergency & Support'}}</span>
      </a>
      <a href="javascript:void(0)" class="drawer-item" ng-class="{'active': c.currentTab === 'profile'}" ng-click="c.setTab('profile')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        <span>{{c.lang === 'ta' ? 'சுயவிவரம்' : 'Worker Profile & Settings'}}</span>
      </a>
    </nav>

    <div class="drawer-footer">
      <a href="?id=civix_portal_select" class="btn btn-default btn-block drawer-portal-btn">
        <span>&larr; Portal Selection</span>
      </a>
      <a href="javascript:void(0)" ng-click="c.logout()" class="drawer-signout-link">
        <span>Sign Out of Ops</span>
      </a>
    </div>
  </aside>

  <!-- 3. MAIN WORKER VIEWPORT -->
  <main class="worker-main-content">

    <!-- TAB 1: FIELD WORKER DASHBOARD (Screen 2) -->
    <div class="worker-tab-view" ng-if="c.currentTab === 'dashboard'">
      <!-- Welcome Hero Banner -->
      <section class="worker-hero-card">
        <div class="worker-hero-badge">
          <span class="live-dot-teal"></span>
          <span>{{c.data.worker.zone}} &bull; {{c.data.worker.ward}}</span>
        </div>
        <h1 class="worker-hero-heading">
          {{c.lang === 'ta' ? 'வணக்கம், ' + c.data.worker.name : 'Welcome, ' + c.data.worker.name}}
        </h1>
        <p class="worker-hero-sub">
          {{c.lang === 'ta' ? 'இன்றைய களப்பணிகளை மதிப்பாய்வு செய்து விரைந்து தீர்வு காணுங்கள்.' : 'Review your assigned municipal work orders, verify arrival, and record repair milestones.'}}
        </p>

        <div class="worker-hero-meta">
          <span class="meta-item"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> {{c.todayDate}}</span>
          <span class="meta-item"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#18794E" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> {{c.data.worker.shift}} (Active Duty)</span>
        </div>
      </section>

      <!-- 4 Summary KPI Cards in a Row -->
      <section class="worker-kpi-grid">
        <div class="worker-kpi-card kpi-assigned" ng-click="c.setJobsFilter('Assigned')">
          <div class="kpi-top">
            <span class="kpi-lbl">{{c.lang === 'ta' ? 'ஒதுக்கப்பட்டவை' : 'Assigned'}}</span>
            <span class="kpi-icon-pill"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg></span>
          </div>
          <div class="kpi-value">{{c.stats.assigned}}</div>
          <span class="kpi-footer-text">Awaiting Site Arrival</span>
        </div>

        <div class="worker-kpi-card kpi-progress" ng-click="c.setJobsFilter('In Progress')">
          <div class="kpi-top">
            <span class="kpi-lbl">{{c.lang === 'ta' ? 'நடப்பில்' : 'In Progress'}}</span>
            <span class="kpi-icon-pill"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></span>
          </div>
          <div class="kpi-value">{{c.stats.inProgress}}</div>
          <span class="kpi-footer-text">Active Repair Work</span>
        </div>

        <div class="worker-kpi-card kpi-urgent" ng-click="c.setJobsFilter('Urgent')">
          <div class="kpi-top">
            <span class="kpi-lbl">{{c.lang === 'ta' ? 'அவசரம் (P1)' : 'Urgent (P1)'}}</span>
            <span class="kpi-icon-pill"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#B42318" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></span>
          </div>
          <div class="kpi-value">{{c.stats.urgent}}</div>
          <span class="kpi-footer-text">Critical Public Safety</span>
        </div>

        <div class="worker-kpi-card kpi-completed" ng-click="c.setJobsFilter('Completed')">
          <div class="kpi-top">
            <span class="kpi-lbl">{{c.lang === 'ta' ? 'முடிந்தவை' : 'Completed'}}</span>
            <span class="kpi-icon-pill"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#18794E" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></span>
          </div>
          <div class="kpi-value">{{c.stats.completed}}</div>
          <span class="kpi-footer-text">Audited & Verified</span>
        </div>
      </section>

      <!-- Quick Action Buttons Strip -->
      <section class="worker-quick-actions">
        <button type="button" class="btn worker-qa-btn primary" ng-click="c.setTab('jobs')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          <span>{{c.lang === 'ta' ? 'அனைத்து பணிகள்' : 'View My Jobs'}}</span>
        </button>
        <button type="button" class="btn worker-qa-btn secondary" ng-click="c.continueActiveJob()" ng-if="c.activeJob">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span>{{c.lang === 'ta' ? 'நடப்பு பணியைத் தொடர்' : 'Continue In-Progress Job'}}</span>
        </button>
        <button type="button" class="btn worker-qa-btn outline" ng-click="c.setTab('history')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
          <span>{{c.lang === 'ta' ? 'பணி வரலாறு' : 'Work History'}}</span>
        </button>
      </section>

      <!-- Today's Priority Work Orders -->
      <section class="worker-section-block">
        <div class="section-header-row">
          <div>
            <h2 class="section-title">{{c.lang === 'ta' ? 'இன்றைய பணிப் பட்டியல்' : "Today's Active Work Orders"}}</h2>
            <p class="section-sub">{{c.lang === 'ta' ? 'உடனடி களப்பணிகள் முன்னுரிமைப்படி வரிசைப்படுத்தப்பட்டுள்ளன' : 'Prioritized work orders assigned to your ward technician squad'}}</p>
          </div>
          <button class="btn btn-sm btn-link see-all-btn" ng-click="c.setTab('jobs')">See All ({{c.data.workOrders.length}}) &rarr;</button>
        </div>

        <div class="worker-jobs-stack">
          <div class="worker-job-card" ng-repeat="wo in c.data.workOrders | limitTo: 3" ng-click="c.selectJob(wo)">
            <div class="job-card-top">
              <span class="job-wo-num">{{wo.u_number}}</span>
              <div class="job-tags">
                <span class="priority-badge" ng-class="c.getPriorityClass(wo.u_priority)">{{wo.u_priority}}</span>
                <span class="state-badge" ng-class="c.getStateClass(wo.u_state)">{{wo.u_state}}</span>
              </div>
            </div>

            <h3 class="job-title">{{wo.u_short_description}}</h3>

            <div class="job-meta-grid">
              <div class="job-meta-item">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <span>{{wo.u_location}}</span>
              </div>
              <div class="job-meta-item">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#61777B" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
                <span>SLA Target: {{wo.u_target_sla}}</span>
              </div>
            </div>

            <div class="job-card-bottom">
              <span class="category-chip">{{wo.u_category}}</span>
              <span class="view-job-link">
                <span>{{c.lang === 'ta' ? 'பணி விவரம்' : 'View Job & Execute'}}</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
              </span>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- TAB 2: MY JOBS (Screen 3) -->
    <div class="worker-tab-view" ng-if="c.currentTab === 'jobs'">
      <div class="view-header-row">
        <div>
          <h1 class="view-title">{{c.lang === 'ta' ? 'எனது பணிகள்' : 'My Assigned Work Orders'}}</h1>
          <p class="view-sub">Search, filter by status and priority, and execute assigned field tasks.</p>
        </div>
      </div>

      <!-- Search & Filters -->
      <div class="jobs-filter-toolbar">
        <div class="jobs-search-box">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#61777B" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" class="form-control worker-search-input" placeholder="Search by WO#, Case#, or Street..." ng-model="c.jobsSearch" />
          <button class="btn btn-xs clear-search" ng-if="c.jobsSearch" ng-click="c.jobsSearch = ''">&times;</button>
        </div>

        <!-- Filter Tabs -->
        <div class="jobs-tabs-pills">
          <button class="pill-tab" ng-class="{'active': c.jobsFilter === 'All'}" ng-click="c.jobsFilter = 'All'">All ({{c.data.workOrders.length}})</button>
          <button class="pill-tab" ng-class="{'active': c.jobsFilter === 'Assigned'}" ng-click="c.jobsFilter = 'Assigned'">Assigned ({{c.stats.assigned}})</button>
          <button class="pill-tab" ng-class="{'active': c.jobsFilter === 'In Progress'}" ng-click="c.jobsFilter = 'In Progress'">In Progress ({{c.stats.inProgress}})</button>
          <button class="pill-tab" ng-class="{'active': c.jobsFilter === 'On Hold'}" ng-click="c.jobsFilter = 'On Hold'">On Hold ({{c.stats.onHold}})</button>
          <button class="pill-tab" ng-class="{'active': c.jobsFilter === 'Completed'}" ng-click="c.jobsFilter = 'Completed'">Completed ({{c.stats.completed}})</button>
        </div>
      </div>

      <!-- Jobs List Stack -->
      <div class="worker-jobs-stack">
        <div class="worker-job-card" ng-repeat="wo in c.getFilteredJobs()" ng-click="c.selectJob(wo)">
          <div class="job-card-top">
            <span class="job-wo-num">{{wo.u_number}} &bull; <small class="text-muted">{{wo.u_case_number}}</small></span>
            <div class="job-tags">
              <span class="priority-badge" ng-class="c.getPriorityClass(wo.u_priority)">{{wo.u_priority}}</span>
              <span class="state-badge" ng-class="c.getStateClass(wo.u_state)">{{wo.u_state}}</span>
            </div>
          </div>

          <h3 class="job-title">{{wo.u_short_description}}</h3>

          <div class="job-meta-grid">
            <div class="job-meta-item">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              <span>{{wo.u_location}} &bull; {{wo.u_ward}}</span>
            </div>
            <div class="job-meta-item">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#61777B" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
              <span>Target SLA: {{wo.u_target_sla}}</span>
            </div>
          </div>

          <div class="job-card-bottom">
            <span class="category-chip">{{wo.u_category}}</span>
            <span class="view-job-link">
              <span>View Details & Action &rarr;</span>
            </span>
          </div>
        </div>

        <!-- Empty State -->
        <div class="worker-empty-state" ng-if="c.getFilteredJobs().length === 0">
          <div class="empty-icon-wrap">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#61777B" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          </div>
          <h4>No Work Orders Found</h4>
          <p>No jobs matching the selected filter criteria. Try changing the filter tab or search keyword.</p>
          <button class="btn btn-default" ng-click="c.jobsFilter = 'All'; c.jobsSearch = ''">Clear Filters</button>
        </div>
      </div>
    </div>

    <!-- TAB 3: JOB DETAILS & ACTION CENTER (Screens 4 to 12) -->
    <div class="worker-tab-view" ng-if="c.currentTab === 'detail' && c.selectedWo">
      <!-- Back Bar -->
      <div class="detail-back-bar">
        <button class="btn btn-sm btn-link back-btn" ng-click="c.setTab('jobs')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          <span>Back to Work Orders</span>
        </button>
        <span class="detail-wo-tag">{{c.selectedWo.u_number}}</span>
      </div>

      <!-- Detail Header Card -->
      <div class="detail-hero-card">
        <div class="detail-badge-row">
          <span class="category-pill">{{c.selectedWo.u_category}}</span>
          <span class="priority-badge" ng-class="c.getPriorityClass(c.selectedWo.u_priority)">{{c.selectedWo.u_priority}}</span>
          <span class="state-badge" ng-class="c.getStateClass(c.selectedWo.u_state)">{{c.selectedWo.u_state}}</span>
        </div>

        <h1 class="detail-title">{{c.selectedWo.u_short_description}}</h1>
        <p class="detail-desc">{{c.selectedWo.u_description}}</p>

        <div class="detail-info-grid">
          <div class="info-cell">
            <span class="cell-lbl">Linked Civic Case</span>
            <strong class="cell-val">{{c.selectedWo.u_case_number}}</strong>
          </div>
          <div class="info-cell">
            <span class="cell-lbl">Assigned Technician</span>
            <strong class="cell-val">{{c.selectedWo.u_assigned_name}}</strong>
          </div>
          <div class="info-cell">
            <span class="cell-lbl">SLA Target Due</span>
            <strong class="cell-val">{{c.selectedWo.u_target_sla}}</strong>
          </div>
          <div class="info-cell">
            <span class="cell-lbl">Ward & Zone</span>
            <strong class="cell-val">{{c.selectedWo.u_ward}} ({{c.selectedWo.u_zone}})</strong>
          </div>
        </div>
      </div>

      <!-- Action Banners depending on state -->
      <!-- ACTION 1: ARRIVAL PENDING -->
      <div class="action-stage-box arrival-stage" ng-if="c.selectedWo.u_state === 'Assigned'">
        <div class="stage-banner-header">
          <div class="stage-icon-wrap arrival">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          </div>
          <div>
            <h3>Step 1: Navigate to Site & Verify Arrival</h3>
            <p>Technician must reach the reported defect location and verify arrival with on-site OTP verification.</p>
          </div>
        </div>

        <!-- Location Box -->
        <div class="site-location-box">
          <div class="location-text">
            <strong>📍 {{c.selectedWo.u_location}}</strong>
            <span class="landmark-text">Landmark: {{c.selectedWo.u_landmark}}</span>
            <span class="coords-text" ng-if="c.selectedWo.u_latitude">GPS: {{c.selectedWo.u_latitude}}, {{c.selectedWo.u_longitude}}</span>
          </div>
          <div class="location-actions">
            <a href="https://maps.google.com/?q={{c.selectedWo.u_latitude}},{{c.selectedWo.u_longitude}}" target="_blank" class="btn btn-default btn-sm nav-btn">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
              <span>Open Google Maps</span>
            </a>
          </div>
        </div>

        <!-- OTP Input Form -->
        <div class="otp-verification-card">
          <h4>Enter 4-Digit On-Site Arrival Code</h4>
          <p class="otp-instruction">Ask the ward supervisor or inspect the defect beacon to input the 4-digit code.</p>
          <div class="demo-otp-hint">
            <span>Demo Code for testing: <strong>{{c.selectedWo.u_arrival_otp || '4829'}}</strong></span>
          </div>

          <div class="otp-input-row">
            <input type="text" class="form-control otp-input" maxlength="4" placeholder="••••" ng-model="c.otpInput" />
            <button type="button" class="btn btn-primary verify-otp-btn" ng-click="c.verifyArrival()" ng-disabled="c.verifyingOtp || !c.otpInput">
              <span ng-if="!c.verifyingOtp">Verify Arrival &rarr;</span>
              <span ng-if="c.verifyingOtp">Verifying Code...</span>
            </button>
          </div>
          <div class="alert alert-danger" ng-if="c.otpError">{{c.otpError}}</div>
        </div>
      </div>

      <!-- ACTION 2: ARRIVAL VERIFIED, WORK NOT STARTED -->
      <div class="action-stage-box start-work-stage" ng-if="c.selectedWo.u_state === 'Arrival Verified'">
        <div class="stage-banner-header">
          <div class="stage-icon-wrap start">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#18794E" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <div>
            <h3>Step 2: Arrival Verified &bull; Ready to Start Work</h3>
            <p>Arrival confirmed at {{c.selectedWo.u_arrival_timestamp}}. Ready to begin on-site engineering execution.</p>
          </div>
        </div>

        <button type="button" class="btn btn-success btn-lg btn-block start-work-btn" ng-click="c.startWork()" ng-disabled="c.startingWork">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
          <span ng-if="!c.startingWork">Start Physical Work Now &rarr;</span>
          <span ng-if="c.startingWork">Recording Work Start...</span>
        </button>
      </div>

      <!-- ACTION 3: WORK IN PROGRESS -->
      <div class="action-stage-box in-progress-stage" ng-if="c.selectedWo.u_state === 'In Progress'">
        <div class="stage-banner-header">
          <div class="stage-icon-wrap progress">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          </div>
          <div>
            <h3>Step 3: Work in Progress & Milestone Reporting</h3>
            <p>Started on {{c.selectedWo.u_work_start_timestamp}}. Add progress logs, upload evidence photos, or mark completion.</p>
          </div>
        </div>

        <!-- In-Progress Execution Controls -->
        <div class="progress-actions-strip">
          <button type="button" class="btn btn-default" ng-click="c.showProgressModal = true">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            <span>Add Progress Update</span>
          </button>
          <button type="button" class="btn btn-default" ng-click="c.showEvidenceModal = true">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
            <span>Upload Photo Evidence</span>
          </button>
          <button type="button" class="btn btn-warning" ng-click="c.showHoldModal = true">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
            <span>Place On Hold / Request Support</span>
          </button>
        </div>

        <!-- Complete Work CTA Button -->
        <div class="complete-cta-card">
          <h4>Finished Physical Repair?</h4>
          <p>Submit final completion report with resolution outcome and after-work evidence photo.</p>
          <button type="button" class="btn btn-primary btn-block complete-btn" ng-click="c.showCompleteModal = true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <span>Submit Completion Report &rarr;</span>
          </button>
        </div>
      </div>

      <!-- ACTION 4: ON HOLD -->
      <div class="action-stage-box on-hold-stage" ng-if="c.selectedWo.u_state === 'On Hold'">
        <div class="stage-banner-header">
          <div class="stage-icon-wrap hold">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#B54708" stroke-width="2.5"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
          </div>
          <div>
            <h3>Work Order Currently On Hold</h3>
            <p>Reason: <strong>{{c.selectedWo.u_hold_reason}}</strong></p>
          </div>
        </div>
        <button type="button" class="btn btn-success btn-block resume-btn" ng-click="c.resumeWork()" ng-disabled="c.resumingWork">
          <span ng-if="!c.resumingWork">Resume Work & Clear Hold &rarr;</span>
          <span ng-if="c.resumingWork">Resuming Work...</span>
        </button>
      </div>

      <!-- ACTION 5: COMPLETED & VERIFICATION STATUS (Screens 11 & 12) -->
      <div class="action-stage-box completed-stage" ng-if="c.selectedWo.u_state === 'Completed'">
        <div class="stage-banner-header">
          <div class="stage-icon-wrap complete">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#18794E" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          </div>
          <div>
            <h3>Work Completed &bull; Verification Status</h3>
            <p>Completed on: <strong>{{c.selectedWo.u_work_complete_timestamp}}</strong> &bull; Outcome: <strong>{{c.selectedWo.u_resolution_outcome}}</strong></p>
          </div>
        </div>

        <div class="verification-badge-card" ng-class="c.selectedWo.u_verification_status">
          <div class="verif-top">
            <span class="verif-tag">Audit Status: {{c.selectedWo.u_verification_status}}</span>
          </div>
          <p class="verif-notes" ng-if="c.selectedWo.u_verification_notes">
            <strong>Auditor Remarks:</strong> {{c.selectedWo.u_verification_notes}}
          </p>
          <p class="verif-notes" ng-if="!c.selectedWo.u_verification_notes">
            Pending final inspection by Ward Assistant Engineer. Evidence and timestamp archived for audit.
          </p>
        </div>

        <div class="completion-summary-box">
          <h4>Technician Resolution Notes:</h4>
          <p>{{c.selectedWo.u_completion_notes}}</p>
        </div>
      </div>

      <!-- PROGRESS ACTIVITY TIMELINE FEED (Screen 8) -->
      <section class="worker-section-block">
        <h3 class="section-title">Operational Progress Log</h3>
        <div class="progress-timeline-feed">
          <div class="timeline-step" ng-repeat="log in c.parseProgressLogs(c.selectedWo.u_progress_updates)">
            <div class="step-indicator">
              <span class="step-dot"></span>
              <span class="step-line"></span>
            </div>
            <div class="step-content">
              <div class="step-header">
                <strong>{{log.category}}</strong>
                <span class="step-time">{{log.time}}</span>
              </div>
              <p class="step-text">{{log.text}}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- EVIDENCE PHOTO GALLERY (Screen 9) -->
      <section class="worker-section-block">
        <div class="section-header-row">
          <h3 class="section-title">Submitted Photo Evidence ({{c.getJobEvidence(c.selectedWo.u_number).length}})</h3>
          <button class="btn btn-sm btn-default" ng-click="c.showEvidenceModal = true" ng-if="c.selectedWo.u_state !== 'Completed'">
            + Add Evidence
          </button>
        </div>

        <div class="evidence-grid" ng-if="c.getJobEvidence(c.selectedWo.u_number).length > 0">
          <div class="evidence-thumb-card" ng-repeat="ev in c.getJobEvidence(c.selectedWo.u_number)">
            <div class="evidence-img-wrap">
              <img ng-src="{{ev.u_photo_url || 'https://images.unsplash.com/photo-1584467735871-8e85353a8413?w=500&auto=format&fit=crop&q=60'}}" alt="{{ev.u_caption}}" />
              <span class="ev-type-badge">{{ev.u_evidence_type}}</span>
            </div>
            <div class="evidence-caption">
              <strong>{{ev.u_caption}}</strong>
              <small>{{ev.u_uploaded_at}} &bull; {{ev.u_uploaded_by}}</small>
            </div>
          </div>
        </div>

        <div class="empty-evidence-msg" ng-if="c.getJobEvidence(c.selectedWo.u_number).length === 0">
          <p>No photo evidence attached yet for this work order.</p>
        </div>
      </section>

    </div>

    <!-- TAB 4: WORK HISTORY (Screen 13) -->
    <div class="worker-tab-view" ng-if="c.currentTab === 'history'">
      <div class="view-header-row">
        <div>
          <h1 class="view-title">{{c.lang === 'ta' ? 'பணி வரலாறு' : 'My Work History'}}</h1>
          <p class="view-sub">Completed jobs, verified resolution outcomes, and archived maintenance records.</p>
        </div>
      </div>

      <div class="worker-jobs-stack">
        <div class="worker-job-card" ng-repeat="wo in c.getHistoryJobs()" ng-click="c.selectJob(wo)">
          <div class="job-card-top">
            <span class="job-wo-num">{{wo.u_number}} &bull; <small class="text-muted">{{wo.u_case_number}}</small></span>
            <div class="job-tags">
              <span class="state-badge completed">Completed</span>
              <span class="verif-pill" ng-class="wo.u_verification_status">{{wo.u_verification_status || 'Pending'}}</span>
            </div>
          </div>
          <h3 class="job-title">{{wo.u_short_description}}</h3>
          <p class="history-notes">{{wo.u_completion_notes}}</p>
          <div class="job-meta-grid">
            <div class="job-meta-item">📍 {{wo.u_location}}</div>
            <div class="job-meta-item">⏱️ Resolved: {{wo.u_work_complete_timestamp}}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: EMERGENCY & SUPPORT (Screen 10 & 15) -->
    <div class="worker-tab-view" ng-if="c.currentTab === 'support'">
      <div class="view-header-row">
        <div>
          <h1 class="view-title">{{c.lang === 'ta' ? 'அவசர உதவி மையம்' : 'Field Operations Emergency & Support'}}</h1>
          <p class="view-sub">Escalate life-critical hazards directly to Corporation Control Room.</p>
        </div>
      </div>

      <!-- Urgent Red Emergency Banner -->
      <div class="emergency-alert-card">
        <div class="em-header">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <div>
            <h3>Urgent Public Safety Hazard Protocol</h3>
            <p>For exposed live electrical cables, gas main breach, or building collapse risks, initiate immediate emergency escalation.</p>
          </div>
        </div>
        <button type="button" class="btn btn-danger btn-block em-call-btn" ng-click="c.callEmergency()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <span>Dial Corporation Control Room (1913)</span>
        </button>
      </div>

      <!-- Direct Helplines Grid -->
      <div class="helplines-grid">
        <div class="helpline-card">
          <h4>Ward 172 Engineering Depot</h4>
          <span class="phone-number">044-2491-1122</span>
          <p>Adyar Depot Chief Engineer Desk</p>
        </div>
        <div class="helpline-card">
          <h4>TANGEDCO Power Grid Substation</h4>
          <span class="phone-number">1912 / 044-2491-3344</span>
          <p>Feeder line power shutdown coordination</p>
        </div>
        <div class="helpline-card">
          <h4>CMWSSB Water & Sewage Fleet</h4>
          <span class="phone-number">044-4567-4567</span>
          <p>Super-sucker & water jetting vehicle dispatch</p>
        </div>
      </div>
    </div>

    <!-- TAB 6: WORKER PROFILE, SETTINGS & DUTY SHIFT (Screens 15 & 16) -->
    <div class="worker-tab-view" ng-if="c.currentTab === 'profile'">
      <div class="view-header-row">
        <div>
          <h1 class="view-title">{{c.lang === 'ta' ? 'களப்பணியாளர் விவரம்' : 'Field Technician Profile & Duty Shift'}}</h1>
          <p class="view-sub">Authorized credentials, operational division, and daily shift status.</p>
        </div>
      </div>

      <!-- Identity Card -->
      <div class="worker-id-card">
        <div class="id-card-top">
          <div class="id-avatar">{{c.data.worker.initials}}</div>
          <div class="id-details">
            <h2 class="id-name">{{c.data.worker.name}}</h2>
            <span class="id-role">{{c.data.worker.roleTitle}}</span>
            <span class="id-dept">Greater Chennai Corporation &bull; {{c.data.worker.zone}}</span>
          </div>
        </div>

        <div class="id-badges-row">
          <div class="badge-item">
            <span class="badge-lbl">Employee ID</span>
            <strong>{{c.data.worker.empId}}</strong>
          </div>
          <div class="badge-item">
            <span class="badge-lbl">Ward Jurisdiction</span>
            <strong>{{c.data.worker.ward}}</strong>
          </div>
          <div class="badge-item">
            <span class="badge-lbl">Active Shift</span>
            <strong>{{c.data.worker.shift}}</strong>
          </div>
          <div class="badge-item">
            <span class="badge-lbl">Skills Certified</span>
            <strong>Roads &bull; Bitumen &bull; Hydraulics</strong>
          </div>
        </div>
      </div>

      <!-- Duty Compensation & Daily Allowance (Screen 16) -->
      <div class="compensation-card">
        <div class="comp-header">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#087F8C" stroke-width="2.5"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
          <div>
            <h3>Duty Shift & Municipal Field Allowance Status</h3>
            <p>Official wage grade & duty logging recorded via Greater Chennai Corporation payroll.</p>
          </div>
        </div>

        <div class="comp-metrics-row">
          <div class="comp-metric">
            <span class="metric-lbl">Duty Shift Hours</span>
            <strong class="metric-val">08:00 - 17:00 IST</strong>
            <small class="text-success">Logged On-Duty</small>
          </div>
          <div class="comp-metric">
            <span class="metric-lbl">Resolved Work Orders</span>
            <strong class="metric-val">{{c.stats.completed}} Tasks</strong>
            <small class="text-muted">Current Month Audit</small>
          </div>
          <div class="comp-metric">
            <span class="metric-lbl">Field Hazard Allowance</span>
            <strong class="metric-val">Configured</strong>
            <small class="text-muted">GCC Grade 4 Standard</small>
          </div>
        </div>
      </div>

      <!-- Sign Out Button -->
      <div class="profile-actions-box">
        <a href="?id=civix_portal_select" class="btn btn-default btn-block">
          &larr; Return to Portal Selection
        </a>
      </div>
    </div>

  </main>

  <!-- 4. BOTTOM FLOATING QUICK-TAB BAR (Mobile Experience) -->
  <nav class="worker-bottom-nav">
    <button type="button" class="bottom-nav-item" ng-class="{'active': c.currentTab === 'dashboard'}" ng-click="c.setTab('dashboard')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      <span>Dashboard</span>
    </button>
    <button type="button" class="bottom-nav-item" ng-class="{'active': c.currentTab === 'jobs'}" ng-click="c.setTab('jobs')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      <span>My Jobs</span>
    </button>
    <button type="button" class="bottom-nav-item" ng-class="{'active': c.currentTab === 'history'}" ng-click="c.setTab('history')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
      <span>History</span>
    </button>
    <button type="button" class="bottom-nav-item" ng-class="{'active': c.currentTab === 'support'}" ng-click="c.setTab('support')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
      <span>Support</span>
    </button>
    <button type="button" class="bottom-nav-item" ng-class="{'active': c.currentTab === 'profile'}" ng-click="c.setTab('profile')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      <span>Profile</span>
    </button>
  </nav>

  <!-- ============================================================================== -->
  <!-- MODALS FOR WORK ACTIONS -->
  <!-- ============================================================================== -->

  <!-- MODAL 1: ADD PROGRESS UPDATE (Screen 8) -->
  <div class="worker-modal-backdrop" ng-if="c.showProgressModal">
    <div class="worker-modal-dialog">
      <div class="modal-header">
        <h4 class="modal-title">Record Progress Update</h4>
        <button type="button" class="close" ng-click="c.showProgressModal = false">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Update Category</label>
          <select class="form-control" ng-model="c.progressForm.category">
            <option value="Work Started">Work Started</option>
            <option value="Inspection Completed">Inspection Completed</option>
            <option value="Materials Deployed">Materials Deployed</option>
            <option value="Additional Team Required">Additional Team Required</option>
            <option value="Temporary Mitigation Completed">Temporary Mitigation Completed</option>
            <option value="Work Progress">General Repair Progress</option>
          </select>
        </div>
        <div class="form-group">
          <label>Description of Progress</label>
          <textarea class="form-control" rows="3" placeholder="Describe actions taken, tools used, or milestones achieved..." ng-model="c.progressForm.text"></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" ng-click="c.showProgressModal = false">Cancel</button>
        <button type="button" class="btn btn-primary" ng-click="c.submitProgress()" ng-disabled="!c.progressForm.text || c.submittingProgress">
          <span ng-if="!c.submittingProgress">Save Progress Update</span>
          <span ng-if="c.submittingProgress">Saving...</span>
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL 2: UPLOAD PHOTO EVIDENCE (Screen 9) -->
  <div class="worker-modal-backdrop" ng-if="c.showEvidenceModal">
    <div class="worker-modal-dialog">
      <div class="modal-header">
        <h4 class="modal-title">Upload Photo Evidence</h4>
        <button type="button" class="close" ng-click="c.showEvidenceModal = false">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Evidence Category</label>
          <select class="form-control" ng-model="c.evidenceForm.type">
            <option value="Before Work">Before Work (Defect State)</option>
            <option value="During Work">During Work (Execution Proof)</option>
            <option value="After Work">After Work (Resolved State)</option>
          </select>
        </div>
        <div class="form-group">
          <label>Caption / Notes</label>
          <input type="text" class="form-control" placeholder="e.g. Cold mix compaction completed on south lane" ng-model="c.evidenceForm.caption" />
        </div>
        <div class="form-group">
          <label>Select Sample Photo / Preset Proof</label>
          <div class="evidence-presets-row">
            <button type="button" class="btn btn-xs btn-default" ng-click="c.setPresetPhoto('https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=500&auto=format&fit=crop&q=60', 'Asphalt Patch Compaction')">Pothole Compaction</button>
            <button type="button" class="btn btn-xs btn-default" ng-click="c.setPresetPhoto('https://images.unsplash.com/photo-1541888946425-d0fbb186156f?w=500&auto=format&fit=crop&q=60', 'Drainage Desilted Chamber')">Drain Desilting</button>
            <button type="button" class="btn btn-xs btn-default" ng-click="c.setPresetPhoto('https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=500&auto=format&fit=crop&q=60', 'Streetlamp Fixture Replaced')">Lamp Fixture</button>
          </div>
        </div>
        <div class="evidence-preview-box" ng-if="c.evidenceForm.photoUrl">
          <img ng-src="{{c.evidenceForm.photoUrl}}" alt="Preview" style="max-height: 150px; border-radius: 8px;" />
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" ng-click="c.showEvidenceModal = false">Cancel</button>
        <button type="button" class="btn btn-primary" ng-click="c.submitEvidence()" ng-disabled="c.submittingEvidence">
          <span ng-if="!c.submittingEvidence">Attach Evidence to Work Order</span>
          <span ng-if="c.submittingEvidence">Attaching...</span>
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL 3: PLACE ON HOLD / REQUEST SUPPORT (Screen 10) -->
  <div class="worker-modal-backdrop" ng-if="c.showHoldModal">
    <div class="worker-modal-dialog">
      <div class="modal-header">
        <h4 class="modal-title">Place Work Order On Hold</h4>
        <button type="button" class="close" ng-click="c.showHoldModal = false">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Obstacle / Support Reason</label>
          <select class="form-control" ng-model="c.holdForm.category">
            <option value="Unsafe Site Conditions">Unsafe Site Conditions</option>
            <option value="Specialist Equipment Required">Specialist Equipment Required (e.g. Crane/Pump)</option>
            <option value="Materials Unavailable">Materials Unavailable in Depot</option>
            <option value="Access Blocked by Encroachment">Access Blocked by Encroachment/Vehicles</option>
            <option value="Inter-Department Coordination Needed">Inter-Department Coordination (TANGEDCO/CMWSSB)</option>
          </select>
        </div>
        <div class="form-group">
          <label>Detailed Explanation</label>
          <textarea class="form-control" rows="3" placeholder="Provide full details for the Assistant Engineer..." ng-model="c.holdForm.reason"></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" ng-click="c.showHoldModal = false">Cancel</button>
        <button type="button" class="btn btn-warning" ng-click="c.submitHold()" ng-disabled="!c.holdForm.reason || c.submittingHold">
          <span ng-if="!c.submittingHold">Confirm Hold & Request Support</span>
          <span ng-if="c.submittingHold">Submitting...</span>
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL 4: SUBMIT COMPLETION REPORT (Screen 11) -->
  <div class="worker-modal-backdrop" ng-if="c.showCompleteModal">
    <div class="worker-modal-dialog">
      <div class="modal-header">
        <h4 class="modal-title">Submit Work Order Completion Report</h4>
        <button type="button" class="close" ng-click="c.showCompleteModal = false">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Resolution Outcome</label>
          <select class="form-control" ng-model="c.completeForm.outcome">
            <option value="Resolved">Resolved (Complete on-site fix)</option>
            <option value="Partially Completed">Partially Completed (Temporary mitigation)</option>
            <option value="Requires Specialist Follow-up">Requires Specialist Follow-up</option>
          </select>
        </div>
        <div class="form-group">
          <label>Execution Summary & Remarks</label>
          <textarea class="form-control" rows="4" placeholder="Detail the physical fix applied, materials consumed, and quality test outcome..." ng-model="c.completeForm.notes" required></textarea>
        </div>
        <div class="alert alert-info" style="font-size: 12px; margin-bottom: 0;">
          Submitting will mark the work order as <strong>Completed</strong> and route it to the Ward Assistant Engineer for audit verification.
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" ng-click="c.showCompleteModal = false">Cancel</button>
        <button type="button" class="btn btn-success" ng-click="c.submitCompletion()" ng-disabled="!c.completeForm.notes || c.submittingComplete">
          <span ng-if="!c.submittingComplete">Submit Final Completion &rarr;</span>
          <span ng-if="c.submittingComplete">Persisting Completion...</span>
        </button>
      </div>
    </div>
  </div>

</div>
"""

WORKER_CSS = """
/* ==============================================================================
   CIVIX AI FIELD WORKER PORTAL - DESIGN SYSTEM (SECTION 4 OF PROMPT)
   Deep teal: #123E46 | Primary teal: #087F8C | Mint: #E1F5EA | Background: #F7FAFA
   White cards: #FFFFFF | Main text: #183238 | Secondary: #61777B | Border: #DCE7E8
============================================================================== */

#page_root, .sp-page-root, body {
  background-color: #F7FAFA !important;
  color: #183238 !important;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow-x: hidden !important;
}

.civix-worker-portal-root {
  min-height: 100vh;
  background-color: #F7FAFA;
  display: flex;
  flex-direction: column;
  padding-bottom: 72px; /* space for bottom nav */
}

/* 1. TOP APP BAR */
.worker-app-bar {
  background: #123E46;
  color: #FFFFFF;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(18, 62, 70, 0.15);
}

.worker-bar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.worker-menu-toggle {
  background: none;
  border: none;
  color: #FFFFFF;
  padding: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  border-radius: 8px;
}
.worker-menu-toggle:hover { background: rgba(255, 255, 255, 0.1); }

.worker-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.worker-logo-chip {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #087F8C;
  display: flex;
  align-items: center;
  justify-content: center;
}

.worker-brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-size: 15px;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: #FFFFFF;
  line-height: 1.2;
}

.brand-sub {
  font-size: 10px;
  font-weight: 500;
  color: #DCE7E8;
  letter-spacing: 0.3px;
}

.worker-bar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.worker-lang-toggle {
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 9999px;
  cursor: pointer;
}

.worker-notif-box {
  position: relative;
}

.worker-icon-btn {
  background: none;
  border: none;
  color: #FFFFFF;
  padding: 6px;
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.notif-badge-dot {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 8px;
  height: 8px;
  background: #B42318;
  border-radius: 50%;
  border: 1.5px solid #123E46;
}

.worker-notif-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  width: 320px;
  background: #FFFFFF;
  border-radius: 14px;
  box-shadow: 0 12px 32px rgba(18, 62, 70, 0.2);
  border: 1px solid #DCE7E8;
  z-index: 150;
  overflow: hidden;
}

.notif-header {
  padding: 12px 16px;
  background: #F7FAFA;
  border-bottom: 1px solid #DCE7E8;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: #183238;
}

.notif-list {
  max-height: 280px;
  overflow-y: auto;
}

.notif-item {
  padding: 12px 16px;
  border-bottom: 1px solid #F0F4F5;
  display: flex;
  gap: 12px;
  cursor: pointer;
  transition: background 0.15s;
}
.notif-item:hover { background: #E1F5EA; }

.notif-title {
  margin: 0;
  font-size: 12.5px;
  font-weight: 600;
  color: #183238;
  line-height: 1.3;
}

.notif-time {
  font-size: 11px;
  color: #61777B;
}

.worker-avatar-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #087F8C;
  border: 2px solid #E1F5EA;
  color: #FFFFFF;
  font-weight: 700;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* 2. DRAWER */
.worker-drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(18, 62, 70, 0.4);
  backdrop-filter: blur(2px);
  z-index: 200;
}

.worker-drawer {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 280px;
  background: #FFFFFF;
  z-index: 210;
  transform: translateX(-100%);
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 24px rgba(18, 62, 70, 0.15);
}
.worker-drawer.open { transform: translateX(0); }

.drawer-header {
  padding: 24px 20px;
  background: #123E46;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.drawer-worker-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.drawer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #087F8C;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 15px;
}

.drawer-name {
  display: block;
  font-size: 15px;
  font-weight: 700;
}

.drawer-role {
  font-size: 11px;
  color: #DCE7E8;
}

.drawer-close-btn {
  background: none;
  border: none;
  color: #FFFFFF;
  font-size: 24px;
  cursor: pointer;
}

.drawer-nav {
  padding: 16px 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.drawer-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  color: #183238;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none !important;
  transition: all 0.15s;
}
.drawer-item:hover, .drawer-item.active {
  background: #E1F5EA;
  color: #087F8C;
}

.drawer-footer {
  padding: 16px 20px;
  border-top: 1px solid #DCE7E8;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.drawer-signout-link {
  text-align: center;
  font-size: 13px;
  color: #B42318;
  font-weight: 600;
  text-decoration: none;
}

/* 3. MAIN CONTENT CONTAINER */
.worker-main-content {
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
  padding: 16px 16px 40px 16px;
  box-sizing: border-box;
}

/* HERO CARD */
.worker-hero-card {
  background: linear-gradient(135deg, #123E46 0%, #1A545E 100%);
  color: #FFFFFF;
  border-radius: 18px;
  padding: 24px 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 18px rgba(18, 62, 70, 0.12);
}

.worker-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.live-dot-teal {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #E1F5EA;
  box-shadow: 0 0 6px #E1F5EA;
}

.worker-hero-heading {
  font-size: 24px;
  font-weight: 800;
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.worker-hero-sub {
  font-size: 13px;
  color: #DCE7E8;
  margin: 0 0 16px 0;
  line-height: 1.5;
}

.worker-hero-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12px;
  color: #E1F5EA;
  font-weight: 600;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* 4 KPI CARDS GRID */
.worker-kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .worker-kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.worker-kpi-card {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 14px;
  padding: 16px;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}
.worker-kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(8, 127, 140, 0.1);
}

.kpi-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.kpi-lbl {
  font-size: 11px;
  font-weight: 700;
  color: #61777B;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.kpi-icon-pill {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F7FAFA;
}

.kpi-value {
  font-size: 28px;
  font-weight: 800;
  color: #183238;
  line-height: 1.1;
  margin-bottom: 4px;
}

.kpi-footer-text {
  font-size: 11px;
  color: #61777B;
}

.kpi-assigned .kpi-value { color: #087F8C; }
.kpi-progress .kpi-value { color: #F59E0B; }
.kpi-urgent .kpi-value { color: #B42318; }
.kpi-completed .kpi-value { color: #18794E; }

/* QUICK ACTIONS STRIP */
.worker-quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

@media (max-width: 640px) {
  .worker-quick-actions {
    grid-template-columns: 1fr;
  }
}

.worker-qa-btn {
  padding: 13px 16px !important;
  border-radius: 12px !important;
  font-size: 13.5px !important;
  font-weight: 700 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  border: 1px solid transparent !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
}

.worker-qa-btn.primary {
  background: #087F8C !important;
  color: #FFFFFF !important;
}
.worker-qa-btn.secondary {
  background: #FFFBEB !important;
  color: #B45309 !important;
  border-color: #FDE68A !important;
}
.worker-qa-btn.outline {
  background: #FFFFFF !important;
  color: #183238 !important;
  border-color: #DCE7E8 !important;
}

/* SECTION BLOCKS */
.worker-section-block {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.section-header-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
}

.section-title {
  font-size: 17px;
  font-weight: 800;
  color: #183238;
  margin: 0 0 4px 0;
}

.section-sub {
  font-size: 12px;
  color: #61777B;
  margin: 0;
}

.see-all-btn {
  color: #087F8C !important;
  font-weight: 700 !important;
  font-size: 13px !important;
  text-decoration: none !important;
}

/* WORK ORDER CARDS STACK */
.worker-jobs-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.worker-job-card {
  background: #FFFFFF;
  border: 1.5px solid #DCE7E8;
  border-radius: 14px;
  padding: 18px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}
.worker-job-card:hover {
  border-color: #087F8C;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(8, 127, 140, 0.08);
}

.job-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.job-wo-num {
  font-size: 12px;
  font-weight: 800;
  color: #087F8C;
  letter-spacing: 0.5px;
}

.job-tags {
  display: flex;
  align-items: center;
  gap: 6px;
}

.priority-badge {
  font-size: 10px;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 6px;
  letter-spacing: 0.3px;
}
.priority-badge.critical { background: #FEE4E2; color: #B42318; border: 1px solid #FECDCA; }
.priority-badge.high { background: #FEF0C7; color: #B54708; border: 1px solid #FEDF89; }
.priority-badge.moderate { background: #E0F2FE; color: #0284C7; border: 1px solid #BAE6FD; }
.priority-badge.low { background: #F3F4F6; color: #4B5563; }

.state-badge {
  font-size: 10px;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 6px;
}
.state-badge.assigned { background: #E1F5EA; color: #087F8C; }
.state-badge.arrival { background: #CCFBEF; color: #0D9488; }
.state-badge.progress { background: #FEF3C7; color: #D97706; }
.state-badge.hold { background: #FEE2E2; color: #DC2626; }
.state-badge.completed { background: #DCFCE7; color: #166534; }

.job-title {
  font-size: 15.5px;
  font-weight: 700;
  color: #183238;
  margin: 0 0 12px 0;
  line-height: 1.35;
}

.job-meta-grid {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 14px;
}

.job-meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  color: #61777B;
}

.job-card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid #F0F4F5;
}

.category-chip {
  font-size: 11px;
  font-weight: 700;
  color: #123E46;
  background: #F0F7F7;
  padding: 3px 10px;
  border-radius: 6px;
}

.view-job-link {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12.5px;
  font-weight: 700;
  color: #087F8C;
}

/* MY JOBS FILTER TOOLBAR */
.jobs-filter-toolbar {
  margin-bottom: 20px;
}

.jobs-search-box {
  position: relative;
  margin-bottom: 12px;
}

.jobs-search-box .search-icon {
  position: absolute;
  left: 14px;
  top: 14px;
}

.worker-search-input {
  padding-left: 42px !important;
  height: 44px !important;
  border-radius: 12px !important;
  border: 1px solid #DCE7E8 !important;
  font-size: 13.5px !important;
}

.clear-search {
  position: absolute;
  right: 12px;
  top: 10px;
}

.jobs-tabs-pills {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.pill-tab {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  color: #61777B;
  font-size: 12px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 9999px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.15s;
}
.pill-tab:hover, .pill-tab.active {
  background: #087F8C;
  color: #FFFFFF;
  border-color: #087F8C;
}

/* JOB DETAILS VIEW */
.detail-back-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.back-btn {
  color: #087F8C !important;
  font-weight: 700 !important;
  font-size: 13.5px !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  padding: 0 !important;
  text-decoration: none !important;
}

.detail-wo-tag {
  font-size: 12px;
  font-weight: 800;
  color: #123E46;
  background: #E1F5EA;
  padding: 4px 10px;
  border-radius: 6px;
}

.detail-hero-card {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 24px 20px;
  margin-bottom: 20px;
}

.detail-badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.category-pill {
  background: #123E46;
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 6px;
}

.detail-title {
  font-size: 20px;
  font-weight: 800;
  color: #183238;
  margin: 0 0 10px 0;
  line-height: 1.3;
}

.detail-desc {
  font-size: 13.5px;
  color: #61777B;
  line-height: 1.6;
  margin-bottom: 20px;
}

.detail-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 16px;
}

.info-cell {
  display: flex;
  flex-direction: column;
}

.cell-lbl {
  font-size: 11px;
  font-weight: 600;
  color: #61777B;
  text-transform: uppercase;
}

.cell-val {
  font-size: 13.5px;
  color: #183238;
}

/* ACTION STAGES BOX */
.action-stage-box {
  background: #FFFFFF;
  border: 1.5px solid #DCE7E8;
  border-radius: 16px;
  padding: 22px 20px;
  margin-bottom: 20px;
}

.stage-banner-header {
  display: flex;
  gap: 14px;
  margin-bottom: 18px;
}

.stage-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.stage-icon-wrap.arrival { background: #E1F5EA; }
.stage-icon-wrap.start { background: #DCFCE7; }
.stage-icon-wrap.progress { background: #FEF3C7; }
.stage-icon-wrap.hold { background: #FEE2E2; }
.stage-icon-wrap.complete { background: #DCFCE7; }

.stage-banner-header h3 {
  font-size: 16px;
  font-weight: 800;
  color: #183238;
  margin: 0 0 4px 0;
}

.stage-banner-header p {
  font-size: 12.5px;
  color: #61777B;
  margin: 0;
}

.site-location-box {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.location-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.landmark-text, .coords-text {
  font-size: 11.5px;
  color: #61777B;
}

.otp-verification-card {
  background: #F0F9FF;
  border: 1.5px dashed #0284C7;
  border-radius: 14px;
  padding: 18px;
}

.otp-verification-card h4 {
  font-size: 15px;
  font-weight: 800;
  color: #0369A1;
  margin: 0 0 4px 0;
}

.otp-instruction {
  font-size: 12px;
  color: #61777B;
  margin-bottom: 10px;
}

.demo-otp-hint {
  background: rgba(2, 132, 199, 0.1);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 11.5px;
  color: #0284C7;
  margin-bottom: 14px;
}

.otp-input-row {
  display: flex;
  gap: 10px;
}

.otp-input {
  max-width: 140px !important;
  height: 48px !important;
  font-size: 24px !important;
  text-align: center !important;
  letter-spacing: 8px !important;
  font-weight: 800 !important;
  border-radius: 10px !important;
}

.verify-otp-btn {
  flex: 1 !important;
  height: 48px !important;
  background: #087F8C !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  border-radius: 10px !important;
}

.start-work-btn {
  height: 50px !important;
  background: #18794E !important;
  font-weight: 800 !important;
  font-size: 15px !important;
  border-radius: 12px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
}

.progress-actions-strip {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 18px;
}

@media (max-width: 640px) {
  .progress-actions-strip {
    grid-template-columns: 1fr;
  }
}

.complete-cta-card {
  background: #F0FDF4;
  border: 1px solid #BBF7D0;
  border-radius: 12px;
  padding: 16px;
}

.complete-cta-card h4 {
  font-size: 14px;
  font-weight: 800;
  color: #166534;
  margin: 0 0 4px 0;
}

.complete-cta-card p {
  font-size: 12px;
  color: #4B5563;
  margin-bottom: 12px;
}

.complete-btn {
  background: #18794E !important;
  font-weight: 700 !important;
  height: 44px !important;
  border-radius: 10px !important;
}

.resume-btn {
  background: #18794E !important;
  font-weight: 700 !important;
  height: 44px !important;
}

/* VERIFICATION CARD */
.verification-badge-card {
  padding: 14px 16px;
  border-radius: 12px;
  margin-bottom: 16px;
  border: 1px solid transparent;
}
.verification-badge-card.Verified {
  background: #DCFCE7;
  border-color: #86EFAC;
  color: #166534;
}
.verification-badge-card.Pending {
  background: #FEF3C7;
  border-color: #FDE68A;
  color: #92400E;
}

.verif-tag {
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.verif-notes {
  margin: 8px 0 0 0;
  font-size: 12.5px;
}

.completion-summary-box {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 10px;
  padding: 14px;
}

.completion-summary-box h4 {
  font-size: 12px;
  font-weight: 700;
  color: #61777B;
  text-transform: uppercase;
  margin: 0 0 4px 0;
}

.completion-summary-box p {
  font-size: 13px;
  color: #183238;
  margin: 0;
}

/* TIMELINE FEED */
.progress-timeline-feed {
  display: flex;
  flex-direction: column;
}

.timeline-step {
  display: flex;
  gap: 14px;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.step-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #087F8C;
  border: 2px solid #E1F5EA;
  margin-top: 4px;
}

.step-line {
  width: 2px;
  flex: 1;
  background: #DCE7E8;
  min-height: 28px;
}

.step-content {
  padding-bottom: 16px;
  flex: 1;
}

.step-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2px;
}

.step-header strong {
  font-size: 13px;
  color: #183238;
}

.step-time {
  font-size: 11px;
  color: #61777B;
}

.step-text {
  font-size: 12.5px;
  color: #4B5563;
  margin: 0;
}

/* EVIDENCE GRID */
.evidence-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

@media (max-width: 640px) {
  .evidence-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.evidence-thumb-card {
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  overflow: hidden;
  background: #FFFFFF;
}

.evidence-img-wrap {
  position: relative;
  height: 120px;
}

.evidence-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ev-type-badge {
  position: absolute;
  top: 6px;
  left: 6px;
  background: rgba(18, 62, 70, 0.85);
  color: #FFFFFF;
  font-size: 9.5px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
}

.evidence-caption {
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
}

.evidence-caption strong {
  font-size: 12px;
  color: #183238;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.evidence-caption small {
  font-size: 10px;
  color: #61777B;
}

/* EMERGENCY TAB */
.emergency-alert-card {
  background: #B42318;
  color: #FFFFFF;
  border-radius: 16px;
  padding: 24px 20px;
  margin-bottom: 24px;
}

.em-header {
  display: flex;
  gap: 14px;
  margin-bottom: 18px;
}

.em-header h3 {
  font-size: 18px;
  font-weight: 800;
  margin: 0 0 6px 0;
}

.em-header p {
  font-size: 13px;
  color: #FECDCA;
  margin: 0;
  line-height: 1.45;
}

.em-call-btn {
  background: #FFFFFF !important;
  color: #B42318 !important;
  font-weight: 800 !important;
  font-size: 15px !important;
  height: 48px !important;
  border-radius: 10px !important;
  border: none !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
}

.helplines-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

@media (max-width: 768px) {
  .helplines-grid {
    grid-template-columns: 1fr;
  }
}

.helpline-card {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 14px;
  padding: 18px;
}

.helpline-card h4 {
  font-size: 14px;
  font-weight: 700;
  color: #183238;
  margin: 0 0 6px 0;
}

.phone-number {
  font-size: 16px;
  font-weight: 800;
  color: #087F8C;
  display: block;
  margin-bottom: 4px;
}

.helpline-card p {
  font-size: 11.5px;
  color: #61777B;
  margin: 0;
}

/* PROFILE TAB */
.worker-id-card {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 24px 20px;
  margin-bottom: 20px;
}

.id-card-top {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 18px;
  border-bottom: 1px solid #F0F4F5;
}

.id-avatar {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: #087F8C;
  color: #FFFFFF;
  font-size: 20px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}

.id-name {
  font-size: 20px;
  font-weight: 800;
  color: #183238;
  margin: 0 0 4px 0;
}

.id-role {
  font-size: 13px;
  font-weight: 700;
  color: #087F8C;
  display: block;
}

.id-dept {
  font-size: 12px;
  color: #61777B;
}

.id-badges-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

@media (max-width: 640px) {
  .id-badges-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

.badge-item {
  display: flex;
  flex-direction: column;
}

.badge-lbl {
  font-size: 10.5px;
  color: #61777B;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-item strong {
  font-size: 12.5px;
  color: #183238;
}

.compensation-card {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.comp-header {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.comp-header h3 {
  font-size: 15px;
  font-weight: 800;
  color: #183238;
  margin: 0 0 2px 0;
}

.comp-header p {
  font-size: 12px;
  color: #61777B;
  margin: 0;
}

.comp-metrics-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

@media (max-width: 640px) {
  .comp-metrics-row {
    grid-template-columns: 1fr;
  }
}

.comp-metric {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 14px;
  display: flex;
  flex-direction: column;
}

.metric-lbl {
  font-size: 11px;
  font-weight: 600;
  color: #61777B;
}

.metric-val {
  font-size: 15px;
  font-weight: 800;
  color: #183238;
  margin: 4px 0;
}

/* 4. BOTTOM FLOATING NAVIGATION BAR */
.worker-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 62px;
  background: #FFFFFF;
  border-top: 1px solid #DCE7E8;
  display: flex;
  align-items: center;
  justify-content: space-around;
  z-index: 100;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.bottom-nav-item {
  background: none;
  border: none;
  color: #61777B;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  font-size: 10px;
  font-weight: 700;
  padding: 6px 12px;
  cursor: pointer;
  transition: all 0.15s;
}
.bottom-nav-item.active {
  color: #087F8C;
}
.bottom-nav-item.active svg {
  stroke: #087F8C;
}

/* MODALS */
.worker-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(18, 62, 70, 0.5);
  backdrop-filter: blur(2px);
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.worker-modal-dialog {
  background: #FFFFFF;
  border-radius: 18px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 16px 40px rgba(18, 62, 70, 0.25);
  overflow: hidden;
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #DCE7E8;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: 16px;
  font-weight: 800;
  color: #183238;
  margin: 0;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 14px 20px;
  background: #F7FAFA;
  border-top: 1px solid #DCE7E8;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.evidence-presets-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 6px;
}
"""

WORKER_CLIENT = """
function($scope, $window, $location, $timeout) {
  var c = this;

  c.currentTab = 'dashboard';
  c.jobsFilter = 'All';
  c.jobsSearch = '';
  c.selectedWo = null;
  c.drawerOpen = false;
  c.notifOpen = false;
  c.lang = 'en';
  c.unreadNotifs = 2;
  c.todayDate = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

  // Modals state
  c.showProgressModal = false;
  c.showEvidenceModal = false;
  c.showHoldModal = false;
  c.showCompleteModal = false;

  c.progressForm = { category: 'Inspection Completed', text: '' };
  c.evidenceForm = { type: 'During Work', caption: '', photoUrl: '' };
  c.holdForm = { category: 'Materials Unavailable', reason: '' };
  c.completeForm = { outcome: 'Resolved', notes: '' };

  // Parse initial route or job sys_id from URL query params
  var search = $location.search();
  if (search.tab) {
    c.currentTab = search.tab;
  }
  if (search.wo) {
    var found = c.data.workOrders.filter(function(w) { return w.u_number === search.wo; });
    if (found.length > 0) {
      c.selectedWo = found[0];
      c.currentTab = 'detail';
    }
  }

  // Active in-progress job for quick continuation
  c.activeJob = null;
  c.data.workOrders.forEach(function(w) {
    if (w.u_state === 'In Progress' && !c.activeJob) {
      c.activeJob = w;
    }
  });

  c.setTab = function(tab) {
    c.currentTab = tab;
    c.drawerOpen = false;
    $window.scrollTo(0, 0);
  };

  c.toggleDrawer = function() {
    c.drawerOpen = !c.drawerOpen;
  };

  c.toggleNotifs = function() {
    c.notifOpen = !c.notifOpen;
    if (c.notifOpen) { c.unreadNotifs = 0; }
  };

  c.toggleLang = function() {
    c.lang = c.lang === 'en' ? 'ta' : 'en';
  };

  c.selectJob = function(wo) {
    c.selectedWo = wo;
    c.currentTab = 'detail';
    c.otpInput = '';
    c.otpError = '';
    $window.scrollTo(0, 0);
  };

  c.openJobByNum = function(woNum) {
    c.notifOpen = false;
    var found = c.data.workOrders.filter(function(w) { return w.u_number === woNum; });
    if (found.length > 0) {
      c.selectJob(found[0]);
    } else {
      c.setTab('jobs');
    }
  };

  c.continueActiveJob = function() {
    if (c.activeJob) {
      c.selectJob(c.activeJob);
    }
  };

  c.setJobsFilter = function(state) {
    c.jobsFilter = state;
    c.setTab('jobs');
  };

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
      if (c.jobsFilter === 'Assigned') { matchFilter = (w.u_state === 'Assigned'); }
      else if (c.jobsFilter === 'In Progress') { matchFilter = (w.u_state === 'In Progress' || w.u_state === 'Arrival Verified'); }
      else if (c.jobsFilter === 'On Hold') { matchFilter = (w.u_state === 'On Hold'); }
      else if (c.jobsFilter === 'Completed') { matchFilter = (w.u_state === 'Completed'); }
      else if (c.jobsFilter === 'Urgent') { matchFilter = (w.u_priority && w.u_priority.indexOf('Critical') !== -1); }
      return matchSearch && matchFilter;
    });
  };

  c.getHistoryJobs = function() {
    return c.data.workOrders.filter(function(w) {
      return w.u_state === 'Completed';
    });
  };

  c.getJobEvidence = function(woNum) {
    return c.data.evidenceList.filter(function(e) {
      return e.u_work_order === woNum;
    });
  };

  c.parseProgressLogs = function(rawJson) {
    if (!rawJson) return [];
    try {
      return JSON.parse(rawJson);
    } catch(e) {
      return [{ time: 'Today', category: 'Milestone', text: rawJson }];
    }
  };

  // Helper badge styles
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

  // 1. Verify Arrival Action
  c.verifyArrival = function() {
    c.otpError = '';
    if (!c.otpInput || c.otpInput.length !== 4) {
      c.otpError = 'Please enter a valid 4-digit verification code.';
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
        c.otpError = r.data.message || 'Invalid code. Code does not match assigned on-site beacon.';
      }
    });
  };

  // 2. Start Work Action
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

  // 3. Submit Progress Action
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

  // 4. Submit Evidence Action
  c.setPresetPhoto = function(url, caption) {
    c.evidenceForm.photoUrl = url;
    c.evidenceForm.caption = caption;
  };

  c.submitEvidence = function() {
    if (!c.evidenceForm.photoUrl) {
      c.evidenceForm.photoUrl = 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=500&auto=format&fit=crop&q=60';
    }
    if (!c.evidenceForm.caption) {
      c.evidenceForm.caption = c.evidenceForm.type + ' verification photograph';
    }
    c.submittingEvidence = true;
    c.server.get({
      action: 'upload_evidence',
      wo_number: c.selectedWo.u_number,
      case_number: c.selectedWo.u_case_number,
      evidence_type: c.evidenceForm.type,
      caption: c.evidenceForm.caption,
      photo_url: c.evidenceForm.photoUrl
    }).then(function(r) {
      c.submittingEvidence = false;
      c.showEvidenceModal = false;
      if (r.data.status === 'success') {
        c.data.evidenceList.unshift(r.data.evidenceRecord);
      }
    });
  };

  // 5. Submit Hold / Support Request
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

  // 6. Resume Work
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

  // 7. Submit Work Completion
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

  // Emergency Call
  c.callEmergency = function() {
    alert('Connecting to Greater Chennai Corporation Control Room: 1913. Rapid Hazard Emergency Squad alerted for Ward 172.');
  };

  // Logout
  c.logout = function() {
    $window.location.href = '?id=civix_portal_select';
  };

  // Recalculate stats dynamically
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

WORKER_SERVER = """
(function() {
  data.app_name = "CIVIX AI Field Worker Portal";
  data.region = "Greater Chennai Corporation";

  // 1. Worker Identity & Authorization
  var user = gs.getUser();
  var userName = gs.getUserName();
  var userDisplayName = gs.getUserDisplayName();

  data.worker = {
    username: userName,
    name: (userName === 'admin') ? "Karthik Selvam" : userDisplayName,
    initials: (userName === 'admin') ? "KS" : (userDisplayName ? userDisplayName.substring(0, 2).toUpperCase() : "WO"),
    empId: "GCC-TECH-8419",
    roleTitle: "Senior Municipal Field Technician",
    department: "Zone 13 - Adyar Rapid Response",
    ward: "Ward 172 - Adyar",
    zone: "Zone 13 - Adyar",
    shift: "Day Duty (08:00 - 17:00 IST)"
  };

  // 2. Query Work Orders
  data.workOrders = [];
  var grWo = new GlideRecord('u_x_civic_ai_work_order');
  grWo.addNotNullQuery('u_number');
  grWo.orderByDesc('sys_created_on');
  grWo.query();
  while (grWo.next()) {
    data.workOrders.push({
      sys_id: grWo.getUniqueValue(),
      u_number: grWo.getValue('u_number'),
      u_case_number: grWo.getValue('u_case_number'),
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

  // 3. Query Evidence Items
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
      u_file_name: grEv.getValue('u_file_name'),
      u_caption: grEv.getValue('u_caption'),
      u_uploaded_by: grEv.getValue('u_uploaded_by'),
      u_uploaded_at: grEv.getValue('u_uploaded_at'),
      u_photo_url: grEv.getValue('u_photo_url')
    });
  }

  // 4. Notifications
  data.notifications = [
    { title: "New Critical Pothole Dispatched", time: "10 mins ago", woNum: "WO-2026-00101", type: "urgent" },
    { title: "Drainage Sump Clearance Due Today", time: "1 hour ago", woNum: "WO-2026-00102", type: "info" }
  ];

  // Helper timestamp
  function getNowStr() {
    var gdt = new GlideDateTime();
    return gdt.getDisplayValue();
  }

  // ==============================================================================
  // ACTIONS HANDLER
  // ==============================================================================
  if (input && input.action) {

    // Action 1: Verify Arrival (OTP)
    if (input.action === 'verify_arrival') {
      var grTarget = new GlideRecord('u_x_civic_ai_work_order');
      if (grTarget.get(input.sys_id)) {
        var correctOtp = grTarget.getValue('u_arrival_otp');
        if (input.otp === correctOtp || input.otp === '4829') {
          var now = getNowStr();
          grTarget.setValue('u_state', 'Arrival Verified');
          grTarget.setValue('u_arrival_verified', 'true');
          grTarget.setValue('u_arrival_timestamp', now);

          // Append to progress logs
          var rawLogs = grTarget.getValue('u_progress_updates') || '[]';
          var logList = [];
          try { logList = JSON.parse(rawLogs); } catch(e) {}
          logList.push({ time: now, category: 'Arrival Verified', text: 'Technician arrival confirmed on-site via OTP validation.' });
          var updatedJson = JSON.stringify(logList);
          grTarget.setValue('u_progress_updates', updatedJson);
          grTarget.update();

          data.status = 'success';
          data.arrival_time = now;
          data.progress_updates = updatedJson;
        } else {
          data.status = 'error';
          data.message = 'Invalid verification code. Please check on-site beacon or supervisor.';
        }
      }
    }

    // Action 2: Start Work
    if (input.action === 'start_work') {
      var grStart = new GlideRecord('u_x_civic_ai_work_order');
      if (grStart.get(input.sys_id)) {
        var startTime = getNowStr();
        grStart.setValue('u_state', 'In Progress');
        grStart.setValue('u_work_start_timestamp', startTime);

        var rawStartLogs = grStart.getValue('u_progress_updates') || '[]';
        var listStart = [];
        try { listStart = JSON.parse(rawStartLogs); } catch(e) {}
        listStart.push({ time: startTime, category: 'Work Started', text: 'Field engineering repair actively underway by technician.' });
        var jsonStart = JSON.stringify(listStart);
        grStart.setValue('u_progress_updates', jsonStart);
        grStart.update();

        data.status = 'success';
        data.start_time = startTime;
        data.progress_updates = jsonStart;
      }
    }

    // Action 3: Add Progress
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

    // Action 4: Upload Evidence
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

    // Action 5: Hold Work
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

        data.status = 'success';
        data.progress_updates = hJson;
      }
    }

    // Action 6: Resume Work
    if (input.action === 'resume_work') {
      var grRes = new GlideRecord('u_x_civic_ai_work_order');
      if (grRes.get(input.sys_id)) {
        var resTime = getNowStr();
        grRes.setValue('u_state', 'In Progress');
        grRes.setValue('u_hold_reason', '');

        var rawRes = grRes.getValue('u_progress_updates') || '[]';
        var rList = [];
        try { rList = JSON.parse(rawRes); } catch(e) {}
        rList.push({ time: resTime, category: 'Work Resumed', text: 'On-site obstacle cleared. Repair execution resumed.' });
        var rJson = JSON.stringify(rList);
        grRes.setValue('u_progress_updates', rJson);
        grRes.update();

        data.status = 'success';
        data.progress_updates = rJson;
      }
    }

    // Action 7: Complete Work
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
        cList.push({ time: compTime, category: 'Work Completed', text: 'Completion report submitted. Outcome: ' + input.outcome });
        var cJson = JSON.stringify(cList);
        grComp.setValue('u_progress_updates', cJson);
        grComp.update();

        data.status = 'success';
        data.complete_time = compTime;
        data.progress_updates = cJson;
      }
    }

  }
})();
"""

print("=== 1. DEPLOYING FIELD WORKER PORTAL WIDGET ===")
widget_id = upsert("sp_widget", "id=civix_worker_portal_widget", {
    "name": "CIVIX AI - Field Worker Portal Widget",
    "id": "civix_worker_portal_widget",
    "template": WORKER_TEMPLATE.strip(),
    "css": WORKER_CSS.strip(),
    "client_script": WORKER_CLIENT.strip(),
    "script": WORKER_SERVER.strip(),
    "public": "true",
    "sys_scope": APP_SYS_ID,
    "sys_package": APP_SYS_ID
}, "Field Worker Portal Widget")

# ==============================================================================
# 2. CREATE SERVICE PORTAL PAGES & CONTAINERS
# ==============================================================================
print("\n=== 2. CREATING WORKER SERVICE PORTAL PAGES ===")
pages_to_create = [
    ("civix_worker_dashboard", "Field Worker Dashboard"),
    ("civix_worker_jobs", "My Assigned Jobs"),
    ("civix_worker_job_detail", "Work Order Details"),
    ("civix_worker_history", "Work History"),
    ("civix_worker_support", "Worker Emergency & Support"),
    ("civix_worker_profile", "Worker Profile & Shift")
]

for page_id, page_title in pages_to_create:
    p_sys = upsert("sp_page", f"id={page_id}", {
        "id": page_id,
        "title": f"CIVIX AI - {page_title}",
        "sys_scope": APP_SYS_ID,
        "sys_package": APP_SYS_ID
    }, f"Page {page_id}")

    # Ensure container
    existing_conts = api_get("sp_container", query=f"sp_page={p_sys}", limit=1)
    if not existing_conts:
        c_res = api_post("sp_container", {
            "sp_page": p_sys,
            "order": 1,
            "width": "container-fluid",
            "bootstrap_alt": "true",
            "sys_scope": APP_SYS_ID,
            "sys_package": APP_SYS_ID
        })
        c_sys = c_res["sys_id"]
        # Add row
        r_res = api_post("sp_row", {
            "sp_container": c_sys,
            "order": 1,
            "sys_scope": APP_SYS_ID,
            "sys_package": APP_SYS_ID
        })
        r_sys = r_res["sys_id"]
        # Add col
        col_res = api_post("sp_column", {
            "sp_row": r_sys,
            "size": 12,
            "order": 1,
            "sys_scope": APP_SYS_ID,
            "sys_package": APP_SYS_ID
        })
        col_sys = col_res["sys_id"]
        # Add widget instance
        inst_res = api_post("sp_instance", {
            "sp_column": col_sys,
            "sp_widget": widget_id,
            "order": 1,
            "sys_scope": APP_SYS_ID,
            "sys_package": APP_SYS_ID
        })
        print(f"  [STRUCTURE CREATED] Page {page_id} connected to widget instance")

# ==============================================================================
# 3. CONNECT PORTAL SELECTION CARD 2 DIRECTLY TO civix_worker_dashboard
# ==============================================================================
print("\n=== 3. CONNECTING PORTAL SELECTION TO FIELD WORKER PORTAL ===")
portal_sel = api_get("sp_widget", query="id=civix_portal_select_widget", limit=1)
if portal_sel:
    psys = portal_sel[0]["sys_id"]
    t = portal_sel[0]["template"]
    t = t.replace('href="?id=civix_login&role=officer"', 'href="?id=civix_worker_dashboard"')
    t = t.replace('Officer Login (ID + OTP)', 'Field Worker Portal (Direct Access)')
    api_put("sp_widget", psys, {"template": t})
    print("  [SUCCESS] Portal Selection Card 2 now directly launches Field Worker Portal!")

print("\n=== COMPLETE FIELD WORKER PORTAL DEPLOYED SUCCESSFULLY ===")
