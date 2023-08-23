LIBRARY_FOLDER = r'D:\Program\Code\1_Programing_Language\Python\Practice\Practice_110\books'


def find_all_files(directory):
    import os
    if not os.path.isdir(directory):
        return []
    directory = os.path.abspath(directory)
    to_check = [directory]
    while to_check:
        current_path = to_check.pop()
        if os.path.isdir(current_path):
            for path in os.listdir(current_path):
                to_check.append(os.path.join(current_path, path))
        elif os.path.isfile(current_path):
            yield current_path