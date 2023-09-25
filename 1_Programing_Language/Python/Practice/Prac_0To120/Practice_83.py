from threading import Timer

def hello():
    print("World!")

t = Timer(3.0, hello)
t.start() # after 30 seconds, "Hello, World!" will be printed
print("Hello")