"""Sports-specific implementations."""

from espn_scores.sports.nfl import nfl
from espn_scores.sports.nba import nba
from espn_scores.sports.nhl import nhl
from espn_scores.sports.cfb import cfb
from espn_scores.sports.cbb import cbb

__all__ = ["nfl", "nba", "nhl", "cfb", "cbb"]
