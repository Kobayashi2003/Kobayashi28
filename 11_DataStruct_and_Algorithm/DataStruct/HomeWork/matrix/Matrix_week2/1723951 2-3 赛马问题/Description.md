# 2-3 赛马问题

# 问题描述

A与B之间将进行一场赛马比赛，C为裁判。A与B分别拥有`n`匹马，这`2n`匹马中每匹马拥有的能力值都不相同。比赛前，参赛的两人先决定自己的马的出场顺序；比赛时，A的第一匹马将对战B的第一匹马，A的第二匹马将对战B的第二匹马，以此类推。在每一轮的比赛当中，能力值较高的马将获得胜利，并记其拥有者加`1`分。进行过`n`轮比赛之后，得分较高的人将获得最终的胜利，并赢得所有的马。当然，可能存在平局的情况，此时算作裁判C胜利，并获得所有的马。

问：给定每一匹马的能力值，**裁判C**能否通过重新调整马匹参赛顺序而获得胜利？

# 输入

第一行输入一个整数`n (1 <= n <= 100)`。

第二行输入`n`个整数，代表选手A所有马匹的能力值。

第二行输入`n`个整数，代表选手B所有马匹的能力值。

# 输出

如果可以平局的话，则输出`"YES"`，否则输出`"NO"`。

# 输入样例

```plain
4
1 2 7 8
3 4 5 6
2
1 2
3 4
```

# 输出样例

```plain
YES
NO
```



