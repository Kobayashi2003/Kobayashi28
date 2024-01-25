import os
import re
import glob
import magic

from common import SUPPORTED_IMAGE_FORMAT_ALL, MAX_DEPTH


class FILTER_BASE:
    def __init__(self):
        pass

    def __call__(self, path):
        return True

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()

    def __and__(self, other):
        return AND_FILTER(self, other)

    def __or__(self, other):
        return OR_FILTER(self, other)

    def __invert__(self):
        return NOT_FILTER(self)


class AND_FILTER(FILTER_BASE):
    def __init__(self, *filters):
        self.filters = filters

    def __call__(self, path):
        for filter in self.filters:
            if not filter(path):
                return False
        return True

    def __repr__(self):
        return ' & '.join([str(filter) for filter in self.filters])


class OR_FILTER(FILTER_BASE):
    def __init__(self, *filters):
        self.filters = filters

    def __call__(self, path):
        for filter in self.filters:
            if filter(path):
                return True
        return False

    def __repr__(self):
        return ' | '.join([str(filter) for filter in self.filters])


class NOT_FILTER(FILTER_BASE):
    def __init__(self, filter):
        self.filter = filter

    def __call__(self, path):
        return not self.filter(path)

    def __repr__(self):
        return 'not ' + str(self.filter)


class TYPE_FILTER(FILTER_BASE):
    def __init__(self, file_type=SUPPORTED_IMAGE_FORMAT_ALL):
        self.file_type = file_type

    def __call__(self, path):
        try:
            ft = str.lower(magic.from_file(path, mime=True).split('/')[1])
        except:
            return False
        if ft in self.file_type:
            return True
        return False

    def __repr__(self):
        return 'type=' + str(self.file_type)


class NAME_FILTER(FILTER_BASE):
    def __init__(self, name_pattern=r'.*'):
        self.name_pattern = name_pattern

    def __call__(self, path):
        filename = os.path.basename(path)
        if re.match(self.name_pattern, filename):
            return True
        return False

    def __repr__(self):
        return 'name=' + str(self.name_pattern)


class PATH_FILTER(FILTER_BASE):
    def __init__(self, path_pattern=r'.*'):
        self.path_pattern = path_pattern

    def __call__(self, path):
        path = os.path.normpath (
                os.path.normcase (
                os.path.abspath(path)))
        if re.match(self.path_pattern, path):
            return True
        return False

    def __repr__(self):
        return 'path=' + str(self.path_pattern)


class SIZE_FILTER(FILTER_BASE):
    def __init__(self, min_size=0, max_size=1e5):
        self.min_size = min_size
        self.max_size = max_size

    def __call__(self, path):
        size = os.path.getsize(path)
        if self.min_size <= size <= self.max_size:
            return True
        return False

    def __repr__(self):
        return 'size=' + str(self.min_size) + '-' + str(self.max_size)


class SORTER_BASE:
    def __init__(self, reverse=False):
        self.reverse = reverse

    def __call__(self, path_list):
        return path_list

    def __repr__(self):
        return f'{self.__class__.__name__}(reverse={self.reverse})'

    def __str__(self):
        return self.__repr__()


class SORT_BY_NAME(SORTER_BASE):
    def __init__(self, reverse=False):
        self.reverse = reverse

    def __call__(self, path_list):
        path_list.sort(key=lambda path: os.path.basename(path), reverse=self.reverse)
        return path_list


class SORT_BY_SIZE(SORTER_BASE):
    def __init__(self, reverse=False):
        self.reverse = reverse

    def __call__(self, path_list):
        path_list.sort(key=lambda path: os.path.getsize(path), reverse=self.reverse)
        return path_list


class SORT_BY_CTIME(SORTER_BASE):
    def __init__(self, reverse=False):
        self.reverse = reverse

    def __call__(self, path_list):
        path_list.sort(key=lambda path: os.path.getctime(path), reverse=self.reverse)
        return path_list


class SORT_BY_MTIME(SORTER_BASE):
    def __init__(self, reverse=False):
        self.reverse = reverse

    def __call__(self, path_list):
        path_list.sort(key=lambda path: os.path.getmtime(path), reverse=self.reverse)
        return path_list


class NATURAL_SORT(SORTER_BASE):
    def __init__(self, reverse=False):
        self.reverse = reverse

    @staticmethod
    def __atoi(text):
        return int(text) if text.isdigit() else text

    @staticmethod
    def __natural_keys(text):
        return [NATURAL_SORT.__atoi(c) for c in re.split('(\d+)', text)]

    def __call__(self, path_list):
        path_list.sort(key=lambda path: NATURAL_SORT.__natural_keys(os.path.basename(path)), reverse=self.reverse)
        return path_list


def fd_files(path, *, depth=0, filter=(TYPE_FILTER() & NAME_FILTER()), sorter=NATURAL_SORT()):
    depth = min(depth, MAX_DEPTH)
    path_glob = glob.glob(path)
    file_list = sorter([ file for file in path_glob if os.path.isfile(file) and filter(file) ])
    if depth == 0:
        return file_list
    d = 1
    dir_list = [ dir for dir in path_glob if os.path.isdir(dir) ]
    while d <= depth and dir_list:
        path_glob = sum([ glob.glob(dir + '/*') for dir in dir_list ], [])
        file_list.extend(sorter([ file for file in path_glob if os.path.isfile(file) and filter(file) ]))
        dir_list = [ dir for dir in path_glob if os.path.isdir(dir) ]
        d += 1
    return file_list


if __name__ == '__main__':
    # a little test
    path = os.getcwd()
    img_list = fd_files(path, depth=MAX_DEPTH)
    print(img_list)
