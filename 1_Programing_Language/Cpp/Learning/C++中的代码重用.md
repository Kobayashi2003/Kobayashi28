# C++中的代码重用

[toc]

一个类包含另一个类的对象，这种方法称为 **包含（containment）**、**组合（composition）** 或
 **层次化（layering）**

<!-- 组合可以用来实现 has-a关系 -->

## 包含对象成员的类

### valarray 类简介

> operator[]() 让您能够访问各个元素

> size() 返回包含的元素数

> sum() 返回所有元素的总和

> max() 返回最大的元素

> min() 返回最小的元素

### 接口和实现

使用公有继承时，类可以是继承接口，可能还有实现（基类的纯虚函数提供接口，但不提供实现）。获得接口是 is-a 关系的组成部分。而使用组合，类可以获得实现，但不能获得接口。不继承接口是 has-a 关系的组成部分。

[Practice_46](../Practice/Practice_46.cpp)

### C++和约束

<!-- 在编译阶段出现错误优于在运行阶段出现错误 -->

1. 初始化被包含的对象初始化列表语法

```cpp
Container(/*parameter list*/) : content(/* parameter list */) {// ...}
```

**初始化顺序**
当初始化列表包含多个项目时，这些项目被初始化的顺序为它们被声明的顺序，而不是它们在初始化列表中的顺序
<!-- Practice_46 一开始的报错也是因为初始化顺序出错 -->

2. 使用被包含对象的接口

被包含对象的接口不是公有的，但可以在类方法中使用它。


## 私有继承

C++还有一种实现 has-a关系的途径——私有继承。使用私有继承，基类的公有成员和保护成员都将成为派生类的私有成员。这意味着基类方法将不会成为派生类对象公有接口的一部分，但可以在派生类的成员函数中使用它们。

<!-- 可以直接理解为派生类不继承基类的接口。正如从被包含对象中看到的，这种不完全继承是 has-a关系的一部分 -->

1. 使用私有继承，类将继承实现
2. 包含将对象作为一个命名的成员对象添加到类中，而私有继承将对象作为一个未被命名的继承对象添加到类中。通常用术语**子对象（subobject）**来表示通过继承或包含添加的对象

<!-- 通常使用包含来建立 has-a关系；如果新类需要访问原有类的保护成员，或需要重新定义虚函数，则应使用私有继承 -->


## 保护继承

使用保护继承时，基类的公有成员和保护成员都将成为派生类的保护成员。和私有继承一样，基类的接口在派生类中也是可用的，但在继承层次结构之外是不可用的。

当从派生类派生出另一个类时，私有继承和保护继承之间的区别便呈现出来了。使用私有继承时，第三代类将不能使用基类的接口，这是因为基类的公有方法在派生类中将变成私有方法；使用保护继承时，基类的公有方法在第二代中将变成受保护的，因此第三代派生类可以使用它们


## 使用 using 重新定义访问权限

使用保护派生或私有派生时，基类的公有成员将成为保护成员或私有成员。假设要让基类的方法在派生类外可用，方法之一是定义一个使用该基类方法的派生类方法

```cpp
// 例如：假设希望 Student 类能够使用 valarray 类的 sun()方法
double Student::sum() const { // public Student method
    return std::vallary<double>::sum(); // use privately-inherited method
}
```

另一个方法是，将函数调用包装在另一个函数调用中，即使用一个 using 声明来指出派生类可以使用特定的基类成员，即使采用的是私有派生、

```cpp
class Student : private std::string, private std::vallarry<double> {
public :
    using std::valarray<double>::min;
    using std::valarray<double>::max;
};
// 上述方法使得valarray<double>::min和valarray<double>::max可用，就像它们是 Student 的公有方法一样

// 注意，using声明只是用成员名——没有圆括号、函数特征标和返回类型
```


## 多重继承

MI描述的是有多个直接基类的类。与单继承一样，公有 MI 表示的也是 is-a关系。

```cpp
// 例如，可以从 A类和 B类派生出 AB类
class AB : public A, public B {// ...};
// 对于未用关键字限定的基类编译器将默认为私有派生
```

### 虚基类

虚基类使得从多个类（它们的基类相同）派生出的对象只继承一个基类对象。

