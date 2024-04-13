#include<iostream>

using namespace std;

int main() {
    enum class Color {black, white, blue};
    Color color  = Color::blue;
    cout << static_cast<int>(color) << endl;

    enum struct Size {big, small, medium};
    Size size = Size::big;
    cout << static_cast<int>(size) << endl;
    cout << int(Size::small) << endl; // 枚举标签的这种特性也可以运用到类定义当中（见Practice_32.cpp）
    return 0;
}