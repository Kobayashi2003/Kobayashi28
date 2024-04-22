from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time
import os

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        super(FileEventHandler, self).__init__()

    def on_moved(self, event):
        if event.is_directory:
            print(f"directory moved from {event.src_path} to {event.dest_path}")
        else:
            print(f"file moved from {event.src_path} to {event.dest_path}")
    
    def on_created(self, event):
        if event.is_directory:
            print(f"directory created:{event.src_path}")
        else:
            print(f"file created:{event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            print(f"directory deleted:{event.src_path}")
        else:
            print(f"file deleted:{event.src_path}")

    def on_modified(self, event):
        if event.is_directory:
            print(f"directory modified:{event.src_path}")
        else:
            print(f"file modified:{event.src_path}")


if __name__ == "__main__":
    path = "."
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
