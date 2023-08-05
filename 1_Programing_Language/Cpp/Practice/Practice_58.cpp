#include<iostream>

using namespace std;

class Shape {
public:
    virtual void showData() = 0;
    virtual double getArea() = 0;
    virtual double getVolume() = 0;
};

class TwoDimShape : public Shape {
public:
    double _area;
};

class ThreeShape : public Shape {
public:
    double _volume;
};

// class Elipse : public TwoDimShape {};

// class Circle : public Elipse {};

class Rectangle : public TwoDimShape {
private:
    double _x, _y;
public:
    Rectangle(double x, double y) {
        _x = x; _y = y;
    }
    ~Rectangle() {}
    virtual void showData() {
        cout << "x: " << _x << "y: " << _y << endl;
    }
    virtual double getArea() {
        return _x * _y;
    }
    virtual double getVolume() {return 0.0;}
};

// class Triangle : public TwoDimShape {};

// class Ball : public ThreeShape {};

// class Cylinder : public ThreeShape {};

class RectangularParallelepiped : public ThreeShape {
private:
    double _x, _y, _z;
public:
    RectangularParallelepiped(double x, double y, double z) {
        _x = x; _y = y; _z = z;
    }
    ~RectangularParallelepiped() {}
    virtual void showData() {
        cout << "x: " << _x << " y: " << _y << " z: " << _z << endl;
    }
    virtual double getArea() {
        return _x*_y + _y*_z + _z*_y;
    }
    virtual double getVolume() {
        return _x * _y * _z;
    }
};


int main() {
    Rectangle A(1.0, 3.3);
    cout << A.getArea() << endl;
    return 0;
}