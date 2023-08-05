#include <iostream>
#include "NDvector.h"

using namespace std ;

//Your code will be insert here .

int main() {
    int M_1, M_2, M_3;
    //输入第1个向量
    std::cin >> M_1;
    NDvector vec_1(M_1);
    std::cin >> vec_1;
    //输入第2个向量
    std::cin >> M_2;
    NDvector vec_2(M_2);
    std::cin >> vec_2;
    //输入第3个向量
    std::cin >> M_3;
    NDvector vec_3(M_3);
    std::cin >> vec_3;

    NDvector vec_4, vec_5;
    int product;
    try{
        vec_4 = vec_1 + vec_2;
    }
    catch (string message) {
        cout << message << endl;
        return 0;
    }
    std::cout << vec_4 << std::endl;
    try {        
        vec_5 = vec_1 - vec_3;
    }
    catch (string message) {
        cout << message << endl;
        return 0;
    }
    std::cout << vec_5 << std::endl;
    try {
        product = vec_2 * vec_3;
    }
    catch (string message) {
        cout << message << endl;
        return 0;
    }
    std::cout << product << std::endl;
    return 0;
}