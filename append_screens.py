"""
Complete Screen Builder for CIVIX AI (Screens 4 to 11)
"""

# Appending to build_all_screens.py
import os
import sys

code_screens_4_to_11 = '''
# ==============================================================================
# SCREEN 4: REGISTRATION WIDGET
# ==============================================================================
def create_register_widget():
    print("\\n>>> Building Screen 4: Registration Widget")
    template = """
<div class="civix-page civix-container civix-auth-page">
  <div class="civix-auth-card">
    <div class="civix-auth-header text-center">
      <div class="civix-brand-mark"><span class="glyphicon glyphicon-user"></span></div>
      <h2 class="civix-auth-title">Create Your CIVIX AI Account</h2>
      <p class="civix-auth-subtitle">Register to report civic issues and follow your service requests.</p>
    </div>

    <div ng-if="c.successMsg" class="alert alert-success civix-alert">
      <h4><span class="glyphicon glyphicon-ok-sign"></span> Registration Successful!</h4>
      <p>{{c.successMsg}}</p>
      <div class="civix-smtp-note">
        <strong>Notice:</strong> Outbound email delivery (SMTP) is inactive on this developer instance. Your citizen account has been created directly in ServiceNow.
      </div>
      <div class="text-center" style="margin-top: 15px;">
        <a href="?id=civix_login" class="btn btn-primary">Proceed to Sign In &rarr;</a>
      </div>
    </div>

    <div ng-if="c.errorMsg" class="alert alert-danger civix-alert">
      <span class="glyphicon glyphicon-exclamation-sign"></span> {{c.errorMsg}}
    </div>

    <form ng-if="!c.successMsg" ng-submit="c.register()" novalidate>
      <!-- Group 1: Personal Details -->
      <div class="civix-form-section">
        <h4 class="civix-form-section-title">1. Personal Details</h4>
        <div class="form-group">
          <label for="fullName">Full Name <span class="text-danger">*</span></label>
          <input type="text" id="fullName" class="form-control" ng-model="c.form.fullName" required placeholder="e.g. Priya Sharma" />
        </div>
        <div class="row">
          <div class="col-md-6 form-group">
            <label for="mobile">Mobile Number (+91) <span class="text-danger">*</span></label>
            <div class="input-group">
              <span class="input-group-addon">+91</span>
              <input type="tel" id="mobile" class="form-control" ng-model="c.form.mobile" maxlength="10" placeholder="9876543210" required />
            </div>
          </div>
          <div class="col-md-6 form-group">
            <label for="email">Email Address <span class="text-danger">*</span></label>
            <input type="email" id="email" class="form-control" ng-model="c.form.email" required placeholder="priya@example.com" />
          </div>
        </div>
      </div>

      <!-- Group 2: Account Security (Independent eye toggles!) -->
      <div class="civix-form-section">
        <h4 class="civix-form-section-title">2. Account Security</h4>
        <div class="row">
          <div class="col-md-6 form-group">
            <label for="password">Password <span class="text-danger">*</span></label>
            <div class="input-group">
              <input type="{{c.showPwd ? 'text' : 'password'}}" id="password" class="form-control" ng-model="c.form.password" required placeholder="Min 8 characters" />
              <span class="input-group-btn">
                <button type="button" class="btn btn-default" ng-click="c.togglePwd()" aria-label="Toggle password visibility">
                  <span class="glyphicon" ng-class="c.showPwd ? 'glyphicon-eye-close' : 'glyphicon-eye-open'"></span>
                </button>
              </span>
            </div>
          </div>
          <div class="col-md-6 form-group">
            <label for="confirmPassword">Confirm Password <span class="text-danger">*</span></label>
            <div class="input-group">
              <input type="{{c.showConfirmPwd ? 'text' : 'password'}}" id="confirmPassword" class="form-control" ng-model="c.form.confirmPassword" required placeholder="Re-enter password" />
              <span class="input-group-btn">
                <button type="button" class="btn btn-default" ng-click="c.toggleConfirmPwd()" aria-label="Toggle confirm password visibility">
                  <span class="glyphicon" ng-class="c.showConfirmPwd ? 'glyphicon-eye-close' : 'glyphicon-eye-open'"></span>
                </button>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Group 3: Location -->
      <div class="civix-form-section">
        <h4 class="civix-form-section-title">3. Municipal Locality</h4>
        <div class="row">
          <div class="col-md-4 form-group">
            <label for="state">State / UT <span class="text-danger">*</span></label>
            <select id="state" class="form-control" ng-model="c.form.state">
              <option value="Tamil Nadu">Tamil Nadu</option>
              <option value="Karnataka">Karnataka</option>
              <option value="Maharashtra">Maharashtra</option>
              <option value="Delhi">Delhi</option>
              <option value="Telangana">Telangana</option>
              <option value="Kerala">Kerala</option>
            </select>
          </div>
          <div class="col-md-4 form-group">
            <label for="district">District <span class="text-danger">*</span></label>
            <input type="text" id="district" class="form-control" ng-model="c.form.district" placeholder="e.g. Chennai" required />
          </div>
          <div class="col-md-4 form-group">
            <label for="city">City / Town <span class="text-danger">*</span></label>
            <input type="text" id="city" class="form-control" ng-model="c.form.city" placeholder="e.g. Chennai" required />
          </div>
        </div>
        <div class="form-group">
          <label for="ward">Ward / Locality (Optional)</label>
          <input type="text" id="ward" class="form-control" ng-model="c.form.ward" placeholder="e.g. Ward 12 - T. Nagar" />
        </div>
      </div>

      <!-- Group 4: Preferences & Consent -->
      <div class="civix-form-section">
        <h4 class="civix-form-section-title">4. Preferences & Consent</h4>
        <div class="form-group">
          <label for="prefLang">Preferred Language</label>
          <select id="prefLang" class="form-control" ng-model="c.form.prefLang">
            <option value="en">English</option>
            <option value="ta">Tamil (தமிழ்)</option>
            <option value="hi">Hindi (हिन्दी)</option>
            <option value="te">Telugu (తెలుగు)</option>
            <option value="kn">Kannada (ಕನ್ನಡ)</option>
            <option value="ml">Malayalam (മലയാളം)</option>
          </select>
        </div>
        <div class="checkbox">
          <label>
            <input type="checkbox" ng-model="c.form.consent" required />
            I agree to the CIVIX AI Municipal Terms of Service and Privacy Policy. I confirm I am a resident registering for civic assistance.
          </label>
        </div>
      </div>

      <div class="civix-form-actions">
        <button type="submit" class="civix-btn civix-btn-primary btn-block btn-lg" ng-disabled="c.loading">
          <span ng-if="c.loading"><span class="glyphicon glyphicon-refresh glyphicon-spin"></span> Creating Account...</span>
          <span ng-if="!c.loading"><span class="glyphicon glyphicon-check"></span> Register Citizen Account</span>
        </button>
      </div>

      <div class="text-center civix-auth-footer">
        Already have an account? <a href="?id=civix_login" class="civix-link">Sign In</a>
      </div>
    </form>
  </div>
</div>
"""

    css = """
.civix-auth-page {
  padding: 50px 20px 80px;
}
.civix-auth-card {
  max-width: 680px;
  margin: 0 auto;
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 36px 32px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}
.civix-brand-mark {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: #E1F5EA;
  color: #087F8C;
  font-size: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}
.civix-auth-title {
  font-size: 24px;
  font-weight: 800;
  color: #123E46;
  margin: 0 0 6px 0;
}
.civix-auth-subtitle {
  color: #61777B;
  font-size: 14px;
  margin-bottom: 24px;
}
.civix-form-section {
  border-bottom: 1px solid #E5E7EB;
  padding-bottom: 20px;
  margin-bottom: 20px;
}
.civix-form-section-title {
  font-size: 14px;
  font-weight: 700;
  color: #087F8C;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 14px;
}
.civix-smtp-note {
  background: #FEF3C7;
  color: #92400E;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 12px;
  margin-top: 10px;
}
.civix-link {
  color: #087F8C;
  font-weight: 700;
}
.civix-auth-footer {
  margin-top: 20px;
  font-size: 14px;
  color: #61777B;
}
"""

    client_script = """
function($scope) {
  var c = this;
  c.form = {
    state: 'Tamil Nadu',
    prefLang: 'en',
    consent: false
  };
  c.showPwd = false;
  c.showConfirmPwd = false;
  c.loading = false;

  c.togglePwd = function() { c.showPwd = !c.showPwd; };
  c.toggleConfirmPwd = function() { c.showConfirmPwd = !c.showConfirmPwd; };

  c.register = function() {
    c.errorMsg = '';
    c.successMsg = '';
    if (!c.form.fullName || !c.form.mobile || !c.form.email || !c.form.password) {
      c.errorMsg = 'Please complete all required fields.';
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
      c.errorMsg = 'You must agree to the Terms of Service to register.';
      return;
    }

    c.loading = true;
    c.server.get({ action: 'register', form: c.form }).then(function(r) {
      c.loading = false;
      if (r.data.status === 'success') {
        c.successMsg = r.data.message;
      } else {
        c.errorMsg = r.data.message || 'Registration failed. Please try again.';
      }
    });
  };
}
"""

    server_script = """
(function() {
  if (input && input.action === 'register') {
    var form = input.form;
    if (!form || !form.email || !form.password) {
      data.status = 'error';
      data.message = 'Missing required registration parameters.';
      return;
    }

    // Check duplicate
    var grUserCheck = new GlideRecord('sys_user');
    grUserCheck.addQuery('email', form.email);
    grUserCheck.query();
    if (grUserCheck.hasNext()) {
      data.status = 'error';
      data.message = 'An account with this email address already exists. Please sign in instead.';
      return;
    }

    // Create user natively in sys_user
    var grUser = new GlideRecord('sys_user');
    grUser.initialize();
    grUser.setValue('user_name', form.email.toLowerCase());
    grUser.setValue('email', form.email.toLowerCase());
    grUser.setValue('first_name', form.fullName.split(' ')[0]);
    var lastParts = form.fullName.split(' ');
    lastParts.shift();
    grUser.setValue('last_name', lastParts.join(' ') || 'Citizen');
    grUser.setValue('mobile_phone', '+91 ' + form.mobile);
    grUser.setValue('city', form.city || form.district || 'Chennai');
    grUser.setValue('user_password', form.password);
    grUser.setValue('active', true);
    var newUserId = grUser.insert();

    if (newUserId) {
      // Safely assign x_civic_ai_citizen role
      var grRole = new GlideRecord('sys_user_role');
      if (grRole.get('name', 'x_civic_ai_citizen')) {
        var grUserRole = new GlideRecord('sys_user_has_role');
        grUserRole.initialize();
        grUserRole.setValue('user', newUserId);
        grUserRole.setValue('role', grRole.getUniqueValue());
        grUserRole.insert();
      }

      data.status = 'success';
      data.message = 'Citizen account successfully created for ' + form.fullName + ' (' + form.email + '). You can now sign in to access your dashboard.';
    } else {
      data.status = 'error';
      data.message = 'Unable to create user record. Please check instance security permissions.';
    }
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Registration",
        "id": "civix_register_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_register_widget", widget_data, "Registration Widget")
    page_id = create_page_structure("civix_register", "Registration", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 5: LOGIN WIDGET
# ==============================================================================
def create_login_widget():
    print("\\n>>> Building Screen 5: Login Widget")
    template = """
<div class="civix-page civix-container civix-auth-page">
  <div class="civix-auth-card civix-login-card">
    <div class="civix-auth-header text-center">
      <div class="civix-brand-mark"><span class="glyphicon glyphicon-lock"></span></div>
      <h2 class="civix-auth-title">Welcome Back</h2>
      <p class="civix-auth-subtitle">Sign in to manage your civic-service requests.</p>
    </div>

    <div ng-if="c.errorMsg" class="alert alert-danger civix-alert">
      <span class="glyphicon glyphicon-exclamation-sign"></span> {{c.errorMsg}}
    </div>

    <div ng-if="c.data.isLoggedIn" class="alert alert-info text-center">
      <p>You are already signed in as <strong>{{c.data.userName}}</strong>.</p>
      <a href="?id=civix_dashboard" class="btn btn-primary" style="margin-top: 10px;">Go to Citizen Dashboard &rarr;</a>
    </div>

    <form ng-if="!c.data.isLoggedIn" ng-submit="c.login()" novalidate>
      <div class="form-group">
        <label for="username">User ID / Registered Email <span class="text-danger">*</span></label>
        <input type="text" id="username" class="form-control" ng-model="c.username" required placeholder="admin or citizen email" />
      </div>

      <div class="form-group">
        <div class="civix-pwd-label-row">
          <label for="loginPassword">Password <span class="text-danger">*</span></label>
          <a href="?id=civix_recovery" class="civix-forgot-link">Forgot Password?</a>
        </div>
        <div class="input-group">
          <input type="{{c.showPwd ? 'text' : 'password'}}" id="loginPassword" class="form-control" ng-model="c.password" required placeholder="Enter your password" />
          <span class="input-group-btn">
            <button type="button" class="btn btn-default" ng-click="c.togglePwd()" aria-label="Toggle password visibility">
              <span class="glyphicon" ng-class="c.showPwd ? 'glyphicon-eye-close' : 'glyphicon-eye-open'"></span>
            </button>
          </span>
        </div>
      </div>

      <div class="checkbox">
        <label>
          <input type="checkbox" ng-model="c.rememberMe" /> Remember me on this device
        </label>
      </div>

      <div class="civix-form-actions">
        <button type="submit" class="civix-btn civix-btn-primary btn-block btn-lg" ng-disabled="c.loading">
          <span ng-if="c.loading"><span class="glyphicon glyphicon-refresh glyphicon-spin"></span> Verifying...</span>
          <span ng-if="!c.loading"><span class="glyphicon glyphicon-log-in"></span> Sign In</span>
        </button>
      </div>

      <div class="text-center civix-auth-footer">
        Don't have an account? <a href="?id=civix_register" class="civix-link">Create Account</a>
      </div>
      <div class="text-center" style="margin-top: 10px;">
        <a href="?id=civix_landing" class="text-muted"><small>&larr; Back to Public Landing Page</small></a>
      </div>
    </form>
  </div>
</div>
"""

    css = """
.civix-login-card {
  max-width: 460px;
}
.civix-pwd-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.civix-forgot-link {
  font-size: 12px;
  color: #087F8C;
  font-weight: 600;
}
"""

    client_script = """
function($scope, $window) {
  var c = this;
  c.showPwd = false;
  c.loading = false;
  c.togglePwd = function() { c.showPwd = !c.showPwd; };

  c.login = function() {
    c.errorMsg = '';
    if (!c.username || !c.password) {
      c.errorMsg = 'Please enter both User ID/Email and Password.';
      return;
    }
    c.loading = true;
    c.server.get({ action: 'login', user: c.username, pass: c.password }).then(function(r) {
      c.loading = false;
      if (r.data.authStatus === 'success') {
        $window.location.href = '?id=civix_dashboard';
      } else {
        c.errorMsg = r.data.authMessage || 'Invalid credentials. Please verify your username and password.';
      }
    });
  };
}
"""

    server_script = """
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
      data.authStatus = 'failed';
      data.authMessage = 'Invalid credentials. Please check your username and password.';
    }
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Login",
        "id": "civix_login_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_login_widget", widget_data, "Login Widget")
    page_id = create_page_structure("civix_login", "Login", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 6: ACCOUNT RECOVERY WIDGET
# ==============================================================================
def create_recovery_widget():
    print("\\n>>> Building Screen 6: Account Recovery Widget")
    template = """
<div class="civix-page civix-container civix-auth-page">
  <div class="civix-auth-card civix-login-card">
    <div class="civix-auth-header text-center">
      <div class="civix-brand-mark"><span class="glyphicon glyphicon-refresh"></span></div>
      <h2 class="civix-auth-title">Account Recovery</h2>
      <p class="civix-auth-subtitle">Enter your registered email address or username to receive password reset guidance.</p>
    </div>

    <div ng-if="c.submitted" class="alert alert-success">
      <h4><span class="glyphicon glyphicon-ok-sign"></span> Recovery Request Received</h4>
      <p>If an account exists for the provided identifier, instructions have been generated according to municipal security policy.</p>
      <div class="civix-smtp-note" style="margin-top: 10px;">
        <strong>Notice:</strong> Outbound SMTP is disabled on this ServiceNow development instance. For sandbox password resets, please contact the instance administrator.
      </div>
      <div class="text-center" style="margin-top: 16px;">
        <a href="?id=civix_login" class="btn btn-default">&larr; Return to Sign In</a>
      </div>
    </div>

    <form ng-if="!c.submitted" ng-submit="c.submitRecovery()">
      <div class="form-group">
        <label for="recoveryId">Registered Email or Username <span class="text-danger">*</span></label>
        <input type="text" id="recoveryId" class="form-control" ng-model="c.recoveryId" required placeholder="priya@example.com" />
      </div>

      <div class="civix-form-actions">
        <button type="submit" class="civix-btn civix-btn-primary btn-block btn-lg" ng-disabled="c.loading">
          <span class="glyphicon glyphicon-send"></span> Submit Recovery Request
        </button>
      </div>

      <div class="text-center civix-auth-footer">
        <a href="?id=civix_login" class="civix-link">&larr; Back to Sign In</a>
      </div>
    </form>
  </div>
</div>
"""

    css = """
.civix-auth-card { max-width: 480px; }
"""

    client_script = """
function($scope) {
  var c = this;
  c.submitted = false;
  c.submitRecovery = function() {
    if (!c.recoveryId) return;
    c.loading = true;
    c.server.get({ action: 'recover', id: c.recoveryId }).then(function() {
      c.loading = false;
      c.submitted = true;
    });
  };
}
"""

    server_script = """
(function() {
  if (input && input.action === 'recover') {
    // Privacy-preserving: Do not reveal whether user exists
    data.received = true;
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Account Recovery",
        "id": "civix_recovery_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_recovery_widget", widget_data, "Recovery Widget")
    page_id = create_page_structure("civix_recovery", "Account Recovery", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 7: CUSTOMER DASHBOARD WIDGET (Faithful to design image reference)
# ==============================================================================
def create_dashboard_widget():
    print("\\n>>> Building Screen 7: Customer Dashboard Widget")
    template = """
<div class="civix-dashboard-page">
  <div class="civix-dashboard-container">
    <!-- Top Greeting Banner -->
    <div class="civix-greeting-banner">
      <div class="civix-greeting-left">
        <h1 class="civix-welcome-text">Welcome back,<br/><span class="civix-welcome-name">{{c.data.citizenName}}!</span> 👋</h1>
        <p class="civix-welcome-sub">Together for a cleaner, safer and smarter city. Report issues, track progress and help improve our community.</p>
      </div>
      <div class="civix-weather-pill">
        <div class="civix-loc-icon"><span class="glyphicon glyphicon-map-marker"></span></div>
        <div class="civix-loc-info">
          <strong>Chennai, Tamil Nadu</strong>
          <small>32°C &bull; Mostly Clear &bull; Ward 12</small>
        </div>
      </div>
    </div>

    <!-- 4 KPI Summary Cards -->
    <div class="row civix-kpi-row">
      <div class="col-md-3 col-sm-6">
        <div class="civix-kpi-card kpi-total">
          <div class="civix-kpi-icon"><span class="glyphicon glyphicon-file"></span></div>
          <div class="civix-kpi-body">
            <div class="civix-kpi-num">{{c.data.counts.total}}</div>
            <div class="civix-kpi-title">Total Complaints</div>
            <div class="civix-kpi-trend text-success">&uarr; 3 this month</div>
          </div>
        </div>
      </div>
      <div class="col-md-3 col-sm-6">
        <div class="civix-kpi-card kpi-resolved">
          <div class="civix-kpi-icon"><span class="glyphicon glyphicon-ok-sign"></span></div>
          <div class="civix-kpi-body">
            <div class="civix-kpi-num">{{c.data.counts.resolved}}</div>
            <div class="civix-kpi-title">Resolved</div>
            <div class="civix-kpi-trend text-success">&uarr; 2 this month</div>
          </div>
        </div>
      </div>
      <div class="col-md-3 col-sm-6">
        <div class="civix-kpi-card kpi-progress">
          <div class="civix-kpi-icon"><span class="glyphicon glyphicon-time"></span></div>
          <div class="civix-kpi-body">
            <div class="civix-kpi-num">{{c.data.counts.in_progress}}</div>
            <div class="civix-kpi-title">In Progress</div>
            <div class="civix-kpi-trend text-warning">&ndash; same as last month</div>
          </div>
        </div>
      </div>
      <div class="col-md-3 col-sm-6">
        <div class="civix-kpi-card kpi-action">
          <div class="civix-kpi-icon"><span class="glyphicon glyphicon-exclamation-sign"></span></div>
          <div class="civix-kpi-body">
            <div class="civix-kpi-num">{{c.data.counts.awaiting}}</div>
            <div class="civix-kpi-title">Awaiting Action</div>
            <div class="civix-kpi-trend text-danger">&darr; 1 from last month</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="row civix-dash-main-row">
      <!-- Left Column: Report Shortcuts & Recent Complaints -->
      <div class="col-md-8 civix-dash-left">
        <!-- Report a New Issue Category Picker -->
        <div class="civix-panel">
          <div class="civix-panel-header">
            <h3>Report a New Issue</h3>
            <p>Select a service category to report an issue in your area.</p>
          </div>
          <div class="row civix-cat-pill-row">
            <div class="col-xs-6 col-md-2-4" ng-repeat="cat in c.categories">
              <a href="?id=civix_report_issue&cat={{cat.name}}" class="civix-category-box">
                <div class="civix-cat-icon" ng-class="cat.css">
                  <span class="glyphicon" ng-class="cat.icon"></span>
                </div>
                <div class="civix-cat-name">{{cat.name}} &gt;</div>
                <div class="civix-cat-desc">{{cat.sub}}</div>
              </a>
            </div>
          </div>
        </div>

        <!-- Recent Complaints Table -->
        <div class="civix-panel">
          <div class="civix-panel-header civix-flex-between">
            <div>
              <h3>Recent Complaints</h3>
              <p>Here are your latest reported civic issues</p>
            </div>
            <a href="?id=civix_my_cases" class="civix-view-all-link">View All &rarr;</a>
          </div>

          <div ng-if="c.data.recentCases.length === 0" class="civix-empty-dash text-center">
            <p>No recent complaints found for this citizen account.</p>
            <a href="?id=civix_report_issue" class="btn btn-sm btn-primary">Report an Issue Now</a>
          </div>

          <div class="civix-complaints-list" ng-if="c.data.recentCases.length > 0">
            <div class="civix-complaint-item" ng-repeat="item in c.data.recentCases">
              <div class="civix-complaint-thumb" ng-class="'thumb-' + item.categoryClass">
                <span class="glyphicon" ng-class="item.icon"></span>
              </div>
              <div class="civix-complaint-info">
                <div class="civix-comp-id">{{item.number}}</div>
                <div class="civix-comp-title">{{item.short_description}}</div>
                <div class="civix-comp-loc">
                  <span class="glyphicon glyphicon-map-marker"></span> {{item.location}} &bull; 
                  <span class="glyphicon glyphicon-calendar"></span> {{item.date}}
                </div>
              </div>
              <div class="civix-complaint-status">
                <span class="civix-status-badge" ng-class="'status-' + item.statusClass">{{item.status}}</span>
              </div>
              <a href="?id=civix_track_case&sys_id={{item.sys_id}}" class="civix-complaint-arrow">&rsaquo;</a>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Nearby Alerts & Civic AI Assistant -->
      <div class="col-md-4 civix-dash-right">
        <!-- Nearby Alerts -->
        <div class="civix-panel">
          <div class="civix-panel-header civix-flex-between">
            <h3>Nearby Alerts</h3>
            <span class="badge badge-info">Chennai</span>
          </div>
          <div class="civix-alerts-list">
            <div class="civix-alert-item" ng-repeat="alert in c.alerts">
              <div class="civix-alert-icon" ng-class="alert.css"><span class="glyphicon" ng-class="alert.icon"></span></div>
              <div class="civix-alert-text">
                <div class="civix-alert-title">{{alert.title}}</div>
                <div class="civix-alert-dist">{{alert.dist}} &bull; {{alert.time}}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Civic AI Assistant Panel (Matches Reference) -->
        <div class="civix-panel civix-assistant-card">
          <div class="civix-assistant-head">
            <div class="civix-assistant-bot-icon">
              <span class="glyphicon glyphicon-cog"></span>
            </div>
            <strong>Civic AI Assistant</strong>
          </div>
          <div class="civix-assistant-body">
            <div class="civix-chat-bubble">
              Hi {{c.data.citizenName}}! 👋<br/>
              I'm your Civic AI Assistant. How can I help you today?
            </div>
            <div class="civix-chat-prompts">
              <a href="?id=civix_my_cases" class="civix-prompt-pill"><span class="glyphicon glyphicon-file"></span> Track my complaint</a>
              <a href="?id=civix_report_issue" class="civix-prompt-pill"><span class="glyphicon glyphicon-plus"></span> Report a new issue</a>
              <a href="?id=civix_landing#services" class="civix-prompt-pill"><span class="glyphicon glyphicon-info-sign"></span> Know service information</a>
              <a href="tel:1913" class="civix-prompt-pill"><span class="glyphicon glyphicon-earphone"></span> Call 1913 Helpline</a>
            </div>
            <div class="civix-chat-input-bar">
              <input type="text" placeholder="Type your message..." class="civix-chat-input" />
              <button class="civix-chat-send-btn" type="button"><span class="glyphicon glyphicon-send"></span></button>
            </div>
            <small class="text-muted text-center" style="display:block; margin-top: 8px;">Supports 22 scheduled Indian languages</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

    css = """
.civix-dashboard-page {
  background: #F7FAFA;
  padding: 30px 20px 80px;
}
.civix-dashboard-container {
  max-width: 1360px;
  margin: 0 auto;
}
.civix-greeting-banner {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 28px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.civix-welcome-text {
  font-size: 28px;
  font-weight: 800;
  color: #123E46;
  margin: 0 0 6px 0;
}
.civix-welcome-name { color: #087F8C; }
.civix-welcome-sub {
  color: #61777B;
  font-size: 14px;
  margin: 0;
}
.civix-weather-pill {
  background: #E1F5EA;
  border: 1px solid #B7E4C7;
  padding: 10px 18px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.civix-loc-icon { font-size: 20px; color: #087F8C; }
.civix-loc-info strong { display: block; font-size: 13px; color: #183238; }
.civix-loc-info small { color: #61777B; font-size: 11px; }

.civix-kpi-row { margin-bottom: 24px; }
.civix-kpi-card {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 14px;
  padding: 20px 18px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.civix-kpi-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}
.kpi-total .civix-kpi-icon { background: #E0F2FE; color: #0284C7; }
.kpi-resolved .civix-kpi-icon { background: #E1F5EA; color: #18794E; }
.kpi-progress .civix-kpi-icon { background: #FEF3C7; color: #D97706; }
.kpi-action .civix-kpi-icon { background: #FEE2E2; color: #DC2626; }
.civix-kpi-num { font-size: 26px; font-weight: 800; color: #183238; line-height: 1; }
.civix-kpi-title { font-size: 13px; font-weight: 600; color: #61777B; margin: 4px 0 2px; }
.civix-kpi-trend { font-size: 11px; font-weight: 600; }

.civix-panel {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 14px;
  padding: 24px;
  margin-bottom: 24px;
}
.civix-panel-header { margin-bottom: 18px; }
.civix-panel-header h3 { font-size: 18px; font-weight: 700; color: #183238; margin: 0 0 4px 0; }
.civix-panel-header p { font-size: 13px; color: #61777B; margin: 0; }
.civix-flex-between { display: flex; justify-content: space-between; align-items: center; }
.civix-view-all-link { font-size: 13px; font-weight: 700; color: #087F8C; text-decoration: none; }

.col-md-2-4 { width: 20%; float: left; padding: 0 6px; }
@media (max-width: 991px) { .col-md-2-4 { width: 50%; margin-bottom: 12px; } }
.civix-category-box {
  display: block;
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 16px 10px;
  text-align: center;
  text-decoration: none;
  transition: all 0.2s;
}
.civix-category-box:hover {
  border-color: #087F8C;
  transform: translateY(-2px);
  text-decoration: none;
}
.civix-cat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  margin: 0 auto 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}
.cat-water { background: #E0F2FE; color: #0284C7; }
.cat-elec { background: #FEF3C7; color: #D97706; }
.cat-roads { background: #F3F4F6; color: #374151; }
.cat-drain { background: #EDE9FE; color: #7C3AED; }
.cat-flood { background: #E0E7FF; color: #4F46E5; }
.civix-cat-name { font-size: 13px; font-weight: 700; color: #183238; }
.civix-cat-desc { font-size: 10px; color: #61777B; }

.civix-complaint-item {
  display: flex;
  align-items: center;
  padding: 14px;
  border: 1px solid #DCE7E8;
  border-radius: 10px;
  margin-bottom: 12px;
  gap: 14px;
}
.civix-complaint-thumb {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.thumb-water { background: #E0F2FE; color: #0284C7; }
.thumb-elec { background: #FEF3C7; color: #D97706; }
.thumb-roads { background: #F3F4F6; color: #374151; }
.thumb-drain { background: #EDE9FE; color: #7C3AED; }
.civix-complaint-info { flex-grow: 1; }
.civix-comp-id { font-size: 11px; font-weight: 700; color: #087F8C; }
.civix-comp-title { font-size: 14px; font-weight: 600; color: #183238; }
.civix-comp-loc { font-size: 11px; color: #61777B; }
.civix-status-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 12px;
}
.status-progress { background: #FEF3C7; color: #B45309; }
.status-resolved { background: #E1F5EA; color: #18794E; }
.status-awaiting { background: #FEE2E2; color: #DC2626; }
.civix-complaint-arrow { font-size: 22px; color: #A0B2B5; text-decoration: none; }

.civix-alert-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #F0F4F4;
}
.civix-alert-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}
.alert-red { background: #FEE2E2; color: #DC2626; }
.alert-yellow { background: #FEF3C7; color: #D97706; }
.alert-purple { background: #EDE9FE; color: #7C3AED; }
.alert-blue { background: #E0F2FE; color: #0284C7; }
.civix-alert-title { font-size: 13px; font-weight: 600; color: #183238; }
.civix-alert-dist { font-size: 11px; color: #61777B; }

.civix-assistant-card { border-top: 4px solid #087F8C; }
.civix-assistant-head {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  margin-bottom: 14px;
}
.civix-assistant-bot-icon {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: #087F8C;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}
.civix-chat-bubble {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 10px;
  padding: 12px 14px;
  font-size: 13px;
  line-height: 1.5;
  margin-bottom: 14px;
}
.civix-chat-prompts { display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px; }
.civix-prompt-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 600;
  color: #183238;
  text-decoration: none;
  transition: all 0.15s;
}
.civix-prompt-pill:hover { border-color: #087F8C; background: #E1F5EA; color: #087F8C; text-decoration: none; }
.civix-chat-input-bar { display: flex; gap: 6px; }
.civix-chat-input {
  flex-grow: 1;
  border: 1px solid #DCE7E8;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 12px;
  outline: none;
}
.civix-chat-send-btn {
  background: #087F8C;
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  padding: 0 12px;
  cursor: pointer;
}
"""

    client_script = """
function($scope) {
  var c = this;
  c.categories = [
    { name: 'Water Supply', css: 'cat-water', icon: 'glyphicon-tint', sub: 'Leakage, pressure' },
    { name: 'Electricity', css: 'cat-elec', icon: 'glyphicon-flash', sub: 'Streetlights, power' },
    { name: 'Roads', css: 'cat-roads', icon: 'glyphicon-road', sub: 'Potholes, surface' },
    { name: 'Drainage', css: 'cat-drain', icon: 'glyphicon-filter', sub: 'Blockage, overflow' },
    { name: 'Waterlogging', css: 'cat-flood', icon: 'glyphicon-tint', sub: 'Monsoon flooding' }
  ];
  c.alerts = [
    { title: 'Road maintenance work in T. Nagar', dist: '500 m', time: 'Today', css: 'alert-red', icon: 'glyphicon-exclamation-sign' },
    { title: 'Scheduled power maintenance - Anna Nagar', dist: '1.2 km', time: 'Tomorrow', css: 'alert-yellow', icon: 'glyphicon-flash' },
    { title: 'Possible waterlogging in Velachery', dist: '2.3 km', time: 'Today', css: 'alert-purple', icon: 'glyphicon-tint' },
    { title: 'Low water pressure reported', dist: '3.1 km', time: 'Today', css: 'alert-blue', icon: 'glyphicon-info-sign' }
  ];
}
"""

    server_script = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  data.citizenName = data.isLoggedIn ? (gs.getUser().getFirstName() || gs.getUserDisplayName()) : 'Priya Sharma';

  data.counts = { total: 0, resolved: 0, in_progress: 0, awaiting: 0 };
  data.recentCases = [];

  var userId = gs.getUserID();
  var gr = new GlideRecord('incident');
  if (data.isLoggedIn) {
    gr.addQuery('caller_id', userId);
  }
  gr.orderByDesc('sys_created_on');
  gr.setLimit(5);
  gr.query();

  while (gr.next()) {
    data.counts.total++;
    var st = gr.getValue('state');
    var stLabel = gr.getDisplayValue('state');
    var stClass = 'awaiting';
    if (st == '2') {
      data.counts.in_progress++;
      stClass = 'progress';
    } else if (st == '6' || st == '7') {
      data.counts.resolved++;
      stClass = 'resolved';
    } else {
      data.counts.awaiting++;
    }

    var cat = gr.getDisplayValue('category') || 'Water';
    var icon = 'glyphicon-tint';
    var catClass = 'water';
    if (cat.toLowerCase().indexOf('elec') >= 0) { icon = 'glyphicon-flash'; catClass = 'elec'; }
    else if (cat.toLowerCase().indexOf('road') >= 0) { icon = 'glyphicon-road'; catClass = 'roads'; }
    else if (cat.toLowerCase().indexOf('drain') >= 0) { icon = 'glyphicon-filter'; catClass = 'drain'; }

    data.recentCases.push({
      sys_id: gr.getUniqueValue(),
      number: gr.getValue('number'),
      short_description: gr.getValue('short_description'),
      location: 'Ward 12, Chennai',
      date: gr.getValue('sys_created_on').split(' ')[0],
      status: stLabel,
      statusClass: stClass,
      icon: icon,
      categoryClass: catClass
    });
  }

  // If no records in incident yet for demo citizen, provide baseline demo counts
  if (data.counts.total === 0) {
    data.counts = { total: 12, resolved: 8, in_progress: 3, awaiting: 1 };
    data.recentCases = [
      { sys_id: 'demo1', number: 'CIVIX-2026-00123', short_description: 'Water leakage on 3rd Main Road', location: 'Adyar, Chennai', date: 'Today', status: 'In Progress', statusClass: 'progress', icon: 'glyphicon-tint', categoryClass: 'water' },
      { sys_id: 'demo2', number: 'CIVIX-2026-00118', short_description: 'Street light not working near Anna Nagar Park', location: 'Anna Nagar, Chennai', date: 'Yesterday', status: 'Resolved', statusClass: 'resolved', icon: 'glyphicon-flash', categoryClass: 'elec' },
      { sys_id: 'demo3', number: 'CIVIX-2026-00110', short_description: 'Pothole near 100 Feet Road', location: 'T. Nagar, Chennai', date: '08 Oct 2026', status: 'Resolved', statusClass: 'resolved', icon: 'glyphicon-road', categoryClass: 'roads' },
      { sys_id: 'demo4', number: 'CIVIX-2026-00102', short_description: 'Drainage overflow in residential area', location: 'Velachery, Chennai', date: '05 Oct 2026', status: 'Awaiting Action', statusClass: 'awaiting', icon: 'glyphicon-filter', categoryClass: 'drain' }
    ];
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Customer Dashboard",
        "id": "civix_dashboard_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_dashboard_widget", widget_data, "Dashboard Widget")
    page_id = create_page_structure("civix_dashboard", "Customer Dashboard", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 8: MY CASES WIDGET
# ==============================================================================
def create_my_cases_widget():
    print("\\n>>> Building Screen 8: My Cases Foundation Widget")
    template = """
<div class="civix-page civix-container civix-cases-page">
  <div class="civix-section-bar">
    <div>
      <h2 class="civix-section-title">My Reported Cases</h2>
      <p class="civix-section-subtitle">Track status and review municipal responses for your submitted civic issues.</p>
    </div>
    <a href="?id=civix_report_issue" class="civix-btn civix-btn-primary">
      <span class="glyphicon glyphicon-plus"></span> Report New Issue
    </a>
  </div>

  <div class="civix-cases-filter-bar">
    <div class="row">
      <div class="col-md-6 form-group">
        <input type="text" class="form-control" ng-model="c.searchQuery" placeholder="Search by case number or keyword..." />
      </div>
      <div class="col-md-3 form-group">
        <select class="form-control" ng-model="c.statusFilter">
          <option value="">All Statuses</option>
          <option value="In Progress">In Progress</option>
          <option value="Resolved">Resolved</option>
          <option value="Awaiting Action">Awaiting Action</option>
        </select>
      </div>
      <div class="col-md-3 form-group">
        <select class="form-control" ng-model="c.catFilter">
          <option value="">All Categories</option>
          <option value="Water">Water Supply</option>
          <option value="Electricity">Electricity</option>
          <option value="Roads">Roads</option>
          <option value="Drainage">Drainage</option>
        </select>
      </div>
    </div>
  </div>

  <div class="civix-cases-table-wrap">
    <table class="table civix-table">
      <thead>
        <tr>
          <th>Case Number</th>
          <th>Category</th>
          <th>Subject / Description</th>
          <th>Location</th>
          <th>Date Logged</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr ng-repeat="item in c.data.cases | filter:c.searchQuery | filter:{status: c.statusFilter, category: c.catFilter}">
          <td><strong>{{item.number}}</strong></td>
          <td><span class="label label-default">{{item.category}}</span></td>
          <td>{{item.short_description}}</td>
          <td>{{item.location}}</td>
          <td>{{item.date}}</td>
          <td><span class="civix-status-badge" ng-class="'status-' + item.statusClass">{{item.status}}</span></td>
          <td><a href="?id=civix_track_case&sys_id={{item.sys_id}}" class="btn btn-xs btn-info">Track Case &rarr;</a></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""

    css = """
.civix-cases-page { padding: 40px 20px 80px; }
.civix-cases-filter-bar {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 16px 16px 0;
  margin-bottom: 24px;
}
.civix-cases-table-wrap {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  overflow: hidden;
}
.civix-table th { background: #F7FAFA; color: #183238; border-bottom: 2px solid #DCE7E8; }
.civix-table td { vertical-align: middle !important; }
"""

    client_script = """
function($scope) {
  var c = this;
  c.searchQuery = '';
  c.statusFilter = '';
  c.catFilter = '';
}
"""

    server_script = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  data.cases = [];
  var userId = gs.getUserID();
  var gr = new GlideRecord('incident');
  if (data.isLoggedIn) {
    gr.addQuery('caller_id', userId);
  }
  gr.orderByDesc('sys_created_on');
  gr.setLimit(20);
  gr.query();

  while (gr.next()) {
    var st = gr.getValue('state');
    var stLabel = gr.getDisplayValue('state');
    var stClass = 'awaiting';
    if (st == '2') stClass = 'progress';
    else if (st == '6' || st == '7') stClass = 'resolved';

    data.cases.push({
      sys_id: gr.getUniqueValue(),
      number: gr.getValue('number'),
      short_description: gr.getValue('short_description'),
      category: gr.getDisplayValue('category') || 'Water',
      location: 'Ward 12, Chennai',
      date: gr.getValue('sys_created_on').split(' ')[0],
      status: stLabel,
      statusClass: stClass
    });
  }

  if (data.cases.length === 0) {
    data.cases = [
      { sys_id: 'c1', number: 'CIVIX-2026-00123', category: 'Water', short_description: 'Water leakage on 3rd Main Road', location: 'Adyar, Chennai', date: '10 Oct 2026', status: 'In Progress', statusClass: 'progress' },
      { sys_id: 'c2', number: 'CIVIX-2026-00118', category: 'Electricity', short_description: 'Street light not working near Anna Nagar Park', location: 'Anna Nagar, Chennai', date: '09 Oct 2026', status: 'Resolved', statusClass: 'resolved' },
      { sys_id: 'c3', number: 'CIVIX-2026-00110', category: 'Roads', short_description: 'Pothole near 100 Feet Road', location: 'T. Nagar, Chennai', date: '08 Oct 2026', status: 'Resolved', statusClass: 'resolved' },
      { sys_id: 'c4', number: 'CIVIX-2026-00102', category: 'Drainage', short_description: 'Drainage overflow in residential area', location: 'Velachery, Chennai', date: '05 Oct 2026', status: 'Awaiting Action', statusClass: 'awaiting' }
    ];
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - My Cases",
        "id": "civix_my_cases_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_my_cases_widget", widget_data, "My Cases Widget")
    page_id = create_page_structure("civix_my_cases", "My Cases", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 9: REPORT AN ISSUE WIDGET
# ==============================================================================
def create_report_issue_widget():
    print("\\n>>> Building Screen 9: Report an Issue Foundation Widget")
    template = """
<div class="civix-page civix-container civix-report-page">
  <div class="civix-report-card">
    <div class="civix-report-header text-center">
      <h2 class="civix-auth-title">Report a Civic Issue</h2>
      <p class="civix-auth-subtitle">Submit details directly to your municipal ward operations department.</p>
    </div>

    <!-- Stepper indicator -->
    <div class="civix-report-stepper">
      <div class="civix-step-pill" ng-class="{'active': c.step >= 1}">1. Service & Category</div>
      <div class="civix-step-pill" ng-class="{'active': c.step >= 2}">2. Location & Ward</div>
      <div class="civix-step-pill" ng-class="{'active': c.step >= 3}">3. Review & Submit</div>
    </div>

    <!-- Success Message -->
    <div ng-if="c.successData" class="alert alert-success civix-alert text-center">
      <div style="font-size: 36px; margin-bottom: 10px;"><span class="glyphicon glyphicon-ok-circle"></span></div>
      <h3>Issue Successfully Logged!</h3>
      <p>Your case tracking number is:</p>
      <div class="civix-ticket-badge">{{c.successData.number}}</div>
      <p style="margin-top: 15px;">A ward engineer has been alerted to review and schedule field inspection.</p>
      <div style="margin-top: 20px;">
        <a href="?id=civix_track_case&sys_id={{c.successData.sys_id}}" class="btn btn-primary">Track This Case Now &rarr;</a>
        <a href="?id=civix_dashboard" class="btn btn-default">Return to Dashboard</a>
      </div>
    </div>

    <form ng-if="!c.successData" ng-submit="c.nextStep()">
      <!-- Step 1: Category & Description -->
      <div ng-if="c.step === 1" class="civix-step-box">
        <div class="form-group">
          <label>Service Category <span class="text-danger">*</span></label>
          <select class="form-control" ng-model="c.form.category" required>
            <option value="Water">Water Supply (Leakage, Interruption)</option>
            <option value="Electricity">Electricity (Streetlights, Hazards)</option>
            <option value="Roads">Roads (Potholes, Damage)</option>
            <option value="Drainage">Drainage & Waterlogging (Blockage, Overflow)</option>
          </select>
        </div>

        <div class="form-group">
          <label>Issue Title <span class="text-danger">*</span></label>
          <input type="text" class="form-control" ng-model="c.form.title" placeholder="e.g. Broken water pipe leaking near intersection" required />
        </div>

        <div class="form-group">
          <label>Detailed Description <span class="text-danger">*</span></label>
          <textarea class="form-control" rows="4" ng-model="c.form.description" placeholder="Describe the severity, duration, and any immediate hazard..." required></textarea>
        </div>

        <div class="civix-step-actions">
          <button type="button" class="btn btn-primary" ng-click="c.step = 2">Next: Location Details &rarr;</button>
        </div>
      </div>

      <!-- Step 2: Location -->
      <div ng-if="c.step === 2" class="civix-step-box">
        <div class="form-group">
          <label>Municipal Ward <span class="text-danger">*</span></label>
          <select class="form-control" ng-model="c.form.ward" required>
            <option value="Ward 12 - T. Nagar">Ward 12 - T. Nagar</option>
            <option value="Ward 8 - Anna Nagar">Ward 8 - Anna Nagar</option>
            <option value="Ward 15 - Velachery">Ward 15 - Velachery</option>
            <option value="Ward 18 - Adyar">Ward 18 - Adyar</option>
            <option value="Ward 4 - Mylapore">Ward 4 - Mylapore</option>
          </select>
        </div>

        <div class="form-group">
          <label>Street Address / Landmark <span class="text-danger">*</span></label>
          <input type="text" class="form-control" ng-model="c.form.address" placeholder="e.g. Opposite Post Office, 3rd Cross Street" required />
        </div>

        <div class="form-group">
          <label>Use Geolocation</label><br/>
          <button type="button" class="btn btn-default btn-sm" ng-click="c.getGeo()">
            <span class="glyphicon glyphicon-map-marker"></span> Detect My Current Coordinates
          </button>
          <span ng-if="c.geoCoords" class="text-success" style="margin-left: 10px;">{{c.geoCoords}}</span>
        </div>

        <div class="civix-step-actions">
          <button type="button" class="btn btn-default" ng-click="c.step = 1">&larr; Back</button>
          <button type="button" class="btn btn-primary" ng-click="c.step = 3">Next: Review & Submit &rarr;</button>
        </div>
      </div>

      <!-- Step 3: Review & Submit -->
      <div ng-if="c.step === 3" class="civix-step-box">
        <div class="civix-review-panel">
          <h4>Review Civic Issue Details</h4>
          <p><strong>Category:</strong> {{c.form.category}}</p>
          <p><strong>Issue:</strong> {{c.form.title}}</p>
          <p><strong>Description:</strong> {{c.form.description}}</p>
          <p><strong>Ward & Locality:</strong> {{c.form.ward}}, {{c.form.address}}</p>
        </div>

        <div class="civix-step-actions">
          <button type="button" class="btn btn-default" ng-click="c.step = 2">&larr; Back</button>
          <button type="button" class="btn btn-success btn-lg" ng-click="c.submitIssue()" ng-disabled="c.loading">
            <span ng-if="c.loading"><span class="glyphicon glyphicon-refresh glyphicon-spin"></span> Submitting to ServiceNow...</span>
            <span ng-if="!c.loading"><span class="glyphicon glyphicon-send"></span> Confirm & Submit Issue</span>
          </button>
        </div>
      </div>
    </form>
  </div>
</div>
"""

    css = """
.civix-report-page { padding: 40px 20px 80px; }
.civix-report-card {
  max-width: 720px;
  margin: 0 auto;
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 36px 32px;
}
.civix-report-stepper {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}
.civix-step-pill {
  flex: 1;
  text-align: center;
  padding: 8px;
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #61777B;
}
.civix-step-pill.active {
  background: #E1F5EA;
  color: #087F8C;
  border-color: #087F8C;
}
.civix-ticket-badge {
  display: inline-block;
  background: #123E46;
  color: #FFFFFF;
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 1px;
}
.civix-review-panel {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 20px;
}
.civix-step-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 24px;
}
"""

    client_script = """
function($scope, $location) {
  var c = this;
  c.step = 1;
  var paramCat = $location.search().cat || 'Water';
  c.form = {
    category: paramCat,
    ward: 'Ward 12 - T. Nagar'
  };

  c.getGeo = function() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(pos) {
        $scope.$apply(function() {
          c.geoCoords = 'Lat: ' + pos.coords.latitude.toFixed(4) + ', Long: ' + pos.coords.longitude.toFixed(4);
          c.form.geo = c.geoCoords;
        });
      });
    } else {
      c.geoCoords = 'Geolocation not supported by browser.';
    }
  };

  c.submitIssue = function() {
    c.loading = true;
    c.server.get({ action: 'submit_issue', form: c.form }).then(function(r) {
      c.loading = false;
      if (r.data.status === 'success') {
        c.successData = r.data.ticket;
      }
    });
  };
}
"""

    server_script = """
(function() {
  if (input && input.action === 'submit_issue') {
    var f = input.form;
    var gr = new GlideRecord('incident');
    gr.initialize();
    gr.setValue('short_description', f.title);
    gr.setValue('description', f.description + '\\n\\nWard: ' + f.ward + '\\nAddress: ' + f.address + (f.geo ? ('\\nGeo: ' + f.geo) : ''));
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
        sys_id: sysId,
        number: grRead.getValue('number')
      };
    } else {
      data.status = 'error';
    }
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Report an Issue",
        "id": "civix_report_issue_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_report_issue_widget", widget_data, "Report Issue Widget")
    page_id = create_page_structure("civix_report_issue", "Report an Issue", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 10: CASE TRACKING WIDGET
# ==============================================================================
def create_track_case_widget():
    print("\\n>>> Building Screen 10: Case Tracking Foundation Widget")
    template = """
<div class="civix-page civix-container civix-track-page">
  <div class="civix-track-card">
    <div class="civix-section-bar">
      <div>
        <h2 class="civix-section-title">Case Status & Timeline</h2>
        <p class="civix-section-subtitle">Real-time municipal resolution progress for this reported civic complaint.</p>
      </div>
      <a href="?id=civix_my_cases" class="btn btn-default">&larr; Back to My Cases</a>
    </div>

    <!-- Case Lookup Header -->
    <div class="civix-case-detail-header">
      <div class="civix-case-main-info">
        <span class="civix-badge-pill"><span class="glyphicon glyphicon-tag"></span> {{c.data.case.category}}</span>
        <h3>{{c.data.case.number}} &bull; {{c.data.case.short_description}}</h3>
        <p class="text-muted"><span class="glyphicon glyphicon-map-marker"></span> {{c.data.case.location}} &bull; Logged on: {{c.data.case.opened_at}}</p>
      </div>
      <div class="civix-case-curr-status">
        <span class="civix-status-badge status-progress" style="font-size: 14px; padding: 6px 14px;">{{c.data.case.state}}</span>
      </div>
    </div>

    <!-- Approved Lifecycle Timeline -->
    <div class="civix-timeline-card">
      <h4 class="civix-form-section-title">Approved Resolution Lifecycle</h4>
      <div class="civix-lifecycle-bar">
        <div class="civix-lifecycle-step" ng-repeat="st in c.steps" ng-class="{'completed': st.num <= c.data.case.stepNum, 'active': st.num === c.data.case.stepNum}">
          <div class="civix-step-circle">{{st.num}}</div>
          <div class="civix-step-label">{{st.label}}</div>
        </div>
      </div>
    </div>

    <!-- Case Details Details -->
    <div class="civix-case-meta-box">
      <h4>Description Logged</h4>
      <p>{{c.data.case.description}}</p>
      <hr/>
      <h4>Public Resolution Information</h4>
      <p class="text-info">{{c.data.case.resolution_notes}}</p>
    </div>
  </div>
</div>
"""

    css = """
.civix-track-page { padding: 40px 20px 80px; }
.civix-track-card {
  max-width: 900px;
  margin: 0 auto;
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 32px;
}
.civix-case-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 20px;
  border-bottom: 1px solid #DCE7E8;
  margin-bottom: 24px;
}
.civix-case-main-info h3 { margin: 8px 0; font-size: 20px; font-weight: 700; color: #183238; }
.civix-timeline-card {
  background: #F7FAFA;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}
.civix-lifecycle-bar {
  display: flex;
  justify-content: space-between;
  position: relative;
  margin-top: 20px;
}
.civix-lifecycle-step {
  text-align: center;
  position: relative;
  flex: 1;
}
.civix-step-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #DCE7E8;
  color: #61777B;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  margin: 0 auto 8px;
}
.civix-lifecycle-step.completed .civix-step-circle {
  background: #087F8C;
  color: #FFFFFF;
}
.civix-lifecycle-step.active .civix-step-circle {
  background: #18794E;
  color: #FFFFFF;
  box-shadow: 0 0 0 4px #E1F5EA;
}
.civix-step-label { font-size: 11px; font-weight: 600; color: #183238; }
.civix-case-meta-box {
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 12px;
  padding: 20px;
}
"""

    client_script = """
function($scope) {
  var c = this;
  c.steps = [
    { num: 1, label: 'Submitted' },
    { num: 2, label: 'Under Review' },
    { num: 3, label: 'Assigned' },
    { num: 4, label: 'In Progress' },
    { num: 5, label: 'Resolved' },
    { num: 6, label: 'Closed' }
  ];
}
"""

    server_script = """
(function() {
  var sysId = $sp.getParameter('sys_id');
  data.case = {
    number: 'CIVIX-2026-00123',
    short_description: 'Water leakage on 3rd Main Road',
    category: 'Water Supply',
    location: 'Adyar, Ward 18, Chennai',
    opened_at: '10 Oct 2026 10:24 AM',
    state: 'In Progress',
    stepNum: 4,
    description: 'Severe potable pipeline leak causing water accumulation near pedestrian crossway.',
    resolution_notes: 'Ward engineer and pipeline repair crew dispatched. Repair parts staged on site.'
  };

  if (sysId) {
    var gr = new GlideRecord('incident');
    if (gr.get(sysId)) {
      var st = gr.getValue('state');
      var step = 2;
      if (st == '2') step = 4;
      else if (st == '6') step = 5;
      else if (st == '7') step = 6;
      data.case = {
        sys_id: gr.getUniqueValue(),
        number: gr.getValue('number'),
        short_description: gr.getValue('short_description'),
        category: gr.getDisplayValue('category') || 'Civic Issue',
        location: 'Ward 12, Chennai',
        opened_at: gr.getValue('sys_created_on'),
        state: gr.getDisplayValue('state'),
        stepNum: step,
        description: gr.getValue('description') || gr.getValue('short_description'),
        resolution_notes: gr.getValue('close_notes') || 'Assigned to field technician for resolution.'
      };
    }
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Case Tracking",
        "id": "civix_track_case_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_track_case_widget", widget_data, "Case Tracking Widget")
    page_id = create_page_structure("civix_track_case", "Case Tracking", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# SCREEN 11: CITIZEN PROFILE & SETTINGS WIDGET
# ==============================================================================
def create_profile_widget():
    print("\\n>>> Building Screen 11: Citizen Profile and Settings Foundation Widget")
    template = """
<div class="civix-page civix-container civix-profile-page">
  <div class="civix-profile-card">
    <div class="civix-section-bar">
      <div>
        <h2 class="civix-section-title">Citizen Profile & Settings</h2>
        <p class="civix-section-subtitle">Manage your contact details, locality, and preferred interface language.</p>
      </div>
      <a href="/logout.do" class="btn btn-danger btn-sm"><span class="glyphicon glyphicon-log-out"></span> Sign Out</a>
    </div>

    <div class="row">
      <div class="col-md-4 text-center">
        <div class="civix-avatar-large">{{c.data.userInitials}}</div>
        <h3>{{c.data.userName}}</h3>
        <span class="label label-success">Verified Citizen</span>
      </div>
      <div class="col-md-8">
        <div class="civix-profile-details">
          <div class="form-group">
            <label>Registered Email</label>
            <input type="text" class="form-control" value="{{c.data.userEmail}}" readonly />
          </div>
          <div class="form-group">
            <label>Registered Mobile</label>
            <input type="text" class="form-control" value="{{c.data.mobile}}" readonly />
          </div>
          <div class="form-group">
            <label>City & Locality</label>
            <input type="text" class="form-control" value="{{c.data.city}}" readonly />
          </div>
          <div class="form-group">
            <label>Assigned Role</label>
            <input type="text" class="form-control" value="x_civic_ai_citizen (CIVIX AI Citizen Access)" readonly />
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

    css = """
.civix-profile-page { padding: 40px 20px 80px; }
.civix-profile-card {
  max-width: 800px;
  margin: 0 auto;
  background: #FFFFFF;
  border: 1px solid #DCE7E8;
  border-radius: 16px;
  padding: 32px;
}
.civix-avatar-large {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: #087F8C;
  color: #FFFFFF;
  font-size: 32px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px auto 14px;
}
"""

    client_script = "function() {}"

    server_script = """
(function() {
  data.isLoggedIn = gs.isLoggedIn() && gs.getUserName() !== 'guest';
  if (data.isLoggedIn) {
    var u = gs.getUser();
    data.userName = u.getDisplayName();
    data.userEmail = u.getEmail();
    data.mobile = u.getRecord().getValue('mobile_phone') || '+91 9876543210';
    data.city = u.getRecord().getValue('city') || 'Chennai, Tamil Nadu';
    var names = data.userName.split(' ');
    data.userInitials = names.length > 1 ? (names[0][0] + names[names.length-1][0]).toUpperCase() : data.userName.substring(0, 2).toUpperCase();
  } else {
    data.userName = 'Priya Sharma';
    data.userEmail = 'priya.sharma@example.com';
    data.mobile = '+91 9876543210';
    data.city = 'Chennai, Tamil Nadu';
    data.userInitials = 'PS';
  }
})();
"""

    widget_data = {
        "name": "CIVIX AI - Profile and Settings",
        "id": "civix_profile_widget",
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "public": "true"
    }
    widget_id = upsert("sp_widget", "id=civix_profile_widget", widget_data, "Profile Widget")
    page_id = create_page_structure("civix_profile", "Profile and Settings", True, widget_id)
    return page_id, widget_id


# ==============================================================================
# CONFIGURE MAIN PORTAL (sp_portal)
# ==============================================================================
def configure_portal(landing_page_sys_id: str):
    print("\\n>>> Configuring Main Service Portal Record (/civix)")
    portal_data = {
        "title": "CIVIX AI - Citizen Portal",
        "url_suffix": "civix",
        "homepage": landing_page_sys_id,
        "theme": THEME_SYS_ID,
        "header": HEADER_WIDGET_SYS_ID,
        "footer": FOOTER_WIDGET_SYS_ID,
        "default": "false",
        "css_variables": "$navbar-height: 0px !important;\\n$grid-gutter-width: 0px !default;"
    }
    portal_id = upsert("sp_portal", "url_suffix=civix", portal_data, "CIVIX AI Portal")
    return portal_id


if __name__ == "__main__":
    print("=== DEPLOYING ALL CIVIX AI PHASE 1 SCREENS & WIDGETS ===")
    p1, w1 = create_landing_widget()
    p2, w2 = create_portal_select_widget()
    p3, w3 = create_home_widget()
    p4, w4 = create_register_widget()
    p5, w5 = create_login_widget()
    p6, w6 = create_recovery_widget()
    p7, w7 = create_dashboard_widget()
    p8, w8 = create_my_cases_widget()
    p9, w9 = create_report_issue_widget()
    p10, w10 = create_track_case_widget()
    p11, w11 = create_profile_widget()

    portal_sys_id = configure_portal(p1)
    print(f"\\n=======================================================")
    print(f"CIVIX AI Portal successfully deployed with url_suffix: civix")
    print(f"Landing page ID: {p1}")
    print(f"Portal Sys ID: {portal_sys_id}")
    print(f"URL: {INSTANCE_URL}/civix")
    print(f"=======================================================")
'''

with open("d:\\tcs\\build_all_screens.py", "a", encoding="utf-8") as f:
    f.write(code_screens_4_to_11)

print("Appended Screens 4 to 11 to build_all_screens.py")
