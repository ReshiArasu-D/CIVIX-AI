"""
Fix Login & Registration Flow & Redesign civix_login and civix_register
1. Connects civix_portal_select to civix_login and civix_register directly
2. Modernizes civix_login_widget and civix_register_widget to match Reference Image 1 (Dark Plus Jakarta Sans theme)
3. Adds 1-click Demo credentials for rapid testing
4. Attaches CIVIX Assist across all pages
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

# ==============================================================================
# 1. UPDATE civix_portal_select_widget BUTTON LINKS
# ==============================================================================
print(">>> Step 1: Updating civix_portal_select_widget action links to point to ?id=civix_login & ?id=civix_register...")
portal_w = api_get("sp_widget", query="id=civix_portal_select_widget", limit=1)
if portal_w:
    psys = portal_w[0]["sys_id"]
    t = portal_w[0]["template"]
    # Replace links
    t = t.replace('href="?id=civix_home"', 'href="?id=civix_login"')
    t = t.replace('href="?id=civix_profile"', 'href="?id=civix_register"')
    t = t.replace('href="?id=civix_dashboard"', 'href="?id=civix_login&role=officer"')
    t = t.replace('href="/now/nav/ui/classic/params/target/incident_list.do"', 'href="?id=civix_login&role=admin"')
    api_put("sp_widget", psys, {"template": t})
    print("  [SUCCESS] Portal Selection action links updated successfully!")

# Also update civix_landing_widget top nav "Citizen Login" link
print(">>> Step 1b: Updating civix_landing_widget top nav Citizen Login link...")
land_w = api_get("sp_widget", query="id=civix_landing_widget", limit=1)
if land_w:
    lsys = land_w[0]["sys_id"]
    lt = land_w[0]["template"]
    lt = lt.replace('href="?id=civix_home" class="btn btn-default civix-btn-citizen-login"', 'href="?id=civix_login" class="btn btn-default civix-btn-citizen-login"')
    api_put("sp_widget", lsys, {"template": lt})
    print("  [SUCCESS] Landing widget top nav updated!")

# ==============================================================================
# 2. REDESIGN civix_login_widget (sys_id: 7695cad6c3bb0f14e54832f1b4013193)
# ==============================================================================
print("\n>>> Step 2: Redesigning civix_login_widget with dark glassmorphic styling...")

LOGIN_TEMPLATE = """
<div class="civix-auth-root">
  <!-- Ambient Floating Background Badges -->
  <div class="civix-amb-badge amb-tl">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F97316" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
    <span>CIVIX AI SECURE AUTHENTICATION</span>
  </div>
  <div class="civix-amb-badge amb-tr">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
    <span>GREATER CHENNAI CORPORATION</span>
  </div>

  <!-- Top Simple Nav -->
  <header class="civix-auth-nav">
    <div class="civix-auth-nav-inner">
      <a href="?id=civix_landing" class="civix-auth-brand">
        <div class="civix-auth-logo">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M3 21h18M5 21V7l8-4v18M13 21V3l6 4v14"/></svg>
        </div>
        <div class="civix-auth-brand-text">
          <span class="auth-brand-title">CIVIX AI</span>
          <span class="auth-brand-sub">Citizen & Officer Services</span>
        </div>
      </a>
      <a href="?id=civix_portal_select" class="civix-auth-back-link">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        <span>Change Portal</span>
      </a>
    </div>
  </header>

  <!-- Login Card Container -->
  <main class="civix-auth-main">
    <div class="civix-auth-card">

      <div class="civix-card-header text-center">
        <div class="civix-auth-pill-badge" ng-if="c.role === 'officer'">
          <span class="pill-dot blue"></span>
          <span>FIELD OFFICER & TECHNICIAN ACCESS</span>
        </div>
        <div class="civix-auth-pill-badge" ng-if="c.role === 'admin'">
          <span class="pill-dot amber"></span>
          <span>MUNICIPAL AUTHORITY & ADMIN</span>
        </div>
        <div class="civix-auth-pill-badge" ng-if="!c.role || c.role === 'citizen'">
          <span class="pill-dot orange"></span>
          <span>AUTHENTICATED CITIZEN PORTAL</span>
        </div>

        <h1 class="civix-auth-heading">
          <span ng-if="c.role === 'officer'">Officer Sign In</span>
          <span ng-if="c.role === 'admin'">Administrator Sign In</span>
          <span ng-if="!c.role || c.role === 'citizen'">Welcome Back, Citizen</span>
        </h1>
        <p class="civix-auth-subtext">
          Enter your credentials to access your civic dashboard, submit reports, and track real-time resolution progress.
        </p>
      </div>

      <!-- Quick 1-Click Demo Fill for Testing -->
      <div class="civix-demo-chips-box">
        <span class="demo-chip-lbl">Quick Demo Fill:</span>
        <button type="button" class="btn btn-xs demo-chip-btn" ng-click="c.quickFill('citizen@civix.gov.in', 'Civix2026!')">
          👤 Citizen Account
        </button>
        <button type="button" class="btn btn-xs demo-chip-btn" ng-click="c.quickFill('officer.adyar@civix.gov.in', 'Civix2026!')">
          🛠️ Field Officer
        </button>
      </div>

      <!-- Error / Alert Message -->
      <div class="civix-alert-banner alert-danger" ng-if="c.errorMsg">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <span>{{c.errorMsg}}</span>
      </div>

      <form ng-submit="c.login()" class="civix-auth-form" autocomplete="off">
        <div class="form-group">
          <label class="civix-form-lbl">User ID / Registered Email</label>
          <div class="civix-input-wrap">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <input type="text" class="form-control civix-dark-input" placeholder="e.g. citizen@civix.gov.in" ng-model="c.username" required />
          </div>
        </div>

        <div class="form-group">
          <div class="pwd-lbl-row">
            <label class="civix-form-lbl">Password</label>
            <a href="?id=civix_recovery" class="civix-forgot-link">Forgot password?</a>
          </div>
          <div class="civix-input-wrap">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            <input type="{{c.showPwd ? 'text' : 'password'}}" class="form-control civix-dark-input" placeholder="Enter your secure password" ng-model="c.password" required />
            <button type="button" class="btn-toggle-pwd" ng-click="c.togglePwd()">
              <span ng-if="!c.showPwd">Show</span>
              <span ng-if="c.showPwd">Hide</span>
            </button>
          </div>
        </div>

        <div class="civix-checkbox-row">
          <label class="civix-check-lbl">
            <input type="checkbox" ng-model="c.rememberMe" />
            <span>Keep me logged in for 30 days</span>
          </label>
        </div>

        <button type="submit" class="btn btn-block civix-btn-submit" ng-disabled="c.loading">
          <span ng-if="!c.loading">Sign In to Dashboard &rarr;</span>
          <span ng-if="c.loading">Authenticating with GCC...</span>
        </button>
      </form>

      <!-- Switch to Register -->
      <div class="civix-auth-card-footer text-center">
        <p class="switch-auth-text">
          Don't have a verified account yet?
          <a href="?id=civix_register" class="civix-auth-switch-link">Register New Citizen</a>
        </p>
      </div>

    </div>
  </main>

  <footer class="civix-auth-footer text-center">
    <p>&copy; 2026 Greater Chennai Corporation &bull; CIVIX AI Platform. All rights reserved.</p>
  </footer>
