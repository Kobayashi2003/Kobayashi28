# What is GDB?

官方文档：
*http://www.sourceware.org/gdb/*

GDB, the GNU Project debugger, allows you to see what is going on `inside' another program while it executes -- or what another program was doing at the moment it crashed.

GDB can do four main kinds of things (plus other things in support of these) to help you catch bugs in the act:

    Start your program, specifying anything that might affect its behavior.
    Make your program stop on specified conditions.
    Examine what has happened, when your program has stopped.
    Change things in your program, so you can experiment with correcting the effects of one bug and go on to learn about another.

Those programs might be executing on the same machine as GDB (native), on another machine (remote), or on a simulator. GDB can run on most popular UNIX and Microsoft Windows variants, as well as on Mac OS X.

# What Languages does GDB Support?
GDB supports the following languages (in alphabetical order):

    Ada
    Assembly
    C
    C++
    D
    Fortran
    Go
    Objective-C
    OpenCL
    Modula-2
    Pascal
    Rust


# 搭建实验环境

安装GDB
> yum -y install gdb

检查GDB是否安装成功
> gdb --version

# 调试前的准备

用gcc编译源程序的时候，编译后的可执行文件不会包含源程序代码，如果您打算编译后的程序可以被调试，编译的时候要加-g的参数，例如：

> gcc -g -o book113 book113.c

在命令提示符下输入gdb book113就可以调试book113程序了。

>  gdb book113

# 基本调试命令

## set args

设置主程序的参数。

例如：./book119 /oracle/c/book1.c /tmp/book1.c

设置参数的方法是：

gdb book119

(gdb) set args /oracle/c/book1.c /tmp/book1.c

## break

> 缩写：b

设置断点，b 20 表示在第20行设置断点，可以设置多个断点。

## run

> 缩写: r

开始运行程序, 程序运行到断点的位置会停下来，如果没有遇到断点，程序一直运行下去。

## next

> 缩写: n

执行当前行语句，如果该语句为函数调用，不会进入函数内部执行。

## step

> 缩写: p

显示变量值，例如：p name表示显示变量name的值

## continue

> 缩写: c

继续程序的运行，直到遇到下一个断点

## set var name=value

设置变量的值，假设程序有两个变量：int ii; char name[21];

set var ii=10 把ii的值设置为10；

set var name="西施" 把name的值设置为"西施"，注意，不是strcpy。

## quit

> 缩写: q

推出gdb环境

## list

查看源代码

## info b

查看断点位置

## print

> 缩写: p

## shell

调用终端命令

## set logging on

开启日志功能

## watchpoint

观察一个变量是否有变化

可以通过info进行查看