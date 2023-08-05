#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#define N 10
enum Direction
{
    up,
    down,
    left,
    right
} direction;
char table[N][N];
bool check(int i, int j)
{
    bool state = false;
    if (i + 1 < N && table[i + 1][j] == '.')
        state = true;
    else if (i - 1 >= 0 && table[i - 1][j] == '.')
        state = true;
    else if (j + 1 < N && table[i][j + 1] == '.')
        state = true;
    else if (j - 1 >= 0 && table[i][j - 1] == '.')
        state = true;
    return state;
}
int main()
{
    memset(table, '.', sizeof(table));
    srand(time(NULL));
    int i = 0, j = 0;
    char c = 'A';
    table[i][j] = c++;
    while (c <= 'Z' && check(i, j))
    {
        direction = rand() % 4;
        switch (direction)
        {
        case up:
            if (i + 1 < N && table[i + 1][j] == '.')
            {
                table[++i][j] = c++;
                break;
            }
            else
                continue;

        case down:
            if (i - 1 >= 0 && table[i - 1][j] == '.')
            {
                table[--i][j] = c++;
                break;
            }
            else
                continue;

        case right:
            if (j + 1 < N && table[i][j + 1] == '.')
            {
                table[i][++j] = c++;
                break;
            }
            else
                continue;

        case left:
            if (j - 1 >= 0 && table[i][j - 1] == '.')
            {
                table[i][--j] = c++;
                break;
            }
            else
                continue;
        }
        /*
                for (int i = 0; i < N; i++)
                {
                    for (int j = 0; j < N; j++)
                        printf("%c ", table[i][j]);
                    putchar('\n');
                }
                putchar('\n');
        */
    };
    for (i = 0; i < N; i++)
    {
        for (j = 0; j < N; j++)
            printf("%c ", table[i][j]);
        putchar('\n');
    }
    return 0;
}