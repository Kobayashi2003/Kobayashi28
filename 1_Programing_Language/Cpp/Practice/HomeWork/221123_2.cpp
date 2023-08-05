#include <iostream>
#include<math.h>

class Rectangle;

class Point {
private:
    double _x;
    double _y;
public:
    Point(double x, double y) : _x(x), _y(y) {}
    friend class Rectangle;
};

class Rectangle :public Point {
private:
	double _l;
	double _h;
public:
    Rectangle(double x, double y, double l, double h) : Point(x, y), _l(l), _h(h) {}
	int position(const Point& src);//点在矩形的4条边或4个角，返回0；点在矩形内部，返回1，点在矩阵外部，返回-1
	int position(const Rectangle& src);//矩阵有重叠部分（包括相交和内离），返回1；矩形无重叠时，矩形相切(包括角重叠)返回0，矩形外离返回-1
};

int Rectangle::position(const Point& src) {
    if (src._x == _x || src._x == _x + _l) {
        if (src._y >= _y && src._y <= _y + _h) {
            return 0;
        }
        else {
            return -1;
        }
    }
    else if (src._y == _y || src._y == _y + _h) {
        if (src._x >= _x && src._x <= _x + _l) {
            return 0;
        }
        else {
            return -1;
        }
    }
    else if (src._x > _x && src._x < _x + _l && src._y > _y && src._y < _y + _h) {
        return 1;
    }
    else {
        return -1;
    }
}

int Rectangle::position(const Rectangle& src) {
    if (src._x > _x + _l || src._y > _y + _h || src._x + src._l < src._x || src._y + src._h < src._y) {
        return -1;
    } else if (src._x + src._l == _x && src._y >= _y - src._h && src._y <= _y + _h) {
        return 0;
    } else if (src._x == _x + _l && src._y >= _y - src._h && src._y <= _y + _h) {
        return 0;
    } else if (src._y + src._h == _y && src._x >= _x - src._l && src._x <= _x + _l) {
        return 0;
    } else if (src._y == _y + _h && src._x >= _x - src._l && src._x <= _x + _l) {
        return 0;
    } else {
        return 1;
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