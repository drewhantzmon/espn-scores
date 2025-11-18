# ESPN Scores

A simple Python package for fetching live sports scores from the ESPN API. Currently supports NFL, NBA, NHL, College Football (CFB), and College Basketball (CBB) with minimal, easy-to-use interface.

## Features

- NFL support (weeks, preseason, playoffs)
- NBA support (date-based queries)
- NHL support (date-based queries)
- CFB support (weeks, postseason, conference filtering)
- CBB support (date-based queries, conference filtering)
- Simple dictionary-based responses
- Real-time data from ESPN
- Filter by game status (final, live, upcoming)

## Installation

```bash
pip install espn-scores
```

## Quick Start

### NFL (Week-based)
```python
from espn_scores import nfl

# Get current week's scores
scores = nfl.current_week()

# Get only final games
final_games = nfl.final_games()

# Get a specific week
week_10 = nfl.week(10)

# Get preseason/playoff games
preseason = nfl.preseason(3)
playoffs = nfl.playoffs(1)  # Wild Card
```

### NBA (Date-based)
```python
from espn_scores import nba

# Get today's games
games = nba.today()

# Get games from a specific date
yesterday = nba.date("20251117")  # or "2025-11-17"

# Get only final games from today
finals = nba.final_games()
```

### NHL (Date-based)
```python
from espn_scores import nhl

# Get today's games
games = nhl.today()

# Get games from a specific date
yesterday = nhl.date("20251117")  # or "2025-11-17"

# Get only final games from today
finals = nhl.final_games()
```

### CFB (Week-based)
```python
from espn_scores import cfb

# Get current week's scores
scores = cfb.current_week()

# Get only final games
final_games = cfb.final_games()

# Get a specific week
week_1 = cfb.week(1)

# Get postseason games (bowl games + playoffs)
bowls = cfb.postseason()

# Filter by conference using string names (case-insensitive)
sec_games = cfb.current_week(groups='SEC')
acc_games = cfb.current_week(groups='acc')
big_ten = cfb.week(5, groups='Big Ten')
```

### CBB (Date-based)
```python
from espn_scores import cbb

# Get today's games
games = cbb.today()

# Get games from a specific date
yesterday = cbb.date("20251117")  # or "2025-11-17"

# Get only final games from today
finals = cbb.final_games()

# Filter by conference using string names (case-insensitive)
acc_games = cbb.today(groups='ACC')
big_ten = cbb.date("20251117", groups='Big Ten')
sec_finals = cbb.final_games(groups='SEC')
```

## Response Format

All methods return a dictionary with minimal game data:

```python
{
  "sport": "NFL",
  "week": 11,
  "season": 2025,
  "games": [
    {
      "id": "401772945",
      "status": "final",  # or "in_progress" or "scheduled"
      "away_team": {"name": "Jets", "score": 14},
      "home_team": {"name": "Patriots", "score": 27}
    }
  ]
}
```

Live games include `game_time` with quarter/period and clock. Scheduled games include `start_time`.

## API Reference

### NFL

| Method | Description |
|--------|-------------|
| `nfl.current_week(status=None, season_type=2)` | Get current week games |
| `nfl.week(week_number, status=None, season_type=2)` | Get specific week (1-18 regular, 1-4 preseason, 1-5 playoffs) |
| `nfl.preseason(week_number=None, status=None)` | Get preseason games (weeks 1-4) |
| `nfl.playoffs(round_number=None, status=None)` | Get playoff games (rounds 1-5) |
| `nfl.final_games()` | Current week completed games |
| `nfl.live_games()` | Current week in-progress games |
| `nfl.upcoming_games()` | Current week scheduled games |

**Season Types:** `1` = Preseason, `2` = Regular Season, `3` = Postseason

### NBA

| Method | Description |
|--------|-------------|
| `nba.today(status=None)` | Get today's games |
| `nba.date(date_str, status=None)` | Get games by date (YYYYMMDD or YYYY-MM-DD) |
| `nba.final_games()` | Today's completed games |
| `nba.live_games()` | Today's in-progress games |
| `nba.upcoming_games()` | Today's scheduled games |

### NHL