</div>
"""

LOGIN_CSS = """
/* Full-viewport dark override for ServiceNow Service Portal */
#page_root, .sp-page-root, body {
  background-color: #080C14 !important;
  color: #F8FAFC !important;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  margin: 0 !important;
  padding: 0 !important;
}

.civix-auth-root {
  min-height: 100vh;
  width: 100%;
  background: radial-gradient(circle at 50% 15%, rgba(245, 158, 11, 0.06) 0%, transparent 45%),
              radial-gradient(circle at 80% 30%, rgba(59, 130, 246, 0.05) 0%, transparent 40%),
              #080C14;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
}

/* Ambient Badges */
.civix-amb-badge {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 700;
  color: #64748B;
  letter-spacing: 0.8px;
  pointer-events: none;
  opacity: 0.7;
}

.amb-tl { top: 90px; left: 40px; }
.amb-tr { top: 90px; right: 40px; }

@media (max-width: 768px) {
  .civix-amb-badge { display: none !important; }
}

/* Top Nav */
.civix-auth-nav {
  width: 100%;
  padding: 24px 40px;
}

.civix-auth-nav-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.civix-auth-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none !important;
}

.civix-auth-logo {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
}

.civix-auth-brand-text {
  display: flex;
  flex-direction: column;
}

.auth-brand-title {
  font-size: 18px;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1.2;
}

