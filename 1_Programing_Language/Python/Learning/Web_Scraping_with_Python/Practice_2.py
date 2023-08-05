from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError


try:
    html = urlopen('http://www.pythonscraping.com/pages/page1.html')
except HTTPError as e:
    print(e)
    # 返回空值，中断程序，或者执行另一个方案
except URLError as e:
    print(e + "The server could not be found!")
else:
    # 程序继续。
    print("It Worded!")
