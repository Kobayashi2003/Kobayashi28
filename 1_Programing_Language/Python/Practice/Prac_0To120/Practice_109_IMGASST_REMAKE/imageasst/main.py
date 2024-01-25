import time
import datetime
from sys import stdout, stderr
from multiprocessing.managers import RemoteError

from Buffers          import Buffers
from analysis_path    import fd_files
from loading_page     import donut_generator
from colors2str       import colors2str
from color_extraction import color_extraction, simple_main_loop

from testing import testing

from common import Result, Status
from common import parallel_run, suppress_keyboard_interrupt
from common import get_terminal_size, get_proc_args, calculate_aspect_ratio
from common import LOG_PATH, LOG_FORMAT, LOG_TIME_FORMAT
from common import MAX_WIDTH, MAX_HEIGHT
from common import MAX_WORKERS, MAX_DEPTH, MAX_LOAD_NUM
from common import CACHEFOLDER_PATH, MAX_CACHE_SIZE
from common import SIMPLE_MODE_CODE, ADVANCED_MODE_CODE, TEST_MODE_CODE


def cache_result(func, id, manager_params, *, args=(), kwargs={}):
    """Cache the result of the function in the process manager"""
    # this function is used to draw the result from the done process
    # so here we need [processing], which contains the processes data,
    # and [results], which is used to store the finnal result
    processing, _, results, _, _, lock = manager_params
    result = func(*args, **kwargs)
    try:

        lock.acquire() # lock [processing] and [results]
        try:
            results[id] = Result(Status.done, result)
            pid = processing.pop(id, None)
        except BrokenPipeError:
            pass
        except EOFError:
            pass
        lock.release()

    except BrokenPipeError:
        return
    except EOFError:
        return

    log_msg = '[id:{}] [function-name:{}] [pid:{}] done'.format(id, func.__name__, pid)


def add_function(func, id, manager_params, *, args=(), kwargs={}):
    """Add the function to the process manager"""
    # this function is used to add a new process to the process manager
    processing, pending, _, _, _, lock = manager_params

    if id in processing:
        log_msg = 'add failed: [id:{}] [function-name:{}] is processing'.format(id, func.__name__)
        return False

    try:

        lock.acquire() # lock [processing] and [pending]
        try:
            pending.pop(id, None)
            pending[id] = (func, args, kwargs)
        except BrokenPipeError:
            lock.release()
            return False
        except EOFError:
            lock.release()
            return False
        lock.release()

    except BrokenPipeError:
        return False
    except EOFError:
        return False

    log_msg = 'add success: [id:{}] [function-name:{}]'.format(id, func.__name__)
    return True


def get_result(id, manager_params):
    """Get the result of the process from the process manager"""
    processing, pending, results, _, _, lock = manager_params

    try:
        results_keys = results.keys()
    except BrokenPipeError:
        return Result(Status.error, 'BrokenPipeError when get the results from the process manager')
    except EOFError:
        return Result(Status.error, 'EOFError when get the results from the process manager')

    try:

        lock.acquire() # lock [results]
        try:
            if id in results_keys:
                result = results[id]
                results.pop(id, None)
            elif id in pending:
                result = Result(Status.pending, 'the process {} is pending'.format(id))
            elif id in processing:
                result = Result(Status.processing, 'the process {} is processing'.format(id))
            else:
                result = Result(Status.unfound, 'the process {} is not found'.format(id))
        except BrokenPipeError:
            result = Result(Status.error, 'BrokenPipeError when get the result of the process {}'.format(id))
        except EOFError:
            result = Result(Status.error, 'EOFError when get the result of the process {}'.format(id))
        except Exception as e:
            result = Result(Status.error, 'Unknown error when get the result of the process {}'.format(id))
        lock.release()

    except BrokenPipeError:
        return Result(Status.error, 'BrokenPipeError when get the Lock from the process manager')
    except EOFError:
        return Result(Status.error, 'EOFError when get the Lock from the process manager')
    except Exception as e:
        return Result(Status.error, 'Unknown error when get the Lock from the process manager')

    return result


