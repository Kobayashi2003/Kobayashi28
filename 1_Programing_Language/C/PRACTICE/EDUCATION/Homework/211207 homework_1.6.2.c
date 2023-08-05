void enter_string(char str[80])
{
    gets(str);
}
void delete_string(char str[],char ch)
{
    int i,j;
    for(i=j=0;str[i]!='\0';i++)
        if(str[i]!=ch)
            str[j++]=str[i];
    str[j]='\0';
}
void print_string(char str[])
{
    printf("%s\n",str);
}
