"""
CIVIX AI Portal Builder
Builds Theme, Header, Footer, Pages, and Widgets inside ServiceNow.
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

INSTANCE_URL = os.getenv("SERVICENOW_INSTANCE_URL", "").rstrip("/")
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")
APP_SYS_ID = "4750065ac37b0f14e54832f1b4013184"
APP_SCOPE = "x_civic_ai"

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
        print(f"POST {table} failed: {resp.status_code} - {resp.text}")
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

# 1. CREATE THEME
def create_theme():
    print("\n--- 1. Configuring CIVIX AI Theme ---")
    css_vars = """
$civix-deep-teal: #123E46 !default;
$civix-action-teal: #087F8C !default;
$civix-mint: #E1F5EA !default;
$civix-bg: #F7FAFA !default;
$civix-surface: #FFFFFF !default;
$civix-text: #183238 !default;
$civix-text-muted: #61777B !default;
$civix-border: #DCE7E8 !default;
$civix-error: #B42318 !default;
$civix-warning: #B54708 !default;
$civix-success: #18794E !default;

$brand-primary: #087F8C;
$body-bg: #F7FAFA;
$text-color: #183238;
$link-color: #087F8C;
$navbar-inverse-bg: #123E46;
$navbar-inverse-color: #FFFFFF;
$navbar-inverse-link-color: #FFFFFF;
$navbar-inverse-link-hover-color: #E1F5EA;
$font-family-base: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans Tamil", "Helvetica Neue", Arial, sans-serif;
"""
    theme_data = {
        "name": "CIVIX AI - Citizen Theme",
        "css_variables": css_vars.strip(),
        "navbar_fixed": "false",
        "footer_fixed": "false"
    }
    return upsert("sp_theme", "name=CIVIX AI - Citizen Theme", theme_data, "Theme")

# 2. CREATE WIDGETS
def create_header_widget():
    print("\n--- 2. Configuring Header Widget ---")
    template = """
