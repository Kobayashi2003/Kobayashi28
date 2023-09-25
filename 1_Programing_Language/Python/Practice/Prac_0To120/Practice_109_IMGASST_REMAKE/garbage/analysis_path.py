import os
import glob
import magic

from common import SUPPORTED_IMAGE_FORMAT_ALL


def find_all_file(path):
    path_glob = glob.glob(path)
    path_list = []
    while path_glob:
        path = os.path.normpath (
                os.path.normcase (
                os.path.abspath(path_glob.pop(0))))
        if os.path.isdir(path):
            path_glob.extend(glob.glob(path + '/*'))
        else:
            path_list.append(path) 
    return path_list


def find_file(path):
    path_glob = glob.glob(path)
    path_file_list = []
    path_dir_list = []

    for path in path_glob:
        path = os.path.normpath (
                os.path.normcase (
                os.path.abspath(path)))
        if os.path.isdir(path):
            path_dir_list.append(path)
        elif os.path.isfile(path):
            path_file_list.append(path)
        
    path_glob = [glob.glob(path + '/*') for path in path_dir_list]
    path_dir_list.extend([path for path in path_glob if os.path.isfile(path)])

    return path_file_list


def file_filter(path_list, file_type=SUPPORTED_IMAGE_FORMAT_ALL):
    path_list_filtered = []
    error_list = []
    for path in path_list:
        try:
            ft = str.lower(magic.from_file(path, mime=True).split('/')[1])
        except:
            error_list.append(path)
            continue
        if ft in file_type:
            path_list_filtered.append(path)
    return path_list_filtered, error_list

    
if __name__ == '__main__':
    path = 'D:/Program/Code/1_Programing_Language/Python/Practice/Practice_109_IMGASST_REMAKE/'
    # path = 'D:/Program/Code/*'
    path_list = find_all_file(path)
    path_list = file_filter(path_list)
    print(path_list)