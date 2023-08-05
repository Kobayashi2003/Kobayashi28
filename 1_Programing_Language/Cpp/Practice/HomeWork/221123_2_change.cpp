#include <iostream>
#include <cmath>

class Rectangle;

class Point {
public:
    double _x = .0, _y = .0;
    Point(double x, double y) : _x(x), _y(y) {}
};

class Rectangle {
private:
    Point _p;
    double _l, _h;
public:
    Rectangle(double x, double y, double l, double h) : _p(x, y), _l(l), _h(h) {}
    Rectangle(double l, double h) : _p(.0, .0), _l(l), _h(h) {}

    // the position of a point
    int position(const Point& src);
    // the position of a rectangle
    int position(const Rectangle& src);
};

int Rectangle::position(const Point& src) {
    if (src._x == _p._x || src._x == _p._x + _l) {
        if (src._y >= _p._y && src._y <= _p._y + _h) 
            return 0;
        else 
            return -1;
    }
    else if (src._y == _p._y || src._y == _p._y + _h) {
        if (src._x >= _p._x && src._x <= _p._x + _l)
            return 0;
        else
            return -1;
    }
    else if (src._x > _p._x && src._x < _p._x + _l && src._y > _p._y && src._y < _p._y + _h)
        return 1;
    return -1;
}

int Rectangle::position(const Rectangle &src) {
    Rectangle tmp(_p._x - src._l, _p._y - src._h, _l + src._l, _h + src._h); // try to change the question to the position of a point
    if (tmp.position(src._p) == 1) {
        return 1;
    } else if (tmp.position(src._p) == 0) {
        return 0;
    } else {
        return -1;
    }
}

int main() {
	double x, y, l, h;
	//输入两个矩形
	std::cin >> x >> y >> l >> h;
	Rectangle rectangle1(x, y, l, h);
	std::cin >> x >> y >> l >> h;
	Rectangle rectangle2(x, y, l, h);
	//输入点
	std::cin >> x >> y;
	Point point1(x, y);
	std::cout << rectangle1.position(rectangle2) << std::endl;
	std::cout << rectangle1.position(point1) << std::endl;
	return 0;
}