[参考](http://www.freecplus.net/94103ae45b9048a7a60b6aca31f57a41.html)

[什么是包管理器](https://gwj1314.blog.csdn.net/article/details/122791478?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-122791478-blog-125702920.pc_relevant_multi_platform_featuressortv2dupreplace&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-122791478-blog-125702920.pc_relevant_multi_platform_featuressortv2dupreplace&utm_relevant_index=1)

[kali官网](https://www.kali.org/)

[GNU官网](https://gnu.io/)

> WSL: Windows Subsystem for Linux

# Linux 命令格式

`命令 [-选项] [参数]`

<!--
1. 有个别命令不遵循此格式
2.  当有多个选项时,可以写在一起
3.  简化选项与完全选项,例如:-a 等于 --all
-->

# 开机

物理机服务器：电源开关

本地虚拟机：在VMware中点击“开启虚拟机”

# 重启和关机

重启和关机都需要系统管理员用户权限

1. 重启
> init 6 或 reboot

2. 关机
> init 0 或 halt

3. 清屏
> clear

4. 查看服务器的ip地址
> ip addr

5. 时间操作
> 查看时间 : date
> 设置时区为中国上海时间 cp/usr/share/zoneinfo/Shanghai/etc/localtime
> 设置时间 data-s"yyyy-mm-dd hh:miss"

6. 目录和文件
    严谨的说，文件名是由目录+文件名组成的。

    对于目录和文件，有一些约定的表述，我们以/usr/etc/readme.txt为例。

    1）全路径文件名包含了完整的目录名和文件名，即/usr/etc/readme.txt，还有一个称呼是“绝对路径文件名”。

    2）readme.txt是文件名，它在/usr/etc目录中。

    3）目录和文件的绝对路径是从根（/）算起，在任何时候都不会有岐义。

    4）登录Linux后，一定处在目录树的某个目录中，这个目录称之为当前工作目录，简称当前目录。

    5）目录和文件的相对路径是从当前工作目录算起，如果当前工作目录是/usr，etc/readme.txt等同于/usr/etc/readme.txt；如果当前工作目录是/usr/etc，readme.txt等同于/usr/etc/readme.txt。

    6）用Linux的命令操作目录和文件的时候，采用绝对路径和相对路径都可以。

    7）一个圆点.表示当前工作目录；

    8）两个圆点..表示当前工作目录的上一级目录。

    理解绝对路径和相对路径的概念非常重要，在日常操作中，绝对路径和相对路径会同时使用，但是程序员在编写的程序中极少使用相对路径。

7. 查看当前工作目录
> pwd

8. 改变当前工作目录
> cd 目录名
exm:
> 进入tmp目录 cd/tmp
> 进入上一级目录 cd ..
> 进入用户的主目录 cd
> /mnt/c/Users/17312/Desktop/Code

9. 列出目录和文件信息
> ls[-lt]目录或文件名
<!-- ls是list的缩写，通过 ls 命令不仅可以查看目录和文件信息，还可以目录和文件权限、大小、主人和组等信息。

选项-l列出目录和文件的详细信息。

选项-lt列出目录和文件的详细信息，按时间降序显示。 -->


> 列出当前工作目录下全部的目录和文件名信息 ls
> 列出当前工作目录下全部的目录和文件名信息 ls -l
> 列出/tmp目录下全部的目录和文件 ls/tmp
> 正则表达式 例如：匹配tmp目录下的所有.txt文件 ls/tmp/*.txt

10.  创建目录
> mkdir 目录名
> 在当前工作目录下创建 aaa目录 mkdir aaa
> 在当前工作目录的 aaa目录下创建 bbb目录 mkdir aaa/bbb
> 创建/tmp/aaa目录 mkdir/tmp/aaa

11.  删除目录和文件

> rm [-rf] 目录或文件夹
> 选项 -r 表示可以删除目录，若没有则只能删除文件
> 选项 -f 表示强制删除，不需要确认

12. 移动目录和文件

> mv 【旧目录或文件名】 【新目录或文件名】

示例：
> 重命名当前目录中的 test.c 文件：mv test.c test1.c

> 若 tmp目录存在 mv test.c /tmp 将当前工作目录下的 test.c 文件移动到 /tmp 目录下（若 tmp 目录不存在，该命令将会被解释为对 test.c 的重命名）

13. 复制目录和文件

> cp [-r] 【旧目录或文件名】 【新目录或文件名】
> 选项 -r 可以复制目录，若没有 -r 选项将只能复制文件

14. 打包压缩和解包解压

tar 命令用来打包压缩和解包解压文件，类似于 windows 的 winrar 工具

压缩：
> tar zcvf 【压缩包文件名】 【目录或文件名列】

解包：
> tar zxvf 【压缩包文件名】

注意：
1）用tar命令打包和解包的目录和文件没有绝对路径的说法，都成了相对的，在包中相对的。

2）用tar命令打包的文件，用winrar可以解开。

3）在Linux系统中，还有其它的打包压缩和解包解压命令，例如zip/unzip和gzip/gunzip。


15. 判断网络是否连通

16. 显示文本文件的内容

cat 命令一次显示整个文件的内容
> cat 【文件名】

more 命令分页显示文件的内容（按空格下一页，按b键上一页）
> more 【文件名】

tail 命令显示文本文件的最后几行，如果文件内容有增加，就实时刷新
> tail -f 【文件名】

17. 统计文本文件的行数、单词数和字节数

> wc 【文件名】

18. 搜索文件中的内容

> grep "内容（若内容中没有空格可以不加引号）" 文件名
> 示例：在所有 .c 文件中搜索 math：grep math *.c

19. 搜索文件

> find 【目录名】 -name 文件名 -print

参数说明：

目录名：待搜索的目录，搜索文件的时候，除了这个目录名，还包括它的各级子目录。

文件名：待搜索的文件名匹配的规则。

> 示例：从当前工作目录开始搜索，显示所有 .c 文件：find . -name *.c -print

20. 增加/删除用户组

21. 修改用户的密码

> passwd [用户名]

22. 切换用户

23. 修改目录和文件的主人和组

> chown [-R] 【用户名:组名】 【目录或文件名列表】

chown将目录或文件的拥有者修改为参数指定的用户名和组，目录或文件名列表用空格分隔。

-R 选项表示处理各及子目录。

24. 查看系统磁盘空间

> df [-h] [-T]

选项-h 以方便阅读的方式显示信息。

选项-T 列出文件系统类型。

25. 设置/删除软链接

[参考](https://blog.csdn.net/weixin_44728499/article/details/110233298)

> [root@localhost /]# ln -s /home/check/best.txt /opt/text

根据将/home/check/best.txt通过软链接，链接到/opt/text的要求，可以得知/home/check/best.txt为源，/opt/text为链接。
*注意创建的语法：ln -s是命令，后面跟源，再后面跟一个当前目录的软链接名

> unlink 【软链接】
<!-- 最为保险的方式 -->



# 命令再学习

[参考](https://www.bilibili.com/video/BV1mW411i7Qf?p=13&spm_id_from=pageDriver&vd_source=bcce080c725a585ecee1019b5ba2569b)

## ls

list

`ls [-ald]`

-a all 显示所有文件,包括隐藏文件

-l long 详细信息显示 -lh 可以以兆字节显示

-d 查看目录属性

-i 查看 i 节点

## mkdir

`mkdir -p [目录名]`

-p 递归创建

## cd

## pwd

## rmdir

`rmdir [目录名]`

删除空目录

## cp

`cp [-rp]`

-r 复制目录

-p 保留文件属性

## mv

## rm

rm -rf [文件或目录]

-r 允许删除目录

-f 强制删除

## touch

创建空文件

## cat

-n 显示行号

## tac

反向显示

## more

分页显示

## less

可以搜索

## head

查看文件的前几行

head -n 行数

## tail

查看后几行

-n

-f 动态显示文件末尾内容

## ln

link

ln -s [源文件] [目标文件]

-s 创建软链接（软链接类似于windows的快捷方式）

无 -s 生成硬链接（硬链接相当于 cp -p 加 同步更新，但即使源文件丢失，硬链接也依旧能够访问对应文件）

## chmod

change the permissions mode of a file

改变文件或目录权限

chmod [{ugoa}{+-=}{rwx}][文件或目录][mode=421][文件或目录] -R 递归修改

r --- 4
w --- 2
x --- 1


## chown

change file ownership

chown [用户] [文件或目录]

改变文件或目录的所有者

## chgrp

改变文件或目录的所有组

## umask

umask [-S]

-S 以rwx的形式显示文件的权限\


## find

文件搜索

find [搜索范围] [匹配条件]

-name 根据文件名搜索

-iname 不区分大小写

-size 根据文件大小进行查找（+n 大于 -n 小于 n 等于）

-user 根据所有者进行查找
-group

-admin 访问时间 （`find /etc -cmin -5` 在etc/目录下查找五分钟之内被更改过的文件）

-cmin 文件属性

-mmin 文件内容

-a 两个条件同时满足

-o 两个条件满足任意一个即可

-exec/-ok 命令 {} \: 对搜索结果执行操作

`find /etc -name init* -a -type f -exec ls -l {} \:`

-type 根据文件类型查找 f（文件） d（目录） l（软链接文件）

-inum 根据i节点查找


## locate

在文件资料库中查找文件

locate [文件名]

updatedb 升级文件资料库

-i 不区分大小写


## which

搜索命令所在目录及别名信息

which [命令]


## whereis

搜索命令所在目录及帮助文档路径

whereis [命令名称]


## grep

在文件中搜寻字串匹配的行并输出

grep -iv [指定字串] [文件]

-i 不区分大小写

-v 排除指定字串



## man（此命令需要另安装）

manual

获得帮助信息

man [命令或配置文件]

`man ls` 查看ls命令的帮助信息

`man services` 查看配置文件services的帮助信息

## help


## useradd

添加新用户


## passwd

设置用户密码


## who

查看登录用户的信息

# w

## uptime


## gzip

GNU zip

压缩文件 压缩后文件格式：gz

gzip [文件]

不能压缩文件夹，而且不会保留原文件

## gunzip

GNU unzip

解压缩.gz的压缩文件

gunzip [压缩文件]


## tar

tar [-zcf] [压缩后文件名] [目录]

-c 打包
-v 显示详细信息
-f 指定文件名
-z 打包同时压缩

压缩后文件格式：.tar.gz

-x 解包
-v 显示详细信息
-f 指定文件名
-z 解压缩

## zip

zip [-r] [压缩后文件名] [文件或目录]

-r 压缩目录

压缩后文件格式：.zip

## unzip

解压 .zip 的压缩文件


## bzip2

bzip2 [-k] [文件]

-k 产生压缩文件后保留原文件

压缩后文件格式 .bz2

`tar -cjf file.tar.bz2 floder`

## bunzip2



## write

给用户发信息，以 Ctrl + D 保存结束

write <用户名>

## wall

发广播信息

wall [message]


## ping

测试网络连通性

ping [-c] IP地址

-c 指定发送次数


## ifconfig

interface configure

查看和设置网卡信息

## mail

查看发送电子邮件

## last

## lastlog

## traceroute

显示数据报到主机间的路径

## netstat

显示网络相关信息

-t TCP协议

-u UDP协议

-ls 监听

-r 路由

-n 显示IP地址和端口号

示例：
netstat -tlun 查看本机监听的端口
netstat -an 查看本机所有的网络连接
netstat -rn 查看本机路由表


## setup

配置网络

## 挂载命令

mount [-t 文件系统] 设备文件名 挂载点


## shutdown

shutdown [-chr] 时间

-c  取消前一个关机命令
-h  关机
-r  重启

cat /etc/inittab


## Vim

a i o


### 定位命令
命令|作用
:-:|:-:
:set nu|设置行号
:set nonu|取消行号
gg|到第一行
G|到最后一行
nG|到第n行
:n|到第n行
$|移至行尾
0|移至行首
---
### 删除命令
命令|作用
:-:|:-:
x|删除光标所在处字符
nx|删除光标所在处后n个字符
dd|删除光标所在行，ndd删除n行
dG|删除光标所在行当文件末尾内容
D|删除光标所在处到行尾内容
:n1,n2d|删除指定范围的行
---
复制和剪切命令
命令|作用
:-:|:-:
yy|复制当前行
nyy|复制当前行以下n行
dd|剪切当前行
ndd|剪切当前行以下n行
p、P|粘贴在当前光标所在行下或行上
---
替换或取消命令
命令|作用
:-:|:-:
r|取代光标所在处字符
R|从光标所在处开始替换字符，按Esc结束
u|取消上一步操作
---
搜索和搜索替换命令
命令|作用
:-:|:-:
/string|搜索指定字符串，搜索时忽略大小写:set ic
n|搜索指定字符串的下一个出现位置
:%s/old/new/g|全文替换指定字符串
:n1,n2s/old/new/g|在一定范围内替换指定字符串
---
保存和退出命令
命令|作用
:-:|:-:
:w|保存修改
:w new_filename|另存为指定文件
:wq|保存修改并退出
ZZ|快捷键，保存修改并退出
:q!|不保存修改退出
:wq!|保存修改并退出（文件所有者及root可使用）

### 使用技巧

- 导入命令指定结果 :r    !命令
- 定义快捷键 :map 快捷键 触发命令
- 连续行注释
  - :n1,n2s/^/#/g
  - :n1,n2s/^#//g
  - :n1,n2s/^/\/\//g
- 替换 :ab mymail samlee@lampbronther


## 软件包

- 源码包
  - 脚本安装包
- 二进制包（RPM包、系统默认包）·



## RPM包管理
