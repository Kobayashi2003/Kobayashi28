from threading import Thread

class mthread(Thread):
    def __init__(self, func, id, *args, **kwargs):
        Thread.__init__(self)
        self.id = id

        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.result = None
        self.error = None

        self.start_flag = False
        self.end_flag = False

    def run(self):
        self.start_flag = True
        try:
            self.result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            print('Error: {}'.format(e))
            self.error = e
        self.end_flag = True
        
    def get_result(self):
        if self.end_flag:
            return self.result
        else:
            # print('Error: the thread is not end')
            return None


class mthmngr(Thread):

    MAX_RUNNING_THREADS = 10

    def __init__(self):
        Thread.__init__(self)
        self.waiting_ths = []
        self.running_ths = []
        self.finished_ths = []
        self.results = []
        self.start_flag = False
        self.end_flag = False

    def create_mthread(self, func, id, *args, **kwargs):
        self.waiting_ths.append(mthread(func, id, *args, **kwargs))

    def add_thread(self, th):
        if not isinstance(th, mthread):
            print('Error: the thread is not a mthread')
            return
        self.waiting_ths.append(th)

    def run(self):
        self.start_flag = True

        while not self.end_flag:
            if len(self.running_ths) < self.MAX_RUNNING_THREADS and len(self.waiting_ths) > 0:
                th = self.waiting_ths.pop(0)
                try:
                    if th.start_flag:
                        th.run()
                    else:
                        th.start()
                    self.running_ths.append(th)
                except Exception as e:
                    print('Error: {}'.format(e))
                    self.finished_ths.append(th)
                    continue

            for th in self.running_ths:
                if th.end_flag:
                    self.finished_ths.append(th)
                    self.running_ths.remove(th)
                    self.results.append(th.get_result())

        for th in self.running_ths:
            if th.is_alive():
                th.join()

    def check_thread_status(self, id):
        for th in self.waiting_ths:
            if th.id == id:
                return 'waiting'
        for th in self.running_ths:
            if th.id == id:
                return 'running'
        for th in self.finished_ths:
            if th.id == id:
                return 'finished'
        return 'not found'

    def restart_thread(self, id):
        for th in self.finished_ths:
            if th.id == id:
                th.end_flag = False
                self.waiting_ths.append(th)
                self.finished_ths.remove(th)
                return
        print('Error: the thread is not found')

    def restart_all_threads(self):
        for th in self.finished_ths:
            th.end_flag = False
            self.waiting_ths.append(th)
        self.finished_ths = []

    def prioty_thread(self, id):
        for th in self.waiting_ths:
            if th.id == id:
                try:
                    self.waiting_ths.remove(th)
                    self.waiting_ths.insert(0, th)
                except:
                    pass
                return
            
    def get_result(self, id):
        for th in self.finished_ths:
            if th.id == id:
                return th.get_result()
        return None

    def get_all_results(self):
        return self.results

    def stop(self):
        self.end_flag = True
    