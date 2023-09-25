import unittest

from Practice_4_name_function import get_formatted_name

class NameTestCase(unittest.TestCase): # 这个类必须继承 unittest.TestCase 类
    def test_first_last_name(self): # 程序运行时，所有以 test_ 打头的方法都将自动运行
        formatted_name = get_formatted_name('janis', 'joplin')
        self.assertEqual(formatted_name, 'Janis Joplin') # 断言方法。断言方法核实得到的结果是否与期望的结果一致。

    def test_first_last_middle_name(self):
        formatted_name = get_formatted_name(
            'wolfgang', 'mozart', 'amadeus')
        self.assertEqual(formatted_name, 'Wolfgang Amadeus Mozart')

# 我们将直接运行给这个文件，的那需要指出的是，很多测试框架都会先导入测试文件再运行。导入文件时，解释器将会在导入的同时执行它
if __name__ == '__main__': # 特殊变量 __name__，这个变量是在程序执行时设置的。如果这个文件作为主程序执行，变量 __name__ 将被设置为 '__main__'
    unittest.main() # 在这里，调用 unittest.main() 来运行测试用例。如果这个文件被测试框架导入，变量 __name__ 的值将不是 '__main__' 因此不会调用 unittest.main()
