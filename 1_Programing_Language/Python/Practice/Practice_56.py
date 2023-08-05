# Find the maximum sum of continuous subsequences

# [3, -4, 2, -1, 2, 6, -5, 4]


from random import randint

memo = {}


def M(nums, i):
    """return the max sum in numbers"""
    if i in memo:
        return memo[i]

    if i == len(nums) - 1:
        return nums[i] if nums[i] > 0 else 0

    max_sum = max(nums[i], nums[i] + M(nums, i + 1))
    memo[i] = max_sum
    return max_sum


def find_max_sum(nums):
    max_sum = max(M(nums, i) for i in range(0, len(nums)))
    return max_sum


testData = [randint(-10, 10) for i in range(0, 900)]
print(testData)
print(find_max_sum(testData))