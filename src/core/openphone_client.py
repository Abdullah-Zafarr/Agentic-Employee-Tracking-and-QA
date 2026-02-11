import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional

load_dotenv()

class OpenPhoneClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENPHONE_API_KEY")
        if not self.api_key:
            raise ValueError("OPENPHONE_API_KEY not found in environment")
        self.url = "https://api.openphone.com/v1"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a GET request to the OpenPhone API."""
        url = f"{self.url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def fetch_phone_numbers(self) -> Dict:
        """Fetch all phone numbers."""
        return self.get("phone-numbers")

    def fetch_calls(self, phone_number_id: str, participants: Optional[str] = None) -> Dict:
        """Fetch calls for a specific phone number."""
        params = {"phoneNumberId": phone_number_id}
        if participants:
            params["participants"] = participants
        return self.get("calls", params=params)

    def fetch_transcript(self, call_id: str) -> Dict:
        """Fetch a transcript for a specific call."""
        return self.get(f"call-transcripts/{call_id}")
