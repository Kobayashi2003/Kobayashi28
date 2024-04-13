#include <cstdlib>
#include <fstream>
#include <iostream>

int main() {
    std::system("echo 'hello world' >temp.txt");
    std::system("powershell -Command \"echo \'hello world\' >>temp.txt\"");
    std::system("powershell -Command ls >>temp.txt");
    std::ifstream ifs("temp.txt");
    std::string str;
    while (std::getline(ifs, str)) {
        std::cout << str << std::endl;
    }
    ifs.close();
}