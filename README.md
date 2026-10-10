# CIVIX AI — Phase 1 Customer Portal Implementation

**CIVIX AI — Agentic Intelligence Platform for Smart Urban Corporation Management**

- **GitHub Repository**: [https://github.com/ReshiArasu-D/CIVIX-AI.git](https://github.com/ReshiArasu-D/CIVIX-AI.git)
- **ServiceNow Instance**: [https://dev187180.service-now.com](https://dev187180.service-now.com)
- **Portal URL**: [https://dev187180.service-now.com/civix](https://dev187180.service-now.com/civix)
- **Application Scope**: `x_civic_ai` (`CIVIX AI` scoped app `4750065ac37b0f14e54832f1b4013184`)
- **Default Update Set**: `4b50865ac37b0f14e54832f1b4013155`

---

## Implemented & Verified Citizen Journey Pages

| Screen | Page ID | Route | Status | Description |
| :--- | :--- | :--- | :--- | :--- |
| **1. Public Landing** | `civix_landing` | `/civix?id=civix_landing` | **Verified (200 OK)** | Hero ("Smarter Cities. Faster Civic Services."), 4 Core Services, How It Works, Ward Notices, Trust & Transparency |
| **2. Portal Selection** | `civix_portal_select` | `/civix?id=civix_portal_select` | **Verified (200 OK)** | Citizen Portal (Phase 1 Active), Officer & Field Worker cards (Phase 2 Scheduled) |
| **3. Citizen Home** | `civix_home` | `/civix?id=civix_home` | **Verified (200 OK)** | "Your Neighbourhood, Better Connected", 4 shortcuts, recent cases, Civic AI assistant banner |
| **4. Registration** | `civix_register` | `/civix?id=civix_register` | **Verified (200 OK)** | Grouped fields, independent eye toggles, mobile (+91), server validation, `x_civic_ai_citizen` role |
| **5. Login** | `civix_login` | `/civix?id=civix_login` | **Verified (200 OK)** | Native ServiceNow authentication, password visibility toggle, redirect to dashboard |
| **6. Account Recovery** | `civix_recovery` | `/civix?id=civix_recovery` | **Verified (200 OK)** | Privacy-preserving password reset intake, reports SMTP developer dependency |
| **7. Dashboard** | `civix_dashboard` | `/civix?id=civix_dashboard` | **Verified (200 OK)** | 4 KPI summary cards, category grid, recent complaints with status badges, alerts, Civic AI Assistant |
| **8. My Cases** | `civix_my_cases` | `/civix?id=civix_my_cases` | **Verified (200 OK)** | Filter by status/category, search by case number, authorized cases table |
| **9. Report Issue** | `civix_report_issue` | `/civix?id=civix_report_issue` | **Verified (200 OK)** | 3-step wizard (Category -> Location & Geo -> Review & Submit), creates real ServiceNow incidents |
| **10. Case Tracking** | `civix_track_case` | `/civix?id=civix_track_case` | **Verified (200 OK)** | Approved lifecycle timeline (Submitted &rarr; Under Review &rarr; Assigned &rarr; In Progress &rarr; Resolved &rarr; Closed) |
| **11. Profile & Settings**| `civix_profile` | `/civix?id=civix_profile` | **Verified (200 OK)** | Citizen details, ward locality, language preference, session logout |

---

## Design System & Theme Tokens

- **Primary Deep Teal**: `#123E46`
- **Primary Action Teal**: `#087F8C`
- **Mint Accent**: `#E1F5EA`
- **Main Background**: `#F7FAFA`
- **White Surface**: `#FFFFFF`
- **Text Main**: `#183238`
- **Text Muted**: `#61777B`
- **Border**: `#DCE7E8`
- **Status Colors**: Error `#B42318`, Warning `#B54708`, Success `#18794E`
- **Typography**: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans Tamil", sans-serif`
- **Language Selector**: Supports all 22 Eighth Schedule Indian languages in header dropdown; English & Tamil (`தமிழ்`) verified interface dictionary.

---

## Scripts & Deployment Tools

- `deploy_civix.py`: Verification and scope connection.
- `build_civix_portal.py`: Generates the portal theme, responsive header, and footer widgets.
- `build_all_screens.py`: Generates and links all 11 Service Portal screens, widgets, and container hierarchies.
- `test_all_pages.py`: Live integration test suite verifying HTTP 200 status and component rendering for all pages.
