# 定位 new 运算符

new 运算符的一种变体，被称为定位（placement）new 运算符，它让我们能够指定到要使用的位置。
<!-- 程序员可能使用这种特性来设置其内存管理规程、处理需要通过特定地址进行访问的硬件或在特定位置创建对象 -->

[Practice_41.cpp](../Practice/Practice_41.cpp)

## 防止重叠

```cpp
pc1 = new (buffer) className;
pc2 = new (buffer + sizeof(className)) className;
```

## 注意

delete 可与常规 new 运算符配合使用，但不能与定位 new 运算符配合使用

解决方案：
显示地为使用定位 new 运算符创建的对象调用析构函数。显式调用析构函数时，必须指定要销毁的对象。
```cpp
pc2 -> ~destructor;
pc1 -> ~destructor;
// 需要注意正确的删除顺序：对于使用定位 new 运算符创建的对象，应当以与创建顺序相反的顺序进行删除。
// 原因在于，晚创建的对象可能依赖于早创建的对象。另外，仅当所有对象都被销毁后，才能释放用于存储这些对象的缓冲区
```