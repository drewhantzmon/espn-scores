"""Parser functions to transform ESPN API responses into clean JSON."""

from typing import Dict, Any, Optional


def parse_espn_response(raw_data: Dict[str, Any], league: str) -> Dict[str, Any]:
    """
    Parse raw ESPN API response into a clean, simplified format.
    
    Args:
        raw_data: Raw JSON response from ESPN API
        league: League name (e.g., "NFL", "NBA", "NHL", "CFB", "CBB")
        
    Returns:
        Cleaned and simplified dictionary with game data in Option 3 format
    """
    # Extract season info - can be at top level or in leagues
    season_data = raw_data.get("season", {})
    
    # If not at top level, check leagues array
    if not season_data and "leagues" in raw_data and raw_data["leagues"]:
        season_data = raw_data["leagues"][0].get("season", {})
    
    # Week info can be in season.week or at the events level (for NFL)
    week_number = None
    if "week" in season_data:
        week_data = season_data.get("week", {})
        week_number = week_data.get("number")
    
    # Check top-level week object (NFL uses this)
    if week_number is None and "week" in raw_data:
        week_number = raw_data.get("week", {}).get("number")
    
    # If not found, try getting from events
    if week_number is None:
        events = raw_data.get("events", [])
        if events and "week" in events[0]:
            week_number = events[0].get("week", {}).get("number")
    
    # For NBA, NHL, and CBB, extract date instead of week
    date = None
    if league in ["NBA", "NHL", "CBB"]:
        events = raw_data.get("events", [])
        if events:
            # Get date from first event and format as YYYY-MM-DD
            event_date = events[0].get("date", "")
            if event_date:
                date = event_date.split("T")[0]
    
    result = {
        "sport": league,
        "season": season_data.get("year"),
        "games": _parse_games(raw_data.get("events", []), league)
    }
    
    # Add week for NFL/CFB, date for NBA/NHL/CBB
    if league in ["NFL", "CFB"]:
        result["week"] = week_number
    elif league in ["NBA", "NHL", "CBB"]:
        result["date"] = date
    
    return result


def _parse_games(events: list, league: str = "NFL") -> list:
    """
    Parse individual game events from ESPN API.
    
    Args:
        events: List of event objects from ESPN API
        league: League name (e.g., "NFL", "NBA", "NHL", "CFB", "CBB")
        
    Returns:
        List of parsed game dictionaries in minimal format
    """
    games = []
    
    for event in events:
        # Get the competition (usually first item in competitions array)
        competitions = event.get("competitions", [])
        if not competitions:
            continue
            
        competition = competitions[0]
        competitors = competition.get("competitors", [])
        
        if len(competitors) < 2:
            continue
        
        # Find home and away teams
        home_team = None
        away_team = None
        
        for competitor in competitors:
            if competitor.get("homeAway") == "home":
                home_team = competitor
            elif competitor.get("homeAway") == "away":
                away_team = competitor
        
        if not home_team or not away_team:
            continue
        
        # Get status info
        status = competition.get("status", {})
        status_type = status.get("type", {})
        status_state = status_type.get("state", "")
        
        # Map ESPN status to our status
        if status_state == "post":
            game_status = "final"
        elif status_state == "in":
            game_status = "in_progress"
        else:
            game_status = "scheduled"
        
        # Build the game object
        game = {
            "id": event.get("id"),
            "status": game_status,
            "away_team": _parse_team(away_team, game_status),
            "home_team": _parse_team(home_team, game_status)
        }
        
        # Add time info for in-progress games
        if game_status == "in_progress":
            game["game_time"] = _parse_game_time(status, league)
        
        # Add start time for scheduled games
        if game_status == "scheduled":
            game["start_time"] = event.get("date")
        
        games.append(game)
    
    return games


def _parse_team(competitor: Dict[str, Any], game_status: str) -> Dict[str, Any]:
    """
    Parse team data from ESPN competitor object.
    
    Args:
        competitor: Competitor object from ESPN API
        game_status: Current status of the game
        
    Returns:
        Parsed team dictionary with minimal info
    """
    team_data = competitor.get("team", {})
    score = competitor.get("score")
    
    # Convert score to int or None
    if score is not None:
        try:
            score = int(score)
        except (ValueError, TypeError):
            score = None
    
    # For scheduled games, score should be None
    if game_status == "scheduled":
        score = None
    
    return {
        "name": team_data.get("displayName", ""),
        "score": score
    }


def _parse_game_time(status: Dict[str, Any], league: str = "NFL") -> Dict[str, Any]:
    """
    Parse game time information for in-progress games.
    
    Args:
        status: Status object from ESPN API
        league: League name (e.g., "NFL", "NBA", "NHL", "CFB", "CBB")
        
    Returns:
        Dictionary with quarter/period and time remaining/clock
    """
    period = status.get("period", 0)
    display_clock = status.get("displayClock", "0:00")
    
    if league in ["NBA", "CBB"]:
        # NBA and CBB use periods (4 halves/quarters) and clock
        if period == 5:
            period_str = "OT"
        elif period > 5:
            period_str = f"OT{period - 4}"
        else:
            period_str = str(period)
        
        return {
            "period": period_str,
            "clock": display_clock
        }
    elif league == "NHL":
        # NHL uses periods (3 periods) and clock
        if period == 4:
            period_str = "OT"
        elif period > 4:
            period_str = f"OT{period - 3}"
        else:
            period_str = str(period)
        
        return {
            "period": period_str,
            "clock": display_clock
        }
    else:
        # NFL and CFB use quarters and time remaining
        if period == 5:
            quarter = "OT"
        elif period > 5:
            quarter = f"OT{period - 4}"
        else:
            quarter = f"Q{period}"
        
        return {
            "quarter": quarter,
            "time_remaining": display_clock
        }
