#include <list>
#include <random>
#include <iostream>

using namespace std;

template <typename Object>
list<Object> intersection(const list<Object> &list1, const list<Object> &list2) {
    list<Object> intersection;
    auto iter1 = list1.begin(), iter2 = list2.begin();
    while (iter1 != list1.end() && iter2 != list2.end()) {
        if (*iter1 == *iter2) {
            intersection.push_back(*iter1);
            ++iter1; ++iter2;
        }
        else if (*iter1 < *iter2) ++iter1;
        else ++iter2;
    }
    return intersection;
}


int main() {

    list<int> list1, list2, list3;

    while (list1.size() < 10) {
        int x = rand() % 20;
        list1.push_back(x);
    }
    list1.sort();
    for (auto iter : list1) cout << iter << " ";
    cout << endl;

    while (list2.size() < 10) {
        int x = rand() % 20;
        list2.push_back(x);
    }
    list2.sort();
    for (auto iter : list2) cout << iter << " ";
    cout << endl;

    list3 = intersection(list1, list2);
    for (auto iter : list3) cout << iter << " ";
    cout << endl;

    return 0;       
}