# HTML & CSS

    HTML : Hyper Text Markup Language 超文本标记语言 --> 定义网页中有什么
    CSS : Cascading Style Sheets 层叠样式表 --> 定义网页中的东西长什么样

[toc]

## 术语

1、web 互联网
2、w3c 万维网联盟（一个非营利性组织）：w3c.org 为互联网提供各种标准
3、XML extension markup language 可扩展的标志语言 用于定义文档结构

```
可以以这种格式来写代码
```

## 什么是HTML

HTML是W3C组织定义的语言标准: HTML是用于描述页面结构的语言

结构：有什么东西，该东西表示什么含义

MDN: Mozilla Development Network, Mozilla开发者社区 ;https://developer.mozilla.org

## 什么是CSS

CSS也是W3C定义的语言标准：CSS是用于描述页面展示的语言

CSS决定了页面长什么样子

## 执行 HTML CSS

HTML、CSS -> 浏览器内核 -> 页面

浏览器:
1、shell: 内核
2、core 内核（JS执行引擎、渲染引擎）

IE：Trident
Firfox: Gecko
Chrome: Webkit / Blink
Safari: Webkit
Opera: Presto / Blink

## 版本和兼容性

HTMLS、CSS3

HEML5: 2014年

CSS3: 目前还没有制定完成

XHTML：可以认为是HTML的另一种版本，完全符合XML的规范

## 显示文件扩展名

## 安装编辑器

windows记事本
Sublime
Atmo
Dreamweaver
VSCode

# 第一个网页

Emmet插件：自动生成HEML代码片段

## 注释

在HTML中，注释使用如下格式书写

```html
<!-- 注释内容 -->  （快捷键 Ctrl + /）
```

## 元素

>其他叫法：标签、标记

```
<a href = "https://pan.baidu.com" title = "前往百度网盘">百度网盘</a>
<title>Document</title>
```

整体：element（元素）

元素 = 起始标记（begin tag）+ 元素属性 + 元素内容（非必须） + 结束标记（end tag）

属性 = 属性名 + 属性值

属性的分类：

- 局部属性：某些元素特有的属性

- 全局属性：所有属性通用


```html
<meta charset="utf-8">
```

有些元素没有结束标记，这样的元素叫做：**空元素**

空元素的两种写法：

1. ```<meta charset = "UTF-8">```
2. ```<meta charset = "UTF-8" />```（以前的写法）

## 元素的嵌套

元素不能相互嵌套

**正确**
```
<body>
    <div>
        <p>
        </p>
    </div>
</body>
```

**错误**
```
<body>
    <div>
        <p>
    </div>
        </p>
</body>
```
一些术语：

**父元素、子元素、祖先元素、后代元素、兄弟元素**（拥有同一个父元素）

## 标准的文档结构

HTML: 页面、HTML文档


```html
<!DOCTYPE html>
```

**文档声明** -> 告诉浏览器当前文档使用的HTML标准是HTML5

（如果不写文档声明，将导致浏览器进入到怪异渲染模式）


```html
<html lang = "en">
</html>

英语："en"
普通话简体："cmn-hans"
```

**根元素**，一个页面最多只能一个，并该元素是其它所有元素的父元素或祖先元素（HTML5版本中没有强制要求书写该元素）

**lang属性**：language，全局属性，表示该元素内部使用的文字是使用哪一种自然语言书写而成的


```html
<head>

</head>
```
**文档头**，文档头内部的内容不会显示到页面上


```html
<meta>
```
**文档的元数据**：附加属性

charset：指定网页内容编码（字符编码表：GB2312,GBK）

<!-- 计算机中，电压电（0~2 V）0，高压电（2~5 V）1 -->


UTF-8：Unicode 编码的一个版本

```html
<title>Document</title>
```

**网页标题**


```html
<body>
</body>
```

**文档体**：页面上所有要参与到显示的元素都应该放置到文档体中

<!-- 元素都是小写 -->

# 语义化

## 什么是语义化
 **选择什么元素，取决于内容的含义，而不是显示出的效果**
1. 每一个HTML元素都有具体的含义
```html
    a元素：超链接
    p元素：段落
    h1元素：一级标题
```
2. 所有元素与展示效果无关

    a. 元素展示到页面中的效果，应该由**CSS**决定

    b. 因为浏览器带有默认的CSS样式，所以每个元素都有一些默认样式

## 为什么需要语义化

1. 为了搜索引擎优化（SEO）

    每隔一段时间，搜索引擎回从整个互联网中，抓取页面源代码

2. 为了让浏览器理解网页

    阅读模式、朗读模式

# 文本元素

HTML5中支持的元素：HTML5元素周期表

## h

**标题**：head

