# rvalue reference 右值引用

```cpp
#include <iostream>

inline double f(double tf) { return 5.0*(tf-32.0)/9.0; }

int main() {

    using namespace std;
    double tc = 21.5;
    double && rd1 = 7.07;
    double && rd2 = tc * 1.8 + 32.0;
    double && rd3 = f(rd2);
    cout << " tc value and address: " << tc << " " << &tc << endl;
    cout << " rd1 value and address: " << rd1 << " " << &rd1 << endl;
    cout << " rd2 value and address: " << rd2 << " " << &rd2 << endl;
    cout << " rd3 value and address: " << rd3 << " " << &rd3 << endl;
    
    return 0;
}
```


## 左值、右值的纯右值、将亡值、右值

- **左值**（lvalue, left value），顾名思义就是赋值符号左边的值。准确来说，左值是表达式（不一定是赋值表达式）后依然存在的持久对象
- **右值**（rvalue, right value），右边的值，是表达式后不再存在的临时对象
  而 C++11 中为了引入强大的右值引用，又将右值分为了纯右值（pure rvalue）和将亡值（xvalue）
- **纯右值**（prvalue, pure rvalue），纯粹的右值，要么是纯粹的字面量，例如 10，true；要么是求值结果相当于字面量或匿名临时对象，例如 1+2。非引用返回的临时变量、运算表达式产生的临时变量、原始字面量、lambda 表达式、函数返回值等都是纯右值

> 需要注意的是，字面量除了字符串字面量外，其他字面量都是纯右值，而字符串字面量是左值，类型为 const char 数组. 例如：

```cpp
#include <type_traits>
int main()
{
    // 正确，"01234" 类型为 const char [6]，因此是左值
    const char(&left)[6] = "01234";

    // 断言正确，确实是 const char [6] 类型，注意 decltype(expr) 在 expr 是左值
    // 且非无括号包裹的 id 表达式与类成员表达式时，会返回左值引用
    static_assert(std::is_same<decltype("01234"), const char(&)[6]>::value, "");

    // 错误，"01234" 是左值，不可被右值引用
    // const char (&&right)[6] = "01234";
}
```

> 但是注意，数组可以被隐式转换成相对应的指针类型，而转换表达式的结果（如果不是左值引用）则一定是个右值（右值引用为将亡值，否则为纯右值）。例如：

```cpp
const char* p = "01234"; // 正确，"01234" 被隐式转换为 const char*
const char*&& pr = "01234"; // 正确，"01234" 被隐式转换为 const char*，该转换的结果是纯右值
// const char*& pl = "01234"; // 错误，此处不存在 const char* 类型的左值
```

- **将亡值**（xvalue, eXpiring value），将要消亡的值，是将要被移动的对象，例如 std::move 返回的值，或者是将要被绑定到右值引用的左值。将亡值是纯右值的子集，但是纯右值不一定是将亡值。例如：

```cpp
std::vector<int> foo() {
    std::vector<int> temp = {1, 2, 3, 4};
    return temp; 
}
std::vector<int> v = foo();
```

在这样的代码中，就传统的理解而言，函数 foo 的返回值 temp 在内部创建然后被赋值给 v，然而 v获得这个对象时，会将整个 temp 拷贝一份，然后把 temp 销毁，如果这个 temp 非常大，这将造成大量额外的开销（这也就是传统 C++ 一直被诟病的问题）。在最后一行中，v 是左值、foo() 返回的值就是右值（也是**纯右值**）。但是，v 可以被别的变量捕获到，而 foo() 产生的那个返回值作为一个临时值，一旦被 v 复制后，将立即被销毁，无法获取、也不能修改。而将亡值就定义了这样一种行为：**临时的值能够被识别、同时又能够被移动**

在 C++11 之后，编译器为我们做了一些工作，此处的左值 temp 会被进行此**隐式右值转换**，等价于
`static_cast<std::vector<int> &&>(temp)`，进而此处的 v 会将 foo 局部返回的值进行移动。也就是
后面我们将会提到的移动语义。


## 左值引用和右值引用

要拿到一个将亡值，就需要用到右值引用：T &&，其中 T 是类型。右值引用的声明让这个临时值的生命周期得以延长、只要变量还活着，那么将亡值将继续存活。
C++11 提供了 std::move 这个方法将左值参数无条件的转换为右值，有了它我们就能够方便的获得一个右值临时对象，例如：

