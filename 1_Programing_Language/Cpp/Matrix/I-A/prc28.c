#include "stdio.h"

#define CAT_NUM 318

int cat_num = CAT_NUM;

static int sleepy_cat = -1;
static int set_flag = 0;


void set_sleepy_cat(int cat_id);

// Use it:
int meow(int start, int end);

// Implement it:
int find_sleepy_cat(int start, int end);

void set_sleepy_cat(int cat_id)
{
    if (!set_flag) {
        sleepy_cat = cat_id;
        set_flag = 1;
    }
    else
        printf("DO NOT CALL set_sleepy_cat()!\n");
}


int meow(int start, int end)
{
    static int meow_counts = 0;
    meow_counts++;
    // printf("%d\n", meow_counts);
    
    if (meow_counts > 18 || end < start || start < 0 || end > cat_num)
        return -1;
    else {
        int sum = (end - start) * 100;
        if (sleepy_cat >= start && sleepy_cat < end)
            sum -= 10;
        return sum;
    }
}

int find_sleepy_cat(int start, int end)
{
    int mid = (start + end) / 2;
    int flg = (start + end) % 2;

    int left = meow(start, mid);
    int right = meow(mid + flg, end);

    if (left == -1 || right == -1)
        return -1;
    else if (left < right)
        return find_sleepy_cat(start, mid);
    else if (left > right)
        return find_sleepy_cat(mid + flg, end);
    else
        return mid;
}

int main()
{
    int sleepy_cat;
    scanf("%d", &sleepy_cat);
    set_sleepy_cat(sleepy_cat);
    printf("%d\n", find_sleepy_cat(0, CAT_NUM));

    return 0;
}
