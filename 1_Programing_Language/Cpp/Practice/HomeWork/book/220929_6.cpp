#include <iostream>

using namespace std;

class Rectangle {
private:
    int _length, _width, _height;
public:
    Rectangle(int length, int width, int height) : _length(length),
                                                   _width(width),
                                                   _height(height) {}
    int volume() const { return _height * _width * _length; }
};

int main() {

    int x, y, z;

    cin >> x >> y >> z;
    Rectangle r1(x, y, z);

    cin >> x >> y >> z;
    Rectangle r2(x, y, z);

    cin >> x >> y >> z;
    Rectangle r3(x, y, z);
    
    cout << "r1:" << r1.volume() << " r2:" << r2.volume() << " r3:" << r3.volume() << endl;
    return 0;
}