# this 指针

this 指针将指向用来调用成员函数的对象（this 被作为隐藏参数传递给方法）

```cpp
// 例如：
// 若有函数调用
obj.function();
// 编译器将会将this设置成obj对象的地址，并将其作为隐藏参数传给function(),使得这个指针可以用于function()
```

## 注意
每个成员函数（包括构造函数和析构函数）都有一个 this 指针。 this 指针指向调用对象。
如果方法需要引用整个调用对象，则可以使用表达式 *this。
在函数的括号后面使用 const 限定符将 this 限定为 const，这样将不能使用 this 来修改对象的值

```cpp
const className & className function() const {
    // function difinition
    return *this;
    // 返回类型为引用意味着返回的为调用对象本身，而不是其副本（cin中的 get()方法与 getline()方法原理类似）
}
```