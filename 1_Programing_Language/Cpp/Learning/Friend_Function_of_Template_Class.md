# 模板类中的友元函数

- **非模板友元**

```cpp example_1.cpp
template <typename T>
class Data {
    ...
public:
    friend void func(); // non-template friend to all Data instantiations
    ...  
}

void func() {
    ...
}
```

如果想要为友元函数提供模板类参数：

```cpp example_2.cpp
template <typename T>
class Data {
    ...
public:
    friend void func(Data<T> &); // bound template friend
    ...
}
```

需要注意，`func()`本身并**不是模板函数**，而仅是使用了一个模板参数，这意味着在定义友元`func()`时必须**先将模板具体化**

```cpp example_2.cpp
void func(Data<int> &) { // explicit specialization for int
    ...
}

void func(Data<double> &) { // explicit specialization for double
    ...
}

void func(Data<size_t> &) { // explicit specialization for size_t
    ...
}
```

下面来让我们先看一个程序：

```cpp program_1.cpp

#include <iostream>

using std::cout;
using std::endl;

template <typename T>
class HasFriend {
private:
    T item;
    static int cnts;
public:
    HasFriend(const T& i) : item(i) { cnts += 1; }
    ~HasFriend() = default;

    friend void counts(); 
    friend void report(HasFriend<T> &); // template class parameter
};

// each specialization has its own static data number
template <typename T>
int HasFriend<T>::cnts = 0;

// non-template friend to all HasFriend<T> classes
void counts() {
    cout << "int count" << HasFriend<int>::cnts << ";";
    cout << "double count" << HasFriend<double>::cnts << endl;
}

//non-template friend to the HasFriend<int> class
void report(HasFriend<int> & hf)
{
    cout<<"HasFriend<int>:"<<hf.item<<endl;
}

//non-template friend to the HasFriend<double> class
void report(HasFriend<double> & hf)
{
    cout<<"HasFriend<double>:"<<hf.item<<endl;
}

int main()
{
    cout<<"No objects declared:";
    counts();
    HasFriend<int> hfi1(10);
    cout<<"After hfi1 declared:";
    counts();
    HasFriend<int> hfi2(20);
    cout<<"After hfi2 declared:";
    counts();
    HasFriend<double> hfdb(15.5);
    cout<<"After hfdb declared:";
    counts();
    report(hfi1);
    report(hfi2);
    report(hfdb);

    return 0;
}
```

程序编译后会有一条警告信息

`friend declaration 'void report(HasFriend<T>&)' declares a non-template function [-Wnon-template-friend]`

至于为什么会产生这条警告信息，我们先暂时放置，交由后面解释

- **模板类的约束（bound）模板友元**

可以修改上面的示例，使友元本身成为模板函数。具体的说，为约束模板友元做准备，要使类的每一个具体化（每一个模板类）都获得**与之匹配**的具体化友元

- 首先，在类定义的前面声明每个函数模板：

```cpp
template <tpyename T> void counts();
template <tpyename T> void reports(T &);
```

- 然后，类中将模板函数声明为友元：

```cpp
template <typename TT>
class HasFriendTem
{
    ...
pulic:
    friend void counts<TT>();
    friend void report<>(HasFriendTem<TT> &); // 当然你也可以写成 friend void report<HasFriendTem<TT>>(HasFriendTem<TT> &);
    ...
};
```

- 最后，我们需要为友元提供模板定义：



来看一下能同时满足三个要求的程序

```cpp program_2.cpp 

#include <iostream>
using std::cout;
using std::endl;

//template prototypes
template <typename T> void counts();
template <typename T> void report(T &);

//template class
template <typename TT>
class HasFriendTem
{
private:
    TT item;
    static int cnts;
public:
    HasFriendTem(const TT & i):item(i){cnts++;}
    ~HasFriendTem(){cnts--;}
    friend void counts<TT>();
    friend void report<>(HasFriendTem<TT> &);
};

template <typename TT>
int HasFriendTem<TT>::cnts=0;

//template friend functions definitions
template <typename T>
void counts()
{
    cout<<"template size:"<<sizeof(HasFriendTem<T>)<<";";
    cout<<"template counts():"<<HasFriendTem<T>::cnts<<endl;
}

template <typename T>
void report(T& hf)
{
    cout<<hf.item<<endl;
}

int main()
{
    counts<int>();
    HasFriendTem<int> hfi1(10);
    HasFriendTem<int> hfi2(20);
    HasFriendTem<double> hfdb(15.5);
    report(hfi1);//generate report(HasFriendTem<int> &)
    report(hfi2);
    report(hfdb);//generate report(HasFriendTem<double> &)
    cout<<"counts<int>() output:\n";
    counts<int>();
    cout<<"counts<double() output:\n";
    counts<double>();

    return 0;
}
```

在本例中，每种模板类都有自己的友元函数

说明： program1包含一个 `counts()`函数，它是所有 HasFriend类模板具体化之后的模板类的友元；而 program2包含两个 `counts()`函数（在具体化的时候被定义），即 `counts<int>()`和 `counts<double>`函数，它们分别是模板类 `HasFriendTem<int>`和模板类 `HasFriendTem<double>`对应的友元。由于 `counts()`函数模板没有参数，所以在调用的时候必须指定具体化类型，但对于 `report()`调用，编译器可以通过从参数中推断出要具体化的类型，当然，使用 `<>`格式也能取得同样的效果


现在我们回看在 program_2.cpp 中编译中的警告

现在我们就能够很好地理解这是为什么了。警告中说友元函数被定义的类型为非模板友元，并提示说如果并非自己打算定义非模板友元，确保在友元名字之后添加<>符号。意思就是如果你打算定义的是模板友元，那你忘了在声明模板友元的时候使用 <>语法（注意只有模板友元的声明中函数名字之后才会用 <>语法）了。

小结一下：模板类的约束模板友元说白了就是友元模板的具体化受着类模板的具体化的限制，两者有着关联关系，类模板具体化之后，模板友元具体化也就确定了。


- **模板类的非约束（unbound）模板友元**

上面的约束模板友元是在类模板外面声明友元模板。通过在**类模板内部声明**友元模板，可以创建**非约束模板友元**，即每个**函数模板的具体化都是每个类模板具体化的友元**。对于非约束模板友元，**友元模板的类型参数和类模板的类型参数是不同的**：

```cpp 
template<typename T>
{
    ...
    template <typename C,typename D> friend void show(C &,D &)
    ...
};
```

```cpp program_3.cpp

#include <iostream>
using std::cout;
using std::endl;

template <typename T>
class ManyFriend
{
private:
    T item;
public:
    ManyFriend(const T & i):item(i){}
    //unbound template friend declation
    template <typename C,typename D> friend void show(C &,D &);
};

template <typename C,typename D> void show(C & c,D & d)
{
    cout<<c.item<<", "<<d.item<<endl;
}

int main()
{
    ManyFriend<int> hfi1(10);
    ManyFriend<int> hfi2(20);
    ManyFriend<double> hfdb(15.5);
    cout<<"hfi1, hfi2: ";
    show(hfi1,hfi2);//generate show<ManyFriend<int> &,ManyFriend<int> &>(ManyFriend<int> & c,ManyFriend<int> & d)
    cout<<"hfdb, hfi2: ";
    show(hfdb,hfi2);//generate show<MantyFriend<double> &,ManyFriend<int> &>(ManyFriend<double> & c,ManyFriend<int> & d)

    return 0;
}

```

小结一下：非约束模板友元指的是每一个具体化的模板类对应所有具体化的友元，每一个具体化的友元也是所有具体化的模板类的友元。