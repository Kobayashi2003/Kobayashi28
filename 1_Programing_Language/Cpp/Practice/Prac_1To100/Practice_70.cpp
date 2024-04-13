#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using vs = std::vector<std::string>;

int main() {

    // open article.txt, read the content and print it to the console line by line
    std::ifstream ifs("article.txt");
    if (!ifs.is_open()) {
        // if the file does not exist, then create a new file
        std::ofstream ofs("article.txt");
        ofs << "This is a test file." << std::endl;
        ofs << "This is the second line." << std::endl;
        ofs << "This is the third line." << std::endl;
    } else {
        // if the file exists, then load the content
        vs content;
        std::string line;
        while (std::getline(ifs, line)) {
            content.push_back(line);
        }
        for (auto &line : content) {
            std::cout << line << std::endl;
        }
    }

    return 0;
}