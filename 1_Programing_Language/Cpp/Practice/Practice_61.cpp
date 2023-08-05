#include <iostream>

using namespace std;

template<typename T>
class DataStore {
private:
    enum {LEN = 10};
    T data[LEN];
    int loc;
public:
    DataStore() {
        loc = 0;
    }
    ~DataStore() {}
    int insert(T elt);
    int Find(T elt);
    int NumElts();
    T &GetData(int n);
};

template<typename T>
int DataStore<T>::insert(T elt) {
    if (loc == 10) {
        return 0;
    }
    data[loc] = elt;
    loc += 1;
    return loc;
}


template<typename T>
int DataStore<T>::Find(T elt) {
    for (int i = 0; i < loc; ++i) {
        if (data[i] == elt) {
            return i;
        }
    }
    return -1;
}


template<typename T>
int DataStore<T>::NumElts() {
    return loc;
}


template<typename T>
T & DataStore<T>::GetData(int n) {
    if (n >= loc || loc + n < 0) {
        cout << "overflow" << endl;
        // 我想要优雅地返回空引用
    }
    return (n >= 0 ? data[n] : data[loc + n]);
}


template<typename T>
using DS = DataStore<T>;


int main() {

    DS <int> data;
    data.insert(0);
    data.insert(7);
    data.insert(2);
    data.insert(1);

    cout << data.GetData(-1) << data.Find(7) << data.NumElts() << endl;

    return 0;
}