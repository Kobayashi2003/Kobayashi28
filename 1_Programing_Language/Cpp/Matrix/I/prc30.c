void Transpose(int (*matrix)[3]);

void Transpose(int (*matrix)[3]) {
    int i, j, temp;
    for (i = 0; i < 3; i++) {
        for (j = i; j < 3; j++) {
            temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }
}