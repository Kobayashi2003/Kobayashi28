// #include<stdio.h>
// #include<stdlib.h>
#include <iostream>

using namespace std;

int fact(int n, int* arr) {
	if (n == 1)
		return 1;
	if (arr[n] == 0) {
		// arr[n] = n * fact(n - 1, arr);
		
	}
	return arr[n];
}

int main() {
	int T = 0;
	int arr[1000] = { 1,1 };
	// scanf("%d", &T);
	cin >> T;
	int i=0;
	for (i = 0; i < T; i++) {
		int n;
		cin >> n;
		int j = 0, total = 0;
		if (n % 2 == 0 && n >= 2) {
			for (j = 1; j <= n / 2; j++)
				total += (fact(n - j + 1,arr) / fact(n - 2 * j + 1,arr)) / fact(j,arr);
		}
		else if (n == 1) {
			total = 1;
		}
		else {
			for (j = 1; j <= (n / 2 + 15); j++)
				total += (fact(n - j + 1,arr) / fact(n - 2 * j + 1,arr)) / fact(j,arr);
		}
		// printf("%d\n", total);
		cout << total << endl;
	}
	return 0;
}
