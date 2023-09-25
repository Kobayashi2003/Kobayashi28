class CoffeeCup:
    coffee = 'empty half full'.split()

    def __init__(self):
        self.coffeeLeft = self.coffee.index('full')
        self.cont = 0
        print("You picked up a cup of coffee")

    def mental_struggle(self):
        if self.cont == 3:
            print("I have drunk three cups of coffee, do I really want to drink another cup?")
            return self.choose()
        elif self.cont == 5:
            print("Oh come on, this is the last cup")
            return True
        elif self.cont > 5:
            print("I think I couldn't drink more")
            return False

    def choose(self):
        return input("My choice is [Y/N]:") == 'Y'

    def drink(self):
        if self.cont >= 3:
            if self.mentalStruggle():
                pass
            else:
                print("I don't want more")
                return 

        if self.coffeeLeft == 0:
            print("Oh the cup is empty, should I refill it?")
            if self.choose():
                print("Let me refill it!")
                self.refill()
            else :
                print("I don't need more")
        else :
            print("Tasty!")
            self.coffeeLeft -= 1

    def refill(self):
        self.coffeeLeft = self.coffee.index('full')


a_cup_of_coffee = CoffeeCup()
