import json
import os, sys

# path = "D:/Program/Code/.vscode/launch.json"
path = os.curdir + "/.vscode/launch.json"
data = None
with open(path, 'r', encoding="UTF=8") as f:
    if f is None:
        print("connot open file")
        exit()
    data = json.load(f)

update_flg = False
while True:

    print("="*20)
    print("0: exit")
    for i, language in enumerate(data['configurations']):
        print(f"{i+1}: {language['name']}")
    print("="*20)
    index = int(input("please input the index of the language: "))
    if index == 0:
        break
    index -= 1

    print("="*20)
    print("""
    0. exit
    1. change console [integratedTerminal|externalTerminal]
    2. set args
    3. show current config
    """)
    print("="*20)
    try:
        func_num = int(input("please input the number of the function: "))
    except ValueError:
        print("please input the number")
        continue

    if func_num == 0:
        break

    elif func_num == 1:
        # console or externalcosole
        if "console" in data['configurations'][index]:
            console_type_now = data['configurations'][index]['console']
            if console_type_now == "integratedTerminal":
                data['configurations'][index]['console'] = "externalTerminal"
            elif console_type_now == "externalTerminal":
                data['configurations'][index]['console'] = "integratedTerminal"

        elif "externalConsole" in data['configurations'][index]:
            console_type_now = data['configurations'][index]['externalConsole']
            if console_type_now == True:
                data['configurations'][index]['externalConsole'] = False
            elif console_type_now == False:
                data['configurations'][index]['externalConsole'] = True

        update_flg = True

    elif func_num == 2:
        if "args" not in data['configurations'][index]:
            data['configurations'][index]['args'] = []
        if len(sys.argv) == 1:
            args = input("please input the args: ")
            args = args.split(" ")
            data['configurations'][index]['args'] = args
        else:
            data['configurations'][index]['args'] = sys.argv[1:]

        update_flg = True

    elif func_num == 3:
        print(json.dumps(data['configurations'][index], indent=4))

# write the data to the file
if update_flg:
    with open(path, 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=4)