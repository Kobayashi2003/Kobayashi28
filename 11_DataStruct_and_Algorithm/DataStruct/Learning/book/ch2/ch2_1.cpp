// 最大子列和问题


#include <vector>

using namespace std;

// O(n^3)
int maxSubSum1(const vector<int> &a)
{
    int maxSum = 0;
    for (int i = 0; i < a.size(); i++)
        for (int j = i; j < a.size(); j++)
        {
            int thisSum = 0;
            for (int k = i; k <= j; k++)
                thisSum += a[k];
            if (thisSum > maxSum)
                maxSum = thisSum;
        }
    return maxSum;
}


int maxSubSum2(const vector<int> &a)
{
    int maxSum = 0;
    for (int i = 0; i < a.size(); i++)
    {
        int thisSum = 0;
        for (int j = i; j < a.size(); j++)
        {
            thisSum += a[j];
            if (thisSum > maxSum)
                maxSum = thisSum;
        }
    }
    return maxSum;
}


int maxSubSum(const vector<int> &a, int left, int right)
{
    if (left == right)
        if (a[left] > 0)
            return a[left];
        else
            return 0;
    int center = (left + right) / 2;
    int maxLeftSum = maxSubSum(a, left, center);
    int maxRightSum = maxSubSum(a, center + 1, right);

    int maxLeftBorderSum = 0, leftBorderSum = 0;
    for (int i = center; i >= left; i--)
    {
        leftBorderSum += a[i];
        if (leftBorderSum > maxLeftBorderSum)
            maxLeftBorderSum = leftBorderSum;
    }

    int maxRightBorderSum = 0, rightBorderSum = 0;
    for (int i = center + 1; i <= right; i++)
    {
        rightBorderSum += a[i];
        if (rightBorderSum > maxRightBorderSum)
            maxRightBorderSum = rightBorderSum;
    }

    // return max3(maxLeftSum, maxRightSum, maxLeftBorderSum + maxRightBorderSum);
    return max(max(maxLeftSum, maxRightSum), maxLeftBorderSum + maxRightBorderSum);
}


int maxSubSum3(const vector<int> &a)
{
    return maxSubSum(a, 0, a.size() - 1);
}


int maxSubSum4(const vector<int> &a)
{
    int maxSum = 0, thisSum = 0;
    for (int i = 0; i < a.size(); i++)
    {
        thisSum += a[i];
        if (thisSum > maxSum)
            maxSum = thisSum;
        else if (thisSum < 0)
            thisSum = 0;
    }
    return maxSum;
}