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
set -g fish_ke_bindings my_vi_bindings
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