# 8-2 二叉搜索树的遍历

## 题目描述：

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;给定一组无序整数，以第一个元素为根节点，生成一棵二叉搜索树，对其进行中序遍历和先序遍历。

## 输入格式：

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;输入包括多组数据，每组数据包含两行：第一行为整数m(1<=m<=3000)，表示该组数据中整数的数目，第二行给出m个整数，相邻整数间用一个空格间隔。最后一组数据后紧跟着包含0的一行输入，标识输入的结束。

## 输出格式：

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;每组输入产生两行输出，第一行是中序遍历结果，第二行是先序遍历结果，每个整数后面带一个空格，每行中第一个整数前无空格。

## 样例输入：

```
9
10 4 16 9 8 15 21 3 12
6
20 19 16 15 45 48
0
```

## 样例输出：

```
3 4 8 9 10 12 15 16 21
10 4 3 9 8 16 15 12 21
15 16 19 20 45 48
20 19 16 15 45 48
```

