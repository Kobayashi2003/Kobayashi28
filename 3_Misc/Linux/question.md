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