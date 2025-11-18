"""
ESPN Scores - A simple Python package for interacting with ESPN Scoreboard API

This package provides a clean, minimal interface to fetch live sports scores
from ESPN's API. Currently supports NFL, NBA, NHL, CFB, and CBB.

Basic Usage - NFL:
    >>> from espn_scores import nfl
    >>> 
    >>> # Get all games from current week
    >>> games = nfl.current_week()
    >>> 
    >>> # Get only final games
    >>> finals = nfl.final_games()
    >>> 
    >>> # Get specific week
    >>> week_10 = nfl.week(10)
    >>> 
    >>> # Get preseason/playoff games
    >>> preseason = nfl.preseason(3)
    >>> playoffs = nfl.playoffs(1)

Basic Usage - NBA:
    >>> from espn_scores import nba
    >>> 
    >>> # Get today's games
    >>> games = nba.today()
    >>> 
    >>> # Get games from specific date
    >>> nov_17 = nba.date("20251117")
    >>> 
    >>> # Get only final games
    >>> finals = nba.final_games()

Basic Usage - NHL:
    >>> from espn_scores import nhl
    >>> 
    >>> # Get today's games
    >>> games = nhl.today()
    >>> 
    >>> # Get games from specific date
    >>> nov_17 = nhl.date("20251117")
    >>> 
    >>> # Get only final games
    >>> finals = nhl.final_games()

Basic Usage - CFB:
    >>> from espn_scores import cfb, Conferences
    >>> 
    >>> # Get current week's games
    >>> games = cfb.current_week()
    >>> 
    >>> # Get only final games
    >>> finals = cfb.final_games()
    >>> 
    >>> # Get specific week
    >>> week_1 = cfb.week(1)
    >>> 
    >>> # Get postseason games
    >>> bowls = cfb.postseason()
    >>> 
    >>> # Filter by conference
    >>> sec_games = cfb.current_week(groups='SEC')
    >>> big_ten = cfb.week(5, groups='Big Ten')

Basic Usage - CBB:
    >>> from espn_scores import cbb, CBBConferences
    >>> 
    >>> # Get today's games
    >>> games = cbb.today()
    >>> 
    >>> # Get games from specific date
    >>> nov_17 = cbb.date("20251117")
    >>> 
    >>> # Get only final games
    >>> finals = cbb.final_games()
    >>> 
    >>> # Filter by conference
    >>> acc_games = cbb.today(groups='ACC')
    >>> big_east = cbb.today(groups='Big East')

Response Format:
    All methods return a dictionary with minimal game information:
    
    NFL:
    {
        "sport": "NFL",
        "week": 11,
        "season": 2025,
        "games": [...]
    }
    
    NBA/NHL:
    {
        "sport": "NBA",
        "date": "2025-11-17",
        "season": 2026,
        "games": [...]
    }
"""

from espn_scores.__version__ import __version__
from espn_scores.sports import nfl, nba, nhl, cfb, cbb
from espn_scores.sports.cfb import Conferences
from espn_scores.sports.cbb import CBBConferences

__all__ = ["nfl", "nba", "nhl", "cfb", "cbb", "Conferences", "CBBConferences", "__version__"]
