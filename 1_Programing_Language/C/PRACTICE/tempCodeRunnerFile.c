int main()
{
    int screen(void);
    void createHaffmanTree(DATA_TYPE *, int *, int);
    void deCode(int);
    void deCode_AUTO(char *);
    // TODO 妥协 受不了了 理想的输入应该是可以在终端中接受包括换行符在内的所有字符 并且输入最终以EOF作为收尾 但试验后发现一般的scanf或者getchar结合循环的输入方式会出现bug 因此相关的输入结构升级放由今后解决

    SeqList Table; //用于记录共有多少种的字符
    Table.data = (DATA_TYPE *)malloc(PER_CAPISITY * sizeof(DATA_TYPE));
    Table.cont = (int *)malloc(PER_CAPISITY * sizeof(int));
    Table.size = 0;
    Table.capisity = PER_CAPISITY;
    Table.n = 1;

    int num = 0;

    switch (screen())
    {
    case 1:
        assert(sizeof(DATA) / sizeof(DATA_TYPE) - 1 > 1);
        for (int i; i < (sizeof(DATA) / sizeof(DATA_TYPE)); i++)
        {
            for (int j = 0; j <= Table.size; j++)
            {
                if (j < Table.size && DATA[i] == Table.data[j])
                {
                    Table.cont[j]++;
                    break;
                }
                else if (j == Table.size)
                {
                    if (Table.size == Table.capisity)
                    {
                        Table.n++;
                        Table.capisity = PER_CAPISITY * Table.n;
                        Table.data = (DATA_TYPE *)realloc(Table.data, Table.capisity * sizeof(DATA_TYPE));
                        Table.cont = (int *)realloc(Table.cont, Table.capisity * sizeof(int));
                    }
                    Table.data[Table.size] = DATA[i];
                    Table.cont[Table.size] = 1;
                    Table.size++;
                    break;
                }
            }
        }
        createHaffmanTree(Table.data, Table.cont, Table.size - 1);
        break;

    case 2:
        if (AUTO_INPUT)
        {
            deCode_AUTO(HaffmanCode);
        }
        else
        {
            printf("Input the number of the types of code: ");
            scanf("%d", &num);
            deCode(num);
        }
        break;
    }
    return 0;
}