import csv
from mimetypes import init
import os
from collections import namedtuple
from datetime import date, datetime

from django.contrib.staticfiles.storage import staticfiles_storage

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


Record = namedtuple("Team", "code wins lossses")
Standings = list[Record]


def standings(date: date, league: str = 'AL') -> Standings:
    """ 
    Returns a list of team records for specified league as of a specified date.
    """
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
    standings = [Record(team, wins[team], losses[team]) for team in wins]
    return standings


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


def initialize():
    if not gamelog:
        initialize_team_names()
        initialize_team_logos()
        initialize_gamelog()


def initialize_gamelog():
    global gamelog

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
