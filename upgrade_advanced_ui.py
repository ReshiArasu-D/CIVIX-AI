"""
CIVIX AI - Advanced UI16-grade Interactive Portal Upgrade
Fixes full-bleed page alignment, eliminates Bootstrap container wrapping,
adds fluid layout, rich micro-animations, interactive AI bot, and crisp SVG visuals.
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

TEMPLATE = """
<div class="civix-viewport-shell">
  <!-- 1. FULL HEIGHT FIXED LEFT SIDEBAR -->
  <aside class="civix-sidebar" role="navigation" aria-label="Sidebar Navigation">
    <div class="civix-sidebar-glow-bg"></div>
    <div class="civix-sidebar-inner">
      <!-- Brand Logo -->
      <div class="civix-brand-block">
        <a href="?id=civix_home" class="civix-brand-link">
          <div class="civix-city-emblem">
            <svg class="civix-city-svg" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="2" y="14" width="6" height="20" rx="1.5" fill="#3B82F6"/>
              <rect x="10" y="7" width="8" height="27" rx="1.5" fill="#2563EB"/>
              <rect x="20" y="3" width="8" height="31" rx="1.5" fill="#1D4ED8"/>
              <rect x="30" y="11" width="5" height="23" rx="1.5" fill="#60A5FA"/>
              <!-- Lit Windows -->
              <circle cx="5" cy="18" r="1" fill="#DBEAFE"/>
              <circle cx="5" cy="23" r="1" fill="#DBEAFE"/>
              <circle cx="14" cy="12" r="1" fill="#EFF6FF"/>
              <circle cx="14" cy="17" r="1" fill="#EFF6FF"/>
              <circle cx="14" cy="22" r="1" fill="#EFF6FF"/>
              <circle cx="24" cy="8" r="1" fill="#FFFFFF"/>
              <circle cx="24" cy="13" r="1" fill="#FFFFFF"/>
              <circle cx="24" cy="18" r="1" fill="#FFFFFF"/>
              <circle cx="24" cy="23" r="1" fill="#FFFFFF"/>
            </svg>
          </div>
          <div class="civix-brand-headings">
            <span class="civix-brand-title">CIVIX AI</span>
            <span class="civix-brand-motto">Smart Cities. Safer Communities.</span>
          </div>
        </a>
      </div>

      <!-- Navigation Menu with animated pills -->
      <nav class="civix-sidebar-menu">
        <a href="?id=civix_home" class="civix-menu-item active" ng-click="c.setActiveMenu('dashboard')">
          <span class="civix-menu-icon"><i class="glyphicon glyphicon-home"></i></span>
          <span class="civix-menu-text">Dashboard</span>
        </a>
        <a href="?id=civix_report_issue" class="civix-menu-item" ng-click="c.setActiveMenu('report')">
          <span class="civix-menu-icon"><i class="glyphicon glyphicon-edit"></i></span>
          <span class="civix-menu-text">Report an Issue</span>
        </a>
        <a href="?id=civix_my_cases" class="civix-menu-item" ng-click="c.setActiveMenu('complaints')">
          <span class="civix-menu-icon"><i class="glyphicon glyphicon-list-alt"></i></span>
          <span class="civix-menu-text">My Complaints</span>
        </a>
        <a href="?id=civix_landing#services" class="civix-menu-item" ng-click="c.setActiveMenu('services')">
          <span class="civix-menu-icon"><i class="glyphicon glyphicon-info-sign"></i></span>
          <span class="civix-menu-text">Service Information</span>
        </a>
        <a href="?id=civix_landing#trust" class="civix-menu-item" ng-click="c.setActiveMenu('help')">
          <span class="civix-menu-icon"><i class="glyphicon glyphicon-headphones"></i></span>
          <span class="civix-menu-text">Help & Support</span>
        </a>
      </nav>

      <!-- Sidebar Bottom Motto with Green Leaf -->
      <div class="civix-sidebar-foot">
        <div class="civix-leaf-box">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>
            <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>
          </svg>
        </div>
        <div class="civix-foot-motto-text">
          <span>Clean Cities</span>
          <span>Green Communities</span>
          <span>Better Tomorrows</span>
        </div>
      </div>
    </div>
  </aside>

  <!-- 2. MAIN APPLICATION WORKSPACE -->
  <div class="civix-workspace">
    <!-- STICKY TOPBAR -->
    <header class="civix-top-header" role="banner">
      <!-- Search Input with Focus Animation -->
      <div class="civix-search-container">
        <div class="civix-search-bar-pill">
          <span class="glyphicon glyphicon-search civix-search-lens"></span>
          <input type="text" class="civix-search-field" placeholder="Search services, complaints or help..." ng-model="c.searchQuery" ng-keydown="c.onSearchKey($event)" />
          <span ng-if="c.searchQuery" class="glyphicon glyphicon-remove civix-clear-search" ng-click="c.searchQuery = ''"></span>
        </div>
      </div>

      <!-- Right Actions: Language, Notification, Profile -->
      <div class="civix-header-actions">
        <!-- 22 Languages Interactive Dropdown -->
        <div class="civix-lang-component">
          <button type="button" class="civix-lang-trigger" ng-click="c.toggleLang()" aria-expanded="{{c.langOpen}}" aria-label="Select Interface Language">
            <span class="glyphicon glyphicon-globe civix-globe-icon"></span>
            <span class="civix-lang-label">{{c.currentLangDisplay}}</span>
            <span class="glyphicon glyphicon-chevron-down civix-lang-arrow"></span>
          </button>

          <!-- Dropdown Popover -->
          <div class="civix-lang-popover" ng-show="c.langOpen">
            <div class="civix-lang-popover-header">
              <span class="glyphicon glyphicon-search"></span>
              <input type="text" ng-model="c.langFilter" placeholder="Filter languages..." class="civix-lang-search-mini" />
            </div>
            <div class="civix-lang-scroll-body">
              <button type="button" ng-repeat="l in c.languages | filter:c.langFilter" 
                      class="civix-lang-opt-row" 
                      ng-class="{'active': c.selectedLang === l.code}"
                      ng-click="c.chooseLang(l)">
                <span class="civix-lang-badge" style="background: {{l.bg}}">{{l.prefix}}</span>
                <span class="civix-lang-native-name">{{l.native}}</span>
                <span class="civix-lang-en-name">{{l.name}}</span>
                <span ng-if="c.selectedLang === l.code" class="glyphicon glyphicon-ok civix-lang-checked"></span>
              </button>
            </div>
          </div>
        </div>

        <!-- Notification Bell with Ripple Pulse -->
        <a href="#alerts" class="civix-notif-button" title="3 Unread Municipal Alerts" aria-label="3 Alerts">
          <span class="glyphicon glyphicon-bell"></span>
          <span class="civix-pulse-ring"></span>
          <span class="civix-bell-count">3</span>
        </a>

        <!-- Profile Chip with Avatar -->
        <div class="civix-user-profile-chip" ng-click="c.toggleProfileMenu()">
          <div class="civix-user-avatar-wrap">
            <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=120&auto=format&fit=crop&q=80" alt="Priya Sharma" class="civix-avatar-img" />
            <span class="civix-online-badge"></span>
          </div>
          <span class="civix-user-name-text">{{c.data.citizenName}}</span>
          <span class="glyphicon glyphicon-chevron-down civix-profile-arrow"></span>
        </div>
      </div>
    </header>

    <!-- MAIN SCROLLABLE CONTENT BODY -->
    <div class="civix-scroll-body">
      <!-- 1. HERO BANNER ROW -->
      <section class="civix-banner-grid">
        <!-- Welcome Card with Skyline Silhouette -->
        <div class="civix-hero-welcome-card">
          <div class="civix-hero-skyline-overlay"></div>
          <div class="civix-hero-content-col">
            <h1 class="civix-hero-big-greeting">Welcome back,<br/><span class="civix-name-gradient">{{c.data.citizenName}}!</span> 👋</h1>
            <p class="civix-hero-tagline-main">Together for a cleaner, safer and smarter city.</p>
            <p class="civix-hero-tagline-sub">Report issues, track progress and help improve our community.</p>
          </div>

          <!-- Glassmorphism Weather & Locality Widget -->
          <div class="civix-glass-weather-widget">
            <div class="civix-weather-header">
              <span class="glyphicon glyphicon-map-marker text-primary"></span>
              <strong>Chennai, Tamil Nadu</strong>
              <span class="glyphicon glyphicon-chevron-down civix-loc-chev"></span>
            </div>
            <div class="civix-weather-split">
              <div class="civix-weather-temp-info">
                <span class="civix-temp-reading">32°C</span>
                <span class="civix-weather-condition">Mostly Clear</span>
              </div>
              <div class="civix-animated-sun-icon">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" class="civix-sun-svg">
                  <circle cx="12" cy="12" r="5" fill="#F59E0B"/>
                  <path d="M12 1v3M12 20v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M1 12h3M20 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Cleaner Cities Promo Card -->
        <div class="civix-hero-promo-card">
          <div class="civix-promo-scenic-bg"></div>
          <div class="civix-promo-gradient-shade">
            <h3 class="civix-promo-headline">Cleaner Cities<br/>Happier People</h3>
            <div class="civix-promo-line-accent"></div>
          </div>
        </div>
      </section>

      <!-- 2. 4 INTERACTIVE KPI METRIC CARDS -->
      <section class="civix-kpi-deck">
        <!-- KPI 1: Total Complaints -->
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
            <div class="civix-kpi-trend-badge trend-green">
              <span>&uarr; 3 this month</span>
            </div>
          </div>
        </a>

        <!-- KPI 2: Resolved -->
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
            <div class="civix-kpi-trend-badge trend-green">
              <span>&uarr; 2 this month</span>
            </div>
          </div>
        </a>

        <!-- KPI 3: In Progress -->
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
            <div class="civix-kpi-trend-badge trend-neutral">
              <span>&ndash; same as last month</span>
            </div>
          </div>
        </a>

        <!-- KPI 4: Awaiting Action -->
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
            <div class="civix-kpi-trend-badge trend-red">
              <span>&darr; 1 from last month</span>
            </div>
          </div>
        </a>
      </section>

      <!-- 3. TRI-PANEL WORKSPACE GRID (Left 50%, Center 27%, Right 23%) -->
      <div class="civix-tri-panel-grid">
        <!-- LEFT COLUMN: Report Issue & Recent Complaints -->
        <div class="civix-column-primary">
          <!-- Report a New Issue Card -->
          <div class="civix-white-box">
            <div class="civix-box-header">
              <h2 class="civix-box-title">Report a New Issue</h2>
              <p class="civix-box-subtitle">Select a service category to report an issue in your area.</p>
            </div>

            <!-- 5 Dynamic Animated Category Cards -->
            <div class="civix-category-cards-grid">
              <!-- Water Supply -->
              <a href="?id=civix_report_issue&cat=Water" class="civix-cat-pill-card">
                <div class="civix-cat-bubble cat-water">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
                  </svg>
                </div>
                <div class="civix-cat-title-text">Water Supply <span class="civix-arrow-accent">&rsaquo;</span></div>
                <p class="civix-cat-subtitle-text">No water, leakage, low pressure</p>
              </a>

              <!-- Electricity -->
              <a href="?id=civix_report_issue&cat=Electricity" class="civix-cat-pill-card">
                <div class="civix-cat-bubble cat-elec">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                  </svg>
                </div>
                <div class="civix-cat-title-text">Electricity <span class="civix-arrow-accent">&rsaquo;</span></div>
                <p class="civix-cat-subtitle-text">Power outage, street lights</p>
              </a>

              <!-- Roads -->
              <a href="?id=civix_report_issue&cat=Roads" class="civix-cat-pill-card">
                <div class="civix-cat-bubble cat-roads">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 19L9 5M20 19L15 5M12 8V11M12 15V17"/>
                  </svg>
                </div>
                <div class="civix-cat-title-text">Roads <span class="civix-arrow-accent">&rsaquo;</span></div>
                <p class="civix-cat-subtitle-text">Potholes, damage, maintenance</p>
              </a>

              <!-- Drainage -->
              <a href="?id=civix_report_issue&cat=Drainage" class="civix-cat-pill-card">
                <div class="civix-cat-bubble cat-drain">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2"/>
                    <line x1="3" y1="9" x2="21" y2="9"/>
                    <line x1="3" y1="15" x2="21" y2="15"/>
                    <line x1="9" y1="3" x2="9" y2="21"/>
                    <line x1="15" y1="3" x2="15" y2="21"/>
                  </svg>
                </div>
                <div class="civix-cat-title-text">Drainage <span class="civix-arrow-accent">&rsaquo;</span></div>
                <p class="civix-cat-subtitle-text">Blockage, overflow, maintenance</p>
              </a>

              <!-- Waterlogging -->
              <a href="?id=civix_report_issue&cat=Waterlogging" class="civix-cat-pill-card">
                <div class="civix-cat-bubble cat-flood">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9333EA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 12c2.5-3 5-3 7.5 0s5 3 7.5 0 5-3 7.5 0M2 17c2.5-3 5-3 7.5 0s5 3 7.5 0 5-3 7.5 0"/>
                  </svg>
                </div>
                <div class="civix-cat-title-text">Waterlogging <span class="civix-arrow-accent">&rsaquo;</span></div>
                <p class="civix-cat-subtitle-text">Rainwater, flooding, stagnation</p>
              </a>
            </div>
          </div>

          <!-- Recent Complaints List Card -->
          <div class="civix-white-box">
            <div class="civix-box-header civix-flex-split">
              <div>
                <h2 class="civix-box-title">Recent Complaints</h2>
                <p class="civix-box-subtitle">Here are your latest reported issues</p>
              </div>
              <a href="?id=civix_my_cases" class="civix-view-all-button">View All &rarr;</a>
            </div>

            <!-- Crisp Visual Complaints List -->
            <div class="civix-complaint-stack">
              <!-- Item 1: Water leakage -->
              <a href="?id=civix_track_case&sys_id={{c.data.recentCases[0].sys_id}}" class="civix-complaint-entry">
                <div class="civix-entry-thumb-box thumb-water-pipe">
                  <svg viewBox="0 0 60 48" class="civix-thumb-vector">
                    <rect width="60" height="48" fill="#E0F2FE"/>
                    <rect x="0" y="20" width="36" height="12" rx="2" fill="#0284C7"/>
                    <path d="M36 20 C42 16, 48 24, 58 14" stroke="#38BDF8" stroke-width="4" stroke-linecap="round"/>
                    <circle cx="48" cy="28" r="3" fill="#60A5FA"/>
                    <circle cx="54" cy="34" r="2" fill="#60A5FA"/>
                  </svg>
                </div>
                <div class="civix-entry-info">
                  <span class="civix-entry-ticket-id">CIVIX-2024-00123</span>
                  <h4 class="civix-entry-headline">Water leakage on 3rd Main Road</h4>
                  <div class="civix-entry-meta">
                    <span><span class="glyphicon glyphicon-map-marker text-primary"></span> Adyar, Chennai</span>
                    <span><span class="glyphicon glyphicon-calendar text-muted"></span> 15 Nov 2024, 10:24 AM</span>
                  </div>
                </div>
                <div class="civix-entry-badge-col">
                  <span class="civix-badge-pill-status pill-in-progress">In Progress</span>
                  <span class="civix-entry-arrow">&rsaquo;</span>
                </div>
              </a>

              <!-- Item 2: Street light -->
              <a href="?id=civix_track_case&sys_id={{c.data.recentCases[1].sys_id}}" class="civix-complaint-entry">
                <div class="civix-entry-thumb-box thumb-streetlight">
                  <svg viewBox="0 0 60 48" class="civix-thumb-vector">
                    <rect width="60" height="48" fill="#1E293B"/>
                    <path d="M30 48 L30 16 Q30 10 40 10" stroke="#94A3B8" stroke-width="3" fill="none"/>
                    <ellipse cx="40" cy="12" rx="6" ry="3" fill="#FBBF24"/>
                    <polygon points="36,12 28,48 52,48 44,12" fill="#FEF08A" opacity="0.35"/>
                  </svg>
                </div>
                <div class="civix-entry-info">
                  <span class="civix-entry-ticket-id">CIVIX-2024-00118</span>
                  <h4 class="civix-entry-headline">Street light not working near Anna Nagar Park</h4>
                  <div class="civix-entry-meta">
                    <span><span class="glyphicon glyphicon-map-marker text-primary"></span> Anna Nagar, Chennai</span>
                    <span><span class="glyphicon glyphicon-calendar text-muted"></span> 10 Nov 2024, 06:12 PM</span>
                  </div>
                </div>
                <div class="civix-entry-badge-col">
                  <span class="civix-badge-pill-status pill-resolved">Resolved</span>
                  <span class="civix-entry-arrow">&rsaquo;</span>
                </div>
              </a>

              <!-- Item 3: Pothole -->
              <a href="?id=civix_track_case&sys_id={{c.data.recentCases[2].sys_id}}" class="civix-complaint-entry">
                <div class="civix-entry-thumb-box thumb-pothole">
                  <svg viewBox="0 0 60 48" class="civix-thumb-vector">
                    <rect width="60" height="48" fill="#475569"/>
                    <line x1="0" y1="24" x2="60" y2="24" stroke="#FDE047" stroke-width="2" stroke-dasharray="6,4"/>
                    <ellipse cx="32" cy="24" rx="14" ry="9" fill="#1E293B"/>
                    <path d="M22 24 Q30 18 42 22 Q36 29 22 24 Z" fill="#0F172A"/>
                  </svg>
                </div>
                <div class="civix-entry-info">
                  <span class="civix-entry-ticket-id">CIVIX-2024-00110</span>
                  <h4 class="civix-entry-headline">Pothole near 100 Feet Road</h4>
                  <div class="civix-entry-meta">
                    <span><span class="glyphicon glyphicon-map-marker text-primary"></span> T. Nagar, Chennai</span>
                    <span><span class="glyphicon glyphicon-calendar text-muted"></span> 05 Nov 2024, 02:30 PM</span>
                  </div>
                </div>
                <div class="civix-entry-badge-col">
                  <span class="civix-badge-pill-status pill-resolved">Resolved</span>
                  <span class="civix-entry-arrow">&rsaquo;</span>
                </div>
              </a>

              <!-- Item 4: Drainage overflow -->
              <a href="?id=civix_track_case&sys_id={{c.data.recentCases[3].sys_id}}" class="civix-complaint-entry">
                <div class="civix-entry-thumb-box thumb-drainage">
                  <svg viewBox="0 0 60 48" class="civix-thumb-vector">
                    <rect width="60" height="48" fill="#F1F5F9"/>
                    <rect x="15" y="16" width="30" height="24" rx="3" fill="#334155"/>
                    <line x1="22" y1="16" x2="22" y2="40" stroke="#CBD5E1" stroke-width="2"/>
                    <line x1="30" y1="16" x2="30" y2="40" stroke="#CBD5E1" stroke-width="2"/>
                    <line x1="38" y1="16" x2="38" y2="40" stroke="#CBD5E1" stroke-width="2"/>
                    <path d="M12 28 Q24 20 48 30 Q30 38 12 28 Z" fill="#38BDF8" opacity="0.6"/>
                  </svg>
                </div>
                <div class="civix-entry-info">
                  <span class="civix-entry-ticket-id">CIVIX-2024-00102</span>
                  <h4 class="civix-entry-headline">Drainage overflow in residential area</h4>
                  <div class="civix-entry-meta">
                    <span><span class="glyphicon glyphicon-map-marker text-primary"></span> Velachery, Chennai</span>
                    <span><span class="glyphicon glyphicon-calendar text-muted"></span> 28 Oct 2024, 09:15 AM</span>
                  </div>
                </div>
                <div class="civix-entry-badge-col">
                  <span class="civix-badge-pill-status pill-awaiting">Awaiting Action</span>
                  <span class="civix-entry-arrow">&rsaquo;</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        <!-- CENTER COLUMN: Interactive Issue Map & Nearby Alerts -->
        <div class="civix-column-center">
          <!-- Issue Map Card -->
          <div class="civix-white-box civix-map-panel">
            <div class="civix-box-header civix-flex-split">
              <h2 class="civix-box-title">Issue Map</h2>
              <a href="?id=civix_landing#services" class="civix-view-all-button">View Full Map &rarr;</a>
            </div>

            <!-- Interactive Vector Chennai Map with Animated Radar Pulse -->
            <div class="civix-map-stage">
              <svg class="civix-map-vector" viewBox="0 0 340 230" xmlns="http://www.w3.org/2000/svg">
                <!-- Water Coastline -->
                <rect width="340" height="230" fill="#F1F5F9"/>
                <path d="M245,0 Q260,80 235,140 Q215,190 255,230 L340,230 L340,0 Z" fill="#BAE6FD"/>
                <text x="260" y="125" font-size="16" font-weight="800" fill="#0284C7" opacity="0.7" letter-spacing="1">Chennai</text>
                
                <!-- City Road Arteries -->
                <path d="M0,95 L245,95" stroke="#CBD5E1" stroke-width="4"/>
                <path d="M0,165 L240,165" stroke="#CBD5E1" stroke-width="3"/>
                <path d="M125,0 L125,230" stroke="#CBD5E1" stroke-width="4"/>
                <path d="M185,0 L185,230" stroke="#CBD5E1" stroke-width="3"/>
                <path d="M40,0 Q135,100 210,230" stroke="#E2E8F0" stroke-width="3"/>

                <!-- Neighborhood Labels -->
                <text x="135" y="60" font-size="10.5" font-weight="700" fill="#475569">Anna Nagar</text>
                <text x="65" y="132" font-size="10.5" font-weight="700" fill="#475569">T. Nagar</text>
                <text x="95" y="195" font-size="10.5" font-weight="700" fill="#475569">Velachery</text>
                <text x="175" y="202" font-size="10.5" font-weight="700" fill="#475569">Adyar</text>

                <!-- RADAR PULSE WAVES at Citizen Locality (T. Nagar) -->
                <circle cx="125" cy="130" r="26" fill="#0066FF" class="civix-radar-wave-1"/>
                <circle cx="125" cy="130" r="16" fill="#0066FF" class="civix-radar-wave-2"/>
                <circle cx="125" cy="130" r="6" fill="#0066FF"/>

                <!-- PINS -->
                <!-- Pin 1 Anna Nagar (Blue Water) -->
                <g class="civix-map-pin" ng-click="c.selectMapPoint('Anna Nagar')">
                  <circle cx="120" cy="52" r="7" fill="#0284C7" stroke="#FFFFFF" stroke-width="2"/>
                </g>
                <!-- Pin 2 T. Nagar (Red Road Work) -->
                <g class="civix-map-pin" ng-click="c.selectMapPoint('T. Nagar')">
                  <circle cx="68" cy="142" r="7" fill="#DC2626" stroke="#FFFFFF" stroke-width="2"/>
                </g>
                <!-- Pin 3 Velachery (Gold Drainage) -->
                <g class="civix-map-pin" ng-click="c.selectMapPoint('Velachery')">
                  <circle cx="145" cy="180" r="7" fill="#EAB308" stroke="#FFFFFF" stroke-width="2"/>
                </g>
                <!-- Pin 4 Adyar (Green Resolved) -->
                <g class="civix-map-pin" ng-click="c.selectMapPoint('Adyar')">
                  <circle cx="195" cy="185" r="7" fill="#16A34A" stroke="#FFFFFF" stroke-width="2"/>
                </g>
              </svg>

              <!-- Map Overlay Controls -->
              <div class="civix-map-zoom-tools">
                <button type="button" class="civix-map-tool-btn" title="Layer View"><span class="glyphicon glyphicon-th-large"></span></button>
                <div class="civix-zoom-stacked">
                  <button type="button" class="civix-map-tool-btn" title="Zoom In">+</button>
                  <button type="button" class="civix-map-tool-btn" title="Zoom Out">&minus;</button>
                </div>
                <button type="button" class="civix-map-tool-btn" title="My Location"><span class="glyphicon glyphicon-screenshot"></span></button>
              </div>
            </div>
          </div>

          <!-- Nearby Alerts Card -->
          <div class="civix-white-box" id="alerts">
            <div class="civix-box-header civix-flex-split">
              <h2 class="civix-box-title">Nearby Alerts</h2>
              <a href="?id=civix_landing#services" class="civix-view-all-button">View All &rarr;</a>
            </div>

            <!-- List of 4 Urgent Alerts -->
            <div class="civix-alert-items-list">
              <!-- Alert 1 -->
              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-red">
                  <span class="glyphicon glyphicon-exclamation-sign"></span>
                </div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Road maintenance work in T. Nagar</h4>
                  <div class="civix-alert-foot-meta">500 m &bull; Today</div>
                </div>
              </div>

              <!-- Alert 2 -->
              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-gold">
                  <span class="glyphicon glyphicon-flash"></span>
                </div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Scheduled power maintenance - Anna Nagar</h4>
                  <div class="civix-alert-foot-meta">1.2 km &bull; Tomorrow</div>
                </div>
              </div>

              <!-- Alert 3 -->
              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-purple">
                  <span class="glyphicon glyphicon-tint"></span>
                </div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Possible waterlogging in Velachery</h4>
                  <div class="civix-alert-foot-meta">2.3 km &bull; Today</div>
                </div>
              </div>

              <!-- Alert 4 -->
              <div class="civix-alert-item-card">
                <div class="civix-alert-icon-ring alert-blue">
                  <span class="glyphicon glyphicon-info-sign"></span>
                </div>
                <div class="civix-alert-info-side">
                  <h4 class="civix-alert-item-title">Low water pressure reported</h4>
                  <div class="civix-alert-foot-meta">3.1 km &bull; Today</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT COLUMN: Interactive Civic AI Assistant Card -->
        <div class="civix-column-assistant">
          <div class="civix-white-box civix-bot-widget-frame">
            <!-- Bot Header with window controls -->
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

            <!-- Bot Body with Floating 3D Robot -->
            <div class="civix-bot-widget-body">
              <!-- Floating Animated Robot Mascot -->
              <div class="civix-robot-mascot-box">
                <svg width="120" height="98" viewBox="0 0 120 98" fill="none" class="civix-robot-vector-anim" xmlns="http://www.w3.org/2000/svg">
                  <!-- Antenna -->
                  <circle cx="60" cy="10" r="5" fill="#0066FF"/>
                  <rect x="58.5" y="14" width="3" height="10" fill="#64748B"/>
                  <!-- Robot Head Shell -->
                  <rect x="28" y="22" width="64" height="42" rx="14" fill="#FFFFFF" stroke="#0066FF" stroke-width="3.5"/>
                  <!-- Visor Screen -->
                  <rect x="34" y="28" width="52" height="28" rx="8" fill="#0F172A"/>
                  <!-- Glowing Blue Eyes with Blink Animation -->
                  <circle cx="48" cy="42" r="5" fill="#38BDF8" class="civix-robot-eye"/>
                  <circle cx="72" cy="42" r="5" fill="#38BDF8" class="civix-robot-eye"/>
                  <!-- Side Headphones -->
                  <rect x="20" y="32" width="8" height="20" rx="3" fill="#0066FF"/>
                  <rect x="92" y="32" width="8" height="20" rx="3" fill="#0066FF"/>
                  <!-- Robot Torso -->
                  <rect x="40" y="66" width="40" height="28" rx="8" fill="#FFFFFF" stroke="#0066FF" stroke-width="3.5"/>
                  <rect x="46" y="72" width="28" height="12" rx="3" fill="#0066FF"/>
                  <text x="49" y="81" font-size="7.5" font-weight="900" fill="#FFFFFF">CIVIX</text>
                  <!-- Arms -->
                  <rect x="26" y="70" width="12" height="6" rx="3" fill="#64748B" transform="rotate(-30 26 70)"/>
                  <rect x="82" y="70" width="12" height="6" rx="3" fill="#64748B" transform="rotate(30 82 70)"/>
                </svg>
              </div>

              <!-- Interactive Conversation Stream -->
              <div class="civix-chat-scroll-area">
                <!-- Welcome Speech Bubble -->
                <div class="civix-chat-bubble-agent">
                  <p class="civix-bubble-hi">Hi Priya! 👋</p>
                  <p class="civix-bubble-text">I'm your Civic AI Assistant.<br/>How can I help you today?</p>
                </div>

                <!-- Dynamically Appended Chat Messages -->
                <div ng-repeat="msg in c.chatHistory" class="civix-chat-msg-row" ng-class="{'agent': msg.sender === 'bot', 'user': msg.sender === 'user'}">
                  <div class="civix-bubble" ng-class="msg.sender === 'bot' ? 'civix-chat-bubble-agent' : 'civix-chat-bubble-user'">
                    {{msg.text}}
                  </div>
                </div>

                <!-- Animated Typing Indicator -->
                <div ng-if="c.isBotTyping" class="civix-chat-bubble-agent civix-typing-anim">
                  <span class="civix-type-dot"></span>
                  <span class="civix-type-dot"></span>
                  <span class="civix-type-dot"></span>
                </div>
              </div>

              <!-- Quick Action Prompt Pills -->
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
                <button type="button" class="civix-action-chip" ng-click="c.sendPrompt('Ask any question')">
                  <span class="glyphicon glyphicon-question-sign"></span> Ask any question
                </button>
              </div>

              <!-- Chat Input Bar with Microphone & Send Ripple -->
              <div class="civix-chat-input-toolbar">
                <input type="text" class="civix-chat-text-box" placeholder="Type your message..." ng-model="c.userMsgInput" ng-keydown="c.onChatEnter($event)" />
                <button type="button" class="civix-chat-mic-btn" ng-click="c.triggerVoice()" aria-label="Voice input">
                  <span class="glyphicon glyphicon-bullhorn"></span>
                </button>
                <button type="button" class="civix-chat-send-btn" ng-click="c.submitChatMessage()" aria-label="Send">
                  <span class="glyphicon glyphicon-send"></span>
                </button>
              </div>

              <div class="civix-bot-caption-notice">
                I can assist you in all Indian languages
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

