# 名称空间
[Practice_24](../Practice/Practice_24.cpp)

## 未命名的名称空间

不能在未命名名称空间所属的文件之外的其他文件中，使用该名称空间的名称，这提供了链接性为内部的静态变量的替代品

```cpp
// example
// 假设有这样的代码
static int counts;
int other() {}
int main() {}

// 可以采用名称空间
namespace {
    int counts;
}

int other() {}
int main() {}
```

## using 声明 和 using 编译指令

## using 声明

using 声明区域::被限定的名称;

```cpp
using mySpace :: value;
// 完成声明后，便可使用 value 替代 mySpace :: value
```

## using 编译

using 声明使一个名称可用，而 using 编译指令使名称空间中的所有指令都可用

using namespace 区域名称;

```cpp
using namespace mySpace;
```

[Practice_25](../Practice/Practice_25.cpp)

<!-- 一般来说，使用 using声明将会比使用 using编译更加安全 -->