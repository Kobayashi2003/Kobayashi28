class Exm:

    items = []

    def __init__(self, *args):

        self.items.extend(list(args))


test = Exm(1, 2, 3, 4, "hello", True)
print(test.items)
