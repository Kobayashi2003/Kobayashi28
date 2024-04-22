import pickle

class TextReader:
    """Print and number lines in a text file."""

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename)
        self.lineno = 0

    def readline(self):
        self.lineno += 1
        line = self.file.readline()
        if not line:
            return None
        if line.endswith('\n'):
            line = line[:-1]
        return "%i: %s" % (self.lineno, line)

    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['file']
        return state

    def __setstate__(self, state):
        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)
        # Restore the previously opened file's state. To do so, we need to
        # reopen it and read from it until the line count is restored.
        file = open(self.filename)
        for _ in range(self.lineno):
            file.readline()
        # Finally, save the file.
        self.file = file


if __name__ == '__main__':

    with open('hello.txt', 'w') as file:
        file.write('hello, world!\n')
        file.write('hello, pickle!\n')
        file.write('hello, python!\n')
        file.write('hello, serialization!\n')

    reader = TextReader("hello.txt")
    print(reader.readline())
    print(reader.readline())
    new_reader = pickle.loads(pickle.dumps(reader))
    print(new_reader.readline())
    print(new_reader.readline())