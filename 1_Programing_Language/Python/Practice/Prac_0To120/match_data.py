import re
import os

def get_match_data(filename):
    # match shape=[...] and dtype=... from log.txt
    # write the result to match_data.txt

    with open(filename) as f:
        content = f.readlines()

    match_data = []
    shape_record = set()
    dtype_record = set()
    for line in content:
        if re.match(r'.*shape=\[.*\].*dtype=.*', line):
            shape_part = re.search(r'shape=\[.*\]', line).group()
            dtype_part = re.search(r'dtype=.*', line).group()
            # process dtype_part: if meet , or blank, then stop
            dtype_part = dtype_part.split(' ')[0]
            dtype_part = dtype_part.split(',')[0]
            match_data.append('shape: ' + shape_part + '\n' + 'dtype: ' + dtype_part + '\n')
            shape_value = shape_part.split('=')[1]
            shape_record.add(shape_value)
            dtype_value = dtype_part.split('=')[1]
            dtype_record.add(dtype_value)

    # write to match_data.txt
    with open('match_data.txt', 'w') as f:
        for line in match_data:
            f.write(line)
        f.write('\n')
        f.write('shape_record: ' + str(shape_record) + '\n')
        f.write('dtype_record: ' + str(dtype_record) + '\n')      
    

if __name__ == '__main__':
    get_match_data('log.txt')
