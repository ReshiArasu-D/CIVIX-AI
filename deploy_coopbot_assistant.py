"""
CIVIX AI - CoopBot Floating Chat Assistant Across All Pages
Deploys the "Ask CoopBot AI" floating pill button + circular avatar + interactive AI chat drawer
across every single portal page in ServiceNow.
"""

import os
import sys
import base64
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

# Load Base64 image of CoopBot mascot
MASCOT_PATH = r"d:\tcs\coopbot_mascot_clean.png"
if os.path.exists(MASCOT_PATH):
    with open(MASCOT_PATH, "rb") as f:
        COOPBOT_IMG_B64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
else:
    COOPBOT_IMG_B64 = ""

# -----------------------------------------------------------------------------
# COOPBOT FLOATING HTML COMPONENT
# -----------------------------------------------------------------------------
COOPBOT_FLOATING_HTML = f"""
<!-- COOPBOT FLOATING ASSISTANT (PRESENT ON ALL PAGES) -->
<div class="coopbot-floating-container" id="coopbotRoot">
  
  <!-- 1. FLOATING LAUNCHER PILL & AVATAR (MATCHING USER SCREENSHOT) -->
  <div class="coopbot-launcher-bar" ng-click="c.toggleCoopBot()" title="Click to chat with CIVIX Assist" ng-show="!c.coopBotOpen">
    <!-- Pill button: Ask CIVIX Assist with Sparkle icon -->
    <div class="coopbot-pill-btn">
      <svg class="coopbot-sparkle-icon" width="16" height="16" viewBox="0 0 24 24" fill="none">
        <path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z" fill="#FF7A00" stroke="#FF7A00" stroke-width="1.5"/>
      </svg>
      <span class="coopbot-pill-label">Ask CIVIX Assist</span>
    </div>

    <!-- Circular Avatar with Orange Ring -->
    <div class="coopbot-avatar-circle-ring">
      <img src="{COOPBOT_IMG_B64}" alt="CIVIX Assist" class="coopbot-mascot-img" />
      <span class="coopbot-pulse-dot" title="Online"></span>
    </div>
  </div>

  <!-- 2. EXPANDABLE CHAT DRAWER / WINDOW -->
  <div class="coopbot-chat-window" ng-show="c.coopBotOpen" role="dialog" aria-label="CIVIX Assist AI Civic Assistant">
    <!-- Header -->
    <div class="coopbot-chat-header">
      <div class="coopbot-header-left">
        <div class="coopbot-header-avatar">
          <img src="{COOPBOT_IMG_B64}" alt="CIVIX Assist" />
        </div>
        <div class="coopbot-header-titles">
          <h4>CIVIX Assist</h4>
          <span class="coopbot-online-badge"><span class="coopbot-green-circle"></span> Online • Civic AI Assistant</span>
        </div>
      </div>
      <div class="coopbot-header-actions">
        <button type="button" class="coopbot-head-btn" ng-click="c.clearCoopBotChat()" title="Reset chat">↺</button>
        <button type="button" class="coopbot-head-btn" ng-click="c.toggleCoopBot()" title="Minimize">&minus;</button>
        <button type="button" class="coopbot-head-btn" ng-click="c.toggleCoopBot()" title="Close">&times;</button>
      </div>
    </div>

    <!-- Chat Messages Feed -->
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

      <!-- Typing Indicator -->
      <div class="coopbot-msg-row msg-bot" ng-show="c.coopBotTyping">
        <div class="coopbot-msg-avatar">
          <img src="{COOPBOT_IMG_B64}" alt="Bot" />
        </div>
        <div class="coopbot-typing-indicator">
          <span></span><span></span><span></span>
        </div>
      </div>
    </div>

    <!-- Prompt Suggestion Chips -->
    <div class="coopbot-chips-bar" ng-if="c.coopBotMessages.length <= 3">
      <button type="button" class="coopbot-chip-btn" ng-click="c.askCoopBotQuick('Track CIVIX-2024-00123')">📄 Track CIVIX-2024-00123</button>
      <button type="button" class="coopbot-chip-btn" ng-click="c.askCoopBotQuick('Report a Pothole or Leakage')">🚨 Report Issue</button>
      <button type="button" class="coopbot-chip-btn" ng-click="c.askCoopBotQuick('Ward 18 Emergency Contacts')">📞 Emergency Contacts</button>
      <button type="button" class="coopbot-chip-btn" ng-click="c.askCoopBotQuick('Water Supply Timings')">💧 Water Timings</button>
    </div>

    <!-- Input Footer -->
    <div class="coopbot-chat-footer">
      <form ng-submit="c.sendCoopBotMessage()" class="coopbot-input-form">
        <input type="text" class="coopbot-input-box" placeholder="Ask CIVIX Assist anything..." ng-model="c.coopBotInput" />
        <button type="submit" class="coopbot-send-btn" title="Send message" ng-disabled="!c.coopBotInput">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        </button>
      </form>
    </div>
  </div>

</div>
"""

