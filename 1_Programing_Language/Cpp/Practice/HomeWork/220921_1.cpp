#include <iostream>

struct complex {
    int x;
    int y;
};

complex add(complex & cx_a, complex & cx_b) {
    complex cx;
    cx.x = cx_a.x + cx_b.x;
    cx.y = cx_a.y + cx_b.y;
    return cx;
}

complex sub(complex & cx_a, complex & cx_b) {
    complex cx;
    cx.x = cx_a.x - cx_b.x;
    cx.y = cx_a.y - cx_b.y;
    return cx;
}

complex mul(complex & cx_a, complex & cx_b) {
    complex cx;
    cx.x = cx_a.x * cx_b.x - cx_a.y * cx_b.y;
    cx.y = cx_a.x * cx_b.y + cx_a.y * cx_b.x;
    return cx;
}

void print(complex & cx) {
    std::cout << cx.x;
    if (cx.y >= 0) {
        std::cout << "+";
    }
    std::cout << cx.y << "i" << std::endl;
}

int main()
{
    complex cx_a;
    std::cin >> cx_a.x >> cx_a.y;

    complex cx_b;
    std::cin >> cx_b.x >> cx_b.y;

    complex cx_c = add(cx_a, cx_b);
    complex cx_d = sub(cx_a, cx_b);
    complex cx_e = mul(cx_a, cx_b);

    print(cx_c);
    print(cx_d);
    print(cx_e);

    return 0;
}