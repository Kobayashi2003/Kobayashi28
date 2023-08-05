#include <iostream>
#define _USE_MATH_DEFINES
#include <cmath>
using namespace std;

class Triangle {
private:
    int _x1, _y1, _x2, _y2, _x3, _y3, _a, _b;

    double calArea (int x1, int y1, int x2, int y2, int x3, int y3) const {
        return abs((x1 * y2 + x2 * y3 + x3 * y1 - x1 * y3 - x2 * y1 - x3 * y2) / 2.0);
    }

    double calSide (int x1, int y1, int x2, int y2) const {
        return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
    }

public:

    double ab, ac, bc;

    Triangle(int x1, int y1, int x2, int y2, int x3, int y3, int a, int b) {
        _x1 = x1;
        _y1 = y1;
        _x2 = x2;
        _y2 = y2;
        _x3 = x3;
        _y3 = y3;
        _a = a;
        _b = b;

        ab = calSide(x1, y1, x2, y2);
        ac = calSide(x2, y2, x3, y3);
        bc = calSide(x3, y3, x1, y1);
    }

    int isLocated() const {
        if (calArea(_x1, _y1, _x2, _y2, _x3, _y3) < calArea(_x1, _y1, _x2, _y2, _a, _b) + calArea(_x1, _y1, _x3, _y3, _a, _b) + calArea(_x2, _y2, _x3, _y3, _a, _b)) {
            return -1;
        }
        else if (calSide(_x1, _y1, _a, _b) + calSide(_x2, _y2, _a, _b) == calSide(_x1, _y1, _x2, _y2) ||
                 calSide(_x1, _y1, _a, _b) + calSide(_x3, _y3, _a, _b) == calSide(_x1, _y1, _x3, _y3) ||
                 calSide(_x2, _y2, _a, _b) + calSide(_x3, _y3, _a, _b) == calSide(_x2, _y2, _x3, _y3)) {

            // cout << calSide(_x1, _y1, _a, _b) + calSide(_x2, _y2, _a, _b) << endl;
            // cout << calSide(_x1, _y1, _a, _b) + calSide(_x3, _y3, _a, _b) << endl;
            // cout << calSide(_x2, _y2, _a, _b) + calSide(_x3, _y3, _a, _b) << endl;
            return 0;
        }
        else {
            return 1;
        }
    }

    double calPerimeter(double l1, double l2, double l3) const {
        return l1 + l2 + l3;
    }

    double calArea(double l1, double l2, double l3) const {
        // heron
        double p = (l1 + l2 + l3) / 2.0;
        return sqrt(p * (p - l1) * (p - l2) * (p - l3));
    }

    int isCollinear(double l1, double l2, double l3) const {
        if (l1 + l2 <= l3 || l1 + l3 <= l2 || l2 + l3 <= l1) {
            return 0;
        } else {
            return 1;
        }
    }
};

int main()
{
    int x1, y1, x2, y2, x3, y3, a, b;
    std::cin >> x1 >> y1 >> x2 >> y2 >> x3 >> y3 >> a >> b;
    Triangle t(x1, y1, x2, y2, x3, y3, a, b);
    int isTriangle = t.isCollinear(t.ab, t.ac, t.bc);
    // 如果三点共线，则输出0
    if (isTriangle == 0)
    {
        cout << isTriangle << endl;
        return 0;
    }
    // 如果三点不共线，则输出1，并继续输出周长/面积/点(a, b)在三角形的位置
    double Perimeter = t.calPerimeter(t.ab, t.ac, t.bc);
    double area = t.calArea(t.ab, t.ac, t.bc);
    int location = t.isLocated();
    cout.precision(4);
    cout << isTriangle << endl;
    cout << Perimeter << endl;
    cout << area << endl;
    cout << location << endl;
    return 0;
}
