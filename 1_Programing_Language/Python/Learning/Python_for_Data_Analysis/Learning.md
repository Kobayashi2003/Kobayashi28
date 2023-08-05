# IPython 基础

## 内省

- 在一个变量名的前后使用问号 `?` 可以显示一些关于该对象的概要信息，如果对象是一个函数或实例方法且文档字符串已经写好，则文档字符串将会显示出来
- 使用 `??` 可以显示函数的源代码


## IPython 常用的魔术命令

命令|描述
-|-
%quickref|显示 IPython 快速参考卡
**%magic**|显示所有魔术命令的详细文档
%debug|从最后发生报错的底部进入交互式调试器
%hist|打印命令输入（也可以打印输出）历史
%pdb|出现任意报错后自动进入调试器
%paste|从剪切板中执行已经预先格式化的 Python 代码
%cpaste|打开一个特殊提示符，手动粘贴待执行的 Python 代码
**%reset**|删除交互式命名空间中所有的变量 / 名称
%page [OBJECT]|通过分页器更美观地显示一个对象
**%run [script.py]**|在 IPython 中运行一个 Python 脚本
%prun [statement]|使用 CProfile
%time [statement]|报告单个语句的执行时间
**%timelit [statement]**|多次执行单个语句计算平均执行时间；在估算代码最短执行时间时有用
**%xdel [variable]**|在 IPython 内部删除一个变量，清除相关引用


# Python 基础

## 一切皆为对象

Python 语言的一个重要特征就是对象模型的一致性。每一个数值、字符串、数据结构、函数、类、模块以及所有存在于 Python 解释器中的事物，都是 Python 对象。每个对象都会关联到一种类型和内部数据。甚至连函数也能被当作对象来操作

## 动态引用、强类型

## 鸭子类型

## 数值类型

类型|描述
-|-
None|Python 的 'null' 值（只存在一个实例）
str|字符串类型，包含 Unicode（UTF-8 编码）字符串
bytes|原生 ASCII 字节（或者 Unicode 编码字节）
float|双精度 64 位浮点数值（请注意没有独立的double类型）
bool|布尔值
int|任意精度无符号整数


## 字节与 Unicode

将 Unicode　字符串转换为　UTF-8 字节可使用 `.encode('utf-8')`

然后可以使用 `decode('utf-8')` 进行解码
