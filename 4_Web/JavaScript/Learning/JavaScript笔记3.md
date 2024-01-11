# DOM

> DOM --> Document Object Model

DOM定义了表示和修改文档所需的方法。
DOM对象即为宿主对象，有浏览器厂商定义，
用来操作HTML和XML功能的一类对象的集合。
也有人称DOM是对HTML以及XML的标准编程接口（实现途径）
<!-- 可以使程序能够间接访问到 CSS -->

<!-- XML与HTML之间最大的区别：XML中标签可自定义（现XML已经几乎被json取代） -->


## DOM基本操作

### 对节点的增删改查

#### 查

1. 查看元素节点

- `document` 代表整个文档
- `document.getElementsByLd()` 元素 id 在 le8 以下的浏览器，不区分 id 大小写，而且也返回匹配 name 属性的元素
- `getElementsByTagName()` 标签名
- `getElementsByName()` 需注意，只有部分标签 name 可生效（表格、表格元素、img、iframe）
- `getElementsByClassName()` 类名，通过 -> 可以同时访问多个 class（ie8 和 ie8 以下的 ie 版本中没有）
- `querySelector()` CSS 选择器，在 ie7 和 ie7 以下的版本中没有
- `querySelectorAll()` CSS 选择器、在 ie7 和 ie7 以下的版本中没有

2. 遍历节点树

- `parentNode` 父节点（最顶端的 parentNode 为 #document）
- `childNodes` 子节点们
- `firstChild` 第一个子节点
- `lastChild` 最后一个子节点
- `nextSibling` 后一个兄弟节点
- `previousSibling` 前一个兄弟节点

3. 基于元素节点树的

- `parentElement` 返回当前元素的父元素节点（IE 不兼容）
- `children` 只返回当前元素子节点
- `node.childElementCount` === `node.children.length` 当前元素节点的子元素节点个数（IE 不兼容）
- `firstElementChild` 返回的是第一个元素节点（IE 不兼容）
- `lastElementChild` 返回的使最后一个元素节点（IE 不兼容）
- `nextElementSibling` / `previousElementSibling` 返回后一个/前一个兄弟元素节点（IE 不兼容）

4. 节点的类型

- 元素节点 —— 1
- 属性节点 —— 2
- 文本节点 —— 3
- 注释节点 —— 8
- document —— 9
- DocumentFragment —— 11

5. 获取节点类型 `nodeType`

6. 节点的四个属性

- `nodeName`
  - 元素的标签名，以大写形式表示，只读
- `nodeValue`
  - Text节点 或 Comment节点的文本内容，可读写
- `nodeType`
  - 该节点的类型，只读
- `attrubutes`
  - Element 节点的属性集合

7. 节点的一个方法 `Node.hasChildNodes()`

#### 增

- `document.createElement()` 创建元素节点
- `document.createTextNode()` 创建文本节点
- `document.createComment()` 创建注释节点
- `document.createDocumentFragment()`

#### 插

- `PARENTNODE.appendChild()`
- `PARENTNODE.insertBefore(a, b)`

#### 删

- `parent.removeChild()`
- `child.remove()` 无返回

#### 替换

- `parent.replaceChild(new, origin)`


### Element 节点的一些属性

- `inner HTML`
- `innerText` 火狐 / `textContent`老版本IE不兼容

### Element节点的一些方法

- `ele.setAttribute('class', 'demo')`
- `ele.getAttribute('class')`