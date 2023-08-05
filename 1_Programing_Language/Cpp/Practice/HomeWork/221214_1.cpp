#include <iostream>

using std::istream;
using std::ostream;

class Point {
protected:
	double _x; double _y;
public:
	Point() = default;

	friend istream& operator>>(istream &is, Point &p) {
		is >> p._x >> p._y;
		return is;
	}

	friend ostream& operator<<(ostream &os, const Point &p) {
		os << "Point{coordinates(" << p._x << "," << p._y << ")}" << std::endl;
		return os;
	}
};

class Rectangle :public Point {
protected:
	double _length; double _width;

public:
	Rectangle() = default;

	friend istream& operator>>(istream &is, Rectangle &r) {
		is >> r._x >> r._y >> r._length >> r._width;
		return is;
	}

	friend ostream& operator<<(ostream &os, Rectangle &r) {
		os << "Rectangle{lower-left-coordinates(" << r._x << "," << r._y << ");size(" << r._length << "," << r._width << ")}" << std::endl;
		return os;
	}
};

class Cuboid :public Rectangle {
protected:
	double _height;
public:
	Cuboid() = default;
	friend istream& operator>>(istream &is, Cuboid &c) {
		is >> c._x >> c._y >> c._length >> c._width >> c._height;
		return is;
	}

	friend ostream& operator<<(ostream &os, Cuboid &c) {
		os << "Cuboid{lower-left-coordinates(" << c._x << "," << c._y << ");size(" << c._length << "," << c._width << "," << c._height << ")}" << std::endl;
		return os;
	}
};


int main() {
	Point point;
	std::cin >> point;
	std::cout << point;
	Rectangle rect;
	std::cin >> rect;
	std::cout << rect;
	Cuboid cuboid;
	std::cin >> cuboid;
	std::cout << cuboid;
	//派生类Cuboid向基类Point或Rectangle对象的引用赋值
	Point& point_new = cuboid;
	std::cout << point_new;
	Rectangle& rect_new = cuboid;
	std::cout << rect_new;
	return 0;
}