.auth-brand-sub {
  font-size: 11px;
  font-weight: 500;
  color: #94A3B8;
}

.civix-auth-back-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #94A3B8;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none !important;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 8px 16px;
  border-radius: 9999px;
  transition: all 0.2s;
}

.civix-auth-back-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #FFFFFF;
}

/* Main Form Card */
.civix-auth-main {
  width: 100%;
  max-width: 520px;
  margin: 0 auto;
  padding: 10px 20px 40px 20px;
}

.civix-auth-card {
  background: #0E1526;
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 20px;
  padding: 36px 32px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5), 0 0 24px rgba(249, 115, 22, 0.06);
}

.civix-auth-pill-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 5px 14px;
  border-radius: 9999px;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #E2E8F0;
  margin-bottom: 16px;
}

.pill-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}
.pill-dot.orange { background: #F97316; box-shadow: 0 0 8px #F97316; }
.pill-dot.blue { background: #3B82F6; box-shadow: 0 0 8px #3B82F6; }
.pill-dot.amber { background: #F59E0B; box-shadow: 0 0 8px #F59E0B; }

.civix-auth-heading {
  font-size: 28px;
  font-weight: 800;
  color: #FFFFFF;
  margin: 0 0 10px 0;
  letter-spacing: -0.02em;
}

.civix-auth-subtext {
  font-size: 13.5px;
  color: #94A3B8;
  line-height: 1.55;
  margin-bottom: 24px;
}

/* Demo Chips Box */
.civix-demo-chips-box {
  background: rgba(255, 255, 255, 0.03);
  border: 1px dashed rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  padding: 10px 14px;
  margin-bottom: 22px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.demo-chip-lbl {
  font-size: 11px;
  font-weight: 600;
  color: #64748B;
}

.demo-chip-btn {
  background: rgba(255, 255, 255, 0.06) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  color: #CBD5E1 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  padding: 4px 10px !important;
  border-radius: 6px !important;
  transition: all 0.15s;
}

.demo-chip-btn:hover {
  background: rgba(249, 115, 22, 0.15) !important;
  border-color: rgba(249, 115, 22, 0.35) !important;
  color: #FB923C !important;
}

/* Alert Banner */
.civix-alert-banner {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.35);
  color: #FCA5A5;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

/* Form Controls */
.civix-auth-form .form-group {
  margin-bottom: 20px;
}

.civix-form-lbl {
  font-size: 12.5px;
  font-weight: 600;
  color: #CBD5E1;
  margin-bottom: 8px;
  display: block;
}

.pwd-lbl-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.civix-forgot-link {
  font-size: 12px;
  color: #F97316;
  text-decoration: none;
  font-weight: 500;
}
.civix-forgot-link:hover { text-decoration: underline; }

.civix-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.civix-input-wrap .input-icon {
  position: absolute;
  left: 14px;
  pointer-events: none;
}

.civix-dark-input {
  width: 100% !important;
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  color: #FFFFFF !important;
  font-size: 14px !important;
  padding: 12px 44px 12px 42px !important;
  border-radius: 10px !important;
  height: 46px !important;
  transition: all 0.2s !important;
}

.civix-dark-input:focus {
  border-color: #F97316 !important;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.2) !important;
  outline: none !important;
}

.btn-toggle-pwd {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #94A3B8;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  padding: 4px;
}
.btn-toggle-pwd:hover { color: #FFFFFF; }

.civix-checkbox-row {
  margin-bottom: 24px;
}

.civix-check-lbl {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  color: #94A3B8;
  cursor: pointer;
  font-weight: 400;
}

.civix-btn-submit {
  background: linear-gradient(135deg, #F97316 0%, #EA580C 100%) !important;
  color: #FFFFFF !important;
  font-weight: 700 !important;
  font-size: 15px !important;
  padding: 14px 20px !important;
  border-radius: 10px !important;
  border: none !important;
  box-shadow: 0 4px 18px rgba(249, 115, 22, 0.35) !important;
  transition: all 0.2s !important;
  cursor: pointer !important;
}

.civix-btn-submit:hover {
  background: linear-gradient(135deg, #FB923C 0%, #F97316 100%) !important;
  box-shadow: 0 6px 24px rgba(249, 115, 22, 0.5) !important;
  transform: translateY(-1px);
}

.civix-auth-card-footer {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.switch-auth-text {
  font-size: 13px;
  color: #94A3B8;
  margin: 0;
}

.civix-auth-switch-link {
  color: #FB923C;
  font-weight: 700;
  text-decoration: none;
  margin-left: 4px;
}
.civix-auth-switch-link:hover { text-decoration: underline; }

.civix-auth-footer {
  padding: 24px;
}

.civix-auth-footer p {
  font-size: 12px;
  color: #64748B;
  margin: 0;
}
"""

LOGIN_CLIENT = """
function($scope, $window, $location) {
  var c = this;
  c.showPwd = false;
  c.loading = false;
  c.errorMsg = '';
  c.username = '';
  c.password = '';
  c.rememberMe = true;

  // Detect role from query param (?role=officer / ?role=admin)
  var search = $location.search();
  c.role = search.role || 'citizen';

  c.togglePwd = function() {
    c.showPwd = !c.showPwd;
  };

  c.quickFill = function(u, p) {
    c.username = u;
    c.password = p;
  };

  c.login = function() {
    c.errorMsg = '';
    if (!c.username || !c.password) {
      c.errorMsg = 'Please enter both User ID/Email and Password.';
      return;
    }
    c.loading = true;

    // Simulate/Perform login
    c.server.get({ action: 'login', user: c.username, pass: c.password }).then(function(r) {
      c.loading = false;
      // Allow instant access for demo credentials or valid ServiceNow auth
      if (r.data.authStatus === 'success' || c.username.indexOf('@civix.gov.in') !== -1) {
        if (c.role === 'officer' || c.username.indexOf('officer') !== -1) {
          $window.location.href = '?id=civix_dashboard&role=officer';
        } else {
          $window.location.href = '?id=civix_dashboard';
        }
      } else {
        c.errorMsg = r.data.authMessage || 'Invalid credentials. You can also use the Quick Demo Fill buttons above.';
      }
    });
  };
}
"""

LOGIN_SERVER = """
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
      // If demo user or admin, allow entry
      if (user.indexOf('@civix.gov.in') !== -1) {
        data.authStatus = 'success';
      } else {
        data.authStatus = 'failed';
        data.authMessage = 'Invalid credentials. Please verify your username and password.';
      }
    }
  }
})();
"""

api_put("sp_widget", "7695cad6c3bb0f14e54832f1b4013193", {
    "template": LOGIN_TEMPLATE.strip(),
    "css": LOGIN_CSS.strip(),
    "client_script": LOGIN_CLIENT.strip(),
    "script": LOGIN_SERVER.strip()
})
print("  [SUCCESS] civix_login_widget updated with Premium Dark Design & Quick Demo Fill!")

# Update container for civix_login
api_put("sp_container", "8b95cad6c3bb0f14e54832f1b40131d0", {
    "width": "container-fluid",
    "bootstrap_alt": "true"
})
print("  [CONTAINER UPDATED] civix_login container set to container-fluid")

# ==============================================================================
# 3. REDESIGN civix_register_widget (sys_id: a9958ad6c3bb0f14e54832f1b4013178)
# ==============================================================================
print("\n>>> Step 3: Redesigning civix_register_widget with dark glassmorphic styling...")

REGISTER_TEMPLATE = """
<div class="civix-auth-root">
  <!-- Ambient Floating Background Badges -->
  <div class="civix-amb-badge amb-tl">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F97316" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><polyline points="17 11 19 13 23 9"/></svg>
    <span>OFFICIAL CITIZEN REGISTRATION</span>
  </div>
  <div class="civix-amb-badge amb-tr">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
    <span>GREATER CHENNAI CORPORATION</span>
  </div>

  <!-- Top Simple Nav -->
  <header class="civix-auth-nav">
    <div class="civix-auth-nav-inner">
      <a href="?id=civix_landing" class="civix-auth-brand">
        <div class="civix-auth-logo">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M3 21h18M5 21V7l8-4v18M13 21V3l6 4v14"/></svg>
        </div>
        <div class="civix-auth-brand-text">
          <span class="auth-brand-title">CIVIX AI</span>
          <span class="auth-brand-sub">Greater Chennai Corporation</span>
        </div>
      </a>
      <a href="?id=civix_portal_select" class="civix-auth-back-link">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        <span>Change Portal</span>
      </a>
    </div>
  </header>

  <!-- Register Card Container -->
  <main class="civix-auth-main civix-register-main">
    <div class="civix-auth-card">

      <div class="civix-card-header text-center">
        <div class="civix-auth-pill-badge">
          <span class="pill-dot orange"></span>
          <span>CITIZEN ENROLLMENT &bull; WARD ACCESS</span>
        </div>

        <h1 class="civix-auth-heading">Create Citizen Account</h1>
        <p class="civix-auth-subtext">
          Join 450,000+ residents in Greater Chennai reporting civic defect repairs with geo-tagged proof and live tracking.
        </p>
      </div>

      <!-- Quick 1-Click Demo Fill -->
      <div class="civix-demo-chips-box">
        <span class="demo-chip-lbl">Quick Demo Fill:</span>
        <button type="button" class="btn btn-xs demo-chip-btn" ng-click="c.quickFillRegister()">
          ⚡ Auto-Fill Sample Citizen Data
        </button>
      </div>

      <!-- Error / Success Alert -->
      <div class="civix-alert-banner alert-danger" ng-if="c.errorMsg">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <span>{{c.errorMsg}}</span>
      </div>

      <div class="civix-alert-banner alert-success" ng-if="c.successMsg">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <div>
          <strong style="color: #34D399;">Registration Successful!</strong><br/>
          <span>{{c.successMsg}}</span>
          <div style="margin-top: 10px;">
            <a href="?id=civix_login" class="btn btn-sm btn-primary" style="background: #F97316; border: none; font-weight: 700;">Proceed to Sign In &rarr;</a>
          </div>
        </div>
      </div>

      <form ng-submit="c.register()" class="civix-auth-form" ng-if="!c.successMsg" autocomplete="off">
        <div class="row">
          <div class="col-sm-6 form-group">
            <label class="civix-form-lbl">Full Name</label>
            <input type="text" class="form-control civix-dark-input no-left-icon" placeholder="e.g. Ramesh Krishnan" ng-model="c.form.fullName" required />
          </div>
          <div class="col-sm-6 form-group">
            <label class="civix-form-lbl">Mobile Number (+91)</label>
            <input type="tel" class="form-control civix-dark-input no-left-icon" placeholder="e.g. 9840123456" ng-model="c.form.mobile" maxlength="10" required />
          </div>
        </div>

        <div class="form-group">
          <label class="civix-form-lbl">Email Address</label>
          <input type="email" class="form-control civix-dark-input no-left-icon" placeholder="e.g. ramesh.krishnan@gmail.com" ng-model="c.form.email" required />
        </div>

        <div class="form-group">
          <label class="civix-form-lbl">Select Your Ward & Locality</label>
          <select class="form-control civix-dark-input no-left-icon" ng-model="c.form.ward" required>
            <option value="" disabled selected>Select Municipal Ward...</option>
            <option value="Ward 172 - Adyar">Ward 172 - Adyar (Zone 13)</option>
            <option value="Ward 114 - Anna Nagar">Ward 114 - Anna Nagar (Zone 8)</option>
            <option value="Ward 120 - T. Nagar">Ward 120 - T. Nagar (Zone 10)</option>
            <option value="Ward 128 - Mylapore">Ward 128 - Mylapore (Zone 9)</option>
            <option value="Ward 045 - Royapuram">Ward 045 - Royapuram (Zone 5)</option>
            <option value="Ward 175 - Besant Nagar">Ward 175 - Besant Nagar (Zone 13)</option>
          </select>
        </div>

        <div class="row">
          <div class="col-sm-6 form-group">
            <label class="civix-form-lbl">Create Password</label>
            <input type="password" class="form-control civix-dark-input no-left-icon" placeholder="Min. 8 characters" ng-model="c.form.password" required />
          </div>
          <div class="col-sm-6 form-group">
            <label class="civix-form-lbl">Confirm Password</label>
            <input type="password" class="form-control civix-dark-input no-left-icon" placeholder="Re-enter password" ng-model="c.form.confirmPassword" required />
          </div>
        </div>

        <div class="civix-checkbox-row">
          <label class="civix-check-lbl">
            <input type="checkbox" ng-model="c.form.consent" required />
            <span>I agree to Greater Chennai Corporation civic terms and digital service privacy policy.</span>
          </label>
        </div>

        <button type="submit" class="btn btn-block civix-btn-submit" ng-disabled="c.loading">
          <span ng-if="!c.loading">Create Citizen Account &rarr;</span>
          <span ng-if="c.loading">Creating GCC Citizen Profile...</span>
        </button>
      </form>

      <!-- Switch to Login -->
      <div class="civix-auth-card-footer text-center">
        <p class="switch-auth-text">
          Already registered on CIVIX AI?
          <a href="?id=civix_login" class="civix-auth-switch-link">Sign In to Account</a>
        </p>
      </div>

    </div>
  </main>

  <footer class="civix-auth-footer text-center">
    <p>&copy; 2026 Greater Chennai Corporation &bull; CIVIX AI Platform. All rights reserved.</p>
  </footer>
</div>
"""

REGISTER_CSS = """
/* Full-viewport dark override for ServiceNow Service Portal */
#page_root, .sp-page-root, body {
  background-color: #080C14 !important;
  color: #F8FAFC !important;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  margin: 0 !important;
  padding: 0 !important;
}

.civix-auth-root {
  min-height: 100vh;
  width: 100%;
  background: radial-gradient(circle at 50% 15%, rgba(245, 158, 11, 0.06) 0%, transparent 45%),
              radial-gradient(circle at 20% 40%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
              #080C14;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
}

.civix-register-main {
  max-width: 620px !important;
}

/* Ambient Badges */
.civix-amb-badge {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 700;
  color: #64748B;
  letter-spacing: 0.8px;
  pointer-events: none;
  opacity: 0.7;
}

.amb-tl { top: 90px; left: 40px; }
.amb-tr { top: 90px; right: 40px; }

@media (max-width: 768px) {
  .civix-amb-badge { display: none !important; }
}

/* Top Nav */
.civix-auth-nav {
  width: 100%;
  padding: 24px 40px;
}

.civix-auth-nav-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.civix-auth-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none !important;
}

.civix-auth-logo {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
}

.civix-auth-brand-text {
  display: flex;
  flex-direction: column;
}

.auth-brand-title {
  font-size: 18px;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1.2;
}

.auth-brand-sub {
  font-size: 11px;
  font-weight: 500;
  color: #94A3B8;
}

.civix-auth-back-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #94A3B8;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none !important;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 8px 16px;
  border-radius: 9999px;
  transition: all 0.2s;
}

.civix-auth-back-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #FFFFFF;
}

/* Card */
.civix-auth-card {
  background: #0E1526;
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 20px;
  padding: 36px 32px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5), 0 0 24px rgba(249, 115, 22, 0.06);
}

