/**
 * C program to sort an array using pointers.
 */

#include <stdio.h>

#define MAX_SIZE 100


/* Function declaration */
void inputArray(int *arr, int size);
void printArray(int *arr, int size);

/* Sort function declaration */
int Ascending(int *num1, int *num2);
int Descending(int *num1, int *num2);

void sort(int *arr, int size, int (* compare)(int *, int *));


void inputArray(int *arr, int size) {
    for (int i = 0; i < size; ++i) {
        scanf("%d", arr + i);
    }
}

void printArray(int *arr, int size) {
    for (int i = 0; i < size; ++i) {
        printf("%d ", *(arr + i));
    }
    printf("\n");
}

int Ascending(int *num1, int *num2) {
    return *num1 > *num2;
}

int Descending(int *num1, int *num2) {
    return *num1 < *num2;
}

void sort(int *arr, int size, int (* compare)(int *, int *)) {
    int temp;

    for (int i = 0; i < size - 1; ++i) {
        for (int j = 0; j < (size - 1 - i); ++j) {
            if (compare(arr + j, arr + j + 1)) {
                temp = *(arr + j);
                *(arr + j) = *(arr + j + 1);
                *(arr + j + 1) = temp;
            }
        }
    }
}

int main()
{
	int arr[MAX_SIZE];
	int size;

	/*
	 * Input array size and elements.
	 */
	//printf("Enter array size: ");
	scanf("%d", &size);
	//printf("Enter elements in array: ");
	inputArray(arr, size);


	printf("Elements before sorting: ");
	printArray(arr, size);


	// Sort and print sorted array in ascending order.
	printf("\nArray in ascending order: ");
	sort(arr, size, Ascending);
	printArray(arr, size);


	// Sort and print sorted array in descending order.
	printf("\nArray in descending order: ");
	sort(arr, size, Descending);
	printArray(arr, size);


	return 0;
}

