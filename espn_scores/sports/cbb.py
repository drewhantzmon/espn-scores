"""College Basketball-specific implementation for ESPN Scores."""

from typing import Dict, Any, Optional
from datetime import datetime
from espn_scores.sports.base import BaseSport
from espn_scores.utils.helpers import format_date, parse_date


class CBB(BaseSport):
    """
    College Basketball-specific implementation of the ESPN Scores API.
    
    This class provides methods to fetch college basketball game scores and information
    from ESPN's API in a clean, minimal format. CBB uses date-based queries like NBA.
    
    Example:
        >>> from espn_scores import cbb
        >>> 
        >>> # Get today's games
        >>> games = cbb.today()
        >>> print(f"Games today: {len(games['games'])}")
        >>> 
        >>> # Get games from specific date
        >>> nov_17 = cbb.date("20251117")
        >>> 
        >>> # Filter by conference
        >>> acc_games = cbb.today(groups='ACC')
    """
    
    @property
    def sport_path(self) -> str:
        """Return the ESPN API path for CBB."""
        return "basketball/mens-college-basketball"
    
    @property
    def league_name(self) -> str:
        """Return the league name."""
        return "CBB"
    
    def today(self, status: Optional[str] = None, groups = None) -> Dict[str, Any]:
        """
        Get scores for today's college basketball games.
        
        Args:
            status: Optional filter by game status. Valid values:
                   - 'final': Only completed games
                   - 'in_progress': Only live games
                   - 'scheduled': Only upcoming games
                   - None: All games (default)
            groups: Optional conference/group ID or name to filter by specific conference.
                   Can be an int (1, 4, 5, 8) or string ('ACC', 'SEC', 'Big Ten', etc.)
            
        Returns:
            Dictionary with minimal game data:
            {
                "sport": "CBB",
                "date": "2025-11-18",
                "season": 2026,
                "games": [...]
            }
            
        Example:
            >>> games = cbb.today()
            >>> finals = cbb.today(status='final')
            >>> acc_games = cbb.today(groups='ACC')
            >>> big_ten = cbb.today(groups='Big Ten')
        """
        today_date = datetime.now().strftime("%Y%m%d")
        return self.date(today_date, status=status, groups=groups)
    
    def date(self, date_str: str, status: Optional[str] = None, groups = None) -> Dict[str, Any]:
        """
        Get scores for college basketball games on a specific date.
        
        Args:
            date_str: Date in YYYYMMDD or YYYY-MM-DD format
            status: Optional filter by game status ('final', 'in_progress', 'scheduled')
            groups: Optional conference/group ID or name to filter by specific conference.
                   Can be an int (1, 4, 5, 8) or string ('ACC', 'SEC', 'Big Ten', etc.)
            
        Returns:
            Dictionary with minimal game data for the specified date
            
        Example:
            >>> nov_17 = cbb.date("20251117")
            >>> nov_17_alt = cbb.date("2025-11-17")
            >>> acc_finals = cbb.date("20251117", groups='ACC', status='final')
        """
        # Normalize date format to YYYYMMDD
        date_obj = parse_date(date_str)
        if date_obj:
            date_str = format_date(date_obj)
        else:
            # If parsing fails, assume it's already in YYYYMMDD format
            date_str = date_str.replace("-", "")
        
        # ESPN API accepts dates as a query parameter
        params = {"dates": date_str}
        
        # Add groups parameter if provided (convert string to ID if needed)
        if groups is not None:
            group_id = CBBConferences.get_id(groups)
            if group_id is not None:
                params["groups"] = group_id
            else:
                raise ValueError(f"Invalid conference name or ID: {groups}")
        
        data = self._get_scoreboard(params=params)
        
        if status:
            data['games'] = [g for g in data['games'] if g['status'] == status]
        
        return data
    
    def final_games(self, groups = None) -> Dict[str, Any]:
        """
        Get only completed games from today.
        
        This is a convenience method equivalent to today(status='final').
        
        Args:
            groups: Optional conference/group ID or name to filter by specific conference.
        
        Returns:
            Dictionary with only completed games from today
            
        Example:
            >>> finals = cbb.final_games()
            >>> acc_finals = cbb.final_games(groups='ACC')
            >>> for game in finals['games']:
            ...     print(f"{game['away_team']['name']} {game['away_team']['score']} @ "
            ...           f"{game['home_team']['name']} {game['home_team']['score']}")
        """
        return self.today(status='final', groups=groups)
    
    def live_games(self, groups = None) -> Dict[str, Any]:
        """
        Get only in-progress games from today.
        
        This is a convenience method equivalent to today(status='in_progress').
        Live games include period and clock information.
        
        Args:
            groups: Optional conference/group ID or name to filter by specific conference.
        
        Returns:
            Dictionary with only games currently being played today
            
        Example:
            >>> live = cbb.live_games()
            >>> big_ten_live = cbb.live_games(groups='Big Ten')
            >>> for game in live['games']:
            ...     gt = game['game_time']
            ...     print(f"{game['away_team']['name']} vs {game['home_team']['name']}")
            ...     print(f"  {gt['period']} - {gt['clock']}")
        """
        return self.today(status='in_progress', groups=groups)
    
    def upcoming_games(self, groups = None) -> Dict[str, Any]:
        """
        Get only scheduled games from today.
        
        This is a convenience method equivalent to today(status='scheduled').
        Upcoming games include start_time information.
        
        Args:
            groups: Optional conference/group ID or name to filter by specific conference.
        
        Returns:
            Dictionary with only games that haven't started yet today
            
        Example:
            >>> upcoming = cbb.upcoming_games()
            >>> sec_upcoming = cbb.upcoming_games(groups='SEC')
            >>> for game in upcoming['games']:
            ...     print(f"{game['away_team']['name']} @ {game['home_team']['name']}")
            ...     print(f"  Tip-off: {game['start_time']}")
        """
        return self.today(status='scheduled', groups=groups)


