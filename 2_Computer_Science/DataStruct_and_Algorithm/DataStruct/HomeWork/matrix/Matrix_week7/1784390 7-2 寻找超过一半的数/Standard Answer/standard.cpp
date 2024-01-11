#include <iostream>
#include <vector>
using namespace std;
int find(const vector<int> & id, int N)
{
	int candidate;
	int ntimes, i;
	for (int i = ntimes = 0; i < N; ++i)
	{
		if (ntimes == 0)
		{
			candidate = id[i];
			ntimes = 1;
		}
		else
		{
			if (candidate == id[i])
			{
				ntimes++;
			}
			else
			{
				ntimes--;
			}
		}
	}
	return candidate;
}
int main()
{
	int N;
	cin >> N;
	vector<int> v(N);
	for (int i = 0; i < N; ++i)
	{
		cin >> v[i];
	}
	cout << find(v, N);
	return 0;
}