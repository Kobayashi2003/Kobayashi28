# 字符串
# string = "this is a string"

## 使用方法修改字符串的大小写 这些函数调用后均不会改变变量本身的值
# print(string.title())
# print(string.upper())
# print(string.lower())

## 在字符串中使用变量

### f字符串

# string1 = "hello"
# string2 = "world"
# string3 = f"{string1} {string2} !" # f 是 format的简写，Python将通过把花括号内的变量替换为其值来设置字符串的格式
# print(string3)

# f字符串是在Python3.6时引入的，如果是使用更早的版本，则需要使用 format() 方法 #

# string4 = "{} {} !".format(string1, string2)
# print(string4)


## 删除空白

# 要确保字符串末尾没有空白，可使用方法 rstrip() 该方法不会改变变量本身的值 #

# string5 = "   blank    "
# print(string5.rstrip() == "blank")

# 也可以剔除字符串开头的空白，或者同时剔除字符串两边的空白 #
# print(string5.lstrip())
# print(string5.strip())


# 数

## 数中的下划线

# 书写很大的数时，可使用下划线将其中的数字分组，使其更加清晰易读 #

# num = 100_100_100 # 这种表示法适用于整数和浮点数，但只有 Python 3.6 和更高版本支持
# print(num) # Python不会打印其中的下划线

## 同时给多个变量赋值

# x, y, z = 0, 0, 0

## 常量

# Python 没有内置的常量类型，一般使用全大写来指出将某个变量视为常量 #

# MAX = 100

## Python 之禅

# import this


# 列表

# List = ["string", 1, 2.3]

# print(List) # 你可以连着 [] 一同将列表打印出来

# 你可以通过负数从后开使访问列表元素 #
# print(List[-1])

# 可以通过 append() 方法在列表末尾添加元素 #
# List.append("string2")
# print(List)

# 通过 insert() 在列表中插入元素 #
# List.insert(1, "string3")
# print(List)

# 通过 del语句 删除元素 #
# del List[-1]
# print(List)

# 通过 pop() 方法弹出 列表末尾 的元素，并使用它 #
# ele = List.pop();
# print(List)
# print(ele)

# 通过 pop() 弹出列表中任何位置的元素 #
# List.pop(1)
# print(List)

# 通过 remove() 方法根据值删除元素 #
# List.remove(1) # remove() 方法只删除第一个指定的值，如果要删除的值可以能在列表中出现多次，就需要使用循环来确保每个数都被删除
# print(List)

# 使用方法 sort() 对列表永久排序 #
# List = ['a', 'c', 'b']
# List.sort();
# print(List)

# 还可以通过向 sort 传递参数 reverse = True 实现反向排序 #
# List.sort(reverse = True)
# print(List)

# 使用函数 sorted() 对列表临时排序 #
# print(sorted(List)) # 同理也可以向 sorted() 传递参数 reverse = True
# print(List)

# 使用 reverse() 方法永久反转列表 #
# List.reverse()
# print(List)

# 使用函数 len() 确认列表的长度 #
# print(len(List))


# 遍历整个列表 #
# i = 0
# for ele in List: # 这有个冒号
#     print(f"the {i} element is {ele}")
#     i += 1 # Python 根据缩进来判读代码行与前一个代码行之间的关系，Python中的代码块可以通过缩进体现


# 使用函数 range() #

# for value in range(0, 5): # Python 将会从指定的第一个值开始，并在到达你指定的第二个值时停止
#     print(value)

# 使用 range() 创建数字列表 #
# 可使用函数 List() 将 range() 的结果直接转换为列表 #
# numbers = list(range(0, 10))
# print(numbers)

# 在使用 range() 的时候还可以为这个函数指定第三个参数来指定步长 #
# numbers = list(range(0, 10, 2))
# print(numbers)

# 对数字列表执行简单的统计计算 #
# print(f"min:{min(numbers)} max:{max(numbers)} sum:{sum(numbers)}")

# 列表切片 #
# print(numbers[0:3])
# print(numbers[:2])

# 遍历切片 #
# for num in numbers[:3]:
    # print(num)

