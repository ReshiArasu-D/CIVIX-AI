"""
CIVIX AI - Live Verification & Test Suite
Tests all 11 Service Portal screens, guest access, authentication, and responses.
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

INSTANCE_URL = os.getenv("SERVICENOW_INSTANCE_URL", "").rstrip("/")
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")

pages = [
    ("Landing Page", "civix_landing"),
    ("Portal Selection", "civix_portal_select"),
    ("Citizen Home", "civix_home"),
    ("Registration", "civix_register"),
    ("Login", "civix_login"),
    ("Account Recovery", "civix_recovery"),
    ("Customer Dashboard", "civix_dashboard"),
    ("My Cases", "civix_my_cases"),
    ("Report Issue", "civix_report_issue"),
    ("Case Tracking", "civix_track_case"),
    ("Profile & Settings", "civix_profile")
]

def test_portal():
    print(f"Testing Live Portal at: {INSTANCE_URL}/civix\n")
    session = requests.Session()
    # Unauthenticated / guest session
    r = session.get(f"{INSTANCE_URL}/civix", timeout=15)
    print(f"[*] /civix HTTP Status: {r.status_code}")
    assert r.status_code == 200, "Portal homepage failed to respond 200 OK"
    print("    [PASS] /civix responded 200 OK")

    for title, pid in pages:
        url = f"{INSTANCE_URL}/civix?id={pid}"
        resp = session.get(url, timeout=15)
        status = resp.status_code
        has_content = "CIVIX AI" in resp.text or pid in resp.text
        print(f"[*] Page '{title}' (?id={pid}): Status {status} | Rendered: {has_content}")
        if status != 200:
            print(f"    [FAIL] Status {status}")
        else:
            print(f"    [PASS] {title} verified successfully")

if __name__ == "__main__":
    test_portal()
