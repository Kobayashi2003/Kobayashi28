// 欧几里得算法

// 定理：若 M>N ，则 M mod N < M/2 

long long gcd(long m, long n) {
    while(n != 0) {
        long rem = m % n;
        m = n;
        n = rem;
    }
    return m;
}