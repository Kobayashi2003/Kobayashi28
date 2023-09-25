from threading import Thread

t = Thread(target=print, args=[1])
t.run()

t = Thread(target=print, args=(1,))
t.run()