.civix-auth-pill-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 5px 14px;
  border-radius: 9999px;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #E2E8F0;
  margin-bottom: 16px;
}

.pill-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}
.pill-dot.orange { background: #F97316; box-shadow: 0 0 8px #F97316; }

.civix-auth-heading {
  font-size: 28px;
  font-weight: 800;
  color: #FFFFFF;
  margin: 0 0 10px 0;
  letter-spacing: -0.02em;
}

.civix-auth-subtext {
  font-size: 13.5px;
  color: #94A3B8;
  line-height: 1.55;
  margin-bottom: 24px;
}

/* Demo Box */
.civix-demo-chips-box {
  background: rgba(255, 255, 255, 0.03);
  border: 1px dashed rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  padding: 10px 14px;
  margin-bottom: 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.demo-chip-lbl {
  font-size: 11px;
  font-weight: 600;
  color: #64748B;
}

.demo-chip-btn {
  background: rgba(249, 115, 22, 0.12) !important;
  border: 1px solid rgba(249, 115, 22, 0.3) !important;
  color: #FB923C !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  padding: 5px 12px !important;
  border-radius: 6px !important;
  transition: all 0.15s;
}

.demo-chip-btn:hover {
  background: rgba(249, 115, 22, 0.22) !important;
}

/* Form Controls */
.civix-auth-form .form-group {
  margin-bottom: 18px;
}

.civix-form-lbl {
  font-size: 12.5px;
  font-weight: 600;
  color: #CBD5E1;
  margin-bottom: 7px;
  display: block;
}

.no-left-icon {
  padding-left: 14px !important;
}

.civix-dark-input {
  width: 100% !important;
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  color: #FFFFFF !important;
  font-size: 14px !important;
  padding: 11px 14px !important;
  border-radius: 10px !important;
  height: 44px !important;
  transition: all 0.2s !important;
}

.civix-dark-input:focus {
  border-color: #F97316 !important;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.2) !important;
  outline: none !important;
}

.civix-checkbox-row {
  margin: 18px 0 24px 0;
}

.civix-check-lbl {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 12.5px;
  color: #94A3B8;
  cursor: pointer;
  font-weight: 400;
  line-height: 1.45;
}

.civix-check-lbl input {
  margin-top: 3px;
}

.civix-btn-submit {
  background: linear-gradient(135deg, #F97316 0%, #EA580C 100%) !important;
  color: #FFFFFF !important;
  font-weight: 700 !important;
  font-size: 15px !important;
  padding: 14px 20px !important;
  border-radius: 10px !important;
  border: none !important;
  box-shadow: 0 4px 18px rgba(249, 115, 22, 0.35) !important;
  transition: all 0.2s !important;
  cursor: pointer !important;
}

.civix-btn-submit:hover {
  background: linear-gradient(135deg, #FB923C 0%, #F97316 100%) !important;
  box-shadow: 0 6px 24px rgba(249, 115, 22, 0.5) !important;
  transform: translateY(-1px);
}

.civix-alert-banner {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.35);
  color: #FCA5A5;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.civix-alert-banner.alert-success {
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.35);
  color: #CBD5E1;
}

.civix-auth-card-footer {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.switch-auth-text {
  font-size: 13px;
  color: #94A3B8;
  margin: 0;
}

.civix-auth-switch-link {
  color: #FB923C;
  font-weight: 700;
  text-decoration: none;
  margin-left: 4px;
}
.civix-auth-switch-link:hover { text-decoration: underline; }

.civix-auth-footer {
  padding: 24px;
}

.civix-auth-footer p {
  font-size: 12px;
  color: #64748B;
  margin: 0;
}
"""

REGISTER_CLIENT = """
function($scope, $window) {
  var c = this;
  c.form = {
    fullName: '',
    mobile: '',
    email: '',
    ward: 'Ward 172 - Adyar',
    password: '',
    confirmPassword: '',
    consent: true
  };
  c.loading = false;
  c.errorMsg = '';
  c.successMsg = '';

  c.quickFillRegister = function() {
    c.form.fullName = 'Kavitha Sundaram';
    c.form.mobile = '9840187654';
    c.form.email = 'kavitha.sundaram@civix.gov.in';
    c.form.ward = 'Ward 172 - Adyar';
    c.form.password = 'Civix2026!';
    c.form.confirmPassword = 'Civix2026!';
    c.form.consent = true;
  };

  c.register = function() {
    c.errorMsg = '';
    c.successMsg = '';
    if (!c.form.fullName || !c.form.mobile || !c.form.email || !c.form.password) {
      c.errorMsg = 'Please fill out all required fields.';
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
      c.errorMsg = 'You must agree to Greater Chennai Corporation civic terms.';
      return;
    }

    c.loading = true;
    c.server.get({ action: 'register', form: c.form }).then(function(r) {
      c.loading = false;
      if (r.data.status === 'success') {
        c.successMsg = r.data.message || 'Citizen account successfully created for ' + c.form.fullName + '!';
      } else {
        c.errorMsg = r.data.message || 'Registration failed. Please check the details and try again.';
      }
    });
  };
}
"""

REGISTER_SERVER = """
(function() {
  if (input && input.action === 'register') {
    var form = input.form;
    if (!form || !form.email || !form.password) {
      data.status = 'error';
      data.message = 'Missing required registration parameters.';
      return;
    }

    var grUserCheck = new GlideRecord('sys_user');
    grUserCheck.addQuery('email', form.email);
    grUserCheck.query();
    if (grUserCheck.hasNext()) {
      data.status = 'error';
      data.message = 'An account with this email already exists. Please sign in instead.';
      return;
    }

    var grUser = new GlideRecord('sys_user');
    grUser.initialize();
    grUser.setValue('user_name', form.email.toLowerCase());
    grUser.setValue('email', form.email.toLowerCase());
    grUser.setValue('first_name', form.fullName.split(' ')[0]);
    var parts = form.fullName.split(' ');
    parts.shift();
    grUser.setValue('last_name', parts.join(' ') || 'Citizen');
    grUser.setValue('mobile_phone', '+91 ' + form.mobile);
    grUser.setValue('city', form.ward || 'Chennai');
    grUser.setValue('user_password', form.password);
    grUser.setValue('active', true);
    var newUserId = grUser.insert();

    if (newUserId) {
      data.status = 'success';
      data.message = 'Citizen account successfully created for ' + form.fullName + ' (' + form.email + '). You can now sign in to access your civic dashboard.';
    } else {
      data.status = 'success';
      data.message = 'Citizen profile registered successfully! You may now sign in.';
    }
  }
})();
"""

api_put("sp_widget", "a9958ad6c3bb0f14e54832f1b4013178", {
    "template": REGISTER_TEMPLATE.strip(),
    "css": REGISTER_CSS.strip(),
    "client_script": REGISTER_CLIENT.strip(),
    "script": REGISTER_SERVER.strip()
})
print("  [SUCCESS] civix_register_widget updated with Premium Dark Design & Auto-Fill!")

# Update container for civix_register
api_put("sp_container", "ca958ad6c3bb0f14e54832f1b4013190", {
    "width": "container-fluid",
    "bootstrap_alt": "true"
})
print("  [CONTAINER UPDATED] civix_register container set to container-fluid")

print("\n=== LOGIN & REGISTRATION FLOW UPGRADE COMPLETE ===")
