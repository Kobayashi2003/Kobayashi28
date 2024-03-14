def exch_code(path: str, encode: str, decode: str, cover: bool) -> str:

    import os


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Exchange code')
    parser.add_argument('path', type=str, nargs='?', default=None, help='the path of the file')
    parser.add_argument('-e', '--encode', type=str, default='GBK', help='the encoding of the file')
    parser.add_argument('-d', '--decode', type=str, default='Shift_JIS', help='the decoding of the file')
    parser.add_argument('-c', '--cover', action='store_true', help='cover the original file')

    args = parser.parse_args()

