#include <stdio.h>
#include <string.h>


int indexOf(char *s1, char *s2)
{
  int i, j, k;
  int l1 = strlen(s1);
  int l2 = strlen(s2);
  for (i = 0; i <= l1 - l2; i++)
  {
    for (j = i, k = 0; k < l2; j++, k++)
    {
      if (s1[j] != s2[k])
        break;
    }
    if (k == l2)
      return i;
  }
  return -1;
}


int main()
{
  int t;
  scanf("%d", &t);
  while(t--)
  {
    // Prompt the user to enter a string
    printf("Enter the first string: ");
    char s1[80];
    scanf("%s",s1);
    // Prompt the user to enter a string
    printf("Enter the second string: ");
    char s2[80];
    scanf("%s",s2);
    printf("%d\n", indexOf(s1, s2));
  }
  return 0;
}
