# CIVIX-AI

AI-Powered Civic Issue Intelligence & Incident Management Platform.

This project is connected with:
- **GitHub Repository**: [https://github.com/ReshiArasu-D/CIVIX-AI.git](https://github.com/ReshiArasu-D/CIVIX-AI.git)
- **ServiceNow Instance**: [https://dev187180.service-now.com](https://dev187180.service-now.com)

---

## Architecture & Integration

CIVIX-AI links civic incident management with ServiceNow's Table API (`/api/now/table/incident`), allowing automated logging, status tracking, and ticket updates.

### Connected Components:
1. **Git Remote**: `origin` points to `https://github.com/ReshiArasu-D/CIVIX-AI.git` on branch `main`.
2. **ServiceNow Table API**: Uses Basic Authentication (`admin`) to interface with developer instance `dev187180`.

---

## Configuration

Credentials and environment parameters are stored in [.env](file:///d:/tcs/.env) (and templated in [.env.example](file:///d:/tcs/.env.example)):

```env
SERVICENOW_INSTANCE_URL=https://dev187180.service-now.com
SERVICENOW_USERNAME=admin
SERVICENOW_PASSWORD=mn%XC1^ScdA4
GIT_REPO_URL=https://github.com/ReshiArasu-D/CIVIX-AI.git
```

> **Note**: Sensitive credentials in `.env` are excluded from version control via [.gitignore](file:///d:/tcs/.gitignore).

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify ServiceNow Connectivity
Run the integration client:
```bash
python servicenow_client.py
```

### 3. Using the ServiceNow Client in Your Code
```python
from servicenow_client import ServiceNowClient

client = ServiceNowClient()

# Check connection
print(client.test_connection())

# Fetch recent incidents
incidents = client.get_incidents(limit=5)

# Create a civic issue ticket
ticket = client.create_incident(
    short_description="Pothole reported on Main St",
    description="Citizen reported large pothole near intersection of 5th & Main.",
    category="Civic Issue",
    urgency=2,
    impact=2
)
print("Created Ticket:", ticket["number"])
```

---

## Git Workflow

To commit and push updates to the GitHub repository:
```bash
git add .
git commit -m "Initialize project structure with ServiceNow connector"
git push -u origin main
```
