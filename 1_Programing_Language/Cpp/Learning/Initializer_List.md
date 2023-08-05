# Initializer List 初始化列表

```cpp example_1.cpp
#include <list>
#include <set>
#include <vector>

using namespace std;

int main() {

    vector<int> v = {1, 2, 3, 4, 5};

    list<int> l = {1, 2, 3, 4, 5};

    set<int> s = {1, 2, 3, 4, 5};
    
    vector< set<int> > v = { {1, 2, 3}, {4, 5, 6} };

    return 0;
}
```

```cpp example_2.cpp
#include <iostream> 
#include <vector>

class Foo {
public:
    int value_a;
    int value_b;
    Foo(int a, int b) : value_a(a), value_b(b) {}
};

int main() {
    // before C++11
    int arr[3] = {1, 2, 3};
    Foo foo(1, 2);
    std::vector<int> vec = {1, 2, 3, 4, 5};

    std::cout << "arr[0]: " << std::endl;
    std::cout << "foo: " << foo.value_a << ", " << foo.value_b << std::endl;

    for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); ++it) {
        std::cout << *it << std::endl;
    }

    return 0;
}
```

```cpp example_3.cpp
#include <initializer_list>
#include <iostream>
#include <vector>
class MagicFoo
{
  public:
    std::vector<int> vec;
    MagicFoo(std::initializer_list<int> list)
    {
        for (std::initializer_list<int>::iterator it = list.begin();
             it != list.end(); ++it)
            vec.push_back(*it);
    }
};
int main()
{
    // after C++11
    MagicFoo magicFoo = {1, 2, 3, 4, 5};
    std::cout << "magicFoo: ";
    for (std::vector<int>::iterator it = magicFoo.vec.begin();
         it != magicFoo.vec.end(); ++it)
        std::cout << *it << std::endl;
}
```
