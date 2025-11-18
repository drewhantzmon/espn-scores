"""NHL-specific implementation for ESPN Scores."""

from typing import Dict, Any, Optional
from datetime import datetime
from espn_scores.sports.base import BaseSport
from espn_scores.utils.helpers import format_date, parse_date


class NHL(BaseSport):
    """
    NHL-specific implementation of the ESPN Scores API.
    
    This class provides methods to fetch NHL game scores and information from
    ESPN's API in a clean, minimal format. NHL uses date-based queries like NBA.
    
    Example:
        >>> from espn_scores import nhl
        >>> 
        >>> # Get today's games
        >>> games = nhl.today()
        >>> print(f"Games today: {len(games['games'])}")
        >>> 
        >>> # Get games from specific date
        >>> nov_17 = nhl.date("20251117")
        >>> 
        >>> # Get only final games
        >>> finals = nhl.final_games()
    """
    
    @property
    def sport_path(self) -> str:
        """Return the ESPN API path for NHL."""
        return "hockey/nhl"
    
    @property
    def league_name(self) -> str:
        """Return the league name."""
        return "NHL"
    
    def today(self, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Get scores for today's NHL games.
        
        Args:
            status: Optional filter by game status. Valid values:
                   - 'final': Only completed games
                   - 'in_progress': Only live games
                   - 'scheduled': Only upcoming games
                   - None: All games (default)
            
        Returns:
            Dictionary with minimal game data:
            {
                "sport": "NHL",
                "date": "2025-11-18",
                "season": 2026,
                "games": [...]
            }
            
        Example:
            >>> games = nhl.today()
            >>> finals = nhl.today(status='final')
        """
        today_date = datetime.now().strftime("%Y%m%d")
        return self.date(today_date, status=status)
    
    def date(self, date_str: str, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Get scores for NHL games on a specific date.
        
        Args:
            date_str: Date in YYYYMMDD or YYYY-MM-DD format
            status: Optional filter by game status ('final', 'in_progress', 'scheduled')
            
        Returns:
            Dictionary with minimal game data for the specified date
            
        Example:
            >>> nov_17 = nhl.date("20251117")
            >>> nov_17_alt = nhl.date("2025-11-17")
            >>> finals = nhl.date("20251117", status='final')
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
        data = self._get_scoreboard(params=params)
        
        if status:
            data['games'] = [g for g in data['games'] if g['status'] == status]
        
        return data
    
    def final_games(self) -> Dict[str, Any]:
        """
        Get only completed games from today.
        
        This is a convenience method equivalent to today(status='final').
        
        Returns:
            Dictionary with only completed games from today
            
        Example:
            >>> finals = nhl.final_games()
            >>> for game in finals['games']:
            ...     print(f"{game['away_team']['name']} {game['away_team']['score']} @ "
            ...           f"{game['home_team']['name']} {game['home_team']['score']}")
        """
        return self.today(status='final')
    
    def live_games(self) -> Dict[str, Any]:
        """
        Get only in-progress games from today.
        
        This is a convenience method equivalent to today(status='in_progress').
        Live games include period and clock information.
        
        Returns:
            Dictionary with only games currently being played today
            
        Example:
            >>> live = nhl.live_games()
            >>> for game in live['games']:
            ...     gt = game['game_time']
            ...     print(f"{game['away_team']['name']} vs {game['home_team']['name']}")
            ...     print(f"  Period {gt['period']} - {gt['clock']}")
        """
        return self.today(status='in_progress')
    
    def upcoming_games(self) -> Dict[str, Any]:
        """
        Get only scheduled games from today.
        
        This is a convenience method equivalent to today(status='scheduled').
        Upcoming games include start_time information.
        
        Returns:
            Dictionary with only games that haven't started yet today
            
        Example:
            >>> upcoming = nhl.upcoming_games()
            >>> for game in upcoming['games']:
            ...     print(f"{game['away_team']['name']} @ {game['home_team']['name']}")
            ...     print(f"  Puck drop: {game['start_time']}")
        """
        return self.today(status='scheduled')


# Create a singleton instance for easy importing
nhl = NHL()
