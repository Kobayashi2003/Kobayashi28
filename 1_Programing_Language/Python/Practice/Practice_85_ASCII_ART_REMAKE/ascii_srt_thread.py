from ascii_srt import ascii_srt

from threading import Thread

class ascii_srt_thread(Thread):
    def __init__(self, param, thread_id):
        Thread.__init__(self)
        self.param = param
        self.thread_id = thread_id
        self.result = None

    def run(self) -> None:
        self.result = ascii_srt(**self.param)

    def get_result(self):
        return self.result