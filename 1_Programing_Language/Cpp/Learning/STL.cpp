// C++ STL（标准模板库）是一套功能强大的 C++ 模板类，提供了通用的模板类和函数
// 这些模板类和函数可以实现多种流行和常用的算法和数据结构，如向量、链表、队列、栈
// C++ 标准模板库的核心包括以下三个组件：

// 容器（Containers）容器是用来管理某一类对象的集合。C++ 提供了各种不同类型的容器，比如 deque、list、vector、map 等。

// 算法（Algorithms）算法作用于容器。它们提供了执行各种操作的方式，包括对容器内容执行初始化、排序、搜索和转换等操作。

// 迭代器用于遍历对象集合的元素。这些集合可能是容器，也可能是容器的子集。

// 参考：https://blog.csdn.net/m0_58086930/article/details/122466500

#include<iostream>

#include<cstring>
#include<cstdlib>
#include<ctime>

#include<vector> // 动态数组（向量）
#include<set> // 集合
#include<unordered_set> // 无序集合
#include<map> // 键值对
#include<unordered_map> // 无序键值对
#include<stack> // 栈
#include<queue> // 队列

#define LEN 10
#define TestData 1

#include<bitset> // 位运算

#include<algorithm> // 算法

#define CRLF cout << endl << endl

using namespace std;


void STL_Part() {
    cout << "Vector Part" << endl;

    vector <int> Vector;
    // vector <int> Vector(LEN, TestData);
    // vector <int> Vector(LEN);
    // vector中未声明的元素默认为0

    // 重置长度
    Vector.resize(LEN);
    // 从后增添
    Vector.push_back(TestData);
    // 输出长度
    cout << "The length of the Vector: " << Vector.size() << endl;

    // 迭代器
    cout << "The elements in the Vector: ";
    for(auto p = Vector.begin(); p != Vector.end(); p++) {
        cout << *p << " ";
    }

    CRLF;

    cout << "Set Part" << endl;

    set <int> Set; // 系统将会自动将Set中元素进行排序
    unordered_set <int> USet; // 无序集合将会省去排序的过程
    // 插入
    Set.insert(TestData);

    // 查找（函数的返回值为一个指针）
    // Set.find(TestData);
    // auto result = Set.find(TestData) != Set.end() ? "True" : "False";
    // cout << result << endl;
    cout << (Set.find(TestData) != Set.end() ? "True" : "False") << endl;

    // 删除
    Set.erase(TestData);

    // 输出长度
    cout << "The length of the Set is: " << Set.size() << endl;

    CRLF;

    cout << "Map Part" << endl;

    map <string, int> Map; // 系统将会依据键的大小自动对元素进行排序
    unordered_map <string, int> UMap; // 无序键值对将会省去排序的过程

    // 添加
    Map["DATA_ONE"/*KEY*/] = TestData /*VALUE*/;
    Map["DATA_TWO"] = TestData + 1;

    // 访问（如果键存在则返回其值，不存在则返回0）
    cout << "The value of the key is: " << Map["DATA_ONE"] << endl;

    // 遍历
    cout << "All keys and values in the Map is:" << endl;
    for(auto p = Map.begin(); p != Map.end(); p++) {
        cout << p -> first << ":" << p -> second << endl;
    }

    // 输出长度
    cout << "The length of the Map is: " << Map.size() << endl;

    // 当访问了一个不存在于Map中的KEY，系统不会报错，而是在Map中增添该KEY，并将其值设为0

    CRLF;

    cout << "Stack Part" << endl;

    stack <int> Stack;

    // 压栈
    Stack.push(TestData);
    Stack.push(TestData);
    // 出栈
    Stack.pop();
    // 访问栈顶
    cout << "The top data of the Stack is: " << Stack.top() << endl;
    // 访问长度
    cout << "The length of the Stack is: " << Stack.size() << endl;

    CRLF;

    cout << "Queue Part" << endl;

    queue <int> Queue;

    // 入队
    Queue.push(TestData);
    // 出队
    Queue.pop();

    for(int i = 0; i < LEN; i ++) {
        Queue.push(i);
    }

    // 访问队首
    cout << "The front data of Queue is: " << Queue.front() << endl;
    // 访问队尾
    cout << "The back data of Queue is: " << Queue.back() << endl;

    // 获取长度
    cout << "The length of the Queue is: " << Queue.size() << endl;
}

