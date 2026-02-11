import json
import os
import pytz
from datetime import datetime
from typing import Optional, Tuple

CST = pytz.timezone("America/Chicago")
UTC = pytz.timezone("UTC")

def convert_utc_to_cst(utc_time_str: str, fmt: str = "%Y-%m-%dT%H:%M:%SZ") -> str:
    """Convert UTC timestamp to CST formatted string."""
    try:
        dt = datetime.strptime(utc_time_str.split(".")[0], "%Y-%m-%dT%H:%M:%S")
        dt = UTC.localize(dt)
        dt_cst = dt.astimezone(CST)
        return dt_cst.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error converting UTC to CST: {e}")
        return utc_time_str

def convert_cst_to_utc(date_str: str, time_str: str) -> Tuple[str, str]:
    """Convert CST date and time to UTC."""
    try:
        datetime_str = f"{date_str} {time_str}"
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        dt_cst = CST.localize(dt)
        dt_utc = dt_cst.astimezone(UTC)
        return dt_utc.strftime("%Y-%m-%d"), dt_utc.strftime("%H:%M:%S")
    except Exception as e:
        print(f"Error converting CST to UTC: {e}")
        return date_str, time_str

def safe_load_json(file_path: str) -> dict:
    """Safely load a JSON file."""
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON {file_path}: {e}")
        return {}

def safe_save_json(data: dict, file_path: str):
    """Safely save data to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving JSON {file_path}: {e}")

def parse_monday_time_value(time_str: Optional[str]) -> Optional[str]:
    """Parse time string from Monday.com JSON."""
    if not time_str:
        return None
    try:
        time_data = json.loads(time_str)
        return time_data.get("time")
    except:
        return None

def parse_monday_date_value(date_str: Optional[str]) -> Optional[str]:
    """Parse date string from Monday.com JSON."""
    if not date_str:
        return None
    try:
        date_data = json.loads(date_str)
        return date_data.get("date")
    except:
        return None
