# C++实现类与类之间的简单关系

```cpp
class Wheel {
    int size;
public:
    Wheel(int sz) : size(sz) {}
    int getSz() { return size; }
};

class Vehicle {
    int weight;
public:
    Vehicle(int wt) : weight(wt) {}
};

class Car : public Vehicle {
    Wheel *wh;
public:
    Car(int wt, int sz) : Vehicle(wt), wh(nullptr) { wh = new Wheel(4); }
    int getSz() { return wh->getSz(); }
    ~Car() { delete wh; }
};

class DrivingSchool {
    Car coachCar[10];
public:
    static void Driver() { cout << "You can drive." << endl; }
};

class Driver {
    Car *car_ptr;
    int learnt;
public:
    Driver(Car *pc) : car_ptr(pc), learnt(0) {}
    void driverlearn() { DrivingSchool::Driver(); }
};

int main() {
    Car c = Car(10000, 5);
    Driver d = Driver(&c);

    d.driverlearn();
    return 0;
}
```