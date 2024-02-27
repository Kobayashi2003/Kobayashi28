import os

class StuData:

    __slots__ = ['data']

    def __init__(self, filename: str) -> None:

        """filedata
        name: str
        stu_num: str
        gender: str
        age: int
        """

        self.data = []

        try:
            with open(filename, 'r') as f:
                for line in f:
                    self.data.append(line.strip().split())
                self.data[-1][3] = int(self.data[-1][3])
        except FileNotFoundError:
            pass

    def __str__(self) -> str:
        return str(self.data)

    def AddData(self, name: str, stu_num: str, gender: str, age: int) -> None:
        self.data.append([name, stu_num, gender, age])

    def SortData(self, attr: str) -> None:
        key_map = {'name': 0, 'stu_num': 1, 'gender': 2, 'age': 3}
        self.data.sort(key=lambda x: x[key_map[attr]])

    def ExportFile(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for line in self.data:
                f.write(' '.join([str(i) for i in line]) + '\n')


if __name__ == "__main__":

    filename = os.path.join(os.path.dirname(__file__), 'data.txt')
    stu = StuData(filename)

    stu.AddData(name='kobayashi0', stu_num='0', gender="M", age=23)
    stu.AddData(name='kobayashi1', stu_num='1', gender="M", age=21)
    stu.AddData(name='kobayashi2', stu_num='2', gender="F", age=22)

    stu.SortData('age')

    stu.ExportFile(os.path.join(os.path.dirname(__file__), 'data1.txt'))

    print(stu)