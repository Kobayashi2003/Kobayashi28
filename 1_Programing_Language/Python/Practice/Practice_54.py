# Find the maximum sum of continuous subsequences

# [3, -4, 2, -1, 2, 6, -5, 4]


from random import randint

# 1. Brute-Force Enumeration
def max_sum(nums):
    """Find the maximum sum of continuous subsequences"""
    max_sum = 0
    for i in range(len(nums)):
        tmp_sum = 0
        for j in range(i, len(nums)):
            tmp_sum += nums[j]
            max_sum = max(max_sum, tmp_sum)
    return max_sum


# nums = [3, -4, 2, -1, 2, 6, -5, 4]

nums = [randint(-100, 100) for i in range(5000)]
print(max_sum(nums))