# group the files in the directory by time

def group_by_time(path: str, year: bool, month: bool, day: bool, clean: bool) -> str:
    import io
    import os
    import time

    if not os.path.exists(path):
        raise FileNotFoundError('group_by_time: no such file or directory')

    if not os.path.isdir(path):
        raise NotADirectoryError('group_by_time: not a directory')

    if year:
        time_format = '%Y'
    elif month:
        time_format = '%Y-%m'
    elif day:
        time_format = '%Y-%m-%d'
    else:
        raise ValueError('group_by_time: invalid time mode')

    log_msg_stream = io.StringIO()
    log_msg_stream.write('group_by_time: path: {}, time mode: {}, clean: {}\n'.format(path, time_format, clean))

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_time = time.strftime(time_format, time.localtime(os.path.getmtime(file_path)))
            new_dir = os.path.join(path, file_time)
            new_path = os.path.join(new_dir, file)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            if file_path != new_path:
                try:
                    os.rename(file_path, new_path)
                    log_msg_stream.write('file: {} -> {}\n'.format(file_path, new_path))
                except FileExistsError:
                    log_msg_stream.write('file: {} exists\n'.format(new_path)) 

    if clean: # clean the empty directories
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    log_msg_stream.write('directory: {} removed\n'.format(dir_path))

    log_msg_stream.seek(0)
    return log_msg_stream.read()


if __name__ == '__main__':
    import argparse
    import sys
    import os

    parser = argparse.ArgumentParser(description='Group by time')
    parser.add_argument('path', type=str, nargs='?', default=None, help='the path of the directory')
    parser.add_argument('-c', '--clean', action='store_true', help='clean the directory')
    # parser.add_argument('-b', '--backup', action='store_true', help='backup the original file group')
    parser.add_argument('-s', '--silent', action='store_true', help='silent mode')
    time_mode_group = parser.add_mutually_exclusive_group()
    time_mode_group.add_argument('--year',   action='store_true', help='group by year')
    time_mode_group.add_argument('--month',  action='store_true', help='group by month')
    time_mode_group.add_argument('--day',    action='store_true', help='group by day')
    parser.set_defaults(year=False, month=False, day=False)
    args = parser.parse_args()

    try:
        log_msg = group_by_time(args.path, args.year, args.month, args.day, args.clean)
    except Exception as e:
        log_msg = 'group_by_time: {}\n'.format(e)
        try:
            sys.stderr.write(log_msg)
        except UnicodeEncodeError:
            sys.stderr.buffer.write(log_msg.encode('utf-8'))
        exit(1)

    if not args.silent:
        try:
            sys.stdout.write(log_msg)
        except UnicodeEncodeError:
            sys.stdout.buffer.write(log_msg.encode('utf-8'))