# 复制列表 #
# new_numbers = numbers[:]
# print(new_numbers) # 新创建的列表将与原来的列表相独立（但如只是将一个列表赋值给另一个列表，将不会产生新的列表：new_numbers = numbers）

# 不可变的列表 —— 元组（tuple） #
# t = ("string1", "string2")  # 如此定义出来的元组中的元素将不能够修改
                            # 严格来说，元组是由逗号标识的，圆括号只是让元组看起来更整洁、更清晰。
                            # 如果你要定义只包含一个元素的元组，必须在这个元素后面加上逗号 t = (1,)
                            # 创建只包含一个元素的元组通常没有意义，但自动生成的元组有可能只有一个元素
# print(t)

# 遍历元组 #
# for i in t :
    # print(i)

# 修改元组变量 #

# 虽然不能修改元组的元素，但可以给存储元组的变量赋值，因此可以重新定义整个元组 #




# if-elif-else 结构
# a = 1
# b = 1
# if a == b:
#     print("true")
# else :
#     print("false")

# 可以使用 and 与 or 检查多个条件 #

# 检查特定值是否包含在列表中 #

# print(2 in numbers)
# print(1 in numbers)

# 检查特定值是否不包含在列表中 #

# print(1 not in numbers)



# 字典

# 在 Python 中， 字典是一系列键值对。每个键都与一个值相关联，你可以使用键来访问相关联的值。与键相关联的值可以是数、字符串、列表乃至字典。事实上，可将任何 Python 对象用作字典中的值 #
# m = {'data1' : "string", 'data2' : 1} # 你也可以先创建一个空字典，然后在往里面添加值
# print(m['data1'])
# print(m['data2'])

# 添加键值对 #
# m['data3'] = True # 你也可以通过这种方法修改键值对中的值
# print(m)

# 删除键值对 #
# del m['data3']
# print(m)

# 使用 get() 来访问值 #
# 为防止由访问不存在的键所导致的问题，可使用方法 get() 在指定的键不存在时返回一个默认值
# 方法 get() 的第一个参数用于指定键，是必不可少的；第二个参数为指定的键不存在时要返回的值，是可选的
# 在调用 get() 时，如果没有指定第二个参数且指定的键不存在，Python 将放回值 None。这个特殊值表示没有相应的值。
# value = m.get('data4', 'No point value assigned')
# print(value)


# 遍历字典 #
# for key, value in m.items(): # items() 返回一个键值对列表
#     print(f"{key}:{value}")

# 遍历字典中的所有键 #
# for name in m.keys(): # 方法 keys() 可以返回一个列表，其中包含字典中的所有键
#     print(name)
# 遍历字典时，会默认遍历所有的键，因此，如果将上述代码替换为：
# for name in m: # 效果相同
#     print(name)


# 按特定顺序遍历字典中的所有键 #
# for name in sorted(m.keys()): # 从 Python 3.7 起，遍历字典时将按插入顺序返回其中的元素
#     print(name)


# 遍历字典中的所有值 #
# for value in m.values():
#     print(value) # 这种做法提取字典中所有的值，而没有考虑是否存在重复

# 设置集合，让每一个值都是唯一的 #
# for value in set(m.values()):
#     print(value)

# 直接创建集合 #
# s = {'string1', 'string2', 'stirng3'}

# Python 中可以实现各种嵌套 #



# input() 函数

# message = input("please input a string:") # input() 接受一个参数——要向用户显示的提示（promote）
# # 同时注意，input() 将用户的输入解释为一个字符串，该函数不会忽略空格
# print(message)

# 使用 int() 来获取数值输入
# 函数 int() 将数的字符串表示转换为数值表示
# age = input("please input a number:")
# age = int(age)
# print(age)


# while 循环
# i = 0
# while i < 3:
#     print(i)
#     i += 1

# flag #
# active = True # 我们称像 active 这样的变量为 标志（flag）
# i = 1
# while active:
#     if i % 7 != 0 :
#         print(i)
#         i += 1
#     else :
#         active = False


# 使用 break 可以退出循环 #
# 使用 continue 可以提前进入下次循环 #