h1 - h6：分别表示一级标题到六级标题

```
<h1>一级标题</h1>
<h2>二级标题</h2>
……
<h6>六级标题</h6>
```

<!--
    快捷生成标题方法
    ```html
    h$*6{$级标题}
    ```
-->

## p

**段落**：paragraphs

>lorem，乱数假文，没有任何实际含义的文字（在VC插件下之际打lorem后按下TAP键即可）
<!-- Lorem ipsum dolor sit amet, consectetur adipisicing elit. Magnam alias velit, facere cupiditate nisi corrupti voluptatem blanditiis maxime quibusdam sed totam, autem quisquam voluptatum rem consequuntur modi enim earum inventore. -->

<!--
    快捷生成
    ```html
    p*6{这是一个段落}
    ```
-->

<!--
    快捷生成乱数假文
    ```html
    p*6lorem66
    ```
    （快捷生成6段，每段包括66个字）
-->

## span【无语意】

**没有语义**，仅用于样式的设计
<!-- Container with semantic meaning -->

> 某些元素在显示时回独占一行 -> 块级元素（h元素，p元素），而某些元素不会 -> 行级元素（span元素）

> 为了满足严格的语义化，到了HTML5已经弃用块级与行级这种说法


## pre

**预格式化文本元素**

空白折叠：在源代码中的连续空白字符（空格、换行、制表），在页面显示时，会被这折叠为一个空格

例外：在pre元素中的内容**不会**出现空白折叠

在pre元素内出现的内容，会按照源代码的格式显示到页面上

（该元素通常用于在网页中显示一些代码）

pre元素功能的本质：它有一个**默认的CSS属性**


>显示代码时，通常外面套code元素，code表示代码区域


# HTML实体

实体字符，HTML Entity

实体字符通常用于在页面中显示一些特殊符号

1. &单词;
2. &#数字;

- 小于符号 &lt;
- 大于符号 &gt;
- 空格 &nbsp;<!-- non-breaking space -->
- 版权符号 ©：&copy;
- &：&amp;
- &iquest;

# a元素

**超链接**

```html
<a href="">
</a>
```

## id属性
> 全局属性，表示元素在该文档中的唯一编号

## href属性

hyper reference（引用）：表示跳转地址

1. 普通链接：跳转地址
```html
<a href="https://baidu.com/">
    百度
</a>
```

2. 锚链接：跳转到某个锚点（**当前页面**（页面不会刷新）的相应位置）（!：锚点也会改变地址）
```html

    <a href="">章节1</a>
    <a href="#chapter2">章节2</a>
    <a href="#chapter3">章节3</a>

    <h2>章节1</h2>
    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Eos, impedit.</p>
    <h2 id="chapter2">章节2</h2>
    <p>Officiis architecto magnam a asperiores exercitationem omnis? Nulla, quod corporis?</p>
    <h2 id="chapter3">章节3</h2>
    <p>Doloremque, numquam doloribus maxime fuga eius temporibus qui sunt libero.</p>

    <a href="#">回到顶部</a>
    （当浏览器发现#后没有跟地址的时候回默认地跳转回到当前页面的顶部）

```

<!--（简写，快速生成（前面加括号表示生成兄弟元素，不加括号则生成子元素）） (h2>{章节1})+p>lorem -->

<!-- 当需要生成多个时可以
a[href="#chapter$"]*6>{章节$}
((h2[id="chapter$"]>{章节$})+p>lorem1000)*6
 -->

3. 功能性链接

点击后，触发某个功能

- 执行JS代码
    ```html
    <a href="javascript:alert('hello world!')">你好！</a>
    ```

- 发送邮件，mailto
> 要求用户计算机上安装有邮件发送软件：exchange

```html
<a href="mailto:1731237095@qq.com">
    点击给我发送邮件
</a>
```

- 拨号，tel（要求有拨号软件）

```html
<a href="tel:17876868003">
    点击给我拨打电话
</a>
```

## target属性

表示跳转窗口位置。

target的取值:

- _self：表示在当前页面窗口打开，默认值

- _blank：在新窗口中打开


# 路径的写法

## 站内资源和站外资源

站内资源：当前网站的资源

站外资源：非当前网站的资源

## 绝对路径和相对路径

站外资源：绝对路径

站内资源：相对路径（也可使用绝对路径）

1. 绝对路径

绝对路径的书写格式：

url地址：

```html
协议名://主机名:端口号/path（路径）

schema://host:port/path
```

协议名：http、https、file

主机名：域名、IP地址

端口号：如果协议时http协议，默认端口号为**80**；如果协议为https协议，默认端口号为**443**

当跳转目标和当且页面的协议相同时，可以省略协议名

2. 相对路径

以./开头，./表示当前资源所在的目录

