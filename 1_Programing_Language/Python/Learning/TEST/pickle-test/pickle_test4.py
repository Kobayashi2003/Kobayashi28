import pickle
from pickle import PickleBuffer

class ZeroCopyByteArray(bytearray):

    def __reduce_ex__(self, protocol):
        if protocol >= 5:
            return type(self)._reconstruct, (PickleBuffer(self),), None
        else:
            # PickleBuffer is forbidden with pickle protocols <= 4.
            return type(self)._reconstruct, (bytearray(self),)

    @classmethod
    def _reconstruct(cls, obj):
        with memoryview(obj) as m:
            # Get a handle over the original buffer object
            obj = m.obj
            if type(obj) is cls:
                # Original buffer object is a ZeroCopyByteArray, return it
                # as-is.
                return obj
            else:
                return cls(obj)

@lambda _:_()
def test1():
    b = ZeroCopyByteArray(b"abc")
    data = pickle.dumps(b, protocol=5)
    new_b = pickle.loads(data)
    print(b == new_b)  # True
    print(b is new_b)  # False: a copy was made


@lambda _:_()
def test2():
    b = ZeroCopyByteArray(b"abc")
    buffers = []
    data = pickle.dumps(b, protocol=5, buffer_callback=buffers.append)
    new_b = pickle.loads(data, buffers=buffers)
    print(b == new_b)  # True
    print(b is new_b)  # True: no copy was made