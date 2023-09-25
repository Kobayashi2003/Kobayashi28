# BMI 计算

class People:

    def __init__(self, height, weight):

        self.__height = height
        self.__weight = weight

        self.BMI = weight / height**2

    def Judge(self):
        if self.BMI < 18.5:
            print("too low")
        elif self.BMI >= 18.5 and self.BMI < 25:
            print("normal")
        elif self.BMI >= 25 and self.BMI < 28:
            print("too high")
        else:
            print("too too high")

xiaowang = People(1.75, 80.5)