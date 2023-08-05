// 快速幂

long long pow(long long x, int n) {
    if (n == 0) return 1;
    if (n == 1) return x;
    if (n % 2 == 0) {
        long long t = pow(x, n / 2);
        return t * t;
    } else {
        long long t = pow(x, n / 2);
        return t * t * x;
    }
}