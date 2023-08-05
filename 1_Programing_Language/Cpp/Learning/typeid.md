# typeid

## 表达式

1. 类型 ID
> typeid(type)
2.运行时刻类型 ID
> typeid(expr)

## 运行规则
如果表达式的类型式类类型且至少包含有一个虚函数，则typeid操作符返回表达式的动态类型，需要在运算时计算；否则typeid操作符返回表达式的静态类型

## t.name()

```cpp
dataType value;
cout << typeid(value).name() << endl;
```

返回类型的C-style字符串，类型名字用系统相关的方法产生

## t1.before(t2)

返回指出t1是否出现在t2之前的bool值