可以书写../表示返回上一级目录

```html
<a herf="./index.html">INDEX</a>
```
```

相对路径中点斜杠可以省略


# 图片元素

## img元素

**image**，空元素

```html
<img src="（图片路径）" alt="">
```

**src**元素：source

**alt**属性：当图片资源失效时，将使用该属性的文字替代图片

## 和a元素联用

## 和map元素联用

**map**：地图

map的子元素只有**area**

衡量坐标时，为了避免误差，需要使用专业的衡量工具：

ps、pxcook

```html
    <a target="_blank" href="（想要访问的链接）">
        <img usemap="#（名字）" src="（图片路径）" alt="（文字内容）">
    </a>

    <map name="（名字）">
        <area shape="circle" coords="（圆心坐标），（半径）" href="http://www.baidu.com/" alt="" target="_blank">
    </map>
    <!-- 区域形状：
    circle（圆形）->（圆心坐标，圆的半径）
    rect（矩形）->（左上角坐标，右下角坐标）
    poly（多边形）->（一次描述每个顶点的坐标）
    -->
    <!-- 坐标原点在该图片的左上角,具体坐标可以用截图工具量取（记得在网页的初始比例下量） -->
```
<!-- 截图工具 "Snipaste" -->
<!-- dreamweaver -->


## 和figure元素

指代、定义，通常用于把图片标题、描述包裹起来

子元素：figcaption：用于包裹标题（在html5环境下建议将标题都用figcaption进行包裹）

```html
<figure>
    <a>
    </a>
    <figcaption>
        <h2>
        </h2>
    </figcaption>
</figure>
```


# 多媒体元素

**video** 视频

**audio** 音频

## video

**controls**：布尔属性，控制控件的显示，取值只能为controls

**autoplay**：布尔属性，自动播放

**muted**：布尔属性，静音播放

**loop**：布尔属性，循环播放

```html
<video src=""></video>
<!-- 视频格式通常只能MP4、webm -->

<video controls="controls" src=""></video>
<!-- 显示控件（若不需要显示，直接不写controls属性即可） -->

```

布尔属性只有两种状态：
1. 不写
2. 取值为属性名

**布尔属性**，在HTML5中可以不书写属性值
```html
<video controls src=""></video>
```


## audio

和视频完全一致（要用网络标准的mp3格式）


## 兼容性

1. 旧版本的浏览器不支持这两个元素
2. 不同的浏览器支持的音视频格式可能补一致

```html
<video controls autoplay muted loop style="width:500px;">
    <source src="---.mp4">
    <source src="---.webm">
</video>
```

# 列表元素

## 有序列表

**ol**：ordered list

**li**：list item

```html
<ol type="1" reversed>
    <!--
    "1"表示序号使用数字（默认值），
    "i"表示使用罗马数字，
    "I"表示使用大写的罗马字母编号，
    "a"表示使用小写字母来排列，
    "A"表示使用大写字母来排列
    -->
    <!-- type这个属性在HTML4中弃用，但是在HTML5中被重新引入。除非列表中序号很重要，否则用CSS list-style-type替代 -->
    <!-- reversed 布尔属性，用于倒序显示 -->
    <li>第一步</li>
    <li>第二步</li>
    <li>第三步</li>
</ol>
```

<!--样式尽可能地使用CSS进行控制 -->

## 无序列表

把ol改为ul即可

**ul**：unordered list

无序列表常用于制作菜单 或 新闻列表


## 定义列表

通常用于一些术语的定义

**dl**：definition list

**dt**：definition title

**dd**：definition description

```html
HTML中的术语解释：
<dl>
    <dt>HTML</dt>
    <dd>
        超文本标记语言
    </dd>
    <dt>元素</dt>
    <dd>
        组成HTML文档的单元
    </dd>
</dl>
```

# 容器元素

**容器元素**：该元素代表一块区域，内部用于放置其它元素

## div元素

没有语义

## 语义化容器元素

**header**：通常用于表示页头，也可以用于表示文章的头部

**footer**：通常用于表示页脚，也可以用于表示文章的尾部

**article**：通常用于表示整篇文章

**section**：通常用于表示文章的章节

**aside**：通常用于表示侧边栏（附加信息）

# 元素的包含关系

以前：块级元素可以包含行级元素；行级元素不能包含块级元素，a元素除外

现在：元素的包含关系由元素的**内容类别**决定

例如，查看h1元素中是否能够包含p元素

1. 从元素的语义进行判断
2. 去MDN查

总结：
1. 容器元素中可以包含任何元素
2. a元素中几乎可以包含任何元素
3. 某些元素有固定的子元素
4. 标题元素和段落元素不能相互嵌套，并且不能包含容器元素