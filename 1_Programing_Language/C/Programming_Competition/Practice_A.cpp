#include <iostream>
#include <cmath>

using namespace std;

using LLI = long long int;

int main() {

    LLI odometer;
    while (true) {
        cin >> odometer;
        if (!odometer) {
            break;
        }
        cout << odometer << ": ";

        int ord = 0;
        while ((LLI)pow(10, ord) <= odometer) {
            int num = odometer / (LLI)pow(10, ord) % 10;
            if (num >= 8) {
                odometer -= 2*(LLI)pow(10, ord);
            } else if (num >= 3) {
                odometer -= 1*(LLI)pow(10, ord);
            }
            ord += 1;
        }

        while (ord != 1) {
            ord -= 1;
            int num = odometer / (LLI)pow(10, ord);
            odometer -= num * 2 * (LLI)pow(10, ord-1);
        }
        cout << odometer << endl;
    }

    return 0;
}