import os
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

def update_widget(widget_id: str, client_script: str = None, template: str = None, server_script: str = None):
    res = api_get("sp_widget", query=f"id={widget_id}", limit=1)
    if not res:
        print(f"Widget {widget_id} not found!")
        return None
    sys_id = res[0]["sys_id"]
    payload = {}
    if client_script:
        payload["client_script"] = client_script.strip()
    if template:
        payload["template"] = template.strip()
    if server_script:
        payload["script"] = server_script.strip()
    api_put("sp_widget", sys_id, payload)
    print(f"  [FIXED] {widget_id} ({sys_id})")
    return sys_id

# ------------------------------------------------------------------------------
# 1. FIXED HOME CLIENT SCRIPT
# ------------------------------------------------------------------------------
HOME_CLIENT_SCRIPT = """
function($scope, $timeout) {
  var c = this;

  c.langOpen = false;
  c.selectedLang = 'en';
  c.currentLangDisplay = 'भारतीय भाषाएं / Language';

  c.languages = [
    { code: 'en', name: 'English', native: 'English', prefix: 'En', bg: '#0066FF' },
    { code: 'hi', name: 'Hindi', native: 'हिन्दी', prefix: 'हि', bg: '#EA580C' },
    { code: 'ta', name: 'Tamil', native: 'தமிழ்', prefix: 'த', bg: '#0284C7' },
    { code: 'te', name: 'Telugu', native: 'తెలుగు', prefix: 'తె', bg: '#16A34A' }
  ];

  c.toggleLang = function() {
    c.langOpen = !c.langOpen;
  };

  c.chooseLang = function(l) {
    c.selectedLang = l.code;
    c.currentLangDisplay = l.native + ' / ' + l.name;
    c.langOpen = false;
  };

  c.quickPrompt = function(msg) {
    c.userMsgInput = msg;
    c.submitChatMessage();
  };

  c.onChatEnter = function($event) {
    if ($event.keyCode === 13) {
      c.submitChatMessage();
    }
  };

  c.submitChatMessage = function() {
    if (!c.userMsgInput) return;
    var userText = c.userMsgInput;
    c.userMsgInput = '';
    alert('Civic AI Assistant responded to: ' + userText);
  };
}
"""

