# 自增（自减）运算符的重载



```cpp
#include <iostream>

using std::cout;
using std::endl;

class Number {
public:
    int num;
    Number() : num(0) {}
    Number(int n) : num(n) {}

    // ++ Number (先自增后使用) 规定了前自增运算符作为一元运算符
    Number& operator++() { // 这个引用，表示该运算有可能有后续操作
        num++;
        return *this;
    }

    // Number ++ (后自增先使用) 规定了后自增运算符作为二元运算符
    Number operator++(int) { // 此处不使用引用，因为后自增运算后的结果不能够作为左值
        Number temp = *this;
        num++;
        return temp;
    }

    friend std::ostream& operator<<(std::ostream& out, const Number& n) {
        out << n.num;
        return out;
    }
};

int main() {
    Number n1(10);
    Number n2(10);

    cout << n1++ << endl;
    cout << n1 << endl;

    cout << ++n2 << endl;
    cout << n2 << endl;

    return 0;
}
```


[参考](https://zhuanlan.zhihu.com/p/95427571#:~:text=%E4%B8%BA%E4%BA%86%E5%8C%BA%E5%88%86%E6%89%80%E9%87%8D%E8%BD%BD%E7%9A%84%E6%98%AF%E5%89%8D%E7%BD%AE%E8%BF%90%E7%AE%97%E7%AC%A6%E8%BF%98%E6%98%AF%E5%90%8E%E7%BD%AE%E8%BF%90%E7%AE%97%E7%AC%A6%EF%BC%8CC%2B%2B%E8%A7%84%E5%AE%9A%EF%BC%9A%20-%20%E5%89%8D%E7%BD%AE%E8%BF%90%E7%AE%97%E7%AC%A6%E4%BD%9C%E4%B8%BA%20%E4%B8%80%E5%85%83%20%E8%BF%90%E7%AE%97%E7%AC%A6%E9%87%8D%E8%BD%BD%EF%BC%8C%E9%87%8D%E8%BD%BD%E4%B8%BA%E6%88%90%E5%91%98%E5%87%BD%E6%95%B0%E7%9A%84%E6%A0%BC%E5%BC%8F%E5%A6%82%E4%B8%8B%EF%BC%9A%20T%20%26,operator%2B%2B%28%29%3B%20%2F%2F%20%E5%89%8D%E7%BD%AE%E8%87%AA%E5%A2%9E%E8%BF%90%E7%AE%97%E7%AC%A6%E7%9A%84%E9%87%8D%E8%BD%BD%E5%87%BD%E6%95%B0%EF%BC%8C%E5%87%BD%E6%95%B0%E5%8F%82%E6%95%B0%E6%98%AF%E7%A9%BA%20T%20%26%20operator--%28%29%3B%20%2F%2F%20%E5%89%8D%E7%BD%AE%E8%87%AA%E5%87%8F%E8%BF%90%E7%AE%97%E7%AC%A6%E7%9A%84%E9%87%8D%E8%BD%BD%E5%87%BD%E6%95%B0%EF%BC%8C%E5%87%BD%E6%95%B0%E5%8F%82%E6%95%B0%E6%98%AF%E7%A9%BA)