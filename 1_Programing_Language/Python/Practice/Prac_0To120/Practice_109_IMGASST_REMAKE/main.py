import time
from multiprocessing import Process, Manager
from sys import stdout, stderr
from functools import partial

from Buffers import Buffers
from common import Result, Status, MAX_WORKERS, parallel_run


def result_cache(func, id, manager_params, *, args=(), kwargs={}):
    """Cache the result of the function"""
    processing, _, results, _ = manager_params
    result = func(*args, **kwargs)
    results[id] = Result(Status.done, result) 
    pid = processing.pop(id, None)
    log_msg = 'done: [id:{}] [function-name:{}] [pid:{}]'.format(id, func.__name__, pid)
    

def add_function(func, id, manager_params, *, args=(), kwargs={}):
    """Add the function to the process manager"""
    processing, pending, _, _ = manager_params
    if id in processing:
        error_msg = 'the process of id {} is processing'.format(id)
        return False
    pending.pop(id, None)
    pending[id] = (func, args, kwargs)
    return True


def get_result(id, manager_params):
    """Get the result of the process"""
    processing, pending, results, _ = manager_params
    try:
        result = results[id]
        results.pop(id, None)
    except KeyError:
        if id in pending:
            error_msg = 'the process is pending'
            status = Status.pending
            result = Result(status, error_msg)
        elif id in processing:
            error_msg = 'the process is processing'
            status = Status.processing
            result = Result(status, error_msg)
        else:
            error_msg = 'the process is not found'
            status = Status.unfound
            result = Result(status, error_msg)
    return result


def main_loop(manager_params):
    processing, pending, _, signal = manager_params
    """The main loop of the process manager"""
    while signal.start_flg:
        if len(processing) < MAX_WORKERS and len(pending) > 0:
            try:
                id, (func, args, kwargs) = pending.popitem()
            except KeyError:
                continue
            new_proc = Process(target=result_cache, args=(func, id, manager_params), kwargs={'args': args, 'kwargs': kwargs})
            new_proc.name = func.__name__
            new_proc.start()
            processing[id] = new_proc.pid
            log_msg = 'start: [id:{}] [function-name:{}] [pid:{}]'.format(id, func.__name__, new_proc.pid)
        elif len(processing) == 0 and len(pending) == 0:
            time.sleep(0.1)


@parallel_run
def output_process(results_memo, func, manager_params, *, args=(), kwargs={}):

    add_func = partial(add_function, manager_params=manager_params)
    get_res = partial(get_result, manager_params=manager_params)

    signal = manager_params[-1]

    ids = results_memo.keys()

    added_flg = { id: False for id in ids }

    import itertools
    for id in itertools.cycle(ids):
        if results_memo[id] is None:
            result = get_res(id)
            if result.status == Status.done:
                result_data = result.data
                args_tmp = (result_data, ) + args
                if not added_flg[id]:
                    add_func(func, id, args=args_tmp, kwargs=kwargs)
                    added_flg[id] = True
                else:
                    results_memo[id] = result_data
            else: # the case of Status.pending, Status.processing, Status.unfound
                continue
        else: 
            if None not in results_memo.values() or not signal.start_flg:
                break


@parallel_run
def show_current(results_memo, update_event, pause_event, manager_params):
    import time
    import itertools
    signal = manager_params[-1]
    buf = Buffers(num=5)
    while True:

        update_event.wait()
        update_event.clear()

        if not signal.start_flg:
            break

        while results_memo[signal.current] is None:
            time.sleep(0.1)
        output = results_memo[signal.current]

        if isinstance(output, str):
            buf.switch()
            buf.write(output)
            buf.flush()

        elif isinstance(output, list):
            duration = output.pop()
            for frame in itertools.cycle(output):

                pause_event.wait()

                if update_event.is_set():
                    break

                if not signal.start_flg:
                    break
 
                t_start = time.perf_counter()
                buf.switch()
                buf.write(frame)
                buf.flush()
                t_end = time.perf_counter()
                time.sleep(duration / 1000 - (t_end - t_start) 
                           if duration / 1000 - (t_end - t_start) > 0 
                           else 0)
            output.append(duration)

        else:
            raise TypeError('output must be a str or a list')

        if not signal.start_flg:
            break


def main():
    
    manager = Manager()
    signal = manager.Namespace()
    processing = manager.dict()
    pending = manager.dict()
    results = manager.dict()
    manager_params = (processing, pending, results, signal)

    signal.start_flg = True

    main_loop_proc = Process(target=main_loop, args=(manager_params,))
    add_func = partial(add_function, manager_params=manager_params)
    get_res = partial(get_result, manager_params=manager_params)


    # --- Before the Main Loop --- #

    import os
    import shutil
    workpath = os.getcwd()
    # workpath = "Z:\Temp\\test\\54*"
    workpath = os.path.abspath(workpath)
    frame_size = shutil.get_terminal_size()

    from analysis_path import fd_files, MAX_DEPTH
    depth = MAX_DEPTH
    img_files = fd_files(workpath, depth=depth)
    total = len(img_files)

    from color_extraction import color_extraction
    img_kwargs = {
        'size': frame_size,
        'mode': 'RGB',
        'aspect_ratio': 0.33
    }

    for i, img_file in enumerate(img_files):
        args = (img_file, )
        add_func(color_extraction, i, args=args, kwargs=img_kwargs)


    # --- Start the Main Loop --- #
    main_loop_proc.start()


    ###### * ---- Work Space ---- * ######

    from colors2str import data_preprocess
    res_memo = { i: None for i in range(total)}

    signal.current = 0

    output_process(res_memo, data_preprocess, manager_params, kwargs={'frame_size': frame_size, 'pos': (0, 0)})

    import threading

    update_event = threading.Event()
    pause_event = threading.Event()

    show_current(res_memo, update_event, pause_event, manager_params)

    update_event.set()
    pause_event.set()

    # TODO

    import msvcrt

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b' ':
                if pause_event.is_set():
                    pause_event.clear()
                else:
                    pause_event.set()
            elif key == b'q':
                break
            elif key  == b'j':
                signal.current = (signal.current + 1) % total
                update_event.set()
            elif key == b'k':
                signal.current = (signal.current -1 + total) % total
                update_event.set()
            else:
                continue
        else:
            continue

    ###### * -------------------- * ######

    # --- End the Main Loop --- #
    signal.start_flg = False
    pause_event.set()
    update_event.set()
    main_loop_proc.join()


if __name__ == '__main__':
    main()