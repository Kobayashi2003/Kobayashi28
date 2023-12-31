# 9-3 求不同形态二叉树


# 题目描述：

在众多的数据结构中，二叉树是一种特殊而重要的结构，有着广泛的应用。二叉树或者是一个结点，或者有且仅有一个结点为二叉树的根，其余结点被分成两个互不相交的子集，一个作为左子集，另一个作为右子集，每个子集又是一个二叉树。

遍历一棵二叉树就是按某条搜索路径巡访其中每个结点，使得每个结点均被访问一次，而且仅被访问一次。最常使用的有三种遍历的方式：

- 前序遍历：若二叉树为空，则空操作；否则先访问根结点，接着前序遍历左子树，最后再前序遍历右子树。
- 中序遍历：若二叉树为空，则空操作；否则先中序遍历左子树，接着访问根结点，最后再前中遍历右子树。
- 后序遍历：若二叉树为空，则空操作；否则先后序遍历左子树，接着后序遍历右子树，最后再访问根结点。

例如下图所示的二叉树：

![file](/api/users/image?path=4262/images/1494856497148.jpg)

前序遍历的顺序是ABCD，中序遍历的顺序是CBAD，后序遍历的顺序是CBDA。

对一棵二叉树，如果给出前序遍历和中许遍历的结点访问顺序，那么后序遍历的顺序是唯一确定的，也很方便地求出来。但如果现在只知道前序遍历和后序遍历的顺序，中序遍历的顺序是不确定的，例如：前序遍历的顺序是ABCD，而后序遍历的顺序是CBDA，那么就有两课二叉树满足这样的顺序（见图(1)和图(2)）。

给定前序遍历和后序遍历的顺序，求出总共有多少棵不同形态的二叉树满足这样的遍历顺序。

# 输入格式：

整个输入有两行，第一行给出前序遍历的访问顺序，第二行给出后序遍历的访问顺序。

二叉树的结点用一个大写字母表示，不会有两个结点标上相同字母。输入数据不包含空格，且保证至少有一棵二叉树符合要求。

# 输出格式：

输出一个整数，为符合要求的不同形态二叉树的数目。

# 样例输入：


```

ABCD
CBDA

```
# 样例输出：
```
2

```

