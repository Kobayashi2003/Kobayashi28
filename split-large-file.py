
def find_large_file(path: list, size: int, ignore: list, recursive: bool) -> set:
    import os, glob
    from functools import reduce

    if recursive:
        expanded_paths = reduce(lambda x, y: x.union(glob.glob(os.path.abspath(y), recursive=True)), path, set())
    else:
        expanded_paths = reduce(lambda x, y: x.union(glob.glob(os.path.abspath(y))), path, set())

    if ignore is None:
        ignored_paths = set()
    elif recursive:
        ignored_paths = reduce(lambda x, y: x.union(glob.glob(os.path.abspath(y), recursive=True)), ignore, set())
    else:
        ignored_paths = reduce(lambda x, y: x.union(glob.glob(os.path.abspath(y))), ignore, set()) 

    paths = expanded_paths - ignored_paths

    files = set(f for f in paths if os.path.isfile(f) and os.path.getsize(f) > size * 1024 * 1024)

    return files


def split_large_file(path: str, split_size: int, output: str, delete: bool) -> None:
    import os
    import subprocess

    command = [
        '7z', 'a',
        '-v{}m'.format(split_size),
        output or os.path.join(os.path.dirname(path), os.path.basename(path) + '.7z'),
        path
    ] 

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise Exception(result.stderr.decode('utf-8'))
    
    if delete:
        os.remove(path)


def test():
    import subprocess
    command = r'python .\split-large-file.py --split-size 50 ** -r -i Temp/** Others/** WorkPlace/** Debug/** -d'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode('utf-8'))


if __name__ == '__main__':

    import argparse
    import sys, os
    from tqdm import tqdm

    parser = argparse.ArgumentParser(description='Split large file')
    parser.add_argument('path', type=str, nargs='+', default=None, help='the path of the file')
    parser.add_argument('-i', '--ignore', type=str, nargs='*', default=None, help='ignore the files or directories')
    parser.add_argument('-o', '--output', type=str, default=None, help='the output directory (default: the same directory as the input file)')
    parser.add_argument('-r', '--recursive', action='store_true', help='split the files in the directory recursively')
    parser.add_argument('-d', '--delete', action='store_true', help='delete the original file after splitting')
    parser.add_argument('-s', '--size', type=int, default=100, help='split the file by size (MB), default: 100')

    split_mode_group = parser.add_mutually_exclusive_group()
    split_mode_group.add_argument('--split-size', type=int, default=None, help='split the file into the specified size (MB)')
    split_mode_group.add_argument('--split-number', type=int, default=None, help='split the file into the specified number of files')

    args = parser.parse_args()
    if args.size <= 0:
        parser.error('split-large-file: invalid size, must be greater than 0')
    if args.split_size is None and args.split_number is None:
        parser.error('split-large-file: the following arguments are required: --split-size or --split-number')
    if args.split_size is not None and args.split_size <= 0:
        parser.error('split-large-file: invalid size, must be greater than 0')
    if args.split_number is not None and args.split_number <= 0:
        parser.error('split-large-file: invalid number, must be greater than 0')

    try:
        files = find_large_file(args.path, args.size, args.ignore, args.recursive)

        if not files:
            sys.stdout.write('split_large_file: no large file found\n')
            sys.exit(0)

        input("THE FILES BELOW WILL BE SPLITTED, PRESS ENTER TO CONTINUE:\n{}\n".format('\n'.join(files)))

        for file in tqdm(files):
            if args.split_size is None:
                split_large_file(file, os.path.getsize(file) // args.split_number, args.output, args.delete)
            else:
                split_large_file(file, args.split_size, args.output, args.delete)
    except Exception as e:
        sys.stderr.write('split_large_file: {}'.format(e))
        sys.exit(1)

# $ python split-large-file.py -h
# usage: split-large-file.py [-h] [-i [IGNORE [IGNORE ...]]] [-o OUTPUT] [-r] [-d] [-s SIZE] [--split-size SPLIT_SIZE | --split-number SPLIT_NUMBER] path [path ...]
