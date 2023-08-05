#include <iostream>
#include<math.h>

class Circle;

class Point {
private:
    double _x;
    double _y;
public:
    Point(double x, double y) : _x(x), _y(y) {}
    friend class Circle;
};

class Circle :public Point {
private:
    double _radius;
public:
    Circle(double x, double y, double radius) : Point(x, y), _radius(radius) {}
    int    position(const Point& src);//如果点在圆上，返回0，点在圆外，返回-1，点在圆内，返回1
    double min_distance(const Point& src);//求点与圆的最短距离
};

int Circle::position(const Point& src) {
    double distance = sqrt(pow(src._x - _x, 2) + pow(src._y - _y, 2));
    if (distance == _radius) {
        return 0;
    }
    else if (distance > _radius) {
        return -1;
    }
    else {
        return 1;
    }
}


double Circle::min_distance(const Point& src) {
    double distance = sqrt(pow(src._x - _x, 2) + pow(src._y - _y, 2));
    return fabs(distance - _radius);
}

int main() {
	double x, y, radius;
	//输入圆的参数
	std::cin >> x >> y >> radius;
	Circle circle1(x, y, radius);
	//输入点的参数
	std::cin >> x >> y;
	Point point1(x, y);
	//判断点与圆的位置关系
	switch (circle1.position(point1))
	{
	case 0:
		std::cout << "on-circle" << std::endl; break;
	case 1:
		std::cout << "inside-circle" << std::endl; break;
	case -1:
		std::cout << "outside-circle" << std::endl;
	default:
		break;
	}
	std::cout << circle1.min_distance(point1) << std::endl;
	return 0;
}