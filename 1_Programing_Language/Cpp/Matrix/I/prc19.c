#include <stdio.h>

int betterBookForReaderA(int book1,int book2);

int find6(int a);

int betterBookForReaderB(int book1,int book2);

int isPalindromic(int a);

int betterBookForReaderC(int book1,int book2);





int betterBookForReaderA(int book1,int book2) {
    while (book1 && book2) {
        book1 /= 10; book2 /= 10;
    }
    if (!book1 && !book2)
        return book1 > book2 ? 1 : 2;
    else if (!book1)
        return 1;
    else if (!book2)
        return 2;
}

int find6(int a) {
    while (a) {
        if (a % 10 == 6) 
            return 1;
        a /= 10;
    }
    return 0;
}

int betterBookForReaderB(int book1, int book2) {
    if (find6(book1))
        return 1;
    else if (find6(book2))
        return 2;
    else
        return -1;
}

int isPalindromic(int a) {
    int b = 0, c = a;
    while (c) {
        b = b * 10 + c % 10;
        c /= 10;
    }
    return a == b;
}

int betterBookForReaderC(int book1, int book2) {
    if (isPalindromic(book1))
        return 1;
    else if (isPalindromic(book2))
        return 2;
    else
        return -1;
}






void printChoice(int choose,int book1,int book2)
{
    if(choose==-1)
        printf("Sorry. Neither of those books.\n");
    else if(choose==1)
        printf("I guess you will prefer: %d\n",book1);
    else if(choose==2)
        printf("I guess you will prefer: %d\n",book2);

}

int main()
{
    char c;
    int book1, book2;
    scanf("%c%d%d", &c, &book1, &book2);
    int choose;
    if(c == 'A')
        choose = betterBookForReaderA(book1, book2);
    else if(c == 'B')
        choose = betterBookForReaderB(book1, book2);
    else if(c == 'C')
        choose = betterBookForReaderC(book1, book2);

    printChoice(choose, book1, book2);
    return 0;
}
