def exch_code(path: str, encode: str, decode: str, cover: bool) -> str:

    import os
    import io

    if not os.path.exists(path):
        raise FileNotFoundError('exch_code: no such file or directory')
    
    if os.path.isdir(path):
        raise IsADirectoryError('exch_code: is a directory')

    new_content_buffer = io.StringIO()

    with open(path, 'r', encoding=encode) as f:
        for line in f.readlines():
            try:
                new_content_buffer.write(line.encode(encode).decode(decode, 'ignore'))
            except:
                new_content_buffer.write('Invalid line: ' + line)

    new_content = new_content_buffer.getvalue()
    new_content_buffer.close()

    if cover:
        with open(path, 'w', encoding=decode) as f:
            f.write(new_content)
        return 'Covered'

    return new_content


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Exchange code')
    parser.add_argument('path', type=str, nargs='?', default=None, help='the path of the file')
    parser.add_argument('-e', '--encode', type=str, default='GBK', help='the encoding of the file')
    parser.add_argument('-d', '--decode', type=str, default='Shift_JIS', help='the decoding of the file')
    parser.add_argument('-c', '--cover', action='store_true', help='cover the original file')
    parser.add_argument('-s', '--string', type=str, default=None, help='the string to exchange code')

    args = parser.parse_args()

    if args.string:
        try:
            sys.stdout.write(args.string.encode(args.encode).decode(args.decode, 'ignore') + '\n')
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
            sys.exit(1)
        sys.exit(0)

    try:
        exchange = exch_code(args.path, args.encode, args.decode, args.cover)
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)

    sys.stdout.write(exchange + '\n')
