# unsorted list of tuples: date, league, visitor, vscore, home, hscore
gamelog = None 

# maps team code to team name, e.g., "BOS" to "Boston Red Sox"
teamcodes = {}

def standings(date, league='AL'):
    """ Returns standings for specified league as of a specified date. """
    if not gamelog: 
        initialize_gamelog()
        initialize_teamcodes()
    
    # unsorted list of tuples: teamcode, wins, losses
    # standings = []
    # for g in gamelog:
    #     pass
    standings = [('BOS', 92, 70), ('DET', 91, 71), ('MIN', 91, 71)]
    return standings        
    
def teamname(teamcode):
    return None

def initialize_gamelog():
    pass

def initialize_teamcodes():
    pass
    