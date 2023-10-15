#include <stdio.h>

int main() {

    int x; scanf("%d",&x);

    int flg1 = x % 2 ? 0 : 1;
    int flg2 = x % 3 ? 0 : 2;
    int flg3 = x % 5 ? 0 : 3;

    int flg_count = (bool(flg1) + bool(flg2) + bool(flg3)) > 1 ? 1 : 0;

    printf("%d\n",flg_count + flg1 + flg2 + flg3);

    return 0;
}