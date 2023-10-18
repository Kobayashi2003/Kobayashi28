#include <stdio.h>

int main() {

    char stack[128] = {0};
    int top = -1;

    char expr[128] = {0}; scanf("%s", expr);

    int i = 0;
    while (expr[i] != '\0') {
        switch (expr[i]) {
            case '(': case '[': case '{':
                stack[++top] = expr[i];
                break;
            case ')':
                if (top != -1 && stack[top] == '(')
                    top--;
                else {
                    printf("No\n");
                    return 0;
                } 
                break;
            case ']':
                if (top != -1 && stack[top] == '[')
                    top--;
                else {
                    printf("No\n");
                    return 0;
                }
                break;
            case '}':
                if (top != -1 && stack[top] == '{')
                    top--;
                else {
                    printf("No\n");
                    return 0;
                }
                break;
        }
        i++;
    } 

    if (top == -1)
        printf("Yes\n");
    else
        printf("No\n");

    return 0;
}