1. `new` 会触发构造函数，`malloc` 不会；`delete` 会触发析构函数，`free` 不会

2. 声明一个无参对象时，不能`class-name object-name()`，而是`class-name object-name`，否则会被当作函数声明

3. 析构函数不是删除对象，而是在撤销对象占用的内存前完成一些清理工作，使得这部分内存可以重新分配

4. 对象数组

```cpp
class-name array-name[array-size] = {
    object1(initializer-list1),
    object2(initializer-list2),
    ...
};
```

5. 成员函数指针

```cpp
class-name::return-type (class-name::*pointer-name)(parameter-list) = &class-name::member-function-name;
```

6. `this`作用域是在类内部，系统默认传递给非静态成员函数的隐含参数

7. 成员函数参数列表后的`const`将会把`this`指针设置为 常量指针，即不能通过`this`指针修改成员变量；若 常对象 在调用非 常成员函数 时，为常量指针的`this`指针无法转换为 非常量指针，因此编译器会报错

8. 指针悬挂：指针指向的内存已经被释放，但是指针还没有被置空

9. 如果程序未对 静态数据成员 进行初始化，编译器会自动将其初始化为0
