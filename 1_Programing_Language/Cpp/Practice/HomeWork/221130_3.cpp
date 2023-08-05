#include <iostream>

class Vehicle {
protected:
    int weight = 0;
public:
    Vehicle(int w) : weight(w) { std::cout << "init Vehicle" << std::endl; }
    void setWeight(int w) { std::cout << "reset weight" << std::endl; weight = w; }
    virtual void display() const {
        std::cout << "weight:" << weight << "t";
    }
};

class Car : virtual public Vehicle {
protected:
    int aird = 0;
public:
    Car(int w, int a) : Vehicle(w), aird(a) { std::cout << "init Car" << std::endl; }
    void setAird(int a) { std::cout << "reset aird" << std::endl; aird = a; }
    virtual void display() const {
        Vehicle::display();
        std::cout << "aird:" << aird << "CC";
    }
};

class Boat : virtual public Vehicle {
protected:
    float tonnage = 0;
public:
    Boat(int w, float t) : Vehicle(w), tonnage(t) { std::cout << "init Boat" << std::endl; }
    void setTonnage(float t) { std::cout << "reset tonnage" << std::endl; tonnage = t; }
    virtual void display() const {
        Vehicle::display();
        std::cout << "tonnage:" << tonnage << "t";
    }
};

class AmphibianCar : public Car, public Boat {
public:
    AmphibianCar(int w, int a, float t) : Vehicle(w), Car(w, a), Boat(w, t) { std::cout << "init AmphibianCar" << std::endl; }
    virtual void display() const {
        Vehicle::display();
        std::cout << ",";
        std::cout << "aird:" << aird << "CC" << "," << "tonnage:" << tonnage << "t" << std::endl;
    }
};


int main () {

    int w; std::cin >> w;
    int a; std::cin >> a;
    float t; std::cin >> t;

    AmphibianCar ac(w, a, t);
    ac.display();

    int rw; std::cin >> rw;
    int ra; std::cin >> ra;
    float rt; std::cin >> rt;

    ac.setWeight(rw);
    ac.setAird(ra);
    ac.setTonnage(rt);

    ac.display();

    return 0;
}