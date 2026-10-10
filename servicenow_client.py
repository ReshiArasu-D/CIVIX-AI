"""
ServiceNow Integration Client for CIVIX-AI.

Provides programmatic access to ServiceNow Table APIs for incident management,
civic issue tracking, ticket updates, and status verification.
"""

import os
from typing import Any, Dict, List, Optional
import requests
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()


class ServiceNowClient:
    """Client for interacting with ServiceNow Table APIs."""

    def __init__(
        self,
        instance_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.instance_url = (instance_url or os.getenv("SERVICENOW_INSTANCE_URL", "")).rstrip("/")
        self.username = username or os.getenv("SERVICENOW_USERNAME", "")
        self.password = password or os.getenv("SERVICENOW_PASSWORD", "")

        if not self.instance_url or not self.username or not self.password:
            raise ValueError(
                "Missing ServiceNow credentials. Ensure SERVICENOW_INSTANCE_URL, "
                "SERVICENOW_USERNAME, and SERVICENOW_PASSWORD are set."
            )

        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def _url(self, endpoint: str) -> str:
        """Construct full URL for a given ServiceNow API endpoint."""
        return f"{self.instance_url}/{endpoint.lstrip('/')}"

    def test_connection(self) -> Dict[str, Any]:
        """
        Verify connection and authentication against the ServiceNow instance.
        Returns instance check details.
        """
        url = self._url("api/now/table/sys_user?sysparm_limit=1")
        response = self.session.get(url, timeout=15)
        response.raise_for_status()
        return {
            "status": "connected",
            "status_code": response.status_code,
            "instance_url": self.instance_url,
            "username": self.username,
        }

    def get_incidents(
        self,
        limit: int = 10,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch incidents from ServiceNow.
        """
        url = self._url("api/now/table/incident")
        params: Dict[str, Any] = {"sysparm_limit": limit}
        if query:
            params["sysparm_query"] = query
        if fields:
            params["sysparm_fields"] = ",".join(fields)

        response = self.session.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json().get("result", [])

    def get_incident(self, sys_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific incident by its sys_id.
        """
        url = self._url(f"api/now/table/incident/{sys_id}")
        response = self.session.get(url, timeout=15)
        response.raise_for_status()
        return response.json().get("result", {})

    def create_incident(
        self,
        short_description: str,
        description: str,
        category: str = "Civic Issue",
        urgency: int = 2,
        impact: int = 2,
        extra_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new incident ticket in ServiceNow.
        """
        url = self._url("api/now/table/incident")
        payload: Dict[str, Any] = {
            "short_description": short_description,
            "description": description,
            "category": category,
            "urgency": str(urgency),
            "impact": str(impact),
        }
        if extra_fields:
            payload.update(extra_fields)

        response = self.session.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json().get("result", {})

    def update_incident(self, sys_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing incident by sys_id.
        """
        url = self._url(f"api/now/table/incident/{sys_id}")
        response = self.session.patch(url, json=fields, timeout=15)
        response.raise_for_status()
        return response.json().get("result", {})


if __name__ == "__main__":
    client = ServiceNowClient()
    conn_info = client.test_connection()
    print("ServiceNow Connection Test Successful:")
    print(conn_info)

    recent_incidents = client.get_incidents(limit=3, fields=["number", "short_description", "state", "sys_id"])
    print(f"\nRetrieved {len(recent_incidents)} recent incidents:")
    for inc in recent_incidents:
        print(f"  - [{inc.get('number')}] {inc.get('short_description')} (sys_id: {inc.get('sys_id')})")
