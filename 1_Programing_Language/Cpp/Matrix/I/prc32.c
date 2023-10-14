void move(int n, int a, int b) {
    printf("move %d from %c to %c\n", n, a+'a', b+'a');
}

void hanoi(int n, int a, int b, int c) {
    if (n == 1) {
        move(1, a, c);
    } else {
        hanoi(n - 1, a, c, b);
        move(n, a, c);
        hanoi(n - 1, b, a, c);
    }
}