# -----------------------------------------------------------------------------
# COOPBOT CSS STYLES
# -----------------------------------------------------------------------------
COOPBOT_CSS = """
/* COOPBOT FLOATING WIDGET STYLES */
.coopbot-floating-container {
  position: fixed;
  bottom: 24px;
  right: 28px;
  z-index: 999999;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* LAUNCHER PILL & AVATAR (EXACT REFERENCE REPRODUCTION) */
.coopbot-launcher-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.coopbot-launcher-bar:hover {
  transform: translateY(-3px);
}

.coopbot-pill-btn {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 9999px;
  padding: 8px 18px 8px 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.12), 0 1px 3px rgba(0,0,0,0.06);
  transition: all 0.25s ease;
}
.coopbot-launcher-bar:hover .coopbot-pill-btn {
  border-color: #FF7A00;
  box-shadow: 0 8px 24px rgba(255, 122, 0, 0.25);
}

.coopbot-sparkle-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  animation: coopbot-twinkle 2.4s ease-in-out infinite;
}
@keyframes coopbot-twinkle {
  0%, 100% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.18) rotate(15deg); }
}

.coopbot-pill-label {
  font-size: 13.5px;
  font-weight: 700;
  color: #1E293B;
  letter-spacing: -0.2px;
  white-space: nowrap;
}

.coopbot-avatar-circle-ring {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid #FF7A00;
  background: #FFFFFF;
  box-shadow: 0 4px 16px rgba(255, 122, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.25s ease;
}
.coopbot-launcher-bar:hover .coopbot-avatar-circle-ring {
  box-shadow: 0 0 0 4px rgba(255, 122, 0, 0.25), 0 8px 20px rgba(255, 122, 0, 0.4);
}

.coopbot-mascot-img {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  display: block;
}

.coopbot-pulse-dot {
  position: absolute;
  top: 1px;
  right: 1px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #10B981;
  border: 2px solid #FFFFFF;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: coopbot-pulse 1.8s infinite;
}
@keyframes coopbot-pulse {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* EXPANDABLE CHAT WINDOW */
.coopbot-chat-window {
  position: fixed;
  bottom: 86px;
  right: 28px;
  width: 380px;
  max-width: calc(100vw - 36px);
  height: 560px;
  max-height: calc(100vh - 110px);
  background: #FFFFFF;
  border-radius: 20px;
  box-shadow: 0 20px 48px rgba(15, 23, 42, 0.22), 0 4px 12px rgba(0,0,0,0.08);
  border: 1px solid #E2E8F0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1000000;
  animation: coopbot-slide-up 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes coopbot-slide-up {
  from { opacity: 0; transform: translateY(20px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.coopbot-chat-header {
  background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
  color: #FFFFFF;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.coopbot-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.coopbot-header-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 2px solid #FF7A00;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.coopbot-header-avatar img {
  width: 34px;
  height: 34px;
  object-fit: cover;
}
.coopbot-header-titles h4 {
  margin: 0;
  font-size: 15px;
  font-weight: 800;
  color: #FFFFFF;
}
.coopbot-online-badge {
  font-size: 11px;
  color: #94A3B8;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 2px;
}
.coopbot-green-circle {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10B981;
  display: inline-block;
}

.coopbot-header-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}
.coopbot-head-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #FFFFFF;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}
.coopbot-head-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* MESSAGE FEED */
.coopbot-messages-feed {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  background: #F8FAFC;
}
.coopbot-msg-row {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  max-width: 88%;
}
.coopbot-msg-row.msg-user {
  margin-left: auto;
  flex-direction: row-reverse;
}
.coopbot-msg-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1.5px solid #FF7A00;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}
.coopbot-msg-avatar img {
  width: 24px;
  height: 24px;
  object-fit: cover;
}
.coopbot-msg-bubble-wrap {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.coopbot-msg-row.msg-user .coopbot-msg-bubble-wrap {
  align-items: flex-end;
}
.coopbot-msg-bubble {
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 13px;
  line-height: 1.45;
  color: #0F172A;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}
.coopbot-msg-row.msg-user .coopbot-msg-bubble {
  background: linear-gradient(135deg, #0066FF, #0284C7);
  color: #FFFFFF;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 102, 255, 0.2);
}
.coopbot-link-btn {
  display: inline-block;
  margin-top: 6px;
  padding: 5px 10px;
  background: #0066FF;
  color: #FFFFFF !important;
  font-weight: 700;
  font-size: 11.5px;
  border-radius: 6px;
  text-decoration: none !important;
}
.coopbot-link-btn:hover {
  background: #0052CC;
}
.coopbot-msg-time {
  font-size: 10px;
  color: #94A3B8;
  padding: 0 4px;
}

/* TYPING INDICATOR */
.coopbot-typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 10px 14px;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
}
.coopbot-typing-indicator span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #94A3B8;
  animation: coopbot-bounce 1.4s infinite ease-in-out both;
}
.coopbot-typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.coopbot-typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
@keyframes coopbot-bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* PROMPT CHIPS */
.coopbot-chips-bar {
  padding: 8px 12px;
  background: #FFFFFF;
  border-top: 1px solid #F1F5F9;
  display: flex;
  gap: 6px;
  overflow-x: auto;
  white-space: nowrap;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.coopbot-chips-bar::-webkit-scrollbar {
  display: none;
}
.coopbot-chip-btn {
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  color: #0066FF;
  font-size: 11.5px;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.15s;
  flex-shrink: 0;
}
.coopbot-chip-btn:hover {
  background: #0066FF;
  color: #FFFFFF;
}

/* FOOTER INPUT */
.coopbot-chat-footer {
  padding: 12px;
  background: #FFFFFF;
  border-top: 1px solid #E2E8F0;
}
.coopbot-input-form {
  display: flex;
  align-items: center;
  gap: 8px;
}
.coopbot-input-box {
  flex: 1;
  padding: 9px 14px;
  border-radius: 9999px;
  border: 1px solid #CBD5E1;
  font-size: 13px;
  outline: none;
  font-family: inherit;
  transition: border-color 0.2s;
}
.coopbot-input-box:focus {
  border-color: #0066FF;
  box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.15);
}
.coopbot-send-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #0066FF;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
  flex-shrink: 0;
}
.coopbot-send-btn:hover:not(:disabled) {
  background: #0052CC;
}
.coopbot-send-btn:disabled {
  background: #CBD5E1;
  cursor: not-allowed;
}
"""

