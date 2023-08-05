#include <iostream>

class CVehicle {
protected:
    int max_speed;
    int speed;
    int weight;
public:
    CVehicle (int ms, int s, int w) : max_speed(ms), speed(s), weight(w) {}
    void display()const {
        std::cout << "max_speed:" << max_speed << std::endl;
        std::cout << "speed:" << speed << std::endl;
        std::cout << "weight:" << weight << std::endl;
    }
};

class CBicycle : public CVehicle {
protected:
    int height;
public:
    CBicycle(int ms, int s, int w, int h) :
        CVehicle(ms, s, w), height(h) {}
    void CB_display() const {
        display();
        std::cout << "height:" << height << std::endl;
    }
};

class CMotocar : public CVehicle {
protected:
    int seat_num;
public:
    CMotocar(int ms, int s, int w, int sn) :
        CVehicle(ms, s, w), seat_num(sn) {}
    void CM_display() const {
        display();
        std::cout << "seat_num:" << seat_num << std::endl;
    }
};

class CMotocycle : public CBicycle, public CMotocar {
public:
    CMotocycle(int ms, int s, int w, int h, int sn) :
        CBicycle(ms, s, w, h), CMotocar(ms, s, w, sn) {}
    void CBM_display() const {
        CBicycle::display();
        std::cout << "height:" << height << std::endl;
        std::cout << "seat_num:" << seat_num << std::endl;
    }
};

int main() {

    int ms, s, w; std::cin >> ms >> s >> w;
    int h; std::cin >> h;
    int sn; std::cin >> sn;

    CVehicle v(ms, s, w);
    std::cout << "Vehicle:" << std::endl;
    v.display();
    std::cout << std::endl;

    CBicycle b(ms, s, w, h);
    std::cout << "Bicycle:" << std::endl;
    b.CB_display();
    std::cout << std::endl;

    CMotocar m(ms, s, w, sn);
    std::cout << "Motocar:" << std::endl;
    m.CM_display();
    std::cout << std::endl;

    CMotocycle mb(ms, s, w, h, sn);
    std::cout << "Motocycle:" << std::endl;
    mb.CBM_display();

    return 0;
}