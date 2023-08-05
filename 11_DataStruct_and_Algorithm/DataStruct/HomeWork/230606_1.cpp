#include<string.h>
#include<iostream>

using namespace std;
void CountingSort(int array[], int nLength_, int nMaxNumber_)
{
    if (nullptr == array || nLength_ <= 0 || nMaxNumber_ <= 0)
        return;

    int* pCountArray = new int[nMaxNumber_ + 1];
    memset(pCountArray, 0, sizeof(int) * (nMaxNumber_ + 1));

    for (int i = 0; i < nLength_; ++i)
        ++pCountArray[array[i]];
    
    int nIndex = 0;
    for (int i = 0; i <= nMaxNumber_; ++i)
    {
        for (int j = 0; j < pCountArray[i]; ++j)
            array[nIndex++] = i;
    }

    delete[] pCountArray;
}


static void PrintArray(int array[], int nLength_);
int main(int argc, char* argv[])
{
	int num;
	cin >> num;
	int M;
	cin >> M;

	int* a = (int*)malloc(sizeof(int) * num);
	// int a[num];
	for (int i = 0; i < num; i++)
	{
		cin >> a[i];
	}
	CountingSort(a, num, M);
	PrintArray(a, num);
	return 0;
}

static void PrintArray(int array[], int nLength_)
{
	if (nullptr == array || nLength_ <= 0)
		return;

	for (int i = 0; i < nLength_; ++i)
	{
		std::cout << array[i] << " ";
	}
}

int main() {
    int n, M;
    cin >> n >> M;
    int *arr = new int[n];
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    CountingSort(arr, n, M);
    PrintArray(arr, n);

    delete[] arr;

    return 0;
}