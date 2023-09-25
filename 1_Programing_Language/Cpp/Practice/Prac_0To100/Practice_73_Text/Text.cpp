#include "Text.h"
#include <iostream>
#include <fstream>
#include <stdexcept>

Text::Text() {
    path = "";
}

Text::Text(_s path) {
    this->path = path;
    loadText();
}

void Text::showText(int num) const {
    if (num != -1) {
        std::cout << content[num] << std::endl;
        return;
    }
    for (auto &str : content) {
        std::cout << str << std::endl;
    }
}

_arr Text::find(_s str) const {
    _arr result;
    for (size_t i = 0; i < content.size(); ++i) {
        if (content[i].find(str) != _s::npos) {
            result[0] = content[i];
            if (color) {
                result[0].replace(content[i].find(str), str.length(), "\033[1;31m" + str + "\033[0m");
            }
            result[1] = std::to_string(i);
            return result;
        }
    }
    result[0] = "Not found";
    result[1] = "Not found";
    return result;
}

void Text::setPath(const _s path) {
    this->path = path;
    loadText();
}

void Text::loadText() {
    std::ifstream file(path);
    if (file.is_open()) {
        _s str;
        while (std::getline(file, str)) {
            content.push_back(str);
        }
    }
    else {
        throw std::runtime_error("File not found");
    }
}