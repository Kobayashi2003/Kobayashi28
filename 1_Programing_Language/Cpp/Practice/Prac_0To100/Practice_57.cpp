#include<iostream>

using namespace std;

class Point {
private:
    float _x, _y;
public:
    /* constructor */
    Point(float x, float y) : _x(x), _y(y){}
    /* destructor */
    virtual ~Point() {}
};

class Circle : public Point  {
private:
    float _radius;
public:
    /* constructor */
    Circle(float x, float y, float radius) : Point(x, y), _radius(radius) {}
    /* destructor */
    virtual ~Circle() {}
    float square() const {
        return 3.14f * _radius * _radius;
    }
};

class Cone : public Circle {
private:
    float _height;
public:
    /* constructor */
    Cone(float x, float y, float radius, float height) : Circle(x, y, radius), _height(height) {}
    /* destructor */
    ~Cone() {}
    float volume() const {
        return _height * square() / 3;
    }
};

int main() {
    return 0;
}