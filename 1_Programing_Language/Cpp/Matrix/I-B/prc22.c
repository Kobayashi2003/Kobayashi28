# include <stdio.h>
#include <string.h>

int compareVersion(char *version1, char *version2);

int compareVersion(char *version1, char *version2) {
    int len1 = strlen(version1), len2 = strlen(version2);

    if (len1 == 0 && len2 == 0) {
        return 0;
    }

    unsigned long long int num1 = 0, num2 = 0;
    int i = 0, j = 0;
    while (i < len1 && version1[i] != '.') {
        num1 = num1 * 10 + version1[i] - '0';
        i++;
    }
    while (j < len2 && version2[j] != '.') {
        num2 = num2 * 10 + version2[j] - '0';
        j++;
    }

    if (num1 == num2) {
        char *p1 = version1 + i + 1, *p2 = version2 + j + 1;
        return compareVersion(p1, p2);
    }

    return num1 > num2 ? 1 : -1;
}

int main()
{
	int rst = 0;
	char ver1[101];
	char ver2[101];

	scanf("%s %s", ver1, ver2);
	rst = compareVersion(ver1, ver2);		//goal function

	switch (rst)
	{
		case 0:
			printf("The same version.");
			break;
		case 1:
			printf("%s is the new version.", ver1);
			break;
		case -1:
			printf("%s is the new version.", ver2);
			break;
		default:
			printf("invalid!");
			break;
	}

	return 0;
}