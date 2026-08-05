from pickle import load
from itertools import islice

with open('moveDatabase.pkl', 'rb') as file:
    database = load(file)
print(f'Complete entries: {dict(islice(database.entries.items(), 2000))}')
print(f'Working set: {dict(islice(database.presentWorkingSet.items(), 2000))}')
print(f'Focus: {dict(islice(database.focus.items(), 2000))}')
