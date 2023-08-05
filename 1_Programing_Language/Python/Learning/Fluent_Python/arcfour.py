def arcfour(key, in_bytes, loops=20):

    kbox = bytearray(256)
    for i, car in enumerate(key): 
        kbox[i] = car 
    j = len(key)
    for i in range(j, 256):
        kbox[i] = kbox[i -j]

    # [1] init sbox
    sbox = bytearray(range(256))

    j = 0
    for k in range(loops):
        for i in range(256):
            j = (j + sbox[i] + kbox[i]) & 255 # j = (j + sbox[i] + kbox[i]) % 256
            sbox[i], sbox[j] = sbox[j], sbox[i]

    i = j = 0
    out_bytes = bytearray()
    
    for car in in_bytes:
        i = (i + 1) & 255
        # [2] upset sbox
        j = (j + sbox[i]) & 255 
        sbox[i], sbox[j] = sbox[j], sbox[i]
        # [3] get t
        t = (sbox[i] + sbox[j]) & 255
        k = sbox[t]
        car ^= k
        out_bytes.append(car)

    return out_bytes


def test():
    from time import time
    clear = bytearray(b'1234567890' * 1000000)
    t0 = time()
    cipher = arcfour(b'key', clear)
    print('elapsed time: %.2fs' % (time() - t0))
    result = arcfour(b'key', cipher)
    assert result == clear, '%r != %r' % (result, clear)
    print('elapsed time: %.2fs' % (time() - t0))
    print('OK')


if __name__ == '__main__':
    test()