<div class="civix-header" role="banner">
  <div class="civix-header-inner">
    <!-- Brand -->
    <a href="?id=civix_landing" class="civix-brand" aria-label="CIVIX AI Home">
      <div class="civix-brand-icon">
        <span class="glyphicon glyphicon-stats"></span>
      </div>
      <div class="civix-brand-text">
        <span class="civix-brand-title">CIVIX AI</span>
        <span class="civix-brand-sub">{{c.t('brand_sub')}}</span>
      </div>
    </a>

    <!-- Navigation links -->
    <nav class="civix-nav" aria-label="Main Navigation">
      <a href="?id=civix_landing" class="civix-nav-link" ng-class="{'active': c.pageId === 'civix_landing'}">{{c.t('nav_home')}}</a>
      <a href="?id=civix_landing#services" class="civix-nav-link">{{c.t('nav_services')}}</a>
      <a href="?id=civix_landing#how-it-works" class="civix-nav-link">{{c.t('nav_how')}}</a>
      <a href="?id=civix_portal_select" class="civix-nav-link" ng-class="{'active': c.pageId === 'civix_portal_select'}">{{c.t('nav_portals')}}</a>
      <a ng-if="c.data.isLoggedIn" href="?id=civix_dashboard" class="civix-nav-link" ng-class="{'active': c.pageId === 'civix_dashboard'}">{{c.t('nav_dashboard')}}</a>
    </nav>

    <!-- Top Right Actions -->
    <div class="civix-top-right">
      <!-- 22 Languages Selector -->
      <div class="civix-lang-dropdown">
        <button class="civix-lang-btn" type="button" ng-click="c.toggleLangMenu()" aria-haspopup="true" aria-expanded="{{c.langOpen}}" aria-label="Select Language">
          <span class="glyphicon glyphicon-globe"></span>
          <span class="civix-lang-current">{{c.currentLangName}}</span>
          <span class="glyphicon glyphicon-chevron-down civix-arrow"></span>
        </button>
        <div class="civix-lang-menu" ng-show="c.langOpen" role="menu">
          <div class="civix-lang-search-box">
            <input type="text" ng-model="c.langSearch" placeholder="Search language..." class="civix-lang-input" />
          </div>
          <div class="civix-lang-list">
            <button ng-repeat="lang in c.languages | filter:c.langSearch" 
                    type="button" 
                    class="civix-lang-item" 
                    ng-class="{'active': c.selectedLang === lang.code}"
                    ng-click="c.setLanguage(lang)">
              <span class="civix-lang-native">{{lang.native}}</span>
              <span class="civix-lang-en">{{lang.name}}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Authenticated View: Notifications & Profile in Top-Right -->
      <div ng-if="c.data.isLoggedIn" class="civix-auth-group">
        <!-- Top Right Notification -->
        <a href="?id=civix_dashboard#alerts" class="civix-notif-btn" aria-label="Notifications" title="Notifications">
          <span class="glyphicon glyphicon-bell"></span>
          <span class="civix-notif-badge">3</span>
        </a>

        <!-- Top Right Profile Menu -->
        <div class="civix-profile-dropdown">
          <button class="civix-profile-btn" type="button" ng-click="c.toggleProfileMenu()" aria-haspopup="true" aria-expanded="{{c.profileOpen}}">
            <div class="civix-avatar">{{c.data.userInitials}}</div>
            <span class="civix-username">{{c.data.userName}}</span>
            <span class="glyphicon glyphicon-chevron-down civix-arrow"></span>
          </button>
          <div class="civix-profile-menu" ng-show="c.profileOpen" role="menu">
            <div class="civix-profile-header">
              <strong>{{c.data.userName}}</strong>
              <small>{{c.data.userEmail}}</small>
            </div>
            <a href="?id=civix_dashboard" class="civix-profile-item"><span class="glyphicon glyphicon-dashboard"></span> {{c.t('profile_dashboard')}}</a>
            <a href="?id=civix_my_cases" class="civix-profile-item"><span class="glyphicon glyphicon-folder-open"></span> {{c.t('profile_my_cases')}}</a>
            <a href="?id=civix_profile" class="civix-profile-item"><span class="glyphicon glyphicon-user"></span> {{c.t('profile_settings')}}</a>
            <hr class="civix-divider" />
            <a href="/logout.do" class="civix-profile-item text-danger"><span class="glyphicon glyphicon-log-out"></span> {{c.t('profile_signout')}}</a>
          </div>
        </div>
      </div>

      <!-- Guest View: Sign In & Get Started -->
      <div ng-if="!c.data.isLoggedIn" class="civix-guest-group">
        <a href="?id=civix_login" class="civix-btn civix-btn-ghost">{{c.t('btn_signin')}}</a>
        <a href="?id=civix_portal_select" class="civix-btn civix-btn-primary">{{c.t('btn_getstarted')}}</a>
      </div>
    </div>
  </div>
</div>
"""

    css = """
