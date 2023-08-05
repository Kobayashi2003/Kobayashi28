from random import randint

memo = {}

def L(nums, i):
    """Returns the length of longest increasing subsequence starting from i"""

    if i in memo:
        return memo[i]

    if i == len(nums) - 1: # last number
        return 1

    max_len = 1
    for j in range(i+1, len(nums)):
        if nums[j] > nums[i]:
            max_len = max(max_len, L(nums, j) + 1)

    memo[i] = max_len
    return max_len

def length_of_LIS(nums):
    return max(L(nums, i) for i in range(len(nums)))

nums = [1, 5, 2, 6, 3, 4]
# nums = [randint(0,100) for i in range(0,5)]
print(length_of_LIS(nums))
