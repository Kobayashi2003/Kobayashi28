#include <iostream>
#define _USE_MATH_DEFINES
#include <math.h>
using namespace std;

class Rectangle {
private:
    int _x, _y, _w, _h, _a, _b;
public:
    Rectangle(int x, int y, int w, int h, int a, int b) {
        _x = x;
        _y = y;
        _w = w;
        _h = h;
        _a = a;
        _b = b;
    }
    int isLocated() {
        if (_a > _x && _a < _x + _w && _b > _y && _b < _y + _h) {
            return 1;
        } else if (_a == _x + _w || _a == _x || _b == _y + _h || _b == _y) {
            return 0;
        } else {
            return -1;
        }
    }
    int calArea() {
        return _w * _h;
    }
    int calPerimeter() {
        return 2 * (_w + _h);
    }
};


int main()
{
    int x, y, w, h, a, b;
    std::cin >> x >> y >> w >> h >> a >> b;
    Rectangle r(x, y, w, h, a, b);
    double perimeter = r.calPerimeter();
    double area = r.calArea();
    int location = r.isLocated();
    cout << perimeter << endl;
    cout << area << endl;
    cout << location << endl;
}