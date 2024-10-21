from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())


def get_links(articleUrl):

    html = urlopen(f'http://en.wikipedia.org{articleUrl}')
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find('div', {'id':'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))


links = get_links('/wiki/Kevin_Bacon')

while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    print(newArticle)
    links = get_links(newArticle)


# 伪随机数 和 随机数种子
# Python 的伪随机数生成器用的是梅森旋转算法，它生成的随机数很难预测且呈均匀分布