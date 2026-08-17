from pickle import load
from itertools import islice

with open('moveDatabase.pkl', 'rb') as file:
    database = load(file)
print(f'Complete entries: {dict(islice(database.entries.items(), 200))}')
print(f'Working set: {dict(islice(database.presentWorkingSet.items(), 200))}')
print(f'Focus: {dict(islice(database.focus.items(), 2000))}')
print(database.entries[''].losingMoves)
print(database.entries['0'].losingMoves)
print(database.entries['00'].losingMoves)
print(database.entries['001'].losingMoves)
print(database.entries['0010'].losingMoves)
print(database.entries['00102'].losingMoves)
print(database.entries['001020'].losingMoves)
#print(database.entries['0010203'].losingMoves)print(database.entries[''].losingMoves)
print(database.entries['0'].winningMoves)
print(database.entries['00'].winningMoves)
print(database.entries['001'].winningMoves)
print(database.entries['0010'].winningMoves)
print(database.entries['00102'].winningMoves)
print(database.entries['001020'].winningMoves)