| Method | Description |
|--------|-------------|
| `nhl.today(status=None)` | Get today's games |
| `nhl.date(date_str, status=None)` | Get games by date (YYYYMMDD or YYYY-MM-DD) |
| `nhl.final_games()` | Today's completed games |
| `nhl.live_games()` | Today's in-progress games |
| `nhl.upcoming_games()` | Today's scheduled games |

### CFB

| Method | Description |
|--------|-------------|
| `cfb.current_week(status=None, season_type=2, groups=None)` | Get current week games |
| `cfb.week(week_number, status=None, season_type=2, groups=None)` | Get specific week (1-15 regular season) |
| `cfb.postseason(week_number=None, status=None, groups=None)` | Get postseason games (bowl games + playoffs) |
| `cfb.final_games()` | Current week completed games |
| `cfb.live_games()` | Current week in-progress games |
| `cfb.upcoming_games()` | Current week scheduled games |

**Season Types:** `2` = Regular Season, `3` = Postseason

**Conference Groups:** Use `groups` parameter to filter games involving teams from a conference (string or int).
- String names (case-insensitive): `'SEC'`, `'ACC'`, `'Big Ten'`, `'Big 12'`, `'American'`, `'Sun Belt'`, etc.
- Or numeric IDs: `1`=ACC, `4`=Big 12, `5`=Big Ten, `8`=SEC
- Or constants: `Conferences.SEC`, `Conferences.BIG_TEN`, etc.
- Note: Returns ALL games involving teams from that conference (including non-conference games)

### CBB

| Method | Description |
|--------|-------------|
| `cbb.today(status=None, groups=None)` | Get today's games |
| `cbb.date(date_str, status=None, groups=None)` | Get games by date (YYYYMMDD or YYYY-MM-DD) |
| `cbb.final_games(groups=None)` | Today's completed games |
| `cbb.live_games(groups=None)` | Today's in-progress games |
| `cbb.upcoming_games(groups=None)` | Today's scheduled games |

**Conference Groups:** Use `groups` parameter to filter games involving teams from a conference (string or int).
- String names (case-insensitive): `'ACC'`, `'Big Ten'`, `'Big 12'`, `'SEC'`, `'Big East'`, `'American'`, `'A-10'`, `'WCC'`, etc.
- Or numeric IDs: `2`=ACC, `4`=Big East, `7`=Big Ten, `8`=Big 12, `23`=SEC
- Or constants: `CBBConferences.ACC`, `CBBConferences.BIG_TEN`, etc.
- Note: Returns ALL games involving teams from that conference (including non-conference games)

**Status Filters:** `'final'`, `'in_progress'`, `'scheduled'`

## Examples

```python
from espn_scores import nfl, nba, nhl, cfb, cbb

# NFL - Current week
games = nfl.current_week()
finals = nfl.final_games()

# NFL - Specific week and playoffs
week_10 = nfl.week(10, status='final')
playoffs = nfl.playoffs(1)  # Wild Card

# NBA - Today's games
games = nba.today()
finals = nba.final_games()

# NBA - Specific date
yesterday = nba.date("20251117")
finals = nba.date("2025-11-17", status='final')

# NHL - Today's games
games = nhl.today()
finals = nhl.final_games()

# NHL - Specific date
yesterday = nhl.date("20251117")
finals = nhl.date("2025-11-17", status='final')

# CFB - Current week
games = cfb.current_week()
finals = cfb.final_games()

# CFB - Specific week and postseason
week_1 = cfb.week(1, status='final')
bowls = cfb.postseason()  # Bowl games + playoffs

# CFB - Conference filtering (strings or IDs)
sec_games = cfb.current_week(groups='SEC')      # String name
acc_games = cfb.current_week(groups='acc')      # Case-insensitive
big_ten_w5 = cfb.week(5, groups='Big Ten')      # String name

# CBB - Today's games
games = cbb.today()
finals = cbb.final_games()

# CBB - Specific date
yesterday = cbb.date("20251117")
finals = cbb.date("2025-11-17", status='final')

# CBB - Conference filtering (strings or IDs)
acc_games = cbb.today(groups='ACC')             # String name
big_ten = cbb.date("20251117", groups='Big Ten') # Case-insensitive
sec_finals = cbb.final_games(groups='SEC')      # String name
```

## Requirements

- Python 3.8+
- requests
- python-dateutil

## License

MIT License

## Disclaimer

This package is not affiliated with ESPN. It uses ESPN's publicly available API.