HOME_SERVER_SCRIPT = """
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
      statusClass: 'in-progress'
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

# ------------------------------------------------------------------------------
# 2. FIXED REPORT ISSUE CLIENT SCRIPT
# ------------------------------------------------------------------------------
REPORT_CLIENT_SCRIPT = """
function($scope, $timeout) {
  var c = this;

  c.langOpen = false;
  c.selectedLang = 'en';
  c.currentLangDisplay = 'भारतीय भाषाएं / Language';

  c.languages = [
    { code: 'en', name: 'English', native: 'English', prefix: 'En', bg: '#0066FF' }
  ];

  c.toggleLang = function() {
    c.langOpen = !c.langOpen;
  };

  c.chooseLang = function(l) {
    c.selectedLang = l.code;
    c.currentLangDisplay = l.native + ' / ' + l.name;
    c.langOpen = false;
  };

  c.step = 1;
  c.form = {
    category: 'Water',
    title: '',
    description: '',
    ward: 'Ward 12 - T. Nagar',
    address: '',
    geo: ''
  };
  c.submitting = false;
  c.successData = null;

  c.detectGeo = function() {
    c.form.geo = '13.0418° N, 80.2341° E (Ward 12 GPS Lock)';
  };

  c.submitIssue = function() {
    c.submitting = true;
    c.server.get({ action: 'submit_issue', form: c.form }).then(function(r) {
      c.submitting = false;
      if (r.data && r.data.status === 'success') {
        c.successData = r.data.ticket;
      }
    });
  };
}
"""

# ------------------------------------------------------------------------------
# 3. FIXED MY CASES CLIENT SCRIPT & TEMPLATE
# ------------------------------------------------------------------------------
CASES_CLIENT_SCRIPT = """
function($scope, $timeout) {
  var c = this;

  c.langOpen = false;
  c.selectedLang = 'en';
  c.currentLangDisplay = 'भारतीय भाषाएं / Language';

  c.languages = [
    { code: 'en', name: 'English', native: 'English', prefix: 'En', bg: '#0066FF' }
  ];

  c.toggleLang = function() {
    c.langOpen = !c.langOpen;
  };

  c.chooseLang = function(l) {
    c.selectedLang = l.code;
    c.currentLangDisplay = l.native + ' / ' + l.name;
    c.langOpen = false;
  };

  c.filterStatus = '';
  c.catFilter = '';
  c.searchFilter = '';

  c.filterCase = function(item) {
    if (!item) return false;
    if (c.filterStatus && item.status !== c.filterStatus) return false;
    if (c.catFilter && item.category !== c.catFilter) return false;
    if (c.searchFilter) {
      var q = c.searchFilter.toLowerCase();
      var mNum = (item.number || '').toLowerCase().indexOf(q) !== -1;
      var mDesc = (item.short_description || '').toLowerCase().indexOf(q) !== -1;
      var mLoc = (item.location || '').toLowerCase().indexOf(q) !== -1;
      if (!mNum && !mDesc && !mLoc) return false;
    }
    return true;
  };

  c.countStatus = function(st) {
    if (!c.data || !c.data.cases) return 0;
    if (!st) return c.data.cases.length;
    return c.data.cases.filter(function(x) { return x.status === st; }).length;
  };
}
"""

CASES_SERVER_SCRIPT = """
(function() {
  data.cases = [
    {
      sys_id: 'c1',
      number: 'CIVIX-2024-00123',
      short_description: 'Water leakage on 3rd Main Road',
      location: 'Adyar, Chennai',
      date: '15 Nov 2024, 10:24 AM',
      category: 'Water',
      status: 'In Progress',
      statusClass: 'in-progress'
    },
    {
      sys_id: 'c2',
      number: 'CIVIX-2024-00118',
      short_description: 'Street light not working near Anna Nagar Park',
      location: 'Anna Nagar, Chennai',
      date: '10 Nov 2024, 06:12 PM',
      category: 'Electricity',
      status: 'Resolved',
      statusClass: 'resolved'
    },
    {
      sys_id: 'c3',
      number: 'CIVIX-2024-00110',
      short_description: 'Pothole near 100 Feet Road',
      location: 'T. Nagar, Chennai',
      date: '05 Nov 2024, 02:30 PM',
      category: 'Roads',
      status: 'Resolved',
      statusClass: 'resolved'
    },
    {
      sys_id: 'c4',
      number: 'CIVIX-2024-00102',
      short_description: 'Drainage overflow in residential area',
      location: 'Velachery, Chennai',
      date: '28 Oct 2024, 09:15 AM',
      category: 'Drainage',
      status: 'Awaiting Action',
      statusClass: 'awaiting'
    }
  ];

  var gr = new GlideRecord('incident');
  gr.orderByDesc('sys_created_on');
  gr.setLimit(5);
  gr.query();
  while (gr.next()) {
    var st = gr.getValue('state');
    var stLabel = gr.getDisplayValue('state');
    var stClass = 'awaiting';
    if (st == '2') stClass = 'in-progress';
    else if (st == '6' || st == '7') stClass = 'resolved';
    data.cases.push({
      sys_id: gr.getUniqueValue(),
      number: gr.getValue('number'),
      short_description: gr.getValue('short_description'),
      location: 'Ward 12, Chennai',
      date: gr.getValue('sys_created_on'),
      category: gr.getDisplayValue('category') || 'Water',
      status: stLabel,
      statusClass: stClass
    });
  }
})();
"""

# Let's read the current templates from deploy_master_redesign.py
with open("d:/tcs/deploy_master_redesign.py", "r", encoding="utf-8") as f:
    text = f.read()

# In CASES_TEMPLATE, update the filter expression to c.filterCase
old_cases_filter = "ng-repeat=\"item in c.data.cases | filter:c.searchFilter | filter:{category: c.catFilter, status: c.filterStatus}\""
new_cases_filter = "ng-repeat=\"item in c.data.cases | filter:c.filterCase\""

# Get CASES_TEMPLATE from deploy_master_redesign.py
start_c = text.find('CASES_TEMPLATE =')
end_c = text.find('CASES_CSS =')
# Extract between start and end
cases_code = text[start_c:end_c]
# Get the evaluated CASES_TEMPLATE by running the script's definitions
from deploy_master_redesign import CASES_TEMPLATE, REPORT_TEMPLATE, HOME_TEMPLATE

CASES_TEMPLATE_FIXED = CASES_TEMPLATE.replace(old_cases_filter, new_cases_filter)

if __name__ == "__main__":
    print("=== DEPLOYING CONTROLLER SCOPE & SYNTAX FIXES ===")
    
    print("\n--- 1. Fixing civix_home_widget & civix_dashboard_widget ---")
    update_widget("civix_home_widget", client_script=HOME_CLIENT_SCRIPT, server_script=HOME_SERVER_SCRIPT)
    update_widget("civix_dashboard_widget", client_script=HOME_CLIENT_SCRIPT, server_script=HOME_SERVER_SCRIPT)

    print("\n--- 2. Fixing civix_report_issue_widget ---")
    update_widget("civix_report_issue_widget", client_script=REPORT_CLIENT_SCRIPT, template=REPORT_TEMPLATE)

    print("\n--- 3. Fixing civix_my_cases_widget ---")
    update_widget("civix_my_cases_widget", client_script=CASES_CLIENT_SCRIPT, template=CASES_TEMPLATE_FIXED, server_script=CASES_SERVER_SCRIPT)

    print("\n=== ALL CONTROLLER DEFECTS FIXED ===")
