# BeautifulSoup

## 运行 BeautifulSoup

当你创建一个 BeautifulSoup 对象时，需要传入两个参数：

`bs = BeautifulSoup(html.read(), 'html.parser')`

- 第一个参数时该对象所基于的 HTML 文本，第二个参数指定了你希望 BeautifulSoup 用来创建该对象的解析器。在大多数情况下，你选择任何一个解析器都差别不大
- `html.parser` 是 Python 3 中的一个解析器，不需要单独安装
- 另一个常用的解析器是 `lxml`，可以通过 pip 进行安装 `pip3 install lxml`
- `html5lib` 也是一个常用的解析器

BeautifulSoup 还可以使用 urlopen 直接返回的文件对象，而不需要先调用 `.read()` 函数

**获取页面中所有指定的标签**

`bs.find_all(tagname, tagAttributes)`

**get_text()**

- get_text() 会清除你正在处理的 HTML 文档中的所有标签，然后返回一个只包含文字的 Unicode 字符串

## BeautifulSoup 中的 find() 和 find_all()

这两个函数能够帮助你通过标签的不同的属性轻松地过滤 HTML 页面，查找需要的标签组或单个标签

定义：

`find_all(tag, attributs, recursive, text, limit, keywords)`
`find(tag, attributs, recursive, text, keywords)`

- 标签参数 tag —— 你可以传递一个标签的名称或多个标签名称组成的 Python 列表做标签参数
- 属性参数 attributs 用一个 Python 字典封装一个标签的若干属性和对应的属性值
- 递归参数 recursive 是一个布尔变量。如果你将其设置为 True， find_all 会根据你的要求去查找标签参数的所有子标签，以及子标签的子标签；如果 recursive 设置为 False， find_all就只查找文档的一级标签。find_all 默认是支持递归查找的（recursive 默认值是 True）
- 文本参数 text 使用标签的文本内容去匹配，而不是标签的属性
- 范围限制参数 limit 显然只用于 find_all 方法。find 其实等价于 limit 等于 1 时的 find_all
- 关键词参数 keyword 可以让你选择那些具有指定属性的标签

## 其它 BeautifulSoup 对象

- BeautifulSoup 对象
- 标签 Tag 对象  BeautifulSoup 对象通过 find 和 find_all，或者直接调用子标签获取的一列对象或单个对象
- NavigableString 对象  用来表示标签里的文字，而不是标签本身
- Comment 对象  用来查找 HTML 文档的注释标签


## 导航树

1. 处理子标签和其它后代标签 孩子（child） 后代（descendant）
2. 处理兄弟标签 next_siblings()  previous_siblings() next_sibling() previous_sibling()
3. 处理父标签 parent() parents()


## 正则表达式 和 BeautifulSoup

- 正则表达式可以作为 BeautifulSoup 语句的任意一个参数

## 获取属性

对于一个标签对象，可以用下面的代码获取它的全部属性：

`myTag.attrs`

注意这一行代码返回的是一个 Python 字典对象，可以轻松获取和操作这些属性。比如要获取图片的源位置src，可以用下面这行代码：

`myTag.attrs['src']`

## Lambda表达式

Lambda 表达式本质上就是一个函数，可以作为变量传入另一个函数；也就是说，一个函数不是定义成 `f(x, y)`，而是可以定义成 `f(g(x), h(y))` 的形式

BeautifulSoup 允许我们把特定类型的函数作为参数传入 find_all 函数。唯一的限制条件式这些函数必须把一个标签对象作为参数并且返回布尔类型的结果。BeautifulSoup 用这个函数来评估它遇到的每个标签对象，最后把评估结果为 真 的标签保留，把其它标签剔除

例如，下面的代码就是获取有两个属性的所有标签：

`bs.find_all(lambda tag: len(tag.attrs) == 2)`

Lambda 函数可以用来替代现有的 Beautiful 函数：

```python
bs.find_all(lambda tag: tag.get_text() == 'something')
```

# 编写网络爬虫

## 遍历单个域名

