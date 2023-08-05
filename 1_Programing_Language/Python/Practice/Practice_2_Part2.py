import os, sys, json
os.chdir(sys.path[0])

filename = 'test.json'
with open(filename) as f:
    username = json.load(f)
    print(f"Welcome back, {username}!")
