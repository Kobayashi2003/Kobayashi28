import functools
import dill
from multiprocessing import Process, Queue, cpu_count
from time import sleep

from common import Result, Status, MAX_WORKERS

class DillProcess(Process):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target = dill.dumps(self._target) # save the target function as bytes, using dill

    def run(self):
        if self._target:
            self._target = dill.loads(self._target) # Unpickle the target function before executing
            self._target(*self._args, **self._kwargs) # Execute the target function

class ProManager:

    def __init__(self, max_workers=MAX_WORKERS):
        self.max_workers = min(max_workers, MAX_WORKERS, cpu_count()-1)
        self.proc_processing = {} # {id: process} 
        self.proc_pending = {}
        self.__results = {}
        self.__queue = Queue()
        self.__start_flag = False
        self.__sleep_flag = False
        self.__main_proc = None

    def PMregister(self, func):
        def wrapper(*args, id, **kwargs):
            if id in self.proc_processing:
                raise ValueError('the process of id {} is processing'.format(id))
            result = func(*args, **kwargs)
            self.__queue.put(id, Result(Status.done, result))
        wrapper.__name__ = func.__name__ + '_PMregister'
        return wrapper
    
    def create_process(self, func, *args, id, **kwargs):
        kwargs['id'] = id
        try:
            PM_func = self.PMregister(func)
            proc = DillProcess(target=PM_func,
                           args=args, kwargs=kwargs)
        except Exception as e:
            print('Error: {}'.format(e))
            return False
        self.proc_pending.pop(id, None)
        self.proc_pending[id] = proc
        self.sleep_flag = False
        return True

    def add_process(self, proc, id):
        """Attention: if you want get the result of the process, 
        you must use register to regist the function of the process first.
        """
        if not isinstance(proc, Process):
            error_msg = 'the process is not a Process'
            print(error_msg)
            return False
        if id in self.proc_processing:
            error_msg = 'the process of id {} is processing'.format(id)
            print(error_msg)
            return False 
        self.proc_pending.pop(id, None)
        self.proc_pending[id] = proc
        self.sleep_flag = False
        return True 

    def get_result(self, id=None):
        if id is None:
            return self.__results
        try:
            return self.__results[id]
        except KeyError:
            if id in self.proc_processing:
                error_msg = 'the process is processing'
                status = Status.processing
                result = Result(status, error_msg)
            elif id in self.proc_pending:
                error_msg = 'the process is pending'
                status = Status.pending
                result = Result(status, error_msg)
            else:
                error_msg = 'the process is not exist'
                status = Status.error
                result = Result(status, error_msg)
            return result

    def __main(self):
        print('main process start')
        while self.__start_flag:
            if len(self.proc_processing) < self.max_workers and len(self.proc_pending) > 0:
                id, proc = self.proc_pending.popitem()
                proc.start()
                self.proc_processing[id] = proc
            if not self.__queue.empty():
                res_tuple = self.__queue.get()
                id, result = res_tuple
                self.__results[id] = result
                self.proc_processing.pop(id, None)
            if len(self.proc_processing) == 0 and len(self.proc_pending) == 0:
                self.__sleep_flag = True
            # low cpu usage
            if self.__sleep_flag:
                sleep(0.1) 

    def start(self):
        if self.__start_flag:
            print('Error: the process manager is running')
            return
        self.__start_flag = True
        # self.__main_proc = Process(target=self.__main)
        # self.__main_proc.start()
        self.__main()


    def stop(self):
        if not self.__start_flag:
            print('Error: the process manager is not running')
            return
        self.__start_flag = False
        # self.__main_proc.terminate()
        self.__sleep_flag = False
        for proc in self.proc_processing.values():
            proc.terminate()
        self.proc_processing.clear()
        self.proc_pending.clear()
        self.__results.clear()
        self.__queue.close()
        self.__queue.join_thread()
