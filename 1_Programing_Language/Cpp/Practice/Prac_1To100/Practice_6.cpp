#include<iostream>

using namespace std;

typedef int dataType;

class Box {
private :
    dataType data;
public :
    Box(dataType tData) {
        data = tData;
    }
    ~Box () {}

    friend void friendFun(Box &);
};

void friendFun(Box &box) {
    cout << box.data << endl;
}

int main() {
    Box box(1);
    friendFun(box);
    return 0;
}