CSS = """
/* ==========================================================================
   GLOBAL SERVICE PORTAL & BOOTSTRAP OVERRIDES (FORCE FULL-BLEED APP SHELL)
   ========================================================================== */
html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  min-height: 100vh !important;
  background-color: #F8FAFC !important;
  overflow-x: hidden !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

/* Remove default Service Portal wrappers padding */
.sp-page-root, #page_root, .page, .container, .container-fluid, .row, .col-xs-12 {
  padding: 0 !important;
  margin: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
}

/* Hide default portal navbar if present */
header.sp-header, nav.navbar-inverse, .navbar, footer.civix-footer {
  display: none !important;
}

/* ROOT SHELL */
.civix-viewport-shell {
  display: flex;
  width: 100vw;
  min-height: 100vh;
  background: #F8FAFC;
  position: relative;
  box-sizing: border-box;
}

/* ==========================================================================
   1. FIXED FULL-HEIGHT LEFT SIDEBAR
   ========================================================================== */
.civix-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 250px;
  height: 100vh;
  background: #0B192C;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.25);
  overflow-y: auto;
}
.civix-sidebar-glow-bg {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(180deg, #0A192F 0%, #0F284E 50%, #0A192F 100%);
  opacity: 0.98;
}
.civix-sidebar-inner {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 24px 16px;
  box-sizing: border-box;
}

/* Brand */
.civix-brand-block {
  margin-bottom: 32px;
  padding-left: 6px;
}
.civix-brand-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}
.civix-brand-link:hover, .civix-brand-link:focus { text-decoration: none; }
.civix-city-emblem {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}
.civix-city-svg {
  width: 100%;
  height: 100%;
}
.civix-brand-headings {
  display: flex;
  flex-direction: column;
}
.civix-brand-title {
  font-size: 21px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: 0.5px;
  line-height: 1.1;
}
.civix-brand-motto {
  font-size: 9.5px;
  color: #94A3B8;
  font-weight: 500;
}

/* Menu Items with High-Level Animations */
.civix-sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-grow: 1;
}
.civix-menu-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 18px;
  border-radius: 12px;
  color: #CBD5E1;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.civix-menu-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #FFFFFF;
  transform: translateX(4px);
  text-decoration: none;
}
.civix-menu-item.active {
  background: #0066FF;
  color: #FFFFFF;
  font-weight: 600;
  box-shadow: 0 4px 16px rgba(0, 102, 255, 0.4);
}
.civix-menu-icon {
  font-size: 16px;
  width: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Sidebar Footer */
.civix-sidebar-foot {
  margin-top: auto;
  padding-top: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.civix-leaf-box {
  flex-shrink: 0;
}
.civix-foot-motto-text {
  display: flex;
  flex-direction: column;
  font-size: 10.5px;
  font-weight: 600;
  color: #22C55E;
  line-height: 1.35;
}

/* ==========================================================================
   2. MAIN APPLICATION WORKSPACE
   ========================================================================== */
.civix-workspace {
  margin-left: 250px;
  width: calc(100% - 250px);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #F8FAFC;
  box-sizing: border-box;
}

/* ==========================================================================
   STICKY TOPBAR
   ========================================================================== */
.civix-top-header {
  position: sticky;
  top: 0;
  height: 72px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid #E2E8F0;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 900;
  box-shadow: 0 1px 4px rgba(0,0,0,0.02);
}
.civix-search-container {
  flex: 1;
  max-width: 520px;
}
.civix-search-bar-pill {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}
.civix-search-lens {
  position: absolute;
  left: 16px;
  color: #94A3B8;
  font-size: 14px;
}
.civix-search-field {
  width: 100%;
  height: 42px;
  background: #F1F5F9;
  border: 1px solid transparent;
  border-radius: 22px;
  padding: 0 36px 0 42px;
  font-size: 13.5px;
  color: #0F172A;
  outline: none;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.civix-search-field:focus {
  background: #FFFFFF;
  border-color: #0066FF;
  box-shadow: 0 0 0 4px rgba(0, 102, 255, 0.12);
}
.civix-clear-search {
  position: absolute;
  right: 14px;
  color: #94A3B8;
  cursor: pointer;
}

/* Header Right Actions */
.civix-header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}
.civix-lang-component {
  position: relative;
}
.civix-lang-trigger {
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.civix-lang-trigger:hover {
  background: #E2E8F0;
  transform: translateY(-1px);
}
.civix-globe-icon { font-size: 14px; color: #0066FF; }
.civix-lang-arrow { font-size: 9px; opacity: 0.6; }

.civix-lang-popover {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 250px;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  box-shadow: 0 16px 36px rgba(0,0,0,0.14);
  z-index: 1050;
  overflow: hidden;
  animation: slideDown 0.2s ease;
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}
.civix-lang-popover-header {
  padding: 10px 14px;
  border-bottom: 1px solid #E2E8F0;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #F8FAFC;
}
.civix-lang-search-mini {
  width: 100%;
  border: none;
  background: transparent;
  outline: none;
  font-size: 12.5px;
}
.civix-lang-scroll-body {
  max-height: 280px;
  overflow-y: auto;
}
.civix-lang-opt-row {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 14px;
  border: none;
  background: transparent;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.15s;
}
.civix-lang-opt-row:hover, .civix-lang-opt-row.active {
  background: #EFF6FF;
  color: #0066FF;
}
.civix-lang-badge {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
.civix-lang-native-name { font-weight: 700; }
.civix-lang-en-name { color: #64748B; font-size: 12px; margin-left: auto; }
.civix-lang-checked { color: #0066FF; font-size: 12px; margin-left: 6px; }

/* Notification Button with Pulse Ring */
.civix-notif-button {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #F1F5F9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #334155;
  text-decoration: none;
  transition: all 0.2s;
}
.civix-notif-button:hover {
  background: #E2E8F0;
  color: #0066FF;
}
.civix-bell-count {
  position: absolute;
  top: -2px;
  right: -2px;
  background: #EF4444;
  color: #FFFFFF;
  font-size: 10px;
  font-weight: 700;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.civix-pulse-ring {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.4);
  animation: pulseBell 2s infinite;
}
@keyframes pulseBell {
  0% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(2.2); opacity: 0; }
}

/* User Profile Chip */
.civix-user-profile-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 24px;
  transition: background 0.2s;
}
.civix-user-profile-chip:hover {
  background: #F1F5F9;
}
.civix-user-avatar-wrap {
  position: relative;
  width: 38px;
  height: 38px;
}
.civix-avatar-img {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #E2E8F0;
}
.civix-online-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #22C55E;
  border: 2px solid #FFFFFF;
}
.civix-user-name-text {
  font-size: 14px;
  font-weight: 700;
  color: #0F172A;
}
.civix-profile-arrow { font-size: 9px; opacity: 0.6; }

/* ==========================================================================
   SCROLLABLE CONTENT BODY
   ========================================================================== */
.civix-scroll-body {
  padding: 24px 32px 60px;
  width: 100%;
  box-sizing: border-box;
}

/* 1. HERO BANNER GRID */
.civix-banner-grid {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 20px;
  margin-bottom: 22px;
}

/* Welcome Card */
.civix-hero-welcome-card {
  background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 50%, #F8FAFC 100%);
  border: 1px solid #BAE6FD;
  border-radius: 18px;
  padding: 30px 34px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 102, 255, 0.05);
}
.civix-hero-skyline-overlay {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 380px;
  background: url('https://images.unsplash.com/photo-1477959858617-67f30bc75b82?w=800&auto=format&fit=crop&q=80') center right/cover no-repeat;
  opacity: 0.15;
  mix-blend-mode: multiply;
  pointer-events: none;
}
.civix-hero-big-greeting {
  font-size: 30px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1.15;
  margin: 0 0 8px 0;
}
.civix-name-gradient {
  background: linear-gradient(90deg, #0066FF, #0284C7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.civix-hero-tagline-main {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  margin: 0;
}
.civix-hero-tagline-sub {
  font-size: 13px;
  color: #64748B;
  margin: 3px 0 0 0;
}

/* Glassmorphism Weather Widget */
.civix-glass-weather-widget {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(16px);
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 14px 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  z-index: 2;
  min-width: 190px;
}
.civix-weather-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  color: #0F172A;
  margin-bottom: 8px;
}
.civix-weather-split {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.civix-temp-reading {
  display: block;
  font-size: 22px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1;
}
.civix-weather-condition {
  font-size: 11.5px;
  color: #64748B;
  font-weight: 500;
}
.civix-animated-sun-icon {
  animation: rotateSun 16s linear infinite;
}
@keyframes rotateSun {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Scenic Promo Card */
.civix-hero-promo-card {
  border-radius: 18px;
  overflow: hidden;
  position: relative;
  background: url('https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=600&auto=format&fit=crop&q=80') center/cover no-repeat;
  border: 1px solid #CBD5E1;
  display: flex;
  align-items: flex-end;
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
}
.civix-promo-gradient-shade {
  width: 100%;
  background: linear-gradient(180deg, transparent 0%, rgba(15, 23, 42, 0.88) 100%);
  padding: 22px 20px;
  color: #FFFFFF;
}
.civix-promo-headline {
  font-size: 17px;
  font-weight: 800;
  line-height: 1.3;
  margin: 0 0 8px 0;
}
.civix-promo-line-accent {
  width: 38px;
  height: 4px;
  background: #38BDF8;
  border-radius: 2px;
}

/* ==========================================================================
   2. 4 KPI METRIC CARDS (INTERACTIVE & ELEVATED)
   ========================================================================== */
.civix-kpi-deck {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-bottom: 24px;
}
.civix-kpi-tile {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.civix-kpi-tile:hover {
  transform: translateY(-4px);
  text-decoration: none;
}
.kpi-tile-blue:hover { border-color: #3B82F6; box-shadow: 0 12px 28px rgba(59, 130, 246, 0.15); }
.kpi-tile-green:hover { border-color: #22C55E; box-shadow: 0 12px 28px rgba(34, 197, 94, 0.15); }
.kpi-tile-gold:hover { border-color: #F59E0B; box-shadow: 0 12px 28px rgba(245, 158, 11, 0.15); }
.kpi-tile-red:hover { border-color: #EF4444; box-shadow: 0 12px 28px rgba(239, 68, 68, 0.15); }

.civix-kpi-icon-bubble {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
  transition: transform 0.25s;
}
.civix-kpi-tile:hover .civix-kpi-icon-bubble { transform: scale(1.1); }
.bg-blue-subtle { background: #EFF6FF; }
.bg-green-subtle { background: #ECFDF5; }
.bg-gold-subtle { background: #FFFBEB; }
.bg-red-subtle { background: #FEF2F2; }
.text-blue { color: #0066FF; }
.text-green { color: #16A34A; }
.text-gold { color: #D97706; }
.text-red { color: #DC2626; }

.civix-kpi-details { flex-grow: 1; }
.civix-kpi-value-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}
.civix-kpi-count {
  font-size: 26px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1;
}
.civix-kpi-arrow-cue { font-size: 18px; color: #94A3B8; }
.civix-kpi-label-text {
  font-size: 13.5px;
  font-weight: 600;
  color: #64748B;
  margin: 4px 0 3px 0;
}
.civix-kpi-trend-badge {
  font-size: 11.5px;
  font-weight: 600;
}
.trend-green { color: #16A34A; }
.trend-neutral { color: #B45309; }
.trend-red { color: #DC2626; }

/* ==========================================================================
   3. TRI-PANEL WORKSPACE GRID
   ========================================================================== */
.civix-tri-panel-grid {
  display: grid;
  grid-template-columns: 1fr 340px 300px;
  gap: 22px;
}
.civix-white-box {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 22px 24px;
  margin-bottom: 22px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  transition: border-color 0.2s;
}
.civix-box-header { margin-bottom: 18px; }
.civix-box-title {
  font-size: 17px;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 4px 0;
}
.civix-box-subtitle {
  font-size: 13px;
  color: #64748B;
  margin: 0;
}
.civix-flex-split {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.civix-view-all-button {
  font-size: 13px;
  font-weight: 700;
  color: #0066FF;
  text-decoration: none;
  transition: transform 0.15s;
}
.civix-view-all-button:hover {
  text-decoration: underline;
  transform: translateX(2px);
}

/* 5 CATEGORY CARDS */
.civix-category-cards-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}
.civix-cat-pill-card {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 18px 10px;
  text-align: center;
  text-decoration: none;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.civix-cat-pill-card:hover {
  background: #FFFFFF;
  border-color: #0066FF;
  transform: translateY(-4px);
  box-shadow: 0 10px 24px rgba(0, 102, 255, 0.1);
  text-decoration: none;
}
.civix-cat-bubble {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  transition: transform 0.2s;
}
.civix-cat-pill-card:hover .civix-cat-bubble { transform: scale(1.12); }
.cat-water { background: #E0F2FE; }
.cat-elec { background: #FEF3C7; }
.cat-roads { background: #F1F5F9; }
.cat-drain { background: #DCFCE7; }
.cat-flood { background: #F3E8FF; }

.civix-cat-title-text {
  font-size: 13.5px;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 4px;
}
.civix-arrow-accent { color: #94A3B8; font-weight: 700; }
.civix-cat-subtitle-text {
  font-size: 11px;
  color: #64748B;
  line-height: 1.35;
  margin: 0;
}

/* RECENT COMPLAINTS LIST */
.civix-complaint-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.civix-complaint-entry {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.civix-complaint-entry:hover {
  background: #F8FAFC;
  border-color: #CBD5E1;
  transform: translateX(4px);
  text-decoration: none;
}
.civix-entry-thumb-box {
  width: 60px;
  height: 48px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
  border: 1px solid #E2E8F0;
}
.civix-thumb-vector {
  width: 100%;
  height: 100%;
  display: block;
}
.civix-entry-info {
  flex-grow: 1;
  min-width: 0;
}
.civix-entry-ticket-id {
  font-size: 11.5px;
  font-weight: 700;
  color: #0066FF;
}
.civix-entry-headline {
  font-size: 14px;
  font-weight: 600;
  color: #0F172A;
  margin: 2px 0 4px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.civix-entry-meta {
  display: flex;
  gap: 16px;
  font-size: 11.5px;
  color: #64748B;
}
.civix-entry-badge-col {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}
.civix-badge-pill-status {
  font-size: 11.5px;
  font-weight: 700;
  padding: 5px 14px;
  border-radius: 16px;
}
.pill-in-progress { background: #FEF3C7; color: #B45309; }
.pill-resolved { background: #DCFCE7; color: #15803D; }
.pill-awaiting { background: #FEE2E2; color: #B91C1C; }
.civix-entry-arrow {
  font-size: 20px;
  color: #94A3B8;
  transition: transform 0.2s;
}
.civix-complaint-entry:hover .civix-entry-arrow {
  transform: translateX(4px);
  color: #0066FF;
}

/* ==========================================================================
   CENTER COLUMN: MAP & ALERTS
   ========================================================================== */
.civix-map-panel { padding-bottom: 16px; }
.civix-map-stage {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #E2E8F0;
  background: #F1F5F9;
}
.civix-map-vector {
  width: 100%;
  height: auto;
  display: block;
}

/* Radar Pulse Animations */
.civix-radar-wave-1 {
  animation: radarPing 2.5s cubic-bezier(0, 0.2, 0.8, 1) infinite;
}
.civix-radar-wave-2 {
  animation: radarPing 2.5s cubic-bezier(0, 0.2, 0.8, 1) infinite 0.75s;
}
@keyframes radarPing {
  0% { r: 6; opacity: 0.8; }
  100% { r: 38; opacity: 0; }
}

.civix-map-pin {
  cursor: pointer;
  transition: transform 0.2s;
}
.civix-map-pin:hover {
  transform: scale(1.3);
}

.civix-map-zoom-tools {
  position: absolute;
  right: 12px;
  bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.civix-map-tool-btn {
  width: 28px;
  height: 28px;
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #334155;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  cursor: pointer;
  transition: all 0.15s;
}
.civix-map-tool-btn:hover {
  background: #F1F5F9;
  color: #0066FF;
}
.civix-zoom-stacked {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

/* Nearby Alerts List */
.civix-alert-items-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.civix-alert-item-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid #F1F5F9;
  transition: transform 0.15s;
}
.civix-alert-item-card:hover { transform: translateX(3px); }
.civix-alert-icon-ring {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  color: #FFFFFF;
  flex-shrink: 0;
  margin-top: 2px;
}
.alert-red { background: #EF4444; }
.alert-gold { background: #F59E0B; }
.alert-purple { background: #A855F7; }
.alert-blue { background: #0EA5E9; }

.civix-alert-info-side { flex-grow: 1; }
.civix-alert-item-title {
  font-size: 13px;
  font-weight: 600;
  color: #0F172A;
  margin: 0 0 3px 0;
  line-height: 1.35;
}
.civix-alert-foot-meta {
  font-size: 11.5px;
  color: #64748B;
}

/* ==========================================================================
   RIGHT COLUMN: CIVIC AI ASSISTANT (HIGH LEVEL ANIMATIONS & CHAT)
   ========================================================================== */
.civix-bot-widget-frame {
  border-top: 4px solid #0066FF;
  padding: 18px 20px 22px;
}
.civix-bot-widget-header {
  padding-bottom: 14px;
  border-bottom: 1px solid #F1F5F9;
  margin-bottom: 14px;
}
.civix-bot-label-group {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14.5px;
  color: #0F172A;
}
.civix-bot-badge-icon {
  color: #0066FF;
  font-size: 16px;
}
.civix-bot-actions-mini {
  display: flex;
  gap: 8px;
  color: #94A3B8;
  font-size: 11px;
}

/* 3D Floating Robot Mascot Animation */
.civix-robot-mascot-box {
  text-align: center;
  margin-bottom: 12px;
  animation: floatRobot 4s ease-in-out infinite;
}
@keyframes floatRobot {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-7px); }
}
.civix-robot-eye {
  animation: robotBlink 3s infinite;
}
@keyframes robotBlink {
  0%, 90%, 100% { transform: scale(1); }
  95% { transform: scale(1, 0.1); }
}

/* Chat Stream Area */
.civix-chat-scroll-area {
  max-height: 220px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 14px;
  padding-right: 4px;
}
.civix-chat-bubble-agent {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 13px;
  line-height: 1.45;
  color: #0F172A;
  align-self: flex-start;
  animation: fadeInBubble 0.25s ease;
}
.civix-chat-bubble-user {
  background: #0066FF;
  color: #FFFFFF;
  border-radius: 12px;
  padding: 10px 14px;
  font-size: 13px;
  align-self: flex-end;
  animation: fadeInBubble 0.25s ease;
}
@keyframes fadeInBubble {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}
.civix-bubble-hi { font-weight: 700; margin: 0 0 2px 0; }
.civix-bubble-text { margin: 0; color: #475569; }

/* Typing animation */
.civix-typing-anim {
  display: flex;
  gap: 4px;
  padding: 10px 14px;
  width: 60px;
}
.civix-type-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #0066FF;
  animation: bounceDot 1.4s infinite ease-in-out;
}
.civix-type-dot:nth-child(2) { animation-delay: 0.2s; }
.civix-type-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounceDot {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* Prompt Pills */
.civix-prompt-buttons-stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}
.civix-action-chip {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  padding: 9px 14px;
  font-size: 12.5px;
  font-weight: 600;
  color: #334155;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.civix-action-chip:hover {
  background: #EFF6FF;
  border-color: #0066FF;
  color: #0066FF;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 102, 255, 0.1);
}
.civix-action-chip:active {
  transform: scale(0.98);
}

/* Chat Input Bar */
.civix-chat-input-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  padding: 6px 8px;
  transition: border-color 0.2s;
}
.civix-chat-input-toolbar:focus-within {
  border-color: #0066FF;
  background: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
}
.civix-chat-text-box {
  flex-grow: 1;
  background: transparent;
  border: none;
  font-size: 12.5px;
  outline: none;
  padding: 4px 6px;
  color: #0F172A;
}
.civix-chat-mic-btn {
  background: transparent;
  border: none;
  color: #64748B;
  font-size: 14px;
  cursor: pointer;
  padding: 4px;
  transition: color 0.15s;
}
.civix-chat-mic-btn:hover { color: #0066FF; }
.civix-chat-send-btn {
  background: #0066FF;
  border: none;
  border-radius: 8px;
  color: #FFFFFF;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.civix-chat-send-btn:hover {
  background: #1D4ED8;
  transform: scale(1.05);
}
.civix-chat-send-btn:active {
  transform: scale(0.95);
}
.civix-bot-caption-notice {
  font-size: 11px;
  color: #94A3B8;
  text-align: center;
  margin-top: 12px;
}

/* ==========================================================================
   RESPONSIVE LAYOUT BREAKPOINTS
   ========================================================================== */
@media (max-width: 1400px) {
  .civix-tri-panel-grid {
    grid-template-columns: 1fr 320px;
  }
  .civix-column-assistant {
    grid-column: span 2;
  }
}
@media (max-width: 1100px) {
  .civix-kpi-deck {
    grid-template-columns: repeat(2, 1fr);
  }
  .civix-category-cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  .civix-banner-grid {
    grid-template-columns: 1fr;
  }
  .civix-tri-panel-grid {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 768px) {
  .civix-sidebar {
    display: none; /* Mobile menu can toggle */
  }
  .civix-workspace {
    margin-left: 0;
    width: 100%;
  }
  .civix-kpi-deck {
    grid-template-columns: 1fr;
  }
  .civix-category-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
"""

