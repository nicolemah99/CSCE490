import csv
import os
from collections import namedtuple
from datetime import date, datetime

from django.contrib.staticfiles.storage import staticfiles_storage

# TODO: follow django best practices
DIR = 'baseball/static/'

TEAMS_FILENAME = os.path.join(DIR, 'baseball/teams.csv')
TEAM_CODE = 'code'
TEAM_NAME = 'name'

GAMELOG_FILENAME = os.path.join(DIR, 'baseball/games.csv')
GAMELOG_DATE = 'Date'
GAMELOG_LEAGUE = 'Visiting Team League'
GAMELOG_VISITING_TEAM = 'Visiting Team'
GAMELOG_VISITING_TEAM_SCORE = 'Visitors Score'
GAMELOG_HOME_TEAM = 'Home Team'
GAMELOG_HOME_TEAM_SCORE = 'Home Score'

Game = namedtuple("Game",
                  "date league visitors visitors_score home home_score")
# unsorted list of Game nametuples
gamelog = None

# maps team code to team name, e.g., "BOS" to "Boston Red Sox"
teamcodes = None

Record = namedtuple("Team", "code wins lossses")
Standings = list[Record]

def standings(date: date, league: str = 'AL') -> Standings:
    """ 
    Returns a list of team records for specified league as of a specified date.
    """
    if not gamelog:
        initialize_teamcodes()
        initialize_gamelog()

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


def teamname(teamcode):
    """ 
    Given a team code (e.g., BOS), returns the associate name (e.g., Boston Red Sox). 
    """
    return teamcodes.get(teamcode, "Unknown")


def initialize_gamelog():
    global gamelog

    gamelog = []
    with open(GAMELOG_FILENAME) as incsvfile:
        reader = csv.DictReader(incsvfile)
        for row in reader:
            d = datetime.strptime(row[GAMELOG_DATE], "%Y%m%d").date()
            game = Game(d, row[GAMELOG_LEAGUE], row[GAMELOG_VISITING_TEAM],
                        int(row[GAMELOG_VISITING_TEAM_SCORE]), row[GAMELOG_HOME_TEAM],
                        int(row[GAMELOG_HOME_TEAM_SCORE]))
            gamelog.append(game)


def initialize_teamcodes():
    global teamcodes

    teamcodes = {}
    with open(TEAMS_FILENAME) as incsvfile:
        reader = csv.DictReader(incsvfile)
        for row in reader:
            teamcodes[row[TEAM_CODE]] = row[TEAM_NAME]


if __name__ == '__main__':
    initialize_teamcodes()
    print(teamname('BOS'))
    print(teamname('CIN'))

    initialize_gamelog()
    for d in ['1967-04-30', '1967-07-04', '1967-10-15']:
        print(standings(date.fromisoformat(d), 'AL'))
        print(standings(date.fromisoformat(d), 'NL'))
        print(standings(date.fromisoformat(d), 'xx'))
