#include <iostream>
#include<math.h>

class Circle;
class Square;

class Point {
private:
    double _x;
    double _y;
public:
    Point(double x, double y) : _x(x), _y(y) {}
    friend class Circle;
    friend class Square;
    void show() const {
        std::cout << "(" << _x << "," << _y << ")";
    }
};

class Circle :public Point {
private:
	double _radius;
public:
    Circle(double _x, double _y, double radius) : Point(_x, _y), _radius(radius) {}
	//......
    friend std::ostream& operator<<(std::ostream& os, const Circle& src) {
        src.show();
        std::cout << " ";
        std::cout << src._radius;
        return os;
    }
};

class Square :public Point {
private:
	double _l;
public:
    Square(double _x, double _y, double l) : Point(_x, _y), _l(l) {}
	Circle inscribed_circle();//生成对应的内切圆对象
	Circle circumscribed_circle();//生成对应的外接圆对象
};

Circle Square::inscribed_circle() {
    return Circle(_x + _l / 2, _y + _l / 2, _l / 2);
}

Circle Square::circumscribed_circle() {
    return Circle(_x + _l / 2, _y + _l / 2, _l / sqrt(2));
}

int main() {
	double x, y, length;
	//输入圆的参数
	std::cin >> x >> y >> length;
	Square square1(x, y, length);
	std::cout << "inscribed circle: " << square1.inscribed_circle() << std::endl;
	std::cout << "circumscribed circle: " << square1.circumscribed_circle() << std::endl;
	return 0;
}