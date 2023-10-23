#define ROW 3
#define COL 3

/* Function declarations */
void matrixInput(int *mat);
void matrixPrint(int *mat);
void matrixMultiply(int *mat1, int *mat2, int *res);


void matrixInput(int *mat)
{
    int row, col;

    for (row = 0; row < ROW; row++)
    {
        for (col = 0; col < COL; col++)
        {
            scanf("%d", (mat + row * COL + col));
        }
    }
}


void matrixPrint(int *mat)
{
    int row, col;

    for (row = 0; row < ROW; row++)
    {
        for (col = 0; col < COL; col++)
        {
            printf("%d ", *(mat + row * COL + col));
        }

        printf("\n");
    }
}


void matrixMultiply(int *mat1, int *mat2, int *res)
{
    int row, col, i;
    int sum;

    for (row = 0; row < ROW; row++)
    {
        for (col = 0; col < COL; col++)
        {
            sum = 0;

            for (i = 0; i < COL; i++)
            {
                sum += *(mat1 + row * COL + i) * *(mat2 + i * COL + col);
            }

            *(res + row * COL + col) = sum;
        }
    }
}