import threading 
import msvcrt

class KeyboardMonitor(threading.Thread):
    def __init__(self, event, share, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event
        self.share = share

    def run(self):
        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                ch = ch.decode('utf-8')
                if ch == 'q':
                    break
                self.share['last_press'] = ch
                self.event.set()

if __name__ == '__main__':
    event = threading.Event()
    share = {'last_press': None}
    keyboard_monitor = KeyboardMonitor(event, share)
    keyboard_monitor.start()
    while True:
        event.wait()
        print(f'you pressed {share["last_press"]}')
        event.clear()