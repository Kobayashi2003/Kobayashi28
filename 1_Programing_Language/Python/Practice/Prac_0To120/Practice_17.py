"""
定义一个工具类
每件工具都有自己的 name
需求 -- 在 类 封装一个 show_tool_count 的类方法，输出使用当前这个类，创建的对象个数
"""

class Tool:

    count = 0

    @classmethod
    def show_tool_count(cls):
        print(f"the number of tools: {cls.count}")

    def __init__(self, name):
        self.name = name
        Tool.count += 1
