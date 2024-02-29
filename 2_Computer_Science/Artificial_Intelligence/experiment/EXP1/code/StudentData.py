class StuData:

    __slots__ = ['data']

    def __init__(self, filename: str) -> None:

        self.data = []

        with open(filename, 'r') as f:
            for line in f:
                data_line = line.strip().split(' ')
                data_line[3] = int(data_line[3])
                self.data.append(data_line)

    def __str__(self) -> str:
        return "\t\t".join(['name', 'stu_num', 'gender', 'age']) + '\n' + '\n'.join(['\t\t'.join([str(i) for i in line]) for line in self.data]) + '\n'

    def AddData(self, name: str, stu_num: str, gender: str, age: int) -> None:
        self.data.append([name, stu_num, gender, age])

    def SortData(self, attr: str) -> None:
        # if you want to throw an exception when the key is not in the dictionary,
        # you can use dict instead of defaultdict
        from collections import defaultdict
        key_map = defaultdict(lambda: 0, {'name': 0, 'stu_num': 1, 'gender': 2, 'age': 3})
        self.data.sort(key=lambda x: x[key_map[attr]])

    def ExportFile(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for line in self.data:
                f.write(' '.join([str(i) for i in line]) + '\n')


if __name__ == "__main__":
    import os

    filename = os.path.join(os.path.dirname(__file__), 'student_data.txt')

    if not os.path.exists(filename):
        import random
        import string
        with open(filename, 'w') as f:
            for i in range(1000):
                random_name = ''.join(random.sample(string.ascii_letters, 5))
                random_stu_num = ''.join(random.sample(string.digits, 8))
                random_gender = random.choice(['F', 'M'])
                random_age = random.randint(18, 25)
                f.write(f'{random_name} {random_stu_num} {random_gender} {random_age}\n')

    stu = StuData(filename)

    stu.SortData('age') 

    stu.ExportFile(os.path.join(os.path.dirname(__file__), 'student_data_sorted.txt'))

    print(stu)
