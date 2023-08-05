# 验证 尼科彻斯定理 即：任何一个整数m的立方都可以写成m个连续奇数之和
# 输入一个正整数 m （m < 100），将 m 的立方写成 m 个连续奇数之和的形式输出

m = int(input("Please input a number: "))

result = [m**2-m+1+2*i for i in range(0, m)]

print(result)