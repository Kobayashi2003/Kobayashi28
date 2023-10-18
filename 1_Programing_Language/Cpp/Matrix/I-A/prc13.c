#include <stdio.h>
#include <math.h>

int convertOctalToDecimal(int octalNumber) {
    int decimalNumber = 0;

    int i = 0;
    while (octalNumber != 0) {
        decimalNumber += (octalNumber % 10) * pow(8, i);
        ++i;
        octalNumber /= 10;
    }

    return decimalNumber;
}


int main() {
    int octalNumber;
    scanf("%d", &octalNumber);
    printf("%d", convertOctalToDecimal(octalNumber));
    return 0;
}