CLIENT_SCRIPT = """
function($scope, $timeout) {
  var c = this;
  c.activeMenu = 'dashboard';
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

  c.setActiveMenu = function(m) {
    c.activeMenu = m;
  };

  c.toggleLang = function() {
    c.langOpen = !c.langOpen;
  };

  c.chooseLang = function(l) {
    c.selectedLang = l.code;
    c.currentLangDisplay = l.native + ' / ' + l.name;
    c.langOpen = false;
  };

  c.selectMapPoint = function(loc) {
    c.chatHistory.push({
      sender: 'bot',
      text: 'Inspecting ' + loc + ' area: 1 active public maintenance order in progress.'
    });
  };

  c.sendPrompt = function(promptText) {
    c.chatHistory.push({ sender: 'user', text: promptText });
    c.isBotTyping = true;
    
    $timeout(function() {
      c.isBotTyping = false;
      var reply = 'I am processing your request for "' + promptText + '". Checking Ward 12 operations in real-time...';
      if (promptText.indexOf('Track') >= 0) {
        reply = 'You have 3 complaints In Progress: CIVIX-2024-00123 (Water leakage, Adyar), CIVIX-2024-00118 (Street light, Anna Nagar), and CIVIX-2024-00102 (Drainage, Velachery).';
      } else if (promptText.indexOf('Report') >= 0) {
        reply = 'Opening quick intake form. Please select your service category above or describe the location and issue.';
      } else if (promptText.indexOf('nearby') >= 0) {
        reply = 'Nearby Alert: Road maintenance on 3rd Main Road, T. Nagar (500m away). Expect minor traffic diversions until 4 PM.';
      }
      c.chatHistory.push({ sender: 'bot', text: reply });
    }, 700);
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
        text: 'Thank you for your report regarding: "' + userText + '". Our civic intelligence agent has logged this for Ward 12 inspection.'
      });
    }, 800);
  };

  c.onChatEnter = function(e) {
    if (e.keyCode === 13) {
      c.submitChatMessage();
    }
  };

  c.triggerVoice = function() {
    c.userMsgInput = 'Water pipeline leaking near cross street';
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
      statusClass: 'progress'
    },
    {
      sys_id: 'c2',
      number: 'CIVIX-2024-00118',
      short_description: 'Street light not working near Anna Nagar Park',
      location: 'Anna Nagar, Chennai',
      date: '10 Nov 2024, 06:12 PM',
      status: 'Resolved',
      statusClass: 'resolved'
    },
    {
      sys_id: 'c3',
      number: 'CIVIX-2024-00110',
      short_description: 'Pothole near 100 Feet Road',
      location: 'T. Nagar, Chennai',
      date: '05 Nov 2024, 02:30 PM',
      status: 'Resolved',
      statusClass: 'resolved'
    },
    {
      sys_id: 'c4',
      number: 'CIVIX-2024-00102',
      short_description: 'Drainage overflow in residential area',
      location: 'Velachery, Chennai',
      date: '28 Oct 2024, 09:15 AM',
      status: 'Awaiting Action',
      statusClass: 'awaiting'
    }
  ];
})();
"""