# 使用 while 循环处理列表和字典 #
# for循环是一种遍历列表的有效方式，但不应在for循环中修改列表，否则将导致 Python 难以追踪其中的元素
# 要在遍历列表的同时对其进行修改，可以使用 while 循环



# 函数

# 定义函数 #
# def greet():
#     print("hello world")
# greet()


# 传递实参 #

## 位置实参 ## 在函数中，可根据需要使用任意数量的位置实参，Python 将按顺序将函数调用中的实参关联到函数定义中相应的形参

## 关键字实参 ## 关键字实参是传递给函数的名称值对。因为直接在实参中将名称和值关联起来，所以向函数传递实参时不会混淆。关键字实参让你无需考虑函数调用中的实参顺序，还清楚地指出了函数调用中各个值得用途

# def fun(data1, data2) :
#     print(f"data1: {data1}, data2: {data2}")
# fun(data2 = 2, data1 = 1)


# 默认值 # 同 C++


# 向函数传递列表副本而非原型 #
# def fun(List):
#     """blank"""
# l = ["string1", "string2"]
# fun(l[:])


# 传递任意数量的实参 # （通用形参名 *args）
# def fun(* parameters):  # * 让 Python 创建一个名为 parameters 的空元组，并将函数收到的所有值都封装到这个元组中
#                         # 你也可以结合使用位置实参和任意数量实参，但前提是必须在函数定义中将接纳任意数量实参的形参放在最后
#     """blank"""


# 使用任意数量的关键字实参 # （通用形参名 **kwargs）
# def fun(** parameters): # ** 让 Python 创建一个名为 parameters 的空字典，并将收到的所有名称值都放到这个字典中
#     """blank"""


# 将函数存储在模块中 #

## 模块是扩展名为 .py 的文件。可用 import 来导入模块，然后通过 module_name.function() 的语法调用模块内的函数
## 也可以通过 from module_name import function_naem 的语法来导入特定的函数


# 使用 as 给函数指定别名 #

## 要给函数指定别名则需要在导入它时指定  from module_name import function_name as other_function_name


# 使用 as 给模块指定别名 #

## import module_name as mn


# 导入模块内的所有函数 #

## import module_name *



# 类

# 创建类 #

# class A:

#     def __init__(self, parameters): # 构造函数，其中参数 self 为必须，Python将会自动传入实参 self，它是一个指向实例本身的引用
#                                     # 以 self 为前缀的所有变量可供类中的所有方法使用，而像这样可以通过实例访问的变量称为属性
#         self.parameters = parameters


# 继承

# class Father:
#     def __init__(self, data1):
#         self.data1 = data1

#     def showData(self):
#         print(self.data1)

# class Son(Father): # 必须在此处指定父类的名称
#     def __init__(self, data1, data2):
#         super().__init__(self, data1) # super() 是一个特殊的函数，让你能够调用父类的方法（父类也称为超类（superclass），super也由此而来）
#         self.data2 = data2


# 重写父类方法 #
## 直接在子类定义相同名称的函数即可，这样，Python 将不会考虑这个父类方法，而只关注你在子类中定义的相应方法

# 将实例用作属性 #


# 导入类 #
## 导入方法同函数的导入



# 文件和异常

# 从文件之中读取数据 #

## 读取整个文件 ##


# import os, sys
# os.chdir(sys.path[0]) # 为了让 Python插件能够正确的通过 Terminal 调用相对路径，你需要加上这两行代码

# with open('test.txt') as file_object:
# # 函数 open() 任何方式使用文件，哪怕仅仅是打印其内容，都得先打开文件，才能访问它。函数 open() 接受一个参数：要打开的文件的名称。Python 在当前执行的文件所在的目录查找指定的文件。函数 open() 返回一个表示文件的对象，Python 会将该对象赋给后面的 file_object 供以后使用
# # 关键字 with 在不再需要访问文件后将其关闭（当然你也可以通过调用 close() 来关闭文件，这不过这样做将会存在一定风险）
# # 方法 read() 读取这个文件的全部内容，并将其作为一个字符串赋给变量 contents
# # read() 在到达文件末尾时返回一个空字符串，而这个空字符串显示出来时就是一个空行。要想删除该多出来的空行，可以在函数调用 print() 中使用 rstrip()
#     contents = file_object.read()
# print(contents)



