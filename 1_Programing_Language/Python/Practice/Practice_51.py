from random import randint

def L(nums, i):
    """Returns the length of longest increasing subsequence starting from i."""

    if i == len(nums) - 1: # last number
        return 1

    max_len = 1
    for j in range(i + 1, len(nums)):
        if nums[j] > nums[i]:
            max_len = max(max_len, L(nums, j) + 1)
    return max_len


def length_of_LIS(nums):
    return max(L(nums, i) for i in range(len(nums)))


# nums = [1, 5, 2, 4, 3]
nums = [randint(0,100) for i in range(0,100)]
print(length_of_LIS(nums))

