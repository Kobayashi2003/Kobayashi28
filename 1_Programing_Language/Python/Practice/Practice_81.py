class Teacher:
    def __init__(self, num, name, sex):
        self.__num = num
        self.__name = name
        self.__sex = sex

    def show(self):
        print(f"num: {self.__num}\nname: {self.__name}\nsex: {self.__sex}")

class BirthDate:
    def __init__(self, year, month, day):
        self.__year = year
        self.__month = month
        self.__day = day

    def reset(self, ny, nm, nd):
        self.__year = ny
        self.__month = nm
        self.__day = nd

    def show(self):
        print(f"birthday: {self.__year}-{self.__month}-{self.__day}")

class Professor(Teacher):
    def __init__(self, num, name, sex, birth):
        super().__init__(num, name, sex)
        self.__birth = birth

    def resetBirth(self, ny, nm, nd):
        self.__birth.reset(ny, nm, nd)

    def show(self):
        super().show()
        self.__birth.show()
        

def main():
    bir = BirthDate(1990, 1, 1)
    prof = Professor(1, "zhangsan", 'm', bir)
    prof.show()
    prof.resetBirth(1991, 2, 2)
    prof.show()

if __name__ == "__main__":
    main()