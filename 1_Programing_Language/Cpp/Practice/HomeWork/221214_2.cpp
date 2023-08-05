#include <iostream>

using namespace std;

class Point {
protected:
	double _x; double _y;
public:
	Point() = default;

	virtual void load() {
		Point &p = *this;
		cin >> p._x >> p._y;
	}

	virtual void display() {
		Point &p = *this;
		cout << "Point{coordinates(" << p._x << "," << p._y << ")}" << std::endl;
	}

	virtual double get_area() {
        return 0;
    } 

};

class Rectangle :public Point {
protected:
	double _length; double _width;

public:
	Rectangle() = default;

	virtual void load() {
		Rectangle& r = *this;
		cin >> r._x >> r._y >> r._length >> r._width;
	}

	virtual void display() {
		Rectangle& r = *this;
		cout << "Rectangle{lower-left-coordinates(" << r._x << "," << r._y << ");size(" << r._length << "," << r._width << ")}" << std::endl;
	}

	virtual double get_area() {
		return _length * _width;
	}

};

class Cuboid :public Rectangle {
protected:
	double _height;
public:
	Cuboid() = default;

	virtual void load() {
		Cuboid& c = *this;
		cin >> c._x >> c._y >> c._length >> c._width >> c._height;
	}

	virtual void display() {
		Cuboid& c = *this;
		cout << "Cuboid{lower-left-coordinates(" << c._x << "," << c._y << ");size(" << c._length << "," << c._width << "," << c._height << ")}" << std::endl;
	}

	virtual double get_area() {
		return 2 * (_length*_width + _length*_height + _width*_height);
	}
};


int main() {
	Cuboid cuboid;
	cuboid.load();
	cuboid.display();
	std::cout << cuboid.get_area() << std::endl;

	Point& point_new = cuboid;
	point_new.display();
	std::cout << point_new.get_area() << std::endl;

	Rectangle& rect_new = cuboid;
	rect_new.display();
	std::cout << rect_new.get_area() << std::endl;
	return 0;
}