import os, sys
from os import path

os.chdir(sys.path[0])

file_path = "candidate_list.txt"


n = int(input("please input the numebr of candidates: "))
candidates = (input().split(' '))

statistics = [0 for i in range(n)]
num_votes = int(input("please input the number of votes: "))
votes = input().split(" ")
invalid = 0
for vote in votes:
    if vote in candidates:
        statistics[candidates.index(vote)] += 1
    else:
        invalid += 1


with open(file_path, "+w") as file:
    for index, candidate in enumerate(candidates):
        file.writelines(f"{candidate} : {statistics[index]}\n")

    file.writelines(f"Invalid : {invalid}")

    file.seek(0)
    contents = file.read()
    print(contents)

file.close()
os.remove(file_path)
