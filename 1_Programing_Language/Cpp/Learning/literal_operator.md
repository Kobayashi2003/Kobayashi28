# 字面量运算符重载

## 原始字符串字面量

C++11 提供了原始字符串字面量的写法，可以在一个字符串前前方使用`R`来修饰这个字符串，同时，将原始字符串使用括号包括

```cpp
#include <iostream>
#include <string>

int main() {
    std::string s = R"(C:\File\Path)";
    std::cout << str << std::endl;
    return 0;
}
```


## 自定义字面量、

C++11 引进了自定义字面量的能力，通过重载双引号后缀运算符实现：

```cpp
std::string operator"" _wow1(const char *wow1, size_t len) {
    return std::string(wow1) + "woooooooooooooow, amazing";
}

std::string operator"" _wow2(usigned long long i) {
    return std::to_string(i) + "woooooooooooooow, amazing";
} 

int main() {
    auto str = "abc"_wow1;
    auto num = 1_wow2;
    std::cout << str << std::endl;
    std::cout << num << std::endl;
    return 0;
}
```

自定义字面量支持四种字面量：

- 整形字面量：重载时必须使用 unsiged long long、const char*、模板字面量算符参数，在上面代码中使用的是前者
- 浮点型字面量：重载时必须使用 long double、const char*、模板字面量算符参数
- 字符串字面量：必须使用 (const char*, size_t) 形式的参数表
- 字符字面量：参数只能是 char, wchar_t, char16_t, char32_t 这几种类型