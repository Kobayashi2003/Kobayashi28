#include<stdio.h>
#include<time.h>
#include<assert.h>
int main()
{
    char rute[]="D:/a.txt";
    int t=clock();
    for(int i=0; i<26;i++)
    {
        FILE *file=fopen(rute, "w");
        assert(file!=NULL);
        for(unsigned long long int i=0;i<=9999999ULL/*(1ULL<<63)*/;i++)
        {
            fprintf(file,"%u ",i);
            if(i%10==0) fprintf(file,"\n");
        }
        fclose(file);
        rute[3]++;
    }
    printf("%.3f",((double)(clock()-t)/CLOCKS_PER_SEC));
    return 0;
}