void BITSET() {
    bitset <LEN/* 表示最大的二进制位数（long long undefined） */> Bitset(TestData /* 用于初始化Bitset的十进制数（undefined int）,不写时默认为 0 */);
    bitset <LEN> Bitset2("0101"/* （A Binary number）string,若位数不足则会在所列数字前自动补 0 */);

    // 输出
    // biset类似于一个字符数组，但是它是以 从二进制的低位到高位依次为 b[0]、b[1]、、、 的方式储存，所以按照 b[i]的方式输出和直接输出 b的结果相反
    cout << "Out1: " << Bitset << endl;
    cout << "Out2: ";
    for(int i = 0; i < LEN; i++) {
        cout << Bitset[i] << " ";
    }
    cout << endl;

    // 判断Bitset中是否有1的二进制位
    cout << "Is there any '1' ? " << (Bitset.any() ? "True" : "False") << endl;
    // 判读Bitset中是否**不存在**1的二进制位
    cout << "Is there none of '1' ? " << (Bitset.none() ? "True" : "False") << endl;
    // Bitset中 1 的个数
    cout << "Count the number of '1' in the Bitset: " << Bitset.count() << endl;
    // Bitset中元素的个数
    cout << "The size of the Bitset is: " << Bitset.size() << endl;
    // 判断Bitset中的第 i 位处是否为二进制数 1
    cout << "Test the i number of the Bitset: "/* 注意bitset容器的存储规则 */ << (Bitset.test(0) ? "True" : "False") << endl;
    // 将Bitset的下标 i 处设为 '1'
    cout << "Set: " << Bitset.set(3) << endl;
    // 将所有位重设为 0
    cout << "Reset: " << Bitset.reset() << endl;
    // 将所有位取反
    cout << "Flip: " << Bitset.flip() << endl;
    // 将第 i 位取反
    cout << "Flip the i number of the Bitset: " << Bitset.flip(3) << endl;
    // 将Bitset转换为 unsigned long类型
    unsigned long UL = Bitset.to_ulong();
    cout << "Change into a Unsigned long number: " << UL << endl;
    // 从字符串 str[pos]开始读取 n 位长度
    string str = "1001010110";
    bitset <LEN> B(str, 0, 5);
    cout << "From String: " << B << endl;
}

void the_Difference_Betweeen_Size_and_Capacity() {
    vector <int> Vector(10);
    cout << "Size: " << Vector.size() << endl;
    cout << "Capacity: " << Vector.capacity() << endl;
    cout << "Address: " << &Vector << endl;
    Vector.push_back(TestData);
    cout << "Size after push: " << Vector.size() << endl;
    cout << "Capacity after push: " << Vector.capacity() << endl;
    cout << "Address after push: " << &Vector << endl;
}

bool cmp(int x, int y) {
    // 返回值为 false时 x与 y的位置互换，为 true不动
    return y - x;
}

void SORT() {
    vector <int> Vector(LEN);

    srand(time(NULL));
    for(auto p = Vector.begin(); p != Vector.end(); p++) {
        *p = rand() % 10;
    }

    cout << "Before sorted: ";
    for(auto p = Vector.begin(); p != Vector.end(); p++) {
        cout << *p << " ";
    }
    cout << endl;

    // sort函数默认为从小到大排序
    sort(Vector.begin(), Vector.end());

    cout << "After sorted: ";
    for(auto p = Vector.begin(); p != Vector.end(); p++) {
        cout << *p << " ";
    }
    cout << endl;

    // 自定义排序方式
    sort(Vector.begin(), Vector.end(), cmp); // cmp 为bool类型函数（可以通过自己修改函数的方式灵活的改变排列方式以及排列所适应的对象）
    cout << "After sorted under my rule: ";
    for(auto p = Vector.begin(); p != Vector.end(); p++) {
        cout << *p << " ";
    }

    CRLF;
}

void FOR() {
        int arr[LEN] = {1};

    for(int i = 0; i < LEN; i++) {
        arr[i] = i;
    }

    // 基于范围内的 for循环（所有的容器都可以使用这种方法进行循环）

    // 传值 输出数组中每一个元素的值，这里不能改变元素的数值
    cout << "OUT1: ";
    for(auto prop : arr) {
        cout << prop << " ";
    }
    cout << endl;

    // 传址
    cout << "OUT2: ";
    for(auto &prop : arr) {
        prop += 1;
    }
    for(auto prop : arr) {
        cout << prop << " ";
    }
    cout << endl;
}

int main() {

    return 0;
}