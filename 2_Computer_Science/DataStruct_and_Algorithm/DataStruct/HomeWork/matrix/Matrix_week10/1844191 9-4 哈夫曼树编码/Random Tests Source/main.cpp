#include <iostream>
#include <vector>
#include <random>
#include <queue>
#include <stdlib.h>
#include <time.h>
#include <queue>
using namespace std;

int main() {
	srand(time(0));
	int k;
    char Dict[]={'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O'};
	k = 5+(rand() % 10);
	cout << k <<endl;
    int val_upper = 100;
	for (int i = 0; i < k; i++) {
		cout <<Dict[i]<<" "<< 1+rand() % val_upper<<endl;
	}
	return 0;
}

