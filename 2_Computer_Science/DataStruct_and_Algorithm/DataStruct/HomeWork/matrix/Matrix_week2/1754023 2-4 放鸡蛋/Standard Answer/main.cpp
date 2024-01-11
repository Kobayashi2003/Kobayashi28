#include <iostream>

using namespace std;

int nums[100], maxPos;

void partition(int n, const int pos, const int maxNum);

int main()
{
	int n, t;
	cin >> t;
	while (t--)
	{
		cin >> n >> maxPos;
		partition(n, 0, n);
	}

	return 0;
}

void partition(const int n, const int pos, const int maxNum )
{
	if (n <= maxNum)
	{
		nums[pos] = n;
		cout << nums[0];
		for (int i=1; i<=pos; i++)
			cout << nums[i];
		for (int i=pos+1; i<maxPos; i++)
			cout << 0;
		cout << endl;
	}

	int tempNum;
	if (n > maxNum)
		tempNum = maxNum;
	else
		tempNum = n;

	while (1)
	{
		nums[pos] = tempNum;
		if (n > tempNum && pos < maxPos-1)
			partition(n-tempNum, pos+1, tempNum);
		tempNum--;
		if (tempNum < 1)
			break;
	}
}
