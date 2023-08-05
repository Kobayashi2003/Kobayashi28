#include <iostream>

using namespace std;

template <typename T, typename U>
// auto add(T t, U u) -> decltype(t + u) { return t + u; }
auto add(T t, U u) { return t + u; }

int main() {
    cout << add(1, 2.1) << endl;
    return 0;
}