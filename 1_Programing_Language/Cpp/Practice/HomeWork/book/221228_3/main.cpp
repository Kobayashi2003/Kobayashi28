// main.cpp
#include "xt8_3_h1.h"
#include "xt8_3_h2.h"
#include <iostream>

using namespace std;
using namespace student1;

int main() {
    Student stud1(1001, "Wang", 18, "123 Beijing Road, Shanghai");
    stud1.show_data();
    student2::Student stud2(1102, "Li", 'f', 89.5);
    stud2.show_data();
    return 0;
}