@suppress_keyboard_interrupt
@parallel_run
def pre_process_loop(manager_params):

    try:
        import multiprocessing
    except:
        raise ImportError('pre_process_loop: import error')

    """The pre_process loop of the process manager"""
    processing, pending, _, signal, _, lock = manager_params

    processing_record = []

    # the task of pre_process loop is to start the pending processes
    # and update the processes status in each loop if there is any free thread
    # until the start_flg is set to False
    while 1:

        try:
            start_flg = signal.start_flg
        except BrokenPipeError:
            break
        except EOFError:
            break
        if not start_flg:
            break

        if len(processing) < MAX_WORKERS and len(pending) > 0:

            try:
                lock.acquire()
                try:
                    id, (func, args, kwargs) = pending.popitem()
                except BrokenPipeError:
                    pass
                except EOFError:
                    pass
                except Exception as e:
                    print(e)
                lock.release()
            except BrokenPipeError:
                break
            except EOFError:
                break

            # generate and start a new process
            new_proc = multiprocessing.Process(target=cache_result, args=(func, id, manager_params), kwargs={'args': args, 'kwargs': kwargs})
            new_proc.name = func.__name__
            new_proc.start()
            processing_record.append(new_proc)

            try:
                lock.acquire()
                try:
                    processing[id] = new_proc.pid
                except BrokenPipeError:
                    pass
                except EOFError:
                    pass
                except Exception as e:
                    print(e)
                lock.release()
            except BrokenPipeError:
                break
            except EOFError:
                break

            log_msg = 'start: [id:{}] [function-name:{}] [pid:{}]'.format(id, func.__name__, new_proc.pid)

        # if all processes are done, slow down the loop
        elif len(processing) == 0 and len(pending) == 0:
            time.sleep(0.1)

        # a little delay to reduce the CPU usage
        time.sleep(0.01)

    for proc in processing_record:
        proc.terminate()

    # stdout.write(LOG_FORMAT.format(time=datetime.datetime.now().strftime(LOG_TIME_FORMAT), func='pre_process_loop', msg='end'))


