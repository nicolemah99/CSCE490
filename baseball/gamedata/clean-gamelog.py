import csv

# https://www.retrosheet.org/boxesetc/1967/Y_1967.htm

INFIELDS = ('Date', 'NumberOfGame', 'DayOfWeek',
          'Visiting Team', 'Visiting Team League', 'Visiting Team Game #',
          'Home Team', 'Home Team League', 'Home Team Game #',
          'Visitors Score', 'Home Score')

OUTFIELDS = ('Date', 'Visiting Team League', 'Visiting Team', 'Visitors Score', 'Home Team', 'Home Score')

def process_file(filename):
    print(f"***FILE: {filename}")
    N = 0
    with open(filename, newline='') as incsvfile:
        with open('games.csv', 'w', newline='') as outcsvfile:
            writer = csv.DictWriter(outcsvfile, fieldnames=OUTFIELDS,  extrasaction='ignore')
            writer.writeheader()
            reader = csv.DictReader(incsvfile, INFIELDS)
            for row in reader:
                if row['Visiting Team League'] in ['AL', 'NL']:
                    h = int(row['Home Score'])
                    v = int(row['Visitors Score'])
                    if h != v:
                        N += 1
                        writer.writerow(row)
    print(f'Lines written: {N}')



python