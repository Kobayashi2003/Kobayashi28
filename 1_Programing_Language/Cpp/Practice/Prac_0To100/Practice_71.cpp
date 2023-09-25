#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using vs = std::vector<std::string>;

class Article {

public:
    Article() = default;
    Article(const std::string &fileName);

    void print();

private:
    vs content;
};


Article::Article(const std::string &fileName) {
    std::ifstream ifs(fileName);
    // 直接当它这个文件有了，省事
    std::string line;
    while (std::getline(ifs, line)) {
        content.push_back(line);
    }
}


void Article::print() {
    for (auto &line : content) {
        std::cout << line << std::endl;
    }
}

int main() {
    Article article("article.txt");
    article.print();
    return 0;
}