"""Helper utility functions."""

from datetime import datetime
from typing import Optional, Dict, Any
from espn_scores.core.client import ESPNClient


def get_league_info(sport_path: str = "football/nfl") -> Dict[str, Any]:
    """
    Get current league information from ESPN API.
    
    Args:
        sport_path: Sport path (e.g., "football/nfl", "football/college-football")
    
    Returns:
        Dictionary with current league information including week number
    """
    try:
        client = ESPNClient()
        data = client.get(f"{sport_path}/scoreboard")
        
        # Extract league info from the response
        if "leagues" in data and len(data["leagues"]) > 0:
            league_data = data["leagues"][0]
            season_data = league_data.get("season", {})
            season_type = season_data.get("type", {})
            
            # Get current week - check multiple locations
            current_week = None
            
            # First check top-level week object
            if "week" in data and isinstance(data["week"], dict):
                current_week = data["week"].get("number")
            # Then check season.week
            elif "week" in season_data:
                current_week = season_data["week"]
            # Finally check first event's week
            elif "events" in data and len(data["events"]) > 0:
                current_week = data["events"][0].get("week", {}).get("number")
            
            return {
                "league_id": league_data.get("id"),
                "league_name": league_data.get("name"),
                "league_abbrev": league_data.get("abbreviation"),
                "season_year": season_data.get("year"),
                "season_type": season_type.get("type"),
                "season_type_name": season_type.get("name"),
                "current_week": current_week
            }
    except Exception:
        pass
    
    # Fallback to reasonable defaults if API call fails
    return {
        "league_id": "28",
        "league_name": "National Football League",
        "league_abbrev": "NFL",
        "season_year": datetime.now().year,
        "season_type": 2,
        "season_type_name": "Regular Season",
        "current_week": 1
    }


def get_current_week(sport_path: str = "football/nfl") -> int:
    """
    Get the current week number for a given sport from ESPN API.
    
    Args:
        sport_path: Sport path (e.g., "football/nfl", "football/college-football")
        
    Returns:
        Current week number
    """
    league_info = get_league_info(sport_path)
    return league_info.get("current_week") or 1


def format_date(date: datetime) -> str:
    """
    Format a datetime object to ESPN API date format (YYYYMMDD).
    
    Args:
        date: datetime object to format
        
    Returns:
        Date string in YYYYMMDD format
    """
    return date.strftime("%Y%m%d")


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse a date string into a datetime object.
    
    Args:
        date_str: Date string to parse
        
    Returns:
        datetime object or None if parsing fails
    """
    try:
        # Try common formats
        for fmt in ["%Y%m%d", "%Y-%m-%d", "%m/%d/%Y"]:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None
    except Exception:
        return None


def get_season_year(sport_path: str = "football/nfl") -> int:
    """
    Get the current season year from ESPN API.
    
    Args:
        sport_path: Sport path (e.g., "football/nfl", "football/college-football")
    
    Returns:
        Current season year
    """
    league_info = get_league_info(sport_path)
    return league_info.get("season_year") or datetime.now().year


def get_current_season_type(sport_path: str = "football/nfl") -> int:
    """
    Get the current season type (preseason, regular, postseason) from ESPN API.
    
    Args:
        sport_path: Sport path (e.g., "football/nfl", "football/college-football")
    
    Returns:
        Season type (1=Preseason, 2=Regular Season, 3=Postseason)
    """
    league_info = get_league_info(sport_path)
    return league_info.get("season_type") or 2
