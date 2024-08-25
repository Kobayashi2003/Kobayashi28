if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Exchange code string')
    parser.add_argument('string', type=str, nargs='?', default=None, help='the string to be exchanged')
    parser.add_argument('-e', '--encode', type=str, default='GBK', help='the encoding of the string')
    parser.add_argument('-d', '--decode', type=str, default='Shift_JIS', help='the decoding of the string')
    args = parser.parse_args()

    try:
        exchange = args.string.encode(args.encode).decode(args.decode, 'ignore')
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)

    sys.stdout.write(exchange + '\n')
