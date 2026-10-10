"""
Fix Portal Selection Card Box Sizes
Adjusts the 3 portal cards to be elegant portrait boxes (340px wide, 480px tall)
centered neatly in the viewport, matching Reference Image 1 exactly.
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

print(">>> Fetching civix_portal_select_widget...")
res = api_get("sp_widget", query="id=civix_portal_select_widget", limit=1)
if not res:
    print("Widget not found!")
    exit(1)

widget = res[0]
sys_id = widget["sys_id"]
css = widget.get("css", "")

NEW_CARD_CSS = """
/* Main Section & Refined Card Dimensions (Matches Reference Image 1) */
.civix-portal-main {
  width: 100%;
  max-width: 1120px !important;
  margin: 0 auto !important;
  padding: 16px 20px 48px 20px !important;
  position: relative;
  z-index: 10;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
}

/* Hero Title Block */
.civix-portal-hero {
  text-align: center;
  max-width: 740px;
  margin-bottom: 40px;
}

.civix-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.35);
  color: #F59E0B;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  padding: 6px 16px;
  border-radius: 9999px;
  margin-bottom: 18px;
}

.civix-portal-headline {
  font-size: 42px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: -0.03em;
  line-height: 1.15;
  margin: 0 0 14px 0;
}

.civix-portal-subtext {
  font-size: 15px;
  font-weight: 400;
  color: #94A3B8;
  line-height: 1.55;
  margin: 0 auto;
  max-width: 620px;
}

/* 3 Cards Container - Centered, Fixed Portrait Proportions (Reference Image 1) */
.civix-cards-grid {
  display: flex !important;
  justify-content: center !important;
  align-items: stretch !important;
  gap: 24px !important;
  width: 100% !important;
  max-width: 1080px !important;
  margin: 0 auto !important;
}

/* Base Card Styling - Sleek Portrait Box */
.civix-card {
  flex: 0 0 340px !important;
  width: 340px !important;
  max-width: 340px !important;
  min-height: 480px !important;
  background: #0E1526 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 20px !important;
  padding: 34px 28px !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35) !important;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
  position: relative;
  box-sizing: border-box !important;
}

.civix-card:hover {
  transform: translateY(-6px);
}

/* Card 1: Citizen (Orange Theme) */
.civix-card-citizen:hover {
  border-color: rgba(249, 115, 22, 0.45) !important;
  box-shadow: 0 16px 40px rgba(249, 115, 22, 0.16), 0 0 20px rgba(249, 115, 22, 0.08) !important;
}

.civix-card-citizen .civix-card-icon-box {
  background: rgba(249, 115, 22, 0.12);
  border: 1px solid rgba(249, 115, 22, 0.3);
  box-shadow: 0 0 20px rgba(249, 115, 22, 0.2);
}

.civix-card-citizen .civix-card-tag {
  color: #FB923C;
}

/* Card 2: Officer (Blue Theme) */
.civix-card-officer:hover {
  border-color: rgba(59, 130, 246, 0.45) !important;
  box-shadow: 0 16px 40px rgba(59, 130, 246, 0.16), 0 0 20px rgba(59, 130, 246, 0.08) !important;
}

.civix-card-officer .civix-card-icon-box {
  background: rgba(59, 130, 246, 0.12);
  border: 1px solid rgba(59, 130, 246, 0.3);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
}

.civix-card-officer .civix-card-tag {
  color: #60A5FA;
}

/* Card 3: Admin (Green / Amber Theme) */
.civix-card-admin:hover {
  border-color: rgba(16, 185, 129, 0.45) !important;
  box-shadow: 0 16px 40px rgba(16, 185, 129, 0.16), 0 0 20px rgba(16, 185, 129, 0.08) !important;
}

.civix-card-admin .civix-card-icon-box {
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.3);
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
}

.civix-card-admin .civix-card-tag {
  color: #34D399;
}

/* Card Inner Elements */
.civix-card-icon-box {
  width: 58px;
  height: 58px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.civix-card-tag {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.4px;
  margin-bottom: 6px;
  display: block;
}

.civix-card-title {
  font-size: 23px;
  font-weight: 700;
  color: #FFFFFF;
  margin: 0 0 12px 0;
  letter-spacing: -0.02em;
}

.civix-card-desc {
  font-size: 13.5px;
  color: #94A3B8;
  line-height: 1.55;
  margin-bottom: 28px;
  min-height: 64px;
}

.civix-card-actions {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}

/* Responsive */
@media (max-width: 1120px) {
  .civix-cards-grid {
    flex-wrap: wrap !important;
    justify-content: center !important;
  }
  .civix-card {
    flex: 0 0 320px !important;
    width: 320px !important;
  }
}

@media (max-width: 768px) {
  .civix-cards-grid {
    flex-direction: column !important;
    align-items: center !important;
  }
  .civix-card {
    flex: 1 1 auto !important;
    width: 100% !important;
    max-width: 380px !important;
  }
  .civix-ambient-pill {
    display: none !important;
  }
  .civix-portal-headline {
    font-size: 30px;
  }
}
"""

# Find where Main Section starts in current CSS
split_marker = "/* Main Section */"
if split_marker in css:
    header_css = css.split(split_marker)[0]
    # Also find buttons and footer
    btn_marker = "/* Buttons */"
    if btn_marker in css:
        btn_footer_css = btn_marker + css.split(btn_marker)[1]
    else:
        btn_footer_css = ""
    updated_css = header_css + "\n" + NEW_CARD_CSS + "\n" + btn_footer_css
else:
    updated_css = css + "\n" + NEW_CARD_CSS

api_put("sp_widget", sys_id, {"css": updated_css.strip()})
print("  [SUCCESS] civix_portal_select_widget CSS updated with elegant 340px portrait card sizes!")
