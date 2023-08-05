#include <iostream>

using namespace std;

class Rectangle{
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
    void show(){
        cout<<"x="<<x<<",y="<<y<<",w="<<w<<",h="<<h<<endl;
    }
};


class RectangleList{
private:

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


public:
    Rectangle* p;
    int N;

    RectangleList(int _N){
        N = _N;
        p = new Rectangle[N];
    }

    ~RectangleList(){
        delete [] p;
        cout << "RectangleList Deconstruct." << endl;
    }

    void showAll(){
        for (int i = 0; i < N; ++i) {
            p[i].show();
        }
    }

    bool isCollide(){
        for (int i = 0; i < N; ++i) {
            for (int j = i + 1; j < N; ++j) {
                if (isCollide(p[i], p[j])) {
                    return true;
                }
            }
        }
        return false;
    }
};


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


int main(){
    int N;
    cin >> N;
    RectangleList l(N);
    for (int i = 0; i < N; i++) {
        int paramNum;
        cin >> paramNum;
        l.p[i] = initRectangle(paramNum);
    }
    l.showAll();
    cout<<l.isCollide()<<endl;
}