## 文件路径 ##

# 相对路径
# 绝对路径


## 逐行读取 ##

# file_path = 'C:/Users/17312/Desktop/Code/PY/test.txt'
# with open(file_path) as file_object:
#     for line in file_object:
#         print(line)


## 创建一个包含文件各行内容的列表 ##

# 使用关键字 with 时，open() 返回的文件对象只在 with 代码块中可用。
# 如果要在 with 代码块外访问文件的内容，可在 with 代码块内将文件的各行存储在一个列表中，并在 with 代码块外使用该列表

# file_path = 'C:/Users/17312/Desktop/Code/PY/test.txt'
# with open(file_path) as file_object:
#     lines = file_object.readlines()



## 注意：读取文本时，Python将其中所有的文本都解读为字符串。如果读取的是数，并要将其作为数值使用，就必须使用函数 int() 将其转换为整数或使用函数 float() 将其转换为浮点数




# 写入文件 #

# file_path = 'C:/Users/17312/Desktop/Code/PY/test.txt'
# with open(file_path, 'w') as file_object: # 打开文件时，可指定读取模式（'r'），写入模式（'w'），附加模式（'a'）或读写模式（'r+'），如果省略了模式实参，Python将默认以只读模式打开文件。
#     # 注意，以写入模式（'w'）打开文件时如果指定的文件已经存在，Python 将在返回文件对象前清空该文件的内容
#     # Python 只能将字符串写入文本文件。要将数值数据存储到文本文件中，必须先使用函数 str() 将其转换为字符串格式
#     file_object.write('hello world !')



# 异常

## try-except 代码块 ##

## try-except-else 代码块 ##

## Python 尝试执行 try 代码块中的代码，只有可能引发异常的代码才需要放在 try 语句中。有时候，有一些仅在 try 代码块成功执行时才需要运行的代码，这些代码应放在 else 代码块中。except 代码块告诉 Python，如果尝试运行 try 代码块中的代码时引发了指定的异常该怎么办

## 处理 FileNotTFOundError 异常 ##

# file_path = 'C:/Users/17312/Desktop/Code/PY/test.txt'

# try:
#     with open(file_path, encoding='utf-8') as f: # 在系统的默认编码与要读取的文件使用的编码不一致时，必须要使用 encoding
#         contents = f.read()
# except FileNotFoundError:
#     print(f"the file {file_path} does not exist")


## 分析文本 ##

## 方法 split() 方法 split() 以空格为分隔符将字符串拆分为多个部分，并将这部分全部存储到一个列表当中

# file_path = 'C:/Users/17312/Desktop/Code/PY/test.txt'
# with open(file_path, encoding = 'utf-8') as f:
#     contents = f.read().split()
#     print(len(contents))


## 静默失败 ##

## 在 expect 代码块中使用 pass 语句，用于让 Python 在代码块中什么都不要做



# 存储数据 #

## JSON （JavaScript Object Notation）

## 使用 json.dump() 和 json.load() ##

# import os, sys, json
# os.chdir(sys.path[0])

# numbers = [0, 1, 2]
# with open('test.json', 'a') as f:
#     json.dump(numbers, f)


# import os, sys, json
# os.chdir(sys.path[0])

# filename = 'test.json'
# with open(filename) as f:
#     numbers = json.load(f)
# print(numbers)





# 测试代码

# 测试函数 #

## 单元测试和测试用例 ##
## 单元测试用于核实函数的某个方面没有问题。测试用例是一组单元测试

## 可通过的测试 ##

## ./Practice_4.py

## 各种断言方法 ##

# assertEqual(a, b)
# assertNotEqual(a, b)
# assertTrue(x)
# assertFalse(x)
# assertIn(item, list)
# assertNotIn(item, list)

# 测试类 #

# 要测试类的行为，需要创建它的实例


