//检测变位词
#include <stdio.h>
#include <string.h>
#define N 25
int main()
{
    char word1[N] = {'\0'}, word2[N] = {'\0'};
    int index[26] = {0};
    printf("Enter first word: ");
    scanf("%[^\n]", word1);
    getchar();
    printf("Enter second word: ");
    scanf("%[^\n]", word2);

    strupr(word1);
    strupr(word2);

    int len1 = strlen(word1), len2 = strlen(word2);
    if (len1 != len2)
    {
        printf("The words are not anagrams.\n");
        return 0;
    }

    for (int i = 0; i < len1; i++)
    {
        index[word1[i] - 'A']++;
    }

    for (int i = 0; i < len2; i++)
    {
        if (index[word2[i] - 'A'] == 0)
        {
            printf("The words are not anagrams.\n");
            return 0;
        }
        else
            index[word2[i] - 'A']--;
    }

    printf("The words are anagrams.\n");
    return 0;
}