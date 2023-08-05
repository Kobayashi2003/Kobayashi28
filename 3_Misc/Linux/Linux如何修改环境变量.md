# Linux 下修改环境变量的方法、

## 方式1：

export PATH=$PAHT:/home/路径
临时修改，只对当前终端生效，立即生效  终端一关闭，就失效了

## 方式2：

修改 家目录下的  .bashrc 文件
这个文件每个用户都有，都放在自己的家目录下
用户每次登录时，都会加载(执行)这个文件

所以，将export XXX=$XXX:xxx  放到.bashrc这个文件中
就会对当前用户一直生效了

修改.bashrc文件后  需要重新登录(重新打开终端 才会生效)
或者  执行  source .bashrc  就可以立即生效了

## 方式3：

修改系统时会加载的文件  如 /etc/environment  或者  /etc/profile
因为这些文件在系统启动时候会被执行
所以在这些文件中修改环境变量，没次启动系统都生效

因为用户修改环境变量时  都是以  PATH=$PATH:的方式追加的
所以每个用户第一次修改时取的基本变量值都是他
所以修改这些文件，是对所有用户有效的

重启生效
    或者执行  source /etc/profile   source /etc/environment 生效


[参考](https://blog.csdn.net/qq_43684791/article/details/120166855)
[配置环境变量](https://blog.csdn.net/shaoming314/article/details/123973828)