```cpp
// 例如，通过在类声明中使用关键字 virtual，可以使 Worker 被用作 Singer 和 Waiter 的虚基类（virtual 和 public 的次序无关紧要）
class Singer : virtual public Worker {// ...};
class Waiter : public Worker {// ...};
// 然后可以将 SingingWaiter 类定义为 ：
class SingingWaiter : public Singer, public Worker {// ...};
// 现在，SingingWaiter 对象将只包含 Worker 对象的一个副本。从本质上说，继承的 Singer 和 Waiter 对象共享一个 Worker 对象，而不是各自引入自己的 Worker 对象副本。因为 SingingWaiter 现在只包含一个 Worker 子对象，所以可以使用多态
```

#### 新的构造函数规则

为避免产生冲突，C++在基类是虚的时，禁止信息通过中间类自动传递给基类。然而，编译器必须在构造派生对象之前构造基类对象组件；在进行显式调用的情况下，编译器将自动调用虚基类的默认构造函数

如果不希望默认构造函数来构造虚基类对象，则需要显示调用所需的基类构造函数
<!-- 注意：显示调用构造函数对于虚基类是合法的，但对于非虚基类来说是非法的 -->

```cpp
SingingWorker(const Worker & wk, int p = 0, int v = Singer::other) : Worker(wk), Waiter(wk, p), Singer(wk, v) {}
```

如果类有间接虚基类，则除非只需使用该虚基类的默认构造函数，否则必须显式调用该虚基类的某个构造函数

#### 多重继承中方法的使用

多重继承可能导致函数调用的二义性。可以使用作用域解析运算符来澄清编程者的意图；然而更好的方法是重新定义要使用的函数

#### 混合使用虚基类和非虚基类

如果基类是虚基类，派生类将包含基类的一个子对象；如果基类不是虚基类，派生类将包含多个子对象。

```cpp
// 假设类 B　被用作类　C 和　D 的虚基类
class C : virtual public B {};
class D : virtual public B {};
// 同时被用作类 X和类　Y的非虚基类
class X : public B {};
class Y : public B {};
// 而类 M是从 C、D、X、Y派生而来的
class M : public C, public D, public X, public Y {};
// 在这种情况下，类 M 从虚派生祖先那里共继承了一个 B 类子对象，并从每一个非虚派生祖先分别继承了一个 B　类子对象。因此，它包含三个　B　类子对象。当类通过多条虚途径和非虚途径继承某个特定的基类时，该类将包含一个表示所有的虚途径的基类子对象和分别表示各条非虚途径的多个基类子对象
```

#### 虚基类和支配

派生类中的名称优先（dominates）于直接或间接祖先类中的相同名称。如果某个名称优先于其他所有名称，则使用它时，即便不使用限定符，也不会导致二义性。


## 类模板

模板提供参数化（parameterized）类型，即能够将类型名作为参数传递给接收方来建立类或函数

### 定义类模板

```cpp
template <typename T>
class className {
public :
    funType function(T value1, T value2);
}

template <typename T>
funType className<T>::function(T value1, T value2) {}
// 如果在类声明中定义了方法（内联定义），则可以省略模板前缀和类限定符
```

### 使用模板类

要想使用模板类就必须要请求实例化。为此，需要声明一个类型为模板类的对象，方法是使用所需的具体类型替换泛型名。

```cpp
className<int> A;
```

[Stack](../Practice/Practice_49_Stack.cpp)

### 模板多功能性

#### 递归使用模板

```cpp
// 沿用上例模板类
className < className<int> > A;
```

#### 使用多个类型参数

模板可以包括多个类型参数。

```cpp
template <typename T1, typename T2, typename T3, typename T4>
class className {
    // ...
}
```

#### 默认类型模板参数

可以为类型参数提供默认值

```cpp
template <typename T = int>
class className {
    // ...
}
// 这样一来，如果省略了T的值，系统将会默认使用 int 类型
// 虽然可以为类模板类型参数提供默认值，但不能为函数模板参数提供默认值。然而，可以为非类型参数提供默认值，这对于类模板和函数模板都是适用的
```

### 模板的具体化

类模板与函数模板很相似，因为可以有隐式实例化、显式实例化和显式具体化，它们统称为具体化（specialization）。模板以泛型的方式描述类，而具体化是使用具体的类型生成类声明。

#### 隐式实例化
