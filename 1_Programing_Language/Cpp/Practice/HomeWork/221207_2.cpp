#include <iostream>

using namespace std;

class Area {
protected:
	double height, weight;
public:
	Area() = default;
	Area(double h, double w) {
		height = h; weight = w;
	}
	virtual double CalArea() = 0;
};

class Rectangle : public Area
{
public:
	Rectangle() = default;
	Rectangle(double h, double w) : Area(h, w) {}
	void SetRectangle(double h, double w) {
		height = h; weight = w;
	}
	virtual double CalArea() { return height * weight; }
};


class Triangle : public Area
{
public:
	Triangle() = default;
	Triangle(double h, double w) : Area(h, w) {}
	void SetTriangle(double h, double w) {
		height = h; weight = w;
	}
	virtual double CalArea() { return height * weight / 2; }
};

int main()
{
	double h, w;
	Rectangle  A;
	Triangle   B;
	cin >> h >> w;
	A.SetRectangle(h, w);
	B.SetTriangle(h, w);
	cout << A.CalArea() << endl;
	cout << B.CalArea() << endl;
	return 0;
}