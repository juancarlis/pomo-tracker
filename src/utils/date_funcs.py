from datetime import datetime
from typing import Optional


def format_date_to_min(date_str: Optional[str]) -> str:
    """Format ISO datetime to 'YYYY-MM-DD HH:MM'."""

    if date_str:
        return datetime.fromisoformat(date_str).strftime("%Y-%m-%d %H:%M")
    return ""
