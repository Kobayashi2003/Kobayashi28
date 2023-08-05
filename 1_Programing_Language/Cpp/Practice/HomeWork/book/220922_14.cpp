// 用同一个函数名对 n 个数据进行从小到大顺序排序，用函数模板实现
// 整型，单精度，双精度
#include <iostream>
#include <vector>
#include <algorithm>


using namespace std;

template<typename T>
void Sort(vector<T> &v) {
    auto sortByIndex = [](const T &a, const T &b) { return (a<b); };
    sort(v.begin(), v.end(), sortByIndex); // 按照 sortByIndex中所写规则进行排序
    for (const auto &prep : v) { // 遍历输出
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