[参考](https://blog.csdn.net/coolzifan/article/details/128657162)

exam:
```cpp
int *arr = new int[10];
```

添加监视：
```cpp
*(int(*)[10])arr
// or
*arr@10
```