import random

def stu_msg(name, ID, **kwargs):
    msg = {
        'name': name,
        'ID': ID,
    }
    msg.update(kwargs)
    return msg

stus = []
used_ID = []

for i in range(11):
    name = ''.join(random.sample([chr(ord('a')+i) for i in range(26)], 5))

    ID = 0
    while ID in used_ID:
        ID = random.randint(1000, 9999)
    used_ID.append(ID)

    _sex = random.choice(["male", "female", "unknown"])

    _hight = random.randint(150, 200)

    _wight = round(random.uniform(50, 80), 2)

    msg = stu_msg(name, ID, sex = _sex, hight = _hight, wight = _wight)

    stus.append(msg)

print(stus)
