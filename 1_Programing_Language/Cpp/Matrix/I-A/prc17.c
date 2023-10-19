#include <stdio.h>

char *insert(char *s1, char*s2, int n) {

    int len1 = 0, len2 = 0;
    while (s1[len1] != '\0') len1++;
    while (s2[len2] != '\0') len2++;

    for (int i = 0; i < len1-n; ++i) {
        s1[len1+len2-i-1] = s1[len1-i-1];
    }

    for (int i = 0; i < len2; ++i) {
        s1[n+i] = s2[i];
    }

    s1[len1+len2] = '\0';

    return s1;
}

int main()
{
	int n = 0;
	char s1[100] = {0};
	char s2[100] = {0};

	scanf("%s", s1);
	scanf("%s", s2);
	scanf("%d", &n);

	char *ss = insert(s1, s2, n);
	printf("%s", ss);

	return 0;
}
