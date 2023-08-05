#include<iostream>
using namespace std;
int main()
{
	int total; cin >> total;
	int num; cin >> num;
	int *ord_arr = new int[total];
	for (int i = 0; i < total; ++i) {
		ord_arr[i] = i + 1;
	}
	int *out_ord = new int[total];
	int count = 0;
	int cur_ord = 0;
	int out_count = 0;
	while (total != out_count) {
		count += 1;
		while (ord_arr[cur_ord] == 0) {
			cur_ord = (cur_ord + 1) % total;
		}
		if (count % num == 0) {
			out_ord[out_count++] = ord_arr[cur_ord];
			ord_arr[cur_ord] = 0;
			count = 0;
		}
		cur_ord = (cur_ord + 1) % total;
	}

	// 输出序列
	for (int i = 0; i < total; ++i) {
		cout << out_ord[i] << " ";
	}

	return 0;
}