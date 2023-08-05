import time
import keyboard

flag = False

def key_press(key):
    global flag
    if key.name == 's':
        flag = True

keyboard.on_press(key_press)

num_iter = 20
for i in range(num_iter):
    print(i)
    time.sleep(0.2)
    if flag: 
        print("Paused")
        ipt = input("Press Enter to continue...")
        print("Continued")
        flag = False

