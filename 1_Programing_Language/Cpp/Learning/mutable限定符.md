# motable

可以用它指出，即使结构（或类）变量为 const，其中的某个成员也可以被修改

```cpp
struct data {
    string name;
    mutable int age;
};
```

[Pracitce_23](../Practice/Practice_23.cpp)