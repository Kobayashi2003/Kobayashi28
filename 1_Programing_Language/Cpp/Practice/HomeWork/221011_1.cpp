#include <iostream>

class Rectangle {
public:
    int x, y, w, h;
    Rectangle(int _x, int _y, int _w, int _h) {
        x = _x;
        y = _y;
        w = _w;
        h = _h;
    }
    Rectangle(int _x=0, int _y=0, int _s=1) {
        x = _x;
        y = _y;
        w = _s;
        h = _s;
    }
    void show();
};


bool isCollide(Rectangle a, Rectangle b){
    if (
            (
                (a.x <= b.x && a.x + a.w > b.x) &&
                (
                    (a.y >= b.y && a.y < b.y + b.h) || (a.y < b.y && a.y + a.h >= b.y)
                )
            ) ||
            (
                (b.x <= a.x && b.x + b.w > a.x) &&
                (
                    (b.y >= a.y && b.y < a.y + a.h) || ((b.y < a.y) && (b.y + b.h >= a.y))
                )
            )
        ) {
            return true;
        }
    return false;
}


Rectangle initRectangle(int paramNum){
    if (paramNum == 4) {
        int x, y, w, h;
        std::cin >> x >> y >> w >> h;
        return Rectangle(x, y, w, h);
    } else if (paramNum == 3) {
        int x, y, s;
        std::cin >> x >> y >> s;
        return Rectangle(x, y, s);
    } else if (paramNum == 2) {
        int x, y;
        std::cin >> x >> y;
        return Rectangle(x, y);
    }
    return Rectangle();
}


int main() {
    int n1, n2;
    std::cin >> n1 >> n2;
    Rectangle a = initRectangle(n1);
    Rectangle b = initRectangle(n2);

    // a.show();
    // b.show();

    std::cout << isCollide(a, b) << std::endl;

    return 0;
}