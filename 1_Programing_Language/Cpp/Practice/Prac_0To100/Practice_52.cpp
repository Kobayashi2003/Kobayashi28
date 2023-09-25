// 先建立一个点类Point，包含数据成员x，y（坐标点）。
// 以它为基类，派生出圆类Circle，增加数据成员radius（半径），
// 再以Cirlcle类为直接基类，派生出圆柱体类Cylinder，再增加数据成员height（高）。要求：
// （1）每个类都有构造函数、用于从键盘获取数据的成员函数set()，用于显示数据的成员函数display()。
// （2）用虚函数输出各类对象信息。

#include<iostream>

using namespace std;

class Point {
protected :
    float x, y;
public :
// constructor and destructor
    Point(float _x = 0.0, float _y = 0.0) : x(_x), y(_y) {}
    virtual ~Point() {}
// public methods
    virtual Point & set();
    virtual Point & display();
};

Point & Point::set() {
    cout << "please input the coordinate: ";
    cin >> x >> y;
    return *this;
}

Point & Point::display() {
    cout << "x: " << x << ", y: " << y << endl;
    return *this;
}

class Circle : public Point {
protected :
    float radius;
public :
// constructor and destructor
    Circle(float _x, float _y, float _radius = 1.0) : Point(_x, _y), radius(_radius) {}
    virtual ~Circle() {}

    virtual Circle & set() {
        cout << "please input the coordinate and the radius: ";
        cin >> x >> y >> radius;
        return *this;
    }
    virtual Circle & display() {
        cout << "x: " << x << ", y: " << y << ", radius: " << radius << endl;
        return *this;
    }
};

class Cylinder : public Circle {
protected :
    float height;
public :
// constructor and destructor
    Cylinder(float _x, float _y, float _radius, float _height = 1.0) : Circle(_x, _y, _radius), height(_height) {}
    ~Cylinder() {}

// public methods
    Cylinder & set() {
        cout << "please input the coordinate and the radius and the height:";
        cin >> x >> y >> radius >> height;
        return *this;
    }
    Cylinder & display() {
        cout << "x: " << x << ", y: " << y << ", radius: " << radius << ", height: " << height << endl;
        return *this;
    }
};

int main() {

    return 0;
}