# -----------------------------------------------------------------------------
# CLIENT CONTROLLER EXTENSION FOR COOPBOT
# -----------------------------------------------------------------------------
COOPBOT_CLIENT_JS_EXT = """
  // === CIVIX ASSIST AI LOGIC ===
  c.coopBotOpen = false;
  c.coopBotTyping = false;
  c.coopBotInput = '';
  c.coopBotMessages = [
    {
      sender: 'bot',
      text: "Hi Priya! 👋 I'm <strong>CIVIX Assist</strong>, your smart civic assistant. How can I help you today?",
      time: 'Just now'
    }
  ];

  c.toggleCoopBot = function() {
    c.coopBotOpen = !c.coopBotOpen;
    if (c.coopBotOpen) {
      $timeout(function() {
        var el = document.getElementById('coopbotMsgFeed');
        if (el) el.scrollTop = el.scrollHeight;
      }, 100);
    }
  };

  c.clearCoopBotChat = function() {
    c.coopBotMessages = [
      {
        sender: 'bot',
        text: "Hi Priya! 👋 I'm <strong>CIVIX Assist</strong>, your smart civic assistant. How can I help you today?",
        time: 'Just now'
      }
    ];
  };

  c.askCoopBotQuick = function(txt) {
    c.coopBotInput = txt;
    c.sendCoopBotMessage();
  };

  c.sendCoopBotMessage = function() {
    var query = (c.coopBotInput || '').trim();
    if (!query) return;

    var now = new Date();
    var timeStr = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

    c.coopBotMessages.push({
      sender: 'user',
      text: query,
      time: timeStr
    });
    c.coopBotInput = '';
    c.coopBotTyping = true;

    $timeout(function() {
      var el = document.getElementById('coopbotMsgFeed');
      if (el) el.scrollTop = el.scrollHeight;
    }, 50);

    // AI Intent Response Resolver
    $timeout(function() {
      c.coopBotTyping = false;
      var q = query.toLowerCase();
      var botReply = "";

      if (q.indexOf('track') !== -1 || q.indexOf('civix-2024-00123') !== -1 || q.indexOf('leakage') !== -1 || q.indexOf('water') !== -1 && q.indexOf('status') !== -1) {
        botReply = "📍 <strong>CIVIX-2024-00123</strong> (Water leakage on 3rd Main Road, Adyar) is currently <strong>In Progress</strong>.<br><br>• Crew: Ward 18 Hydraulic Works<br>• Target Resolution: 18 Nov 2024, 05:00 PM<br><br><a href='?id=civix_track_case&sys_id=c1' class='coopbot-link-btn'>View Case Tracking Details →</a>";
      } else if (q.indexOf('pothole') !== -1 || q.indexOf('civix-2024-00110') !== -1) {
        botReply = "✅ Case <strong>CIVIX-2024-00110</strong> (Pothole near 100 Feet Road, T. Nagar) has been <strong>Resolved</strong> by the Corporation Roads Division.<br><br><a href='?id=civix_track_case&sys_id=c3' class='coopbot-link-btn'>View Resolved Case →</a>";
      } else if (q.indexOf('report') !== -1 || q.indexOf('issue') !== -1 || q.indexOf('new') !== -1) {
        botReply = "🚨 Ready to report an issue? Choose a department:<br><br>• <a href='?id=civix_report_issue' class='coopbot-link-btn'>Open Issue Report Portal</a><br>Or tell me your location and complaint category (Water, Roads, Electricity, Drainage).";
      } else if (q.indexOf('emergency') !== -1 || q.indexOf('contact') !== -1 || q.indexOf('phone') !== -1 || q.indexOf('ward') !== -1) {
        botReply = "📞 <strong>Municipal Ward Contacts:</strong><br><br>• Ward 18 (Adyar) Hotline: <strong>1800-425-0018</strong><br>• Central Corporation Control Room: <strong>1913</strong><br>• Junior Engineer: <strong>V. Murugan</strong> (94440-12345)";
      } else if (q.indexOf('map') !== -1) {
        botReply = "🗺️ You can inspect verified civic incidents live across Chennai on our interactive Issue Map:<br><br><a href='?id=civix_home#map' class='coopbot-link-btn'>Open Chennai Issue Map →</a>";
      } else if (q.indexOf('hi') !== -1 || q.indexOf('hello') !== -1 || q.indexOf('namaste') !== -1) {
        botReply = "Namaste Priya! 🙏 How can I assist you today with municipal services or ticket status?";
      } else {
        botReply = "I understand you are asking about <em>" + query + "</em>. I have logged your civic inquiry. You can track all active cases under <a href='?id=civix_my_cases' class='coopbot-link-btn'>My Complaints</a> or reach the Ward 18 desk at 1800-425-0018.";
      }

      c.coopBotMessages.push({
        sender: 'bot',
        text: botReply,
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
      });

      $timeout(function() {
        var el = document.getElementById('coopbotMsgFeed');
        if (el) el.scrollTop = el.scrollHeight;
      }, 50);
    }, 600);
  };
"""

