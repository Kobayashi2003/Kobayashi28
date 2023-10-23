#include <stdio.h>
#include <string.h>

void intToRoman(char roman[], int num, char removeStr[]);

void intToRoman(char roman[], int num, char removeStr[]) {
    int len = 0;

    if (num >= 1000) {
        int i = 0;
        while (i < num / 1000) {
            roman[len++] = 'M';
            i++;
        }
        num %= 1000;
    }

    if (num >= 900) {
        roman[len++] = 'C';
        roman[len++] = 'M';
        num %= 900;
    }

    if (num >= 500) {
        roman[len++] = 'D';
        num %= 500;
    }

    if (num >= 400) {
        roman[len++] = 'C';
        roman[len++] = 'D';
        num %= 400;
    }

    if (num >= 100) {
        int i = 0;
        while (i < num / 100) {
            roman[len++] = 'C';
            i++;
        }
        num %= 100;
    }

    if (num >= 90) {
        roman[len++] = 'X';
        roman[len++] = 'C';
        num %= 90;
    }

    if (num >= 50) {
        roman[len++] = 'L';
        num %= 50;
    }

    if (num >= 40) {
        roman[len++] = 'X';
        roman[len++] = 'L';
        num %= 40;
    }

    if (num >= 10) {
        int i = 0;
        while (i < num / 10) {
            roman[len++] = 'X';
            i++;
        }
        num %= 10;
    }

    if (num >= 9) {
        roman[len++] = 'I';
        roman[len++] = 'X';
        num %= 9;
    }

    if (num >= 5) {
        roman[len++] = 'V';
        num %= 5;
    }

    if (num >= 4) {
        roman[len++] = 'I';
        roman[len++] = 'V';
        num %= 4;
    }

    if (num >= 1) {
        int i = 0;
        while (i < num) {
            roman[len++] = 'I';
            i++;
        }
    }

    
    // remove the char in removeStr from roman
    int i = 0;
    while (removeStr[i] != '\0') {
        int j = 0;
        while (roman[j] != '\0') {
            if (roman[j] == removeStr[i]) {
                int k = j;
                while (roman[k] != '\0') {
                    roman[k] = roman[k + 1];
                    k++;
                }
            } else {
                j++;
            }
        }
        i++;
    }

    return;
}

int main(){
    int num;
    char ch[4];
    char roman[30];
    // freopen("test.txt","r",stdin);
    // freopen("ans2.txt","w",stdout);
    memset(roman,0,sizeof(roman));
    scanf("%d",&num);
    scanf("%s",ch);
    intToRoman(roman,num,ch);
    printf("%s\n",roman);
    return 0;
}
