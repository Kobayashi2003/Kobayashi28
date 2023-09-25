// It's fairly common knoledge that if you access an
// element of an array as arr[i] in C that you can 
// also access the element as i[arr], because these 
// just boil down to *(arr + i) and additon is commutative.


#include <iostream>

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    std::cout << arr[2] << std::endl;
    std::cout << 2[arr] << std::endl;
    std::cout << *(arr + 2) << std::endl;
    std::cout << *(2 + arr) << std::endl;
    return 0;
}