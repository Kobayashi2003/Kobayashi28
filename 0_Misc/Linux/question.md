# permission denied

> su

# su: Authentication failure

> sudo passwd root

# 关于VMware在运行centos报错：Device/Credential Guard的解决方法

https://blog.csdn.net/qq_44281591/article/details/116082175

https://www.somode.com/course/10412.html

# vscode远程连接到远程服务器后，无修改文件权限

错误信息：
> Failed to save “test’’: Unable to write file (NoPermissions (FileSystemError): Error: EACCES: permission denied, open…

修改权限：
> sudo chown -R myuser /path/to/folder

# kali 换源

https://blog.csdn.net/weixin_51178129/article/details/126037386?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2-126037386-blog-123599370.pc_relevant_multi_platform_featuressortv2removedup&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2-126037386-blog-123599370.pc_relevant_multi_platform_featuressortv2removedup&utm_relevant_index=4

修改 etc/apt/sources.list

然后更新源
> sudo apt-get update


# 将wsl1发配升级到wsl2

> wsl --set-version kali-linux 2


# 将 wsl2 中的端口映射到 windows 中

[参考](https://blog.csdn.net/keyiis_sh/article/details/113819244)

查看 wsl 的版本
> wsl -l -v

查看 wsl2 的 ip 地址
> wsl -- ifconfig eth0

linux 中查看端口占用
> lsof -i:8080

Windows 中查看端口占用
> netstat -ano | findstr 8080

> netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=172.27.3.243


# 将Linux的终端更换为 fish

> sudo apt-get install fish
> chsh -s /usr/bin/fish


# fish shell 的配置文件

fish shell 的配置文件是 `~/.config/fish/config.fish`，每次fish运行时都会加载这个配置文件。

同时，fish还提供了一个Web界面的配置工具，可以通过 `fish_config` 命令来打开。

fish_promt 配置文件是 `~/.config/fish/functions/fish_prompt.fish`，可以通过 `funced fish_prompt` 命令来打开。


# BrokPipeError: in fish shell

```shell
❯ Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>                                    (base)
BrokenPipeError: [Errno 32] Broken pipe
```

If you got error as above in your fish terminal when using Conda, just adding status is-interactive && into your config.fish will this problem.

```fish
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
if test -f /Users/keonabut/miniconda3/bin/conda
  status is-interactive && eval /Users/keonabut/miniconda3/bin/conda "shell.fish" "hook" $argv | source
end
# <<< conda initialize <<<
```

# oh-my-fish 

[oh-my-fish](https://github.com/oh-my-fish/oh-my-fish)

oh-my-fish 是 Fish 的主题核插件管理工具

- Install 
  
```shell
curl -L https://get.oh-my.fish | fish
```

# fish shell 中使用 fasd

[congfig](https://github.com/fishgretel/fasd)


# fish shell 使用 vi 模式

在 Fish 2.3.0 及以上版本中，可以使用 `fish_vi_key_bindings` 命令来启用 vi 模式。

```shell
$ fish_vi_key_bindings # start vi mode
$ fish_default_key_bindings # back to default mode
```

如果想将 vi 模式设置为默认模式，可以在 `~/.config/fish/config.fish` 中添加如下内容：

```shell
fish_vi_key_bindings
```

我的配置如下：

```shell
# fish_vi_mode
function my_vi_bindings
    fish_vi_key_bindings
    bind -M insert -m default 'jk' backward-char force-repaint
    bind -M insert -m default 'kj' backward-char force-repaint
    set  -g fish_cursor_insert line
    set  -g fish_cursor_visual blck
    set  -g fish_cursor_replace_one underscore
end
set -g fish_vi_key_bindings my_vi_bindings
```


**对于其他shell**

- Bash: `set -o vi`
- Zsh:  `bindkey -V`


# wsl 使用 windows 的本地代理

[microsoft参考](https://learn.microsoft.com/zh-cn/windows/wsl/wsl-config)

**对于WSL2**

在windows用户目录下的`.wslconfig`文件中添加如下内容：

```txt
[experimental]
autoMemoryReclaim=gradual
networkingMode=mirrored
dnsTunneling=true
firewall=true
autoProxy=true
```


# 如何使 ranger 在退出时留在所选目录

- bash or zsh
```shell
which "ranger" >/dev/null 2>&1
if [ $? -eq 0 ]; then
  alias ranger='ranger --choosedir=$HOME/.rangerdir; LASTDIR=`cat $HOME/.rangerdir`; cd "$LASTDIR"'
fi
```

- fish
```shell
function ranger
  command ranger --choosedir=$HOME/.rangerdir
  set -l LASTDIR (cat $HOME/.rangerdir)
  cd $LASTDIR
end
```



# 安装了VMware Tools，但无法实现主机与虚拟机之间的文件拖拽和复制粘贴

[REF](https://www.cnblogs.com/zhouzhihao/p/16486787.html)


1. 卸载VMware Tools

```shell
sudo apt-get autoremove open-vm-tools
```

2. 联网安装VMware Tools

```shell
sudo apt-get install open-vm-tools-desktop
```

如果出错了，尝试执行下面两条指令：

```shell
sudo apt-get update
sudo apt-get instal open-vm-tools-desktop fuse
```

3. 重启虚拟机即可



# Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend)

环境：Ubuntu 18.04-amd64

apt, apt-get 执行报错


1. 进程中存在与apt相关的正在运行的进程：

- 首先检查是否在运行apt、apt-get相关的进程

```shell
ps aux | grep -i apt
```

- 如果存在相关进程，可以使用kill命令杀死进程，或者等待进程结束后再执行apt、apt-get命令。

```shell
sudo kill -9 <pid>
```

- 或者更为简单粗暴的：

```shell
sudo killall apt apt-get
```

2. 锁文件未被正常清除

`lock file`用于防止两个或多个进程同时使用相同的数据。当运行apt、apt-get命令时，会创建一个`lock file`。当前一个apt、apt-get指令未正常终止时，`lock file`未被正常清除，将会导致后续apt、apt-get指令无法正常执行。

- 使用`lsof`指令获取持有lock file的进程ID，如果存在相关的进程，需要kill掉：

```shell
lsof /var/lib/dpkg/lock
lsof /var/lib/apt/lists/lock
lsof /var/cache/apt/archives/lock
```

- 删除所有的lock file

```shell
sudo rm /var/lib/apt/lists/lock
sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/dpkg/lock*
```

- 重新配置dpkg

```shell
sudo dpkg --configure -a
```

如果仍存在如下的报错：

```shell
dpkg: error: dpkg frontend is locked by another process
```

- 找出正在锁定lock file的进程，然后kill掉：

```shell
lsof /var/lib/dpkg/lock-fronted
kill -9 <pid>
```

- 删除lock file，并重新配置：

```shell
sudo rm /var/lib/dpkg/lock-frontend
sudo dpkg --configure -a
```


# 为WSL2做快照与回滚

1. 查看已安装的系统：

```shell
wsl --list --verbose
```

2. 为系统创建快照：

```shell
wsl --export Ubuntu-20.04 D:\wsl\Ubuntu-20.04\Ubuntu-20.04-snapshot.tar
```

3. 回滚系统：

- 注销当前系统

```shell
wsl --unregister Ubuntu-20.04
```

- 回滚

```shell
wsl --import Ubuntu-20.04 D:\wsl\Ubuntu-20.04\ D:\wsl\Ubuntu-20.04\Ubuntu-20.04-snapshot.tar --version 2
```

- 设置默认登陆用户为安装时用户名

```shell
unbuntu2004 config --default-user [USERNAME]
```