import sys

list = [1, 2, 3, 4]
it = iter(list) # this builds an iterator object
print(next(it)) # print next available element in iterator
# Iterator object can be traversed using regular for statment
for x in it:
    print(x, end=" ")
# using next() function
while True:
    try:
        print(next(it))
    except StopIteration:
        sys.exit() # you have to import sys module for this