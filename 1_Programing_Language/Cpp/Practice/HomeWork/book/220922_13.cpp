// 用同一个函数名对 n 个数据进行从小到大顺序排序，用重载函数实现
// 整型，单精度，双精度
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void Sort(vector<int> &vi) {
    auto sortByIndex = [](const auto &a, const auto &b) { return (a<b); };
    sort(vi.begin(), vi.end(), sortByIndex);
    for (const auto &prep : vi) {
        cout << prep << " ";
    }
    cout << endl;
}

void Sort(vector<float> &vf) {
    auto sortByIndex = [](const auto &a, const auto &b) { return (a<b); };
    sort(vf.begin(), vf.end(), sortByIndex);
    for (const auto &prep : vf) {
        cout << prep << " ";
    }
    cout << endl;
}

void Sort(vector<double> &vd) {
    auto sortByIndex = [](const auto &a, const auto &b) { return (a<b); };
    sort(vd.begin(), vd.end(), sortByIndex);
    for (const auto &prep : vd) {
        cout << prep << " ";
    }
    cout << endl;
}

int main() {

    vector <int> vi = {1, 2, 9, 10, 0, 3, 4, 5, 6, 7, 8};
    vector <float> vf = {1.1F, 2.f, 9.f, 10.f, 0.f, 3.f, 4.f, 5.f, 6.f, 7.f};
    vector <double> vd = {1.6, 2., 9., 10., 0., 3., 4., 5., 6., 7., 8.};
    Sort(vi);
    Sort(vf);
    Sort(vd);
    return 0;
}