```cpp
#include <iostream> 
#include <string>

void reference(std::string& str) {
    std::cout << " 左值" << std::endl;
}

void reference(std::string&& str) {
    std::cout << " 右值" << std::endl;
}

int main()
{
    std::string lv1 = "string,"; // lv1 是一个左值
    // std::string&& r1 = lv1; // 非法, 右值引用不能引用左值
    std::string&& rv1 = std::move(lv1); // 合法, std::move 可以将左值转移为右值
    std::cout << rv1 << std::endl; // string,


    const std::string& lv2 = lv1 + lv1; // 合法, 常量左值引用能够延长临时变量的生命周期
    // lv2 += "Test"; // 非法, 常量引用无法被修改
    std::cout << lv2 << std::endl; // string,string,


    std::string&& rv2 = lv1 + lv2; // 合法, 右值引用延长临时对象生周期
    rv2 += "Test"; // 合法, 非常量引用能够修改临时变量
    std::cout << rv2 << std::endl; // string,string,string,Test


    reference(rv2); // 输出左值


    return 0;
}
```

rv2 虽然引用了一个右值，但由于它是一个引用，所以 rv2 依然是一个左值。
注意，这里有一个很有趣的历史遗留问题，我们先看下面的代码：

```cpp
#include <iostream>
int main() {
    // int &a = std::move(1); // 不合法，非常量左引用无法引用右值
    const int &b = std::move(1); // 合法, 常量左引用允许引用右值
    std::cout << a << b << std::endl;
}
```

第一个问题，为什么不允许非常量引用绑定到非左值？这是因为这种做法存在逻辑错误：

```cpp
void increase(int & v) {
    v++;
}

void foo() {
    double s = 1;
    increase(s);
}
```

由于 int& 不能引用 double 类型的参数，因此必须产生一个临时值来保存 s 的值，从而当increase() 修改这个临时值时，调用完成后 s 本身并没有被修改。
第二个问题，为什么常量引用允许绑定到非左值？原因很简单，因为 Fortran 需要。


## 移动语义

传统 C++ 通过拷贝构造函数和赋值操作符为类对象设计了拷贝/复制的概念，但为了实现对资源的移动操作，调用者必须使用先复制、再析构的方式，否则就需要自己实现移动对象的接口。试想，搬家的时候是把家里的东西直接搬到新家去，而不是将所有东西复制一份（重买）再放到新家、再把原来的东西全部扔掉（销毁），这是非常反人类的一件事情。

传统的 C++ 没有区分『移动』和『拷贝』的概念，造成了大量的数据拷贝，浪费时间和空间。右值引用的出现恰好就解决了这两个概念的混淆问题，例如：

```cpp
#include <iostream>
class A {
public:
    int *pointer;
    A():pointer(new int(1)) {
        std::cout << " 构造" << pointer << std::endl;
    }
    A(A& a):pointer(new int(*a.pointer)) {
        std::cout << " 拷贝" << pointer << std::endl;
    } // 无意义的对象拷贝
    A(A&& a):pointer(a.pointer) {
        a.pointer = nullptr;
        std::cout << " 移动" << pointer << std::endl;
    }
    ~A(){
        std::cout << " 析构" << pointer << std::endl;
        delete pointer;
    }
};
// 防止编译器优化
A return_rvalue(bool test) {
    A a,b;
    if(test) return a; // 等价于 static_cast<A&&>(a);
    else return b; // 等价于 static_cast<A&&>(b);
}
int main() {
    A obj = return_rvalue(false);
    std::cout << "obj:" << std::endl;
    std::cout << obj.pointer << std::endl;
    std::cout << *obj.pointer << std::endl;
    return 0;
}
```

在上面的代码中：
1. 首先会在 return_rvalue 内部构造两个 A 对象，于是获得两个构造函数的输出；
2. 函数返回后，产生一个将亡值，被 A 的移动构造（A(A&&)）引用，从而延长生命周期，并将这个右值中的指针拿到，保存到了 obj 中，而将亡值的指针被设置为 nullptr，防止了这块内存区域被销毁。