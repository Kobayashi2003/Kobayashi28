#include <iostream>
#include <string>
#include <memory>

int main() {
    using namespace std;

    string one("Hello World!");
    cout << one << endl;

    string two(20, '$');
    cout << two << endl;

    string three(one);
    cout << three << endl;

    one += " Goodbye!";
    cout << one << endl;

    two = "C++ Programming";
    cout << two << endl;

    three[0] = 'Y';
    cout << three << endl;

    string four;
    four = two + " is fun!";
    cout << four << endl;

    char alls[] = "All's well that ends well";
    string five(alls, 20);
    cout << five << "!\n";

    string six(alls + 6, alls + 10);
    cout << six << ", ";
    string seven(&five[6], &five[10]);
    cout << seven << "...\n";

    string eight(four, 7, 16);
    cout << eight << " in motion!" << endl;
    

    return 0;
}
