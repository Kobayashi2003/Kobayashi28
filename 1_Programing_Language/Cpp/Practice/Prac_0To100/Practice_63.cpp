#include <stdio.h>
#include <stdlib.h>
struct node
{
    char data;
    struct node *link;
};
node *top;

void InitStack()
{
    top = NULL;
}

int isEmpty()
{
    if (top == NULL)
    {
        return 1;
    }
    else
        return 0;
}

void push(char x)
{
    node *p;
    p = (node *)malloc(sizeof(node));
    p->data = x;
    p->link = top;
    top = p;
}

int pop()
{
    if (isEmpty())
    {
        return 0; //说明不能操作 但是不是很好 怎么改？
    }
    else
    {
        node *p;
        p = (node *)malloc(sizeof(node));
        p = top;
        top = top->link;
        char res;
        res = p->data;
        free(p);
        return (res);
    }
}
int main()
{
    InitStack();
    // 1.输入
    char s[1000] = {0};
    gets_s(s, 1000*sizeof(char));
    int i = 0;
    int a = 0;
    // 2.主函数
    while (s[i] != '\0')
    {
        if (isEmpty())
        {
            push(s[i]);
            i++;
        }
        else
        {
            if ((top->data == '(') && (s[i] == ')'))
            {
                a = pop();
                i++;
            }
            else if ((top->data == '[') && (s[i] == ']'))
            {
                a = pop();
                i++;
            }
            else if ((top->data == '{') && (s[i] == '}'))
            {
                a = pop();
                i++;
            }
            else
            {
                push(s[i]);
                i++;
            }
        }
    }
    if (isEmpty())
    {
        printf("True");
    }
    else
    {
        printf("False");
    }

    return 0;
}