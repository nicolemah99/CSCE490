import csv
import os
from collections import namedtuple
from datetime import date, datetime


# TODO: follow django best practices
DIR = 'baseball/static/'

TEAMS_FILENAME = 'baseball/teams.csv'
TEAM_CODE = 'code'
TEAM_NAME = 'name'

GAMELOG_FILENAME = 'baseball/games.csv'
GAMELOG_DATE = 'Date'
GAMELOG_LEAGUE = 'Visiting Team League'
GAMELOG_VISITING_TEAM = 'Visiting Team'
GAMELOG_VISITING_TEAM_SCORE = 'Visitors Score'
GAMELOG_HOME_TEAM = 'Home Team'
GAMELOG_HOME_TEAM_SCORE = 'Home Score'

LOGO_FILENAME = 'baseball/logos.csv'
LOGO_TEAM_CODE = 'team'
LOGO_URL = 'logo-url'


def path(filename):
    return os.path.join(DIR, filename)


Game = namedtuple("Game",
                  "date league visitors visitors_score home home_score")
# unsorted list of Game namedtuples
gamelog = None

# maps team code to team name, e.g., "BOS" to "Boston Red Sox"
team_names = None

# maps team code to team logo, e.g., "BOS" to "https://content.sportslogos.net/logos/53/53/thumbs/c0whfsa9j0vbs079opk2s05lx.gif"
team_logos = None

Record = namedtuple("Team", "code wins losses gb")
# list of teams records, first place to last place
Standings = list[Record]

def standings(date: date, league: str = 'AL') -> Standings:
    """ 
    Returns a list of team records for specified league as of a specified date.
    The team are in sorted order, from 1st place to last place. 
    """
    def gb(team, leader):
        return ((wins.get(leader, 0)-wins.get(team, 0)) + (losses.get(team, 0)-losses.get(leader, 0)))/2
    initialize()
    wins = {}
    losses = {}
    for g in gamelog:
        if g.league == league and g.date <= date:
            if g.home_score > g.visitors_score:
                winner, loser = g.home, g.visitors
            else:
                winner, loser = g.visitors, g.home
            wins.update({winner: wins.get(winner, 0) + 1})
            losses.update({loser: losses.get(loser, 0) + 1})
    if len(wins)+len(losses) == 0:
        return []
    codes = set(wins.keys())
    for k in losses.keys():
        codes.add(k)
    leader = max(wins, key=lambda k: wins.get(k, 0)/(wins.get(k, 0)+losses.get(k, 0)))
    unsorted_standings = [Record(team, wins.get(team, 0), losses.get(team, 0), gb(team, leader)) for team in codes]
    return sorted(unsorted_standings, key=lambda s: s.gb)


ExtendedRecord = namedtuple("ExtendedRecord",
                            "code name logo_url wins losses pct_str gb")

def extend_record(r: Record) -> ExtendedRecord:
    """"
    Retunrs the ExtendedRecord version of the Record: converts code to team name, logo; formats winning pct. 
    """
    return ExtendedRecord(r.code, team_name(r.code), team_logo(r.code), r.wins, r.losses, format_pct(r.wins, r.losses), r.gb)


def format_pct(wins, losses):
    """
    Returns winning percentage, nicely formatted (i.e., .ddd or 1.000)
    """
    pct = wins/(wins+losses) if wins + losses > 0 else 0
    pct_str = f'{pct:0.3f}'
    if pct_str[0] == '0':
        pct_str = pct_str[1:]
    return pct_str


def team_name(code):
    """ 
    Given a team code (e.g., BOS), returns the associated name (e.g., Boston Red Sox)
    """
    initialize()
    return team_names.get(code, "Unknown")


def team_logo(code):
    """ 
    Given a team code (e.g., BOS), returns the URL of the associated logo
    """
    initialize()
    return team_logos.get(code, "Unknown")


def end_of_season():
    """
    Returns the date of the last game of the season
    """
    initialize()
    return max(gamelog, key=lambda g: g.date).date


def start_of_season():
    """
    Returns the date of the first game of the season
    """
    initialize()
    return min(gamelog, key=lambda g: g.date).date


def initialize():
    if not gamelog:
        initialize_team_names()
        initialize_team_logos()
        initialize_gamelog()


def initialize_gamelog():
    global gamelog, first_game, last_game

    gamelog = []
    with open(path(GAMELOG_FILENAME)) as incsvfile:
        reader = csv.DictReader(incsvfile)
        for row in reader:
            d = datetime.strptime(row[GAMELOG_DATE], "%Y%m%d").date()
            game = Game(d, row[GAMELOG_LEAGUE], row[GAMELOG_VISITING_TEAM],
                        int(row[GAMELOG_VISITING_TEAM_SCORE]
                            ), row[GAMELOG_HOME_TEAM],
                        int(row[GAMELOG_HOME_TEAM_SCORE]))
            gamelog.append(game)


def initialize_team_logos():
    global team_logos

    team_logos = {}
    with open(path(LOGO_FILENAME)) as incsvfile:
        reader = csv.DictReader(incsvfile)
        for row in reader:
            team_logos[row[LOGO_TEAM_CODE]] = row[LOGO_URL]


def initialize_team_names():
    global team_names

    team_names = {}
    with open(path(TEAMS_FILENAME)) as incsvfile:
        reader = csv.DictReader(incsvfile)
        for row in reader:
            team_names[row[TEAM_CODE]] = row[TEAM_NAME]


if __name__ == '__main__':
    initialize_team_names()
    initialize_team_logos()

    print(team_name('BOS'))
    print(team_name('CIN'))
    print(team_logo('BOS'))
    print(team_logo('CIN'))

    initialize_gamelog()
    for d in ['1967-04-30', '1967-07-04', '1967-10-15']:
        print(standings(date.fromisoformat(d), 'AL'))
        print(standings(date.fromisoformat(d), 'NL'))
        print(standings(date.fromisoformat(d), 'xx'))
