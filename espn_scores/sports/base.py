"""Base class for all sport-specific implementations."""

from typing import Dict, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod
from espn_scores.core.client import ESPNClient
from espn_scores.utils.parsers import parse_espn_response


class BaseSport(ABC):
    """
    Abstract base class for sport-specific implementations.
    Each sport (NFL, NBA, MLB, etc.) should inherit from this class.
    """
    
    def __init__(self):
        """Initialize the sport with an ESPN API client."""
        self.client = ESPNClient()
    
    @property
    @abstractmethod
    def sport_path(self) -> str:
        """
        Return the ESPN API path for this sport.
        E.g., "football/nfl", "basketball/nba", etc.
        """
        pass
    
    @property
    @abstractmethod
    def league_name(self) -> str:
        """Return the league name (e.g., "NFL", "NBA")."""
        pass
    
    def _get_scoreboard(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fetch scoreboard data from ESPN API.
        
        Args:
            params: Query parameters for the API request
            
        Returns:
            Parsed scoreboard data as dictionary
        """
        endpoint = f"{self.sport_path}/scoreboard"
        raw_data = self.client.get(endpoint, params=params)
        return parse_espn_response(raw_data, self.league_name)
    
    def today(self) -> Dict[str, Any]:
        """
        Get today's games.
        
        Returns:
            Dictionary with game data
        """
        return self._get_scoreboard()
    
    def date(self, date: str) -> Dict[str, Any]:
        """
        Get games for a specific date.
        
        Args:
            date: Date string in YYYYMMDD format
            
        Returns:
            Dictionary with game data
        """
        return self._get_scoreboard(params={"dates": date})
