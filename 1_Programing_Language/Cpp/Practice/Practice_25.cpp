#include<iostream>

using namespace std;
// 注意：假设名称空间和声明区域定义了相同的名称。如果试图使用 using 声明将名称空间的名称导入该声明区域，则两个名称将会发生冲突，从而报错
// 如果使用 using 编译指令将该名称空间的名称导入该声明区域，则局部名称将覆盖名称空间版本

// 期间遇到了在自定义的名称空间中使用 data报错的情况，经检查后发现为在 std中包含data定义，与自定义的名称产生了冲突

namespace mySpace {
    int my_data;
    string my_str;
}

using namespace mySpace;

namespace myAnotherSpace {
    int my_another_data;
}

using myAnotherSpace::my_another_data;

int main() {
    my_data = 1;
    my_str = "hello world !";
    cout << my_data << endl;
    cout << my_str << endl;

    my_another_data =2;
    cout << my_another_data << endl;
    return 0;
}