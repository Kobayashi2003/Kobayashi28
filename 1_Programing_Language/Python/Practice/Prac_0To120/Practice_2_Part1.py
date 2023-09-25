import os, sys, json

os.chdir(sys.path[0])

username = input("What is your name? ")
filename = 'test.json'
with open(filename, 'w') as f:
    json.dump(username, f)
    print(f"We'll remember you when you come back, {username}!")
