"""NFL-specific implementation for ESPN Scores."""

from typing import Dict, Any, Optional
from espn_scores.sports.base import BaseSport
from espn_scores.core.exceptions import InvalidWeekException


class NFL(BaseSport):
    """
    NFL-specific implementation of the ESPN Scores API.
    
    This class provides methods to fetch NFL game scores and information from
    ESPN's API in a clean, minimal format. Supports preseason, regular season,
    and postseason games.
    
    Example:
        >>> from espn_scores import nfl
        >>> 
        >>> # Get current week games
        >>> games = nfl.current_week()
        >>> print(f"Week {games['week']}: {len(games['games'])} games")
        >>> 
        >>> # Get only final games
        >>> finals = nfl.final_games()
        >>> 
        >>> # Get specific week
        >>> week_10 = nfl.week(10, status='final')
        >>> 
        >>> # Get preseason games
        >>> preseason = nfl.preseason(3)
        >>> 
        >>> # Get playoff games
        >>> playoffs = nfl.playoffs(1)  # Wild Card
    """
    
    @property
    def sport_path(self) -> str:
        """Return the ESPN API path for NFL."""
        return "football/nfl"
    
    @property
    def league_name(self) -> str:
        """Return the league name."""
        return "NFL"
    
    def current_week(self, status: Optional[str] = None, season_type: int = 2) -> Dict[str, Any]:
        """
        Get scores for the current NFL week.
        
        Args:
            status: Optional filter by game status. Valid values:
                   - 'final': Only completed games
                   - 'in_progress': Only live games
                   - 'scheduled': Only upcoming games
                   - None: All games (default)
            season_type: Season type (1=Preseason, 2=Regular Season, 3=Postseason). Default: 2
            
        Returns:
            Dictionary with minimal game data:
            {
                "sport": "NFL",
                "week": 11,
                "season": 2025,
                "games": [...]
            }
            
        Example:
            >>> games = nfl.current_week()
            >>> finals = nfl.current_week(status='final')
            >>> preseason = nfl.current_week(season_type=1)
        """
        params = {"seasontype": season_type} if season_type != 2 else {}
        data = self._get_scoreboard(params=params)
        
        if status:
            data['games'] = [g for g in data['games'] if g['status'] == status]
        
        return data
    
    def week(self, week_number: int, status: Optional[str] = None, season_type: int = 2) -> Dict[str, Any]:
        """
        Get scores for a specific NFL week.
        
        Args:
            week_number: The week/round number
                        - Preseason (season_type=1): 1-4
                        - Regular Season (season_type=2): 1-18
                        - Postseason (season_type=3): 1-5
            status: Optional filter by game status ('final', 'in_progress', 'scheduled')
            season_type: Season type (1=Preseason, 2=Regular Season, 3=Postseason). Default: 2
            
        Returns:
            Dictionary with minimal game data for the specified week
            
        Raises:
            InvalidWeekException: If week number is out of valid range for the season type
            
        Example:
            >>> week_10 = nfl.week(10)
            >>> week_10_finals = nfl.week(10, status='final')
            >>> preseason_week_3 = nfl.week(3, season_type=1)
            >>> wild_card = nfl.week(1, season_type=3)
        """
        # Validate week number based on season type
        max_weeks = {1: 4, 2: 18, 3: 5}
        max_week = max_weeks.get(season_type, 18)
        
        if not 1 <= week_number <= max_week:
            season_names = {1: "Preseason", 2: "Regular Season", 3: "Postseason"}
            season_name = season_names.get(season_type, "Regular Season")
            raise InvalidWeekException(
                f"Invalid week number: {week_number}. {season_name} must be between 1 and {max_week}."
            )
        
        # ESPN API accepts week and seasontype as query parameters
        params = {"week": week_number, "seasontype": season_type}
        data = self._get_scoreboard(params=params)
        
        if status:
            data['games'] = [g for g in data['games'] if g['status'] == status]
        
        return data
    
    def final_games(self) -> Dict[str, Any]:
        """
        Get only completed games from the current week.
        
        This is a convenience method equivalent to current_week(status='final').
        Note: Only returns games from the current week. For other weeks, use
        week(week_number, status='final').
        
        Returns:
            Dictionary with only completed games from the current week
            
        Example:
            >>> finals = nfl.final_games()
            >>> for game in finals['games']:
            ...     print(f"{game['away_team']['name']} {game['away_team']['score']} @ "
            ...           f"{game['home_team']['name']} {game['home_team']['score']}")
        """
        return self.current_week(status='final')
    
    def live_games(self) -> Dict[str, Any]:
        """
        Get only in-progress games from the current week.
        
        This is a convenience method equivalent to current_week(status='in_progress').
        Live games include quarter and time remaining information.
        Note: Only returns games from the current week. For other weeks, use
        week(week_number, status='in_progress').
        
        Returns:
            Dictionary with only games currently being played in the current week
            
        Example:
            >>> live = nfl.live_games()
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
        Note: Only returns games from the current week. For other weeks, use
        week(week_number, status='scheduled').
        
        Returns:
            Dictionary with only games that haven't started yet in the current week
            
        Example:
            >>> upcoming = nfl.upcoming_games()
            >>> for game in upcoming['games']:
            ...     print(f"{game['away_team']['name']} @ {game['home_team']['name']}")
            ...     print(f"  Kickoff: {game['start_time']}")
        """
        return self.current_week(status='scheduled')
    
    def preseason(self, week_number: Optional[int] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Get preseason games.
        
        This is a convenience method for accessing preseason games (season_type=1).
        Preseason has 4 weeks: Hall of Fame Weekend and Weeks 1-3.
        
        Args:
            week_number: Optional preseason week (1-4). If None, returns current preseason week.
            status: Optional filter by game status ('final', 'in_progress', 'scheduled')
            
        Returns:
            Dictionary with preseason game data
            
        Raises:
            InvalidWeekException: If week_number is not between 1 and 4
            
        Example:
            >>> preseason = nfl.preseason()  # Current preseason week
            >>> week_3 = nfl.preseason(3)  # Preseason week 3
            >>> week_3_finals = nfl.preseason(3, status='final')
        """
        if week_number is None:
            return self.current_week(status=status, season_type=1)
        return self.week(week_number, status=status, season_type=1)
    
    def playoffs(self, round_number: Optional[int] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Get playoff games.
        
        This is a convenience method for accessing playoff games (season_type=3).
        Postseason has 5 rounds:
        - Round 1: Wild Card
        - Round 2: Divisional Round
        - Round 3: Conference Championship
        - Round 4: Pro Bowl
        - Round 5: Super Bowl
        
        Args:
            round_number: Optional playoff round (1-5). If None, returns current playoff round.
            status: Optional filter by game status ('final', 'in_progress', 'scheduled')
            
        Returns:
            Dictionary with playoff game data
            
        Raises:
            InvalidWeekException: If round_number is not between 1 and 5
            
        Example:
            >>> playoffs = nfl.playoffs()  # Current playoff round
            >>> wild_card = nfl.playoffs(1)  # Wild Card round
            >>> super_bowl = nfl.playoffs(5)  # Super Bowl
            >>> super_bowl_final = nfl.playoffs(5, status='final')
        """
        if round_number is None:
            return self.current_week(status=status, season_type=3)
        return self.week(round_number, status=status, season_type=3)


# Create a singleton instance for easy importing
nfl = NFL()