.civix-header {
  background-color: #123E46;
  color: #FFFFFF;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(18, 62, 70, 0.15);
}
.civix-header-inner {
  max-width: 1360px;
  margin: 0 auto;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.civix-brand {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #FFFFFF;
  gap: 12px;
}
.civix-brand:hover, .civix-brand:focus {
  text-decoration: none;
  color: #E1F5EA;
}
.civix-brand-icon {
  width: 40px;
  height: 40px;
  background: #087F8C;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #FFFFFF;
}
.civix-brand-text {
  display: flex;
  flex-direction: column;
}
.civix-brand-title {
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 0.5px;
  line-height: 1.2;
}
.civix-brand-sub {
  font-size: 11px;
  color: #E1F5EA;
  font-weight: 500;
  letter-spacing: 0.3px;
}
.civix-nav {
  display: flex;
  gap: 20px;
}
.civix-nav-link {
  color: #E1F5EA;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 6px;
  text-decoration: none;
  transition: all 0.2s ease;
}
.civix-nav-link:hover, .civix-nav-link:focus, .civix-nav-link.active {
  color: #FFFFFF;
  background: rgba(8, 127, 140, 0.3);
  text-decoration: none;
}
.civix-top-right {
  display: flex;
  align-items: center;
  gap: 16px;
}
.civix-lang-dropdown, .civix-profile-dropdown {
  position: relative;
}
.civix-lang-btn, .civix-profile-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #FFFFFF;
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.civix-lang-btn:hover, .civix-profile-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}
.civix-arrow {
  font-size: 10px;
  opacity: 0.7;
}
.civix-lang-menu, .civix-profile-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: #FFFFFF;
  color: #183238;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 280px;
  z-index: 1010;
  border: 1px solid #DCE7E8;
  overflow: hidden;
}
.civix-lang-search-box {
  padding: 10px 12px;
  border-bottom: 1px solid #DCE7E8;
  background: #F7FAFA;
}
.civix-lang-input {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #DCE7E8;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
}
.civix-lang-list {
  max-height: 260px;
  overflow-y: auto;
}
.civix-lang-item {
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  padding: 8px 14px;
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.15s;
}
.civix-lang-item:hover, .civix-lang-item.active {
  background: #E1F5EA;
  color: #087F8C;
  font-weight: 600;
}
.civix-lang-native {
  font-weight: 600;
}
.civix-lang-en {
  color: #61777B;
  font-size: 12px;
}
.civix-auth-group {
  display: flex;
  align-items: center;
  gap: 14px;
}
.civix-notif-btn {
  position: relative;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  text-decoration: none;
}
.civix-notif-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: #B42318;
  color: #FFFFFF;
  font-size: 10px;
  font-weight: 700;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.civix-avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #087F8C;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
}
.civix-profile-header {
  padding: 12px 16px;
  background: #F7FAFA;
  border-bottom: 1px solid #DCE7E8;
  display: flex;
  flex-direction: column;
}
.civix-profile-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  color: #183238;
  font-size: 13px;
  text-decoration: none;
}
.civix-profile-item:hover {
  background: #F7FAFA;
  color: #087F8C;
  text-decoration: none;
}
.civix-divider {
  margin: 4px 0;
  border: 0;
  border-top: 1px solid #DCE7E8;
}
.civix-guest-group {
  display: flex;
  gap: 10px;
}
.civix-btn {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.civix-btn-ghost {
  background: transparent;
  color: #FFFFFF;
  border: 1px solid rgba(255, 255, 255, 0.4);
}
.civix-btn-ghost:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #FFFFFF;
  text-decoration: none;
}
.civix-btn-primary {
  background: #087F8C;
  color: #FFFFFF;
  border: 1px solid #087F8C;
}
.civix-btn-primary:hover {
  background: #0d96a5;
  color: #FFFFFF;
  text-decoration: none;
}
@media (max-width: 900px) {
  .civix-nav { display: none; }
  .civix-brand-sub { display: none; }
}
"""

    client_script = """
