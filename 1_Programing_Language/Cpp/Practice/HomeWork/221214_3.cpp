#include <iostream>

using namespace std;

class Shape {
public:
	virtual void load() = 0;
	virtual void display_shape_name() = 0;
	virtual void display() = 0;
	virtual double get_area() = 0;
};

class Point : public Shape {
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
		cout << "coordinates:(" << p._x << "," << p._y << ")" << std::endl;
	}

	virtual double get_area() {
		return 0;
	}

	virtual void display_shape_name() {
		cout << "shape_name:Point" << endl;
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
		cout << "lower-left-coordinates:(" << r._x << "," << r._y << ")" << endl << "size:(" << r._length << "," << r._width << ")" << std::endl;
	}

	virtual double get_area() {
		return _length * _width;
	}

	virtual void display_shape_name() {
		cout << "shape_name:Rectangle" << endl;
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
		cout << "lower-left-coordinates:(" << c._x << "," << c._y << ")" << endl << "size:(" << c._length << "," << c._width << "," << c._height << ")" << std::endl;
	}

	virtual double get_area() {
		return 2 * (_length*_width + _length * _height + _width * _height);
	}

	virtual void display_shape_name() {
		cout << "shape_name:Cuboid" << endl;
	}

};


int main() {
	Point point; Rectangle rectangle; Cuboid cuboid;

	Shape* p_shape;
	p_shape = &point;
	p_shape->load();
	p_shape->display_shape_name();
	p_shape->display();
	std::cout << "area:" << p_shape->get_area() << std::endl;

	p_shape = &rectangle;
	p_shape->load();
	p_shape->display_shape_name();
	p_shape->display();
	std::cout << "area:" << p_shape->get_area() << std::endl;

	p_shape = &cuboid;
	p_shape->load();
	p_shape->display_shape_name();
	p_shape->display();
	std::cout << "area:" << p_shape->get_area() << std::endl;

	return 0;
}