@suppress_keyboard_interrupt
@parallel_run
def further_process_loop(results_memo, func, manager_params, *, args=(), kwargs={}):

    try:
        import random
        import string
        import os
        import json
        import msgspec
        import itertools
        import functools
        import array
    except:
        raise ImportError('further_process_loop: import error')

    """Get the result of the process"""
    add_func = functools.partial(add_function, manager_params=manager_params)
    get_res = functools.partial(get_result, manager_params=manager_params)

    # this function is used to get the initial result of the process
    # and carry out a further process on the result in each loop
    lock   = manager_params[-1]
    values = manager_params[-2]
    signal = manager_params[-3]

    ids = results_memo.keys()
    # ids_list = list(ids)
    ids_list = array.array('I', ids)

    added_flg            = { id: False for id in ids } # whether the process is added to run further process
    results_cache_origin = { id: None  for id in ids } # original pre-process results
    results_cache_fpath  = { id: None  for id in ids } # cache file path for further processed results
    lru_table            = { id:  0    for id in ids } # least recently used table
    missing_count        = { id:  0    for id in ids } # missing count

    for id in itertools.cycle(ids):

        try:
            start_flg = signal.start_flg
            cur_index = ids_list.index(values.current)
        except BrokenPipeError:
            break
        except EOFError:
            break
        if not start_flg:
            break

        loadable_id = set( [ ids_list[(cur_index + i) % len(ids_list)] for i in range(MAX_LOAD_NUM//2+1)] +
                           [ ids_list[(cur_index - i) % len(ids_list)] for i in range(-(-MAX_LOAD_NUM//2))])

        # all records in the lru_table will be reduced by 1
        lru_table = { id : lru_table[id] + 1 if id in loadable_id else
                           lru_table[id] - 1 if lru_table[id] > 0 else 0 for id in ids }

        if results_memo[id] is None and id in loadable_id:
            result = get_res(id)

            if added_flg[id] == False:
                # if the pre-result is not added to the process manager
                if results_cache_origin[id] is not None:
                    try:
                        add_func(func, id, args=((results_cache_origin[id],) + args), kwargs=kwargs)
                    except:
                        results_memo[id] = "Cannot Generate Further Process"
                    else:
                        added_flg[id] = True
                elif result.status == Status.done:
                    try:
                        add_func(func, id, args=((result.data,) + args), kwargs=kwargs)
                    except:
                        results_memo[id] = "Cannot Generate Further Process"
                    else:
                        added_flg[id] = True
                    finally:
                        results_cache_origin[id] = result.data
                elif result.status == Status.error:
                    results_memo[id] = "The Original Process Has Error"
                elif result.status == Status.unfound:
                    if missing_count[id] > 100:
                        results_memo[id] = "The Original Process Is Not Found"
                    else:
                        missing_count[id] += 1

            else:
                # if the pre-result is added to the process manager
                if results_cache_fpath[id] is not None:
                    try:
                        results_memo[id] = msgspec.json.decode(open(results_cache_fpath[id], 'rb').read())
                    except:
                        results_memo[id] = "Cannot Load Cache File"
                elif result.status == Status.done:
                    try:
                        results_memo[id] = result.data
                    except:
                        results_memo[id] = "The Further Process Has Error"
                elif result.status == Status.error:
                    results_memo[id] = "The Further Process Has Error"
                elif result.status == Status.unfound:
                    if missing_count[id] > 100:
                        results_memo[id] = "The Original Process Is Not Found"
                    else:
                        missing_count[id] += 1

        elif results_memo[id] is not None and id not in loadable_id:

            if results_cache_fpath[id] is None:
                # if the process is done, but the id is not in the loadable_id
                # then save the result to the cache file to save the memory

                # generate an unexisted filename
                random.seed(time.perf_counter())
                filename = CACHEFOLDER_PATH + '/' + ''.join(random.sample(string.ascii_letters + string.digits, random.randint(15, 20)))
                filename = filename.replace('\\', '/').replace('//', '/')
                try: # try to save the final result to the cache file
                    try:
                        open(filename, 'wb').write(msgspec.json.encode(results_memo[id]))
                    except:
                        json.dump(results_memo[id], open(filename, 'w'))
                except: # if failed, reset the added_flg, then next time the process will generate from the original result again
                    results_cache_fpath[id] = None
                    added_flg[id] = False
                else: # if success, set the cache file path to the results_cache_fpath, then next time the process will load from the cache file
                    results_cache_fpath[id] = filename
                finally: # whatever the result is, reset the results_memo to None
                    results_memo[id] = None

            # if the cache folder is bigger than MAX_CACHE_SIZE
            while sum([os.path.getsize(filename) for filename in results_cache_fpath.values() if filename is not None]) > MAX_CACHE_SIZE:

                min_key = min(lru_table, key=lambda key: lru_table[key] if results_cache_fpath[key] is not None else float('inf'))

                if (min_key == None): # if all the cache files are None, then
                    break
                if (min_key == cur_index): # if the min_key is the current index, then
                    break

                try:
                    os.remove(results_cache_fpath[min_key])
                except:
                    pass

                # reset the added_flg and results_cache_fpath
                added_flg[min_key] = False
                results_cache_fpath[min_key] = None

        # a little delay to reduce the CPU usage
        time.sleep(0.01)

    # stdout.write(LOG_FORMAT.format(time=datetime.datetime.now().strftime(LOG_TIME_FORMAT), func='further_process_loop', msg='end'))


@suppress_keyboard_interrupt
@parallel_run
def output_result_loop(results_memo, update_event, run_event, manager_params, *, args=(), kwargs={}):

    try:
        import itertools
    except:
        raise ImportError('output_result_loop: import error')

    """show the current result"""
    lock   = manager_params[-1]
    values = manager_params[-2]
    signal = manager_params[-3]
    buf = Buffers(num=3)
    wait_count = 0

    while 1:
        # the loop will be blocked until the update_event is set
        update_event.wait()
        update_event.clear()

        wait_time = time.perf_counter()
        while 1:

            try:
                lock.acquire()
                try:
                    current_result = results_memo[values.current]
                except BrokenPipeError:
                    current_result = None
                except EOFError:
                    current_result = None
                    current_result = None
                lock.release()
            except BrokenPipeError:
                return
            except EOFError:
                return
            except RemoteError:
                return

            if current_result is not None:
                break

            if time.perf_counter() - wait_time > 0.1:
                wait_count += 1
                wait_time = time.perf_counter()
            buf.switch()
            if kwargs.get('loading_page_generator', None) is not None:
                buf.write(kwargs['loading_page_generator'](wait_count))
            else:
                buf.write('loading' + '.' * wait_count)
            buf.flush()

            # if update_event is set, stop waiting
            if update_event.is_set():
                break

        # start_flg check
        try:
            start_flg = signal.start_flg
            output = results_memo[values.current]
        except BrokenPipeError:
            break
        except EOFError:
            break
        if not start_flg:
            break

        if not isinstance(output, list) and output is not None:
            buf.switch()
            buf.write(output)
            buf.flush()

        elif isinstance(output, list):
            duration = int(output.pop())

            t_get_time_start = time.perf_counter()
            time.perf_counter()
            t_get_time_end = time.perf_counter()
            t_get_time = (t_get_time_end - t_get_time_start) * 10

            for frame in itertools.cycle(output):
                # the loop to show the list of frames
                t_start = time.perf_counter()
                run_event.wait()
                if update_event.is_set():
                    break
                buf.switch()
                buf.write(frame)
                buf.flush()
                t_end = time.perf_counter()

                now = time.perf_counter()
                end = time.perf_counter() + duration / 1000 - t_get_time - (t_end - t_start)
                while now < end:
                    now = time.perf_counter()

            output.append(duration)

        # start_flg check
        try:
            start_flg = signal.start_flg
        except BrokenPipeError:
            break
        except EOFError:
            break
        if not start_flg:
            break

        # a little delay to reduce the CPU usage
        time.sleep(0.01)

    # stdout.write(LOG_FORMAT.format(time=datetime.datetime.now().strftime(LOG_TIME_FORMAT), func='output_result_loop', msg='end'))


@suppress_keyboard_interrupt
@parallel_run
def input_loop(update_event, run_event, manager_params):

    try:
        import msvcrt
    except:
        raise ImportError('input_loop: import error')

    # key      |  function      | code
    # -------- |  ------------- | ----
    # q        |  quit          | b'q'
    # j        |  next          | b'j'
    # J        |  next 10       | b'J'
    # k        |  previous      | b'k'
    # K        |  previous 10   | b'K'
    # h        |  go to first   | b'h'
    # l        |  go to last    | b'l'
    # r        |  redo (TODO)   | b'r'
    # R        |  restart       | b'R'
    # <blank>  |  pause         | b' '
    # <esc>    |  quit          | b'\x1b'
    # <enter>  |  next          | b'\x0d'
    # <back>   |  previous      | b'\x08'
    # <right>  |  next          | (TODO)
    # <left>   |  previous      | (TODO)
    # <C-right>|  next 10       | (TODO)
    # <C-left> |  previous 10   | (TODO)

    lock   = manager_params[-1]
    values = manager_params[-2]
    signal = manager_params[-3]

    elem_count = values.elem_count

    while 1:

        if msvcrt.kbhit():
            key = msvcrt.getch()

            try:
                start_flg = signal.start_flg
                lock.acquire()
            except BrokenPipeError:
                break
            except EOFError:
                break
            if not start_flg:
                break

            if key != ' ':
                update_event.set()
                run_event.set()

            if key == b'q' or key == b'\x1b':
                signal.start_flg = False
                break

            elif key == b'j' or key == b'\x0d':
                values.current = (values.current + 1) % elem_count
            elif key == b'k' or key == b'\x08':
                values.current = (values.current - 1 + elem_count) % elem_count

            elif key == b'J':
                if values.current + 10 >= elem_count:
                    values.current = elem_count - 1
                else:
                    values.current = values.current + 10
            elif key == b'K':
                if values.current - 10 < 0:
                    values.current = 0
                else:
                    values.current = values.current - 10

            elif key == b'h':
                values.current = 0
            elif key == b'l':
                values.current = elem_count - 1

            elif key == b' ':
                if run_event.is_set():
                    run_event.clear()
                else:
                    run_event.set()
                update_event.set()

            elif key == b'R':
                signal.restart_flg = True
                signal.start_flg = False
                break
            elif key == b'C':
                signal.change_proc_mode = True
                signal.start_flg = False
                break
            elif key == b'T':
                signal.change_test_mode = True
                signal.start_flg = False
                break

            try:
                lock.release()
            except BrokenPipeError:
                break
            except EOFError:
                break

        else:
            # a little delay to reduce the CPU usage
            time.sleep(0.05)

    # stdout.write(LOG_FORMAT.format(time=datetime.datetime.now().strftime(LOG_TIME_FORMAT), func='input_loop', msg='end'))


def record_aspect_ratio():
    import json
    from PIL import Image
    import msvcrt
    import os
    import shutil

    aspect_ratio_table = {}

    with open('aspect_ratio_table.json', 'r') as f:
        try:
            aspect_ratio_table = json.load(f)
        except:
            pass
    if len(aspect_ratio_table) != 0:
        # change the key from string to float
        aspect_ratio_table = { float(key): value for key, value in aspect_ratio_table.items() }

    aspect_ratio = 1
    buffers = Buffers(num=2)

    update_flg = True
    im = None
    lst_width, lst_height = 0, 0
    while 1:
        terminal_width, terminal_height = shutil.get_terminal_size()
        if (lst_width, lst_height) != (terminal_width, terminal_height) or update_flg:
            update_flg = False
            lst_width, lst_height = terminal_width, terminal_height

            if im is not None:
                im.close()
            im_edgelen = int(min(terminal_width, terminal_height) / 1.5)
            im = Image.new('RGB', (im_edgelen, im_edgelen), (255, 255, 255))
            im.format = 'jpg'

            res = color_extraction(im, mode='RGB', aspect_ratio=aspect_ratio)
            output = colors2str(res, frame_size=(terminal_width, terminal_height),
                                     pos=((terminal_width - im_edgelen) // 2, (terminal_height - im_edgelen) // 2))

            os.system('cls')
            print(output)
            print("aspect_ratio:  %0.2f" % aspect_ratio)
            print("terminal_size: %d x %d" % (terminal_width, terminal_height))
            print("image_size:    %d x %d" % (im_edgelen, im_edgelen))

        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key in b'jkJKc':
                update_flg = True
            if key == b'q':
                break
            elif key == b'j':
                aspect_ratio = min(3.0, aspect_ratio + 0.1)
            elif key == b'k':
                aspect_ratio = max(0.1, aspect_ratio - 0.1)
            elif key == b'J':
                aspect_ratio = min(3.0, aspect_ratio + 0.01)
            elif key == b'K':
                aspect_ratio = max(0.1, aspect_ratio - 0.01)
            elif key == b' ':
                aspect_ratio_table[terminal_width / terminal_height] = aspect_ratio
            elif key == b'c':
                if len(aspect_ratio_table) > 5:
                    aspect_ratio = calculate_aspect_ratio((terminal_width, terminal_height), aspect_ratio_table)
        else:
            continue

    os.system('cls')
    # sort by the terminal width / height
    aspect_ratio_table = dict(sorted(aspect_ratio_table.items(), key=lambda item: item[0]))
    print(aspect_ratio_table)

    with open('aspect_ratio_table.json', 'w') as f:
        json.dump(aspect_ratio_table, f)

    return 0


def main_loop():

    try:
        import threading
        import multiprocessing
        import functools
        import os
        import shutil
        import gc
        import json
    except:
        raise ImportError('main_loop: import error')

    gc.enable()

    # --- Initialize the Manager --- #

    # [   manager   ]  is used to share the data between processes
        # manager_params:
    # [   signal    ]  is a namespace which is used to control the processes
    # [  processing ]  is a dictionary which is used to record the processes which are processing
    # [   pending   ]  is a dictionary which is used to record the processes which are pending
    # [   results   ]  is a dictionary which is used to store the results of the processes which are done
    manager    = multiprocessing.Manager()
    signal     = manager.Namespace()
    processing = manager.dict()
    pending    = manager.dict()
    results    = manager.dict()
    values     = manager.dict()
    lock       = manager.Lock()
    manager_params = (processing, pending, results, signal, values, lock)

    add_func = functools.partial(add_function, manager_params=manager_params)
    get_res  = functools.partial(get_result, manager_params=manager_params)

    # --- Check the Cache Folder --- #
    cachefolder_path = os.path.abspath(CACHEFOLDER_PATH)

    if os.path.exists(cachefolder_path):
        if not os.path.isdir(cachefolder_path):
            raise ValueError('The cache folder is not a folder')
        if len(os.listdir(cachefolder_path)) > 0:
            # input('The cache folder is not empty, press enter to continue...')
            pass
    else:
        try:
            os.mkdir(cachefolder_path)
        except:
            raise ValueError('Cannot create the cache folder')


    # --- Get the Arguments --- #

    proc_args = get_proc_args()
    args_path = proc_args.path
    args_fit  = proc_args.fit
    args_mode = proc_args.mode
    args_aspect_ratio = proc_args.aspect_ratio
    # size group
    args_size   = proc_args.size

    # frame size
    columns, width = get_terminal_size() if args_size is None else args_size
    frame_size = (columns if args_fit & 2 else MAX_WIDTH, width if args_fit & 1 else MAX_HEIGHT)
    # image mode
    img_mode = args_mode if args_mode in ('RGB', 'RGBA', 'L', 'P') else 'RGB'
    # aspect ratio
    try:
        aspect_ratio = calculate_aspect_ratio((frame_size[0], frame_size[1]), json.loads(open('aspect_ratio_table.json', 'r').read()))
    except:
        aspect_ratio = 1
    aspect_ratio = args_aspect_ratio if args_aspect_ratio is not None else aspect_ratio

    img_kwargs = {
        'size': frame_size,
        'mode': img_mode,
        'aspect_ratio': aspect_ratio
    }

    # --- Get the Image Files --- #
    workpath = os.getcwd() if args_path is None else args_path
    workpath = os.path.abspath(workpath)
    img_files = fd_files(workpath, depth=MAX_DEPTH)
    elem_count = len(img_files)

    for i, img_file in enumerate(img_files):
        args = (img_file, )
        add_func(color_extraction, i, args=args, kwargs=img_kwargs)

    # --- Shared Variables --- #
    signal.start_flg = True
    signal.restart_flg = False
    signal.change_proc_mode = False
    signal.change_test_mode = False
    values.current = 0
    values.elem_count = elem_count
    res_memo = { i: None for i in range(elem_count)}
    update_event = threading.Event()
    run_event    = threading.Event()
    update_event.set()
    run_event.set()


    # -- Rehook KeyboardInterrupt -- #
    def rehook_keyboard_interrupt():
        import sys
        old_except_hook = sys.excepthook

        def new_hook(exctype, value, traceback):
            if exctype == KeyboardInterrupt:
                signal.start_flg = False
                manager.shutdown()
                shutil.rmtree(cachefolder_path)
            else:
                old_except_hook(exctype, value, traceback)
        sys.excepthook = new_hook

    rehook_keyboard_interrupt()


    # --- Start loop --- #
    input_loop(update_event, run_event, manager_params)
    pre_process_loop(manager_params)
    further_process_loop(res_memo, colors2str, manager_params, kwargs={'frame_size': frame_size, 'pos': None})
    output_result_loop(res_memo, update_event, run_event, manager_params, kwargs={'loading_page_generator': donut_generator(*frame_size)})

    ###### * ---- Work Space ---- * ######

    while 1:
        if signal.start_flg == False:
            break

    ###### * -------------------- * ######

    # --- End and Clean --- #

    restart_flg = 0

    if signal.restart_flg:
        restart_flg = ADVANCED_MODE_CODE
    if signal.change_proc_mode:
        restart_flg = SIMPLE_MODE_CODE
    if signal.change_test_mode:
        restart_flg = TEST_MODE_CODE

    manager.shutdown()
    shutil.rmtree(cachefolder_path)

    # stdout.write(LOG_FORMAT.format(time=datetime.datetime.now().strftime(LOG_TIME_FORMAT), func='main_loop', msg='end'))

    return restart_flg


if __name__ == '__main__':

    proc_args = get_proc_args()
    if proc_args.simple:
        return_code = SIMPLE_MODE_CODE
    elif proc_args.test:
        return_code = TEST_MODE_CODE
    elif proc_args.advanced:
        return_code = ADVANCED_MODE_CODE
    else:
        return_code = ADVANCED_MODE_CODE

    while 1:
        if return_code == SIMPLE_MODE_CODE:
            return_code = simple_main_loop()
        elif return_code == ADVANCED_MODE_CODE:
            return_code = main_loop()
        elif return_code == TEST_MODE_CODE:
            return_code = testing()
        if return_code == 0:
            break
        input('\033[2BYou can change the terminal size now, then press enter to continue...')
