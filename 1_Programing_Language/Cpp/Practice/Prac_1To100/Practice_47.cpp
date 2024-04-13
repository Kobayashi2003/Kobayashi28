#include<iostream>

double hmean(double a, double b) {
    if(a == -b) {
        throw "bad hmean() arguments: a = -b not allowed";
    }
    return 2.0 * a * b / (a + b);
}

int main() {
    double x, y, z;
    std::cout << "Enter two numbers: ";
    while(std::cin >> x >> y) {
        try {// start of try block
            z = hmean(x, y);
        }// end of try block
        catch(const char * s) {// start of exception handler
            std::cout << s << std::endl;
            std::cout << "Enter a new pair of numbers: ";
            continue;
        }// end of exception handler
        std::cout << "Harmonic mean of " << x << " and " << y << " is "  << z << std::endl;
        std::cout << "Enter next set of numbers <q to quit>"; // cin 输入失败后自动返回 false
    }
    std::cout << "Bye!" << std::endl;
    return 0;
}