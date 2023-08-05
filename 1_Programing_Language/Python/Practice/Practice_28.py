# 提示用户输入一个整数
try:
    num = int(input("please input a integer number: "))
    # 使用 8 除以用户输入的整数并且输出
    result = 8 / num
    print(result)

except ZeroDivisionError:
    print("除零错误")

except ValueError:
    print("请输入正确的整数")

except Exception as result:
    print(f"未知错误 {result}")