#include <stdio.h>
#include <string.h>
 
bool BadChar(const char *pattern, int nLen, int *pArray, int nArrayLen)
{
    if (nArrayLen < 256)
    {
        return false;
    }
    for (int i = 0; i < 256; i++)
    {
        pArray[i] = -1;
    }
    for (int i = 0; i < nLen; i++)
    {
        pArray[pattern[i]] = i;
    }
    return true;
}
 
int SundaySearch(const char *dest, int nDLen,
                 const char *pattern, int nPLen,
                 int *pArray)
{
    if (0 == nPLen)
    {
        return -1;
    }
    for (int nBegin = 0; nBegin <= nDLen-nPLen; )
    {
        int i = nBegin, j = 0; 
        for ( ;j < nPLen && i < nDLen && dest[i] == pattern[j];i++, j++);
        if (j == nPLen)
        {
            return nBegin;
        }
        if (nBegin + nPLen > nDLen)
        {
            return -1;
        }
        else
        {
            nBegin += nPLen - pArray[dest[nBegin+nPLen]];
        }
    }
    return -1;
}
 
void TestSundaySearch()
{
    int         nFind;
    int         nBadArray[256]  = {0};
                               //        1         2         3         4
                               //0123456789012345678901234567890123456789012345678901234
    const char  dest[]      =   "abcxxxbaaaabaaaxbbaaabcdamno";
    const char  pattern[][40] = {
        "a",
        "ab",
        "abc",
        "abcd",
        "x",
        "xx",
        "xxx",
        "ax",
        "axb",
        "xb",
        "b",
        "m",
        "mn",
        "mno",
        "no",
        "o",
        "",
        "aaabaaaab",
        "baaaabaaa",
        "aabaaaxbbaaabcd",
        "abcxxxbaaaabaaaxbbaaabcdamno",
    };
 
    for (int i = 0; i < sizeof(pattern)/sizeof(pattern[0]); i++)
    {
        BadChar(pattern[i], strlen(pattern[i]), nBadArray, 256);
        nFind = SundaySearch(dest, strlen(dest), pattern[i], strlen(pattern[i]), nBadArray);
        if (-1 != nFind)
        {
            printf("Found    \"%s\" at %d \t%s\r\n", pattern[i], nFind, dest+nFind);
        }
        else
        {
            printf("Found    \"%s\" no result.\r\n", pattern[i]);
        }
 
    }}
 
int main(int argc, char* argv[])
{
    TestSundaySearch();
	return 0;
}