def update_widget(widget_id: str, template: str, css: str, client_script: str, server_script: str):
    res = api_get("sp_widget", query=f"id={widget_id}", limit=1)
    if not res:
        print(f"Widget {widget_id} not found!")
        return None
    sys_id = res[0]["sys_id"]
    payload = {
        "template": template.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "sys_scope": APP_SYS_ID,
        "sys_package": APP_SYS_ID,
        "public": "true"
    }
    api_put("sp_widget", sys_id, payload)
    print(f"  [UPDATED] {widget_id} ({sys_id})")
    return sys_id

# -----------------------------------------------------------------------------
# APPLY COOPBOT TO A WIDGET
# -----------------------------------------------------------------------------
def inject_coopbot(widget_id: str):
    res = api_get("sp_widget", query=f"id={widget_id}", limit=1)
    if not res:
        print(f"Widget {widget_id} not found!")
        return
    row = res[0]
    sys_id = row["sys_id"]
    tmpl = row.get("template", "")
    css = row.get("css", "")
    client_script = row.get("client_script", "")
    server_script = row.get("script", "")

    # Clean and replace Template
    if "<!-- COOPBOT FLOATING ASSISTANT" in tmpl:
        tmpl = tmpl.split("<!-- COOPBOT FLOATING ASSISTANT")[0].strip()
        if not tmpl.endswith("</div>"):
            tmpl += "\n</div>"

    if "</div>" in tmpl:
        last_idx = tmpl.rfind("</div>")
        tmpl = tmpl[:last_idx] + "\n" + COOPBOT_FLOATING_HTML + "\n</div>" + tmpl[last_idx+6:]
    else:
        tmpl = tmpl + "\n" + COOPBOT_FLOATING_HTML

    # Clean and replace CSS
    if "/* COOPBOT FLOATING WIDGET STYLES */" in css:
        css = css.split("/* COOPBOT FLOATING WIDGET STYLES */")[0].strip()
    css = css + "\n\n" + COOPBOT_CSS

    # Clean and replace Client Script
    if "// === COOPBOT AI ASSISTANT LOGIC ===" in client_script:
        client_script = client_script.split("// === COOPBOT AI ASSISTANT LOGIC ===")[0].strip()
        if not client_script.endswith("}"):
            client_script += "\n}"

    last_brace = client_script.rfind("}")
    if last_brace != -1:
        client_script = client_script[:last_brace] + "\n" + COOPBOT_CLIENT_JS_EXT + "\n" + client_script[last_brace:]
    else:
        client_script = client_script + "\n" + COOPBOT_CLIENT_JS_EXT

    payload = {
        "template": tmpl.strip(),
        "css": css.strip(),
        "client_script": client_script.strip(),
        "script": server_script.strip(),
        "sys_scope": APP_SYS_ID,
        "sys_package": APP_SYS_ID,
        "public": "true"
    }
    api_put("sp_widget", sys_id, payload)
    print(f"  [COOPBOT ATTACHED] {widget_id} ({sys_id})")

# -----------------------------------------------------------------------------
# MAIN DEPLOYMENT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== DEPLOYING COOPBOT AI FLOATING ASSISTANT ACROSS ALL PAGES ===")

    widgets = [
        "civix_home_widget",
        "civix_dashboard_widget",
        "civix_track_case_widget",
        "civix_report_issue_widget",
        "civix_my_cases_widget",
        "civix_landing_widget",
        "civix_portal_select_widget",
        "civix_profile_widget"
    ]

    for w in widgets:
        inject_coopbot(w)

    print("\n=== ALL PORTAL WIDGETS UPGRADED WITH FLOATING COOPBOT AI ===")
