"""College Football-specific implementation for ESPN Scores."""

from typing import Dict, Any, Optional
from espn_scores.sports.base import BaseSport
from espn_scores.utils.helpers import get_current_week, get_season_year, get_current_season_type


class CFB(BaseSport):
    """
    College Football-specific implementation of the ESPN Scores API.
    
    This class provides methods to fetch college football game scores and information
    from ESPN's API in a clean, minimal format. CFB uses week-based queries like NFL.
    
    Example:
        >>> from espn_scores import cfb
        >>> 
        >>> # Get current week's games
        >>> games = cfb.current_week()
        >>> print(f"Games this week: {len(games['games'])}")
        >>> 
        >>> # Get games from specific week
        >>> week_1 = cfb.week(1)
        >>> 
        >>> # Get postseason games (bowl games + playoffs)
        >>> bowls = cfb.postseason()
        >>> 
        >>> # Get only final games
        >>> finals = cfb.final_games()
    """
    
    @property
    def sport_path(self) -> str:
        """Return the ESPN API path for CFB."""
        return "football/college-football"
    
    @property
    def league_name(self) -> str:
        """Return the league name."""
        return "CFB"
    
    def current_week(self, status: Optional[str] = None, season_type: int = 2, groups = None) -> Dict[str, Any]:
        """
        Get scores for the current week of college football.
        
        Args:
            status: Optional filter by game status. Valid values:
                   - 'final': Only completed games
                   - 'in_progress': Only live games
                   - 'scheduled': Only upcoming games
                   - None: All games (default)
            season_type: Season type (2 = Regular Season, 3 = Postseason). Default is 2.
            groups: Optional conference/group ID or name to filter by specific conference.
                   Can be an int (1, 4, 5, 8) or string ('ACC', 'SEC', 'Big Ten', etc.)
                   Examples: 1=ACC, 4=Big 12, 5=Big Ten, 8=SEC, 151=American, 37=Sun Belt
                   None: Returns top ranked teams across all conferences (default)
            
        Returns:
            Dictionary with minimal game data:
            {
                "sport": "CFB",
                "week": 13,
                "season": 2025,
                "games": [...]
            }
            
        Example:
            >>> games = cfb.current_week()
            >>> finals = cfb.current_week(status='final')
            >>> sec_games = cfb.current_week(groups='SEC')  # String name
            >>> big_ten = cfb.current_week(groups=5)         # Or ID number
            >>> acc_games = cfb.current_week(groups='acc')   # Case-insensitive
        """
        current_week = get_current_week(self.sport_path)
        current_season_type = get_current_season_type(self.sport_path)
        
        # Use provided season_type or detected current season type
        season_type_to_use = season_type if season_type else current_season_type
        
        return self.week(current_week, status=status, season_type=season_type_to_use, groups=groups)
    
    def week(self, week_number: int, status: Optional[str] = None, season_type: int = 2, groups = None) -> Dict[str, Any]:
        """
        Get scores for a specific week of college football.
        
        Args:
            week_number: Week number (typically 1-15 for regular season)
            status: Optional filter by game status ('final', 'in_progress', 'scheduled')
            season_type: Season type (2 = Regular Season, 3 = Postseason). Default is 2.
            groups: Optional conference/group ID or name to filter by specific conference.
                   Can be an int (1, 4, 5, 8) or string ('ACC', 'SEC', 'Big Ten', etc.)
                   Examples: 1=ACC, 4=Big 12, 5=Big Ten, 8=SEC, 151=American, 37=Sun Belt
            
        Returns:
            Dictionary with minimal game data for the specified week
            
        Example:
            >>> week_1 = cfb.week(1)
            >>> week_13_finals = cfb.week(13, status='final')
            >>> sec_week_5 = cfb.week(5, groups='SEC')     # String name
            >>> big_ten_w1 = cfb.week(1, groups='Big Ten')  # Case-insensitive
        """
        params = {
            "week": week_number,
            "seasontype": season_type
        }
        
        # Add groups parameter if provided (convert string to ID if needed)
        if groups is not None:
            group_id = Conferences.get_id(groups)
            if group_id is not None:
                params["groups"] = group_id
            else:
                raise ValueError(f"Invalid conference name or ID: {groups}")
        
        data = self._get_scoreboard(params=params)
        
        if status:
            data['games'] = [g for g in data['games'] if g['status'] == status]
        
        return data
    
    def postseason(self, week_number: Optional[int] = None, status: Optional[str] = None, groups = None) -> Dict[str, Any]:
        """
        Get postseason games (bowl games and College Football Playoff).
        
        Args:
            week_number: Optional specific postseason week. If None, gets current postseason week.
            status: Optional filter by game status ('final', 'in_progress', 'scheduled')
            groups: Optional conference/group ID or name to filter by specific conference.
                   Can be an int or string ('ACC', 'SEC', 'Big Ten', etc.)
            
        Returns:
            Dictionary with postseason game data
            
        Example:
            >>> bowls = cfb.postseason()
            >>> cfp_finals = cfb.postseason(status='final')
        """
        if week_number is None:
            # Get current week in postseason
            week_number = get_current_week(self.sport_path)
        
        return self.week(week_number, status=status, season_type=3, groups=groups)
    
    def final_games(self) -> Dict[str, Any]:
        """
        Get only completed games from the current week.
        
        This is a convenience method equivalent to current_week(status='final').
        
        Returns:
            Dictionary with only completed games from the current week
            
        Example:
            >>> finals = cfb.final_games()
            >>> for game in finals['games']:
            ...     print(f"{game['away_team']['name']} {game['away_team']['score']} @ "
            ...           f"{game['home_team']['name']} {game['home_team']['score']}")
        """
        return self.current_week(status='final')
    
    def live_games(self) -> Dict[str, Any]:
        """
        Get only in-progress games from the current week.
        
        This is a convenience method equivalent to current_week(status='in_progress').
        Live games include quarter and time_remaining information.
        
        Returns:
            Dictionary with only games currently being played in the current week
            
        Example:
            >>> live = cfb.live_games()
            >>> for game in live['games']:
            ...     gt = game['game_time']
            ...     print(f"{game['away_team']['name']} vs {game['home_team']['name']}")
            ...     print(f"  {gt['quarter']} - {gt['time_remaining']}")
        """
        return self.current_week(status='in_progress')
    
    def upcoming_games(self) -> Dict[str, Any]:
        """
        Get only scheduled games from the current week.
        
        This is a convenience method equivalent to current_week(status='scheduled').
        Upcoming games include start_time information.
        
        Returns:
            Dictionary with only games that haven't started yet in the current week
            
        Example:
            >>> upcoming = cfb.upcoming_games()
            >>> for game in upcoming['games']:
            ...     print(f"{game['away_team']['name']} @ {game['home_team']['name']}")
            ...     print(f"  Kickoff: {game['start_time']}")
        """
        return self.current_week(status='scheduled')


