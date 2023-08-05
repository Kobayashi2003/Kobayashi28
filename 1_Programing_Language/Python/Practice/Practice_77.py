import os, sys

file_path = "candidates_list.txt"

n = int(input("please input the number of candidates: "))

candidates = {}
name_list = input().split(" ")
for name in name_list:
    candidates[name] = 0

votes_num = int(input("please input the number of votes: "))
votes = input().split(" ")
invalid = 0
for vote in votes:
    if vote in candidates.keys():
        candidates[vote] += 1
    else:
        invalid += 1

with open(file_path, "+w") as file:
    for key, value in candidates.items():
        file.write(f"{key} : {value}\n")
    file.write(f"Invalid : {invalid}")

    file.seek(0)
    print(file.read())

file.close()
os.remove(file_path)