function($scope, $location, $window) {
  var c = this;
  c.pageId = $location.search().id || 'civix_landing';
  c.langOpen = false;
  c.profileOpen = false;
  c.selectedLang = localStorage.getItem('civix_lang') || 'en';

  // 22 Scheduled Indian Languages + English
  c.languages = [
    { code: 'en', name: 'English', native: 'English' },
    { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
    { code: 'hi', name: 'Hindi', native: 'हिन्दी' },
    { code: 'te', name: 'Telugu', native: 'తెలుగు' },
    { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
    { code: 'ml', name: 'Malayalam', native: 'മലയാളം' },
    { code: 'bn', name: 'Bengali', native: 'বাংলা' },
    { code: 'mr', name: 'Marathi', native: 'मराठी' },
    { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' },
    { code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
    { code: 'or', name: 'Odia', native: 'ଓଡ଼ିଆ' },
    { code: 'as', name: 'Assamese', native: 'অসমীয়া' },
    { code: 'ur', name: 'Urdu', native: 'اردو' },
    { code: 'sa', name: 'Sanskrit', native: 'संस्कृतम्' },
    { code: 'ks', name: 'Kashmiri', native: 'कॉशुर' },
    { code: 'kok', name: 'Konkani', native: 'कोंकणी' },
    { code: 'mai', name: 'Maithili', native: 'मैथिली' },
    { code: 'mni', name: 'Manipuri', native: 'মৈতৈলোন্' },
    { code: 'ne', name: 'Nepali', native: 'नेपाली' },
    { code: 'sd', name: 'Sindhi', native: 'سنڌي' },
    { code: 'sat', name: 'Santali', native: 'संताली' },
    { code: 'brx', name: 'Bodo', native: 'बड़ो' },
    { code: 'doi', name: 'Dogri', native: 'डोगरी' }
  ];

  // Localization Dictionary (English & Tamil verified, extensible)
  var dict = {
    'brand_sub': { en: 'Smart Urban Services', ta: 'ஸ்மார்ட் நகர்ப்புற சேவைகள்' },
    'nav_home': { en: 'Home', ta: 'முகப்பு' },
    'nav_services': { en: 'Services', ta: 'சேவைகள்' },
    'nav_how': { en: 'How It Works', ta: 'செயல்படும் முறை' },
    'nav_portals': { en: 'Portals', ta: 'தளங்கள்' },
    'nav_dashboard': { en: 'Dashboard', ta: 'டாஷ்போர்டு' },
    'btn_signin': { en: 'Sign In', ta: 'உள்நுழைக' },
    'btn_getstarted': { en: 'Get Started', ta: 'தொடங்குக' },
    'profile_dashboard': { en: 'Citizen Dashboard', ta: 'குடிமக்கள் டாஷ்போர்டு' },
    'profile_my_cases': { en: 'My Reported Cases', ta: 'எனது புகார்கள்' },
    'profile_settings': { en: 'Profile & Settings', ta: 'சுயவிவரம் மற்றும் அமைப்புகள்' },
    'profile_signout': { en: 'Sign Out', ta: 'வெளியேறுக' }
  };

  c.t = function(key) {
    if (dict[key]) {
      return dict[key][c.selectedLang] || dict[key]['en'] || key;
    }
    return key;
  };

  function updateLangLabel() {
    for (var i = 0; i < c.languages.length; i++) {
      if (c.languages[i].code === c.selectedLang) {
        c.currentLangName = c.languages[i].native;
        return;
      }
    }
    c.currentLangName = 'English';
  }
  updateLangLabel();

  c.toggleLangMenu = function() {
    c.langOpen = !c.langOpen;
    if (c.langOpen) c.profileOpen = false;
  };

  c.toggleProfileMenu = function() {
    c.profileOpen = !c.profileOpen;
    if (c.profileOpen) c.langOpen = false;
  };

  c.setLanguage = function(lang) {
    c.selectedLang = lang.code;
    localStorage.setItem('civix_lang', lang.code);
    updateLangLabel();
    c.langOpen = false;
    $scope.$emit('civix:lang_changed', lang.code);
  };
}
"""

    server_script = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  if (data.isLoggedIn) {
    var user = gs.getUser();
    data.userName = user.getDisplayName() || gs.getUserName();
    data.userEmail = user.getEmail() || '';
    data.userId = gs.getUserID();
    var names = data.userName.split(' ');
    data.userInitials = names.length > 1 ? (names[0][0] + names[names.length-1][0]).toUpperCase() : data.userName.substring(0, 2).toUpperCase();
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Header",
        "id": "civix_header",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    return upsert("sp_widget", "id=civix_header", widget_data, "Header Widget")

def create_footer_widget():
    print("\n--- 3. Configuring Footer Widget ---")
    template = """
<footer class="civix-footer" role="contentinfo">
  <div class="civix-footer-inner">
    <div class="row">
      <div class="col-md-4 col-sm-6 civix-footer-col">
        <div class="civix-footer-brand">
          <div class="civix-footer-logo">CIVIX AI</div>
          <p class="civix-footer-desc">Agentic Intelligence Platform for Smart Urban Corporation Management. Smarter Cities. Faster Civic Services.</p>
        </div>
      </div>
      <div class="col-md-2 col-sm-6 civix-footer-col">
        <h4 class="civix-footer-heading">Navigation</h4>
        <ul class="civix-footer-links">
          <li><a href="?id=civix_landing">Home</a></li>
          <li><a href="?id=civix_landing#services">Civic Services</a></li>
          <li><a href="?id=civix_landing#how-it-works">How It Works</a></li>
          <li><a href="?id=civix_portal_select">Portal Selection</a></li>
        </ul>
      </div>
      <div class="col-md-3 col-sm-6 civix-footer-col">
        <h4 class="civix-footer-heading">Civic Services</h4>
        <ul class="civix-footer-links">
          <li><a href="?id=civix_report_issue&cat=water">Water Supply & Leakage</a></li>
          <li><a href="?id=civix_report_issue&cat=electricity">Electricity & Lighting</a></li>
          <li><a href="?id=civix_report_issue&cat=roads">Roads & Maintenance</a></li>
          <li><a href="?id=civix_report_issue&cat=drainage">Drainage & Waterlogging</a></li>
        </ul>
      </div>
      <div class="col-md-3 col-sm-6 civix-footer-col">
        <h4 class="civix-footer-heading">Transparency & Trust</h4>
        <ul class="civix-footer-links">
          <li><a href="?id=civix_landing#trust">Responsible AI Oversight</a></li>
          <li><a href="?id=civix_landing#trust">Citizen Privacy Policy</a></li>
          <li><a href="?id=civix_recovery">Account Recovery</a></li>
          <li><span>24x7 Civic Helpline: 1913</span></li>
        </ul>
      </div>
    </div>
    <div class="civix-footer-bottom">
      <p>&copy; 2026 Smart Urban Municipal Corporation &bull; CIVIX AI Platform. All rights reserved.</p>
      <p class="civix-lang-notice">Available in 22 Official Scheduled Indian Languages &bull; தமிழ் &bull; English</p>
    </div>
  </div>
</footer>
"""

    css = """
.civix-footer {
  background: #123E46;
  color: #E1F5EA;
  padding: 48px 24px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
}
.civix-footer-inner {
  max-width: 1360px;
  margin: 0 auto;
}
.civix-footer-logo {
  font-size: 22px;
  font-weight: 800;
  color: #FFFFFF;
  margin-bottom: 12px;
  letter-spacing: 0.5px;
}
.civix-footer-desc {
  font-size: 13px;
  line-height: 1.6;
  color: #E1F5EA;
  opacity: 0.85;
}
.civix-footer-heading {
  font-size: 14px;
  font-weight: 700;
  color: #FFFFFF;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 16px;
}
.civix-footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}
.civix-footer-links li {
  margin-bottom: 8px;
}
.civix-footer-links a {
  color: #E1F5EA;
  opacity: 0.8;
  font-size: 13px;
  text-decoration: none;
  transition: opacity 0.2s;
}
.civix-footer-links a:hover {
  opacity: 1;
  color: #FFFFFF;
  text-decoration: underline;
}
.civix-footer-links span {
  font-size: 13px;
  opacity: 0.9;
  color: #FFFFFF;
  font-weight: 600;
}
.civix-footer-bottom {
  margin-top: 36px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  font-size: 12px;
  opacity: 0.75;
}
@media (max-width: 768px) {
  .civix-footer-bottom { flex-direction: column; text-align: center; gap: 8px; }
  .civix-footer-col { margin-bottom: 24px; }
}
"""

    widget_data = {
        "name": "CIVIX AI - Footer",
        "id": "civix_footer",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": "function() {}",
        "script": "(function() {})();",
        "public": "true"
    }
    return upsert("sp_widget", "id=civix_footer", widget_data, "Footer Widget")

if __name__ == "__main__":
    theme_id = create_theme()
    header_id = create_header_widget()
    footer_id = create_footer_widget()
    print("\nFoundation Theme, Header, and Footer ready!")