# Conference/Group ID constants for easy reference
class Conferences:
    """
    College Football conference/group IDs for filtering games.
    
    Use these constants with the groups parameter in CFB methods.
    Can also pass conference names as strings.
    
    Example:
        >>> from espn_scores.sports.cfb import cfb, Conferences
        >>> 
        >>> # Get SEC games using constant
        >>> sec_games = cfb.current_week(groups=Conferences.SEC)
        >>> 
        >>> # Or use string name (case-insensitive)
        >>> sec_games = cfb.current_week(groups='SEC')
        >>> acc_games = cfb.current_week(groups='acc')
        >>> 
        >>> # Get Big Ten week 5 games
        >>> big_ten_w5 = cfb.week(5, groups='Big Ten')
    """
    # Power 4 Conferences
    ACC = 1
    BIG_12 = 4
    BIG_TEN = 5
    SEC = 8
    
    # Group of 5 Conferences
    AMERICAN = 151
    CUSA = 12  # Conference USA
    MAC = 15   # Mid-American
    MOUNTAIN_WEST = 17
    SUN_BELT = 37
    
    # FCS Conferences
    BIG_SKY = 20
    CAA = 48
    IVY_LEAGUE = 22
    MVFC = 21
    PIONEER = 28
    SWAC = 31
    
    # Mapping of conference names to IDs (case-insensitive lookup)
    _NAME_TO_ID = {
        'acc': 1,
        'atlantic coast': 1,
        'atlantic coast conference': 1,
        'big 12': 4,
        'big12': 4,
        'big 10': 5,
        'big10': 5,
        'big ten': 5,
        'bigten': 5,
        'sec': 8,
        'southeastern': 8,
        'southeastern conference': 8,
        'american': 151,
        'aac': 151,
        'american athletic': 151,
        'american athletic conference': 151,
        'cusa': 12,
        'c-usa': 12,
        'conference usa': 12,
        'mac': 15,
        'mid-american': 15,
        'mid american': 15,
        'mountain west': 17,
        'mwc': 17,
        'sun belt': 37,
        'sunbelt': 37,
        'big sky': 20,
        'caa': 48,
        'coastal athletic': 48,
        'ivy': 22,
        'ivy league': 22,
        'mvfc': 21,
        'missouri valley': 21,
        'pioneer': 28,
        'swac': 31,
        'southwestern athletic': 31,
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
            >>> Conferences.get_id('SEC')
            8
            >>> Conferences.get_id('acc')
            1
            >>> Conferences.get_id(5)
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
cfb = CFB()