# Conference/Group ID constants for easy reference
class CBBConferences:
    """
    College Basketball conference/group IDs for filtering games.
    
    Use these constants with the groups parameter in CBB methods.
    Can also pass conference names as strings.
    
    Example:
        >>> from espn_scores import cbb
        >>> from espn_scores.sports.cbb import CBBConferences
        >>> 
        >>> # Get SEC games using constant
        >>> sec_games = cbb.today(groups=CBBConferences.SEC)
        >>> 
        >>> # Or use string name (case-insensitive)
        >>> sec_games = cbb.today(groups='SEC')
        >>> acc_games = cbb.today(groups='acc')
    """
    # Power Conferences
    ACC = 2
    BIG_12 = 8
    BIG_TEN = 7
    SEC = 23
    BIG_EAST = 4
    
    # Other Major Conferences
    AMERICAN = 62
    ATLANTIC_10 = 3
    CONFERENCE_USA = 11
    MAC = 15
    MOUNTAIN_WEST = 17
    PAC_12 = 21  # Historical
    SUN_BELT = 37
    WEST_COAST = 18
    
    # Mapping of conference names to IDs (case-insensitive lookup)
    _NAME_TO_ID = {
        'acc': 2,
        'atlantic coast': 2,
        'atlantic coast conference': 2,
        'big east': 4,
        'bigeast': 4,
        'big 12': 8,
        'big12': 8,
        'big 10': 7,
        'big10': 7,
        'big ten': 7,
        'bigten': 7,
        'sec': 23,
        'southeastern': 23,
        'southeastern conference': 23,
        'american': 62,
        'aac': 62,
        'american athletic': 62,
        'atlantic 10': 3,
        'a10': 3,
        'a-10': 3,
        'cusa': 11,
        'c-usa': 11,
        'conference usa': 11,
        'mac': 15,
        'mid-american': 15,
        'mid american': 15,
        'mountain west': 17,
        'mwc': 17,
        'pac 12': 21,
        'pac-12': 21,
        'sun belt': 37,
        'sunbelt': 37,
        'wcc': 18,
        'west coast': 18,
        'west coast conference': 18,
    }
    
    @classmethod
    def get_id(cls, name_or_id):
        """
        Get conference ID from name or ID.
        
        Args:
            name_or_id: Conference name (string) or ID (int)
            
        Returns:
            Conference ID (int) or None if not found
            
        Example:
            >>> CBBConferences.get_id('SEC')
            8
            >>> CBBConferences.get_id('big ten')
            5
            >>> CBBConferences.get_id(5)
            5
        """
        # If already an int, return it
        if isinstance(name_or_id, int):
            return name_or_id
        
        # If string, lookup in mapping
        if isinstance(name_or_id, str):
            return cls._NAME_TO_ID.get(name_or_id.lower().strip())
        
        return None


# Create a singleton instance for easy importing
cbb = CBB()
