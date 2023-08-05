# if/switch 变量声明强化

现在可将临时变量声明放在 if 语句内】

```cpp
if (const auto itr = std::find(vec.begin(), vec.end(), 3);
    itr != vec.end()) {
    *itr = 4;
}

```