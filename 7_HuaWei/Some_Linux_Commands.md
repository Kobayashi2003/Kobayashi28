# some linux commands

## diff

> find the difference between two files

> 找到两个文件之间的差异

> `diff file1 file2` 

## mount

> mount a device to a directory

> 将设备挂载到目录

> `mount /dev/sda1 /mnt`

## ifconfig

> interface configure

> 查看和设置网卡信息

> `ifconfig`

> `ifconfig eth0 10.22.1.103 netmask 255.255.255.0` # set ip address

> `ifconfig eth0 down` # shutdown the network card
> `ifconfig eth0 up` # open the network card


## crontab

> cron table

> 定时任务

> `crontab -e` # edit crontab

> `crontab -l` # list crontab

> `crontab -r` # remove crontab


**确保服务是开启的**
> `service crond status` # check crond status

> `service crond start` # start crond

**监控执行**

> `tail -f /var/log/cron` # monitor the execution of crontab
>  - 如果发现 cron 为空，可能没有开启服务
>  - service rsyncd status # check rsyncd status
>  - service rsyncd start # start rsyncd

## df

> disk free

> 磁盘空间

> `df -h` # show disk space

## du

> disk usage

> 磁盘使用情况

> `du -h` # show disk usage

> `du -sh *` # show disk usage of current directory


## Linux的文件系统结构

- /bin binaray 这个目录存放着最经常使用的命令
- /boot boot loader files 这里存放的是启动 Linux 时使用的一些核心文件，包括一些连接文件以及镜像文件
- /dev device 这个目录下存放的是 Linux 的外部设备，在 Linux 中访问设备的方式和访问文件的方式是相同的
- /etc config files 这个目录用来存放所有的系统管理所需要的配置文件和子目录
- /home user's home dir 每个用户的主目录，在 Linux 中，每个用户都有一个自己的目录，一般该目录名是以用户的账号命名的
- /lib system library 这个目录里存放的是系统最基本的动态连接共享库，其作用类似于 Windows 下的 DLL 文件。几乎所有的应用程序都需要用到这些共享库
- /mnt mount dir 系统提供该目录是为了让用户临时挂载别的文件系统的
- /opt add-on application sofeware 这是给主机额外安装软件所摆放的目录
- /proc process 这个目录是一个虚拟的目录，它是内存文件系统，它的作用是：让内核把所有进程的信息都集中显示在这个目录下，所以你可以通过直接访问这个目录来获取系统信息
- /root root dir 超级用户 root 的用户主目录
- /sbin system binaray 这里存放的是系统管理员使用的系统管理程序
- /tmp temp dir 这个目录是用来存放一些临时文件的
- /usr unix shared resources 这是一个非常重要的目录，用户的很多应用程序和文件都放在这个目录下，类似于 Windows 下的 Program Files 目录
- /var variable 这个目录中存放着经常被改变的数据，比如各种日志文件


## nohup

[参考](https://blog.csdn.net/c_base_jin/article/details/87894722)

> no hang up

> 不挂断

> `nohup command &` # run command in background

> `nohup command > /dev/null 2>&1 &` # run command in background and redirect output to /dev/null

> `ps -ef | grep command` # find the process id of command
> `kill -9 process_id` # kill the process
> `killall command` # kill the process

## ps

> process status

> 进程状态

> `ps -ef` # show all processes

> `ps -ef | grep command` # find the process id of command


## top

> top

> 进程状态

> `top` # show all processes

> `top -p process_id` # show the process


## awk

> awk

> 文本处理

> `awk '{print $1}'` # print the first column of the input

> `awk '{print $1,$2}'` # print the first and second column of the input

> `awk '{print $1,$2}' file` # print the first and second column of the file


## 特殊变量

> $0 # 当前脚本的文件名
> $n # 传递给脚本或函数的参数。n（1~9） 是一个数字，表示第几个参数。例如，第一个参数是 $1，第二个参数是 $2。
> $# # 传递给脚本或函数的参数个数。
> $? # 上个命令的退出状态，或函数的返回值。
> $* / $@ # 传递给脚本或函数的所有参数。