def update_sp_theme_variables():
    print("Updating sp_theme to zero out gutters and enable full-bleed app layout...")
    css_vars = """
$navbar-height: 0px !important;
$grid-gutter-width: 0px !important;
$container-large-desktop: 100% !important;
$container-desktop: 100% !important;
$container-tablet: 100% !important;
$body-bg: #F8FAFC !important;
"""
    api_put("sp_theme", "9b84c616c3bb0f14e54832f1b401319b", {"css_variables": css_vars.strip()})
    print("[UPDATED] sp_theme CSS variables")

def update_widgets():
    print("Updating civix_home_widget and civix_dashboard_widget...")
    for wid in ["civix_home_widget", "civix_dashboard_widget"]:
        res = api_get("sp_widget", query=f"id={wid}", limit=1)
        if res:
            sys_id = res[0]["sys_id"]
            payload = {
                "template": TEMPLATE.strip(),
                "css": CSS.strip(),
                "client_script": CLIENT_SCRIPT.strip(),
                "script": SERVER_SCRIPT.strip(),
                "sys_scope": APP_SYS_ID,
                "sys_package": APP_SYS_ID,
                "public": "true"
            }
            api_put("sp_widget", sys_id, payload)
            print(f"[UPDATED] {wid} ({sys_id})")

if __name__ == "__main__":
    update_sp_theme_variables()
    update_widgets()
    print("UI16-grade advanced UI upgrade deployed successfully!")
