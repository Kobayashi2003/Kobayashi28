#include "matrix.h"

int main() {

    matrix<int> a(3, 4, {{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}});
    matrix<int> b(4, 3, {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}});
    matrix<int> c(3, 4, {{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}});

    cout << "a = " << endl << a << endl;

    cout << "a + c = " << endl << a + c << endl;

    cout << "a - c = " << endl << a - c << endl;

    cout << "a * b = " << endl << a * b << endl;

    return 0;
}