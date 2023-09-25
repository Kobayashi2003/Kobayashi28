#include<iostream>

using namespace std;

struct Data {
    mutable int num;
    // int num; 
};

void function(const Data &data) {
    data.num += 1;
    cout << data.num << endl;
}

int main() {
    Data data;
    data.num = 0;
    function(data);
    return 0;
}