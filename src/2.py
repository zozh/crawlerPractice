import json

names = {'joker': 1, 'joe': 2, 'nacy': 3, 'timi': 4}
filename = 'names.json'
with open(filename, 'w') as file_obj:
    json.dump(names, file_obj)
