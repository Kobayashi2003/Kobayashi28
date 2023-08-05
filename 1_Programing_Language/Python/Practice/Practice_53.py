def length_of_LIS(nums):
    n = len(nums) # 5
    L = [1] * n # initial value: [1, 1, 1, 1, 1]

    for i in reversed(range(n)):
        for j in range(i + 1, n):
            if nums[j] > nums[i]: # is increasing seq
                L[i] = max(L[i], L[j] + 1)

    return max(L)

nums = [1, 5, 2, 4, 3]
print(length_of_LIS(nums))
