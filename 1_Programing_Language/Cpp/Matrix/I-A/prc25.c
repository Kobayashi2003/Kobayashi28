// Enter the input as an integer whose last two digits represent the cents. For example, the input 1156 represents 11 dollars and 56 cents.

// The output should display non-zero denominations only, using singular words for single units like 1 dollar and 1 penny, and plural words for more than one unit like 2 dollars and 3 pennies.

// 1 quarter = 25 cents
// 1 dime = 10 cents
// 1 nickel = 5 cents
// 1 penny = 1 cent

#include <stdio.h>

int main() {

    int input; scanf("%d", &input);

    int dollars = input / 100;
    int cents = input % 100;

    int quarters = cents / 25;

    cents = cents % 25;

    int dimes = cents / 10;

    cents = cents % 10;

    int nickels = cents / 5;

    cents = cents % 5;

    int pennies = cents;

    printf("Your amount %d consists of \n", input);

    if (dollars > 0) {
        if (dollars == 1) {
            printf("%d dollar\n", dollars);
        } else {
            printf("%d dollars\n", dollars);
        }
    }

    if (quarters > 0) {
        if (quarters == 1) {
            printf("%d quarter\n", quarters);
        } else {
            printf("%d quarters\n", quarters);
        }
    }

    if (dimes > 0) {
        if (dimes == 1) {
            printf("%d dime\n", dimes);
        } else {
            printf("%d dimes\n", dimes);
        }
    }


    if (nickels > 0) {
        if (nickels == 1) {
            printf("%d nickel\n", nickels);
        } else {
            printf("%d nickels\n", nickels);
        }
    }


    if (pennies > 0) {
        if (pennies == 1) {
            printf("%d penny\n", pennies);
        } else {
            printf("%d pennies\n", pennies);
        }
    }

    return 0;
}