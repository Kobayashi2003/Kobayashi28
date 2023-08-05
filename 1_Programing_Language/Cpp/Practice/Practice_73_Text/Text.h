#pragma once
#include <vector>
#include <string>
#include <array>

using _vs = std::vector<std::string>;
using _s = std::string;
using _arr = std::array<std::string, 2>;
using _c_char = const char;

class Text {
public:
    Text();
    Text(_s path);
    void setPath(const _s path);
    _arr find(_s str) const;
    void showText(int num=-1) const;
public:
    bool color = true;
private:
    void loadText();
private:
    _vs content;
    _s path;
};