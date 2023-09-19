
#include <cstdio>
#include <algorithm>

using namespace std;

int a[100], b[100];
int n;

int main() {
	while (scanf("%d", &n) != EOF) {
		for (int i = 0; i < n; i++)scanf("%d", &a[i]);
		for (int i = 0; i < n; i++)scanf("%d", &b[i]);
		if (n % 2 == 1) {
			printf("NO");
			continue;
		}
		sort(a, a + n);
		sort(b, b + n);
		int ok = 1;
		for (int i = 0; i < n / 2; i++) {
			if (a[i] > b[i + n / 2])
				ok = 0;
		}
		for (int i = 0; i < n / 2; i++) {
			if (b[i] > a[i + n / 2])
				ok = 0;
		}
		if (ok) printf("YES");
		else printf("NO");
	}
	return 0;
}