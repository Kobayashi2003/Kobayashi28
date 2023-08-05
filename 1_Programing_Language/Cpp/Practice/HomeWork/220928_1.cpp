#include <iostream>
#define _USE_MATH_DEFINES
#include <math.h>
using namespace std;

class Circle {
private:
    int _x, _y, _r, _a, _b;
public:
    Circle(int x, int y, int r, int a, int b) {
        _x = x;
        _y = y;
        _r = r;
        _a = a;
        _b = b;
    }
    
    int isLocated() {
        if (sqrt(pow(_x - _a, 2) + pow(_y - _b, 2)) < _r) {
            return 1;
        } else if (sqrt(pow(_x - _a, 2) + pow(_y - _b, 2)) == _r) {
            return 0;
        } else {
            return -1;
        }

    }
    double calCircumference() {
        return 2 * M_PI * _r;
    }
    double calArea() {
        return M_PI * _r * _r;
    }
};

int main()
{
    int x, y, r, a, b;
    std::cin >> x >> y >> r >> a >> b;
    Circle c(x, y, r, a, b);
    double circumference = c.calCircumference();
    double area = c.calArea();
    int location = c.isLocated();
    cout << circumference << endl;
    cout << area << endl;
    cout << location << endl;
    return 0;
}