// f(n, m) = [f(n-1, m) + m] % n (n > 1)
// f(1, m) = 0

#include <iostream>

using namespace std;

int JosephusRing(int n, int m) {
	if (n == 1) { return 0; }
	return (JosephusRing(n - 1, m) + m) % n;
}

int main() {

	int n, m;
	cin >> n >> m;

	cout << JosephusRing(n, m) + 1 << endl;

	return 0;
}