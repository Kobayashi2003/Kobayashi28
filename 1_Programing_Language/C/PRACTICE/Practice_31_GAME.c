#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<stdbool.h>
int ROUND;
bool PLAY_ROLL_DICE()
{
    bool ROLL_DICE(int);
    srand(time(NULL));
    int target=rand()%6+rand()%6+2;
    printf("Round%d: %d\n",ROUND,target);
    switch(target)
    {
        case 7: case 11:
        return true;

        case 2: case 3: case 12:
        return false;

        default:
        getchar();
        ROUND++;
        return ROLL_DICE(target);
    }
}
bool ROLL_DICE(int target)
{
    srand(time(NULL));
    int tmp=rand()%6+rand()%6+2;
    printf("Round%d: %d\n",ROUND,tmp);

    if(tmp==target)
        return true;
    switch(tmp)
    {
        case 7:
        return false;
        default:
        getchar();
        ROUND++;
        return ROLL_DICE(target);
    }
}
int main()
{
    bool ROLL_DICE_F(void),ROLL_DICE(int);
    char c;
    do
    {
        ROUND=1;
        switch(PLAY_ROLL_DICE())
        {
            case true:
            printf("YOU ARE WIN!!\n");break;
            case false:
            printf("YOU ARE LOST..\n");break;
        }
        printf("Do you want to start the next game?(Y(yes)||N(no))\n");
        scanf("%c",&c);
        getchar();
    }while(c=='Y'||c=='y');

    return 0;
}