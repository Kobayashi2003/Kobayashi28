#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<stdbool.h>
#define NUM_SULTS 4
#define NUM_RANKERS 13
int main()
{
    bool in_hand[NUM_SULTS][NUM_RANKERS]={false};
    int num_cards,rank,suit;
    const char rank_code[]={'2','3','4','5','6','7','8','9','t','j','q','k','a'};
    const char suit_code[]={'c','d','h','s'};
    srand((unsigned)time(NULL));
    printf("Enter number of cards in hand: ");
    scanf("%d",&num_cards);
    printf("Your hand:");
    while(num_cards > 0)
    {
        suit=rand()%NUM_SULTS;
        rank=rand()%NUM_RANKERS;
        if(!in_hand[suit][rank])
        {
            in_hand[suit][rank]=true;
            num_cards--;
            printf(" %c%c",rank_code[rank],suit_code[suit]);
        }
    }
    printf("\n");
    return 0;
}