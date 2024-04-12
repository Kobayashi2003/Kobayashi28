# win10拒绝访问,需要安全选项卡如何操作？

[解决](https://blog.csdn.net/andymagickai/article/details/123344275)

# 锐捷客户端犯病，8021.exe 无法访问无法关闭

[解决](https://blog.csdn.net/qq_43317133/article/details/115704806)


# 在wsl2中无法使用系统代理流量的问题

[分析](https://blog.sy-zhou.com/%E6%88%91%E4%BD%BF%E7%94%A8%E4%BB%A3%E7%90%86%E6%97%B6%E9%81%87%E5%88%B0%E7%9A%84%E9%82%A3%E4%BA%9B%E5%9D%91/)

[解决WSL下使用ClashforWindows](https://zhuanlan.zhihu.com/p/451198301)

# 【CUDA】nvcc和nvidia-smi显示的版本不一致？

[解决](https://www.jianshu.com/p/eb5335708f2a)

# [卸载Anaconda后命令行提示符与cmd闪退](https://blog.csdn.net/qq_45740547/article/details/123211655)

```powershell
C:\Windows\System32\reg.exe DELETE "HKCU\Software\Microsoft\Command Processor" /v AutoRun /f
```

# 浏览器打印时背景色丢失

添加以下css代码到打印样式表中

```css
/* google chrome explorer */
-webkit-print-color-adjust: exact;

/* firefox explorer */
-moz-print-color-adjust: exact;
color-adjust: exact;
```


# Windows 7 的VMware虚拟机中无法安装 VMware Tools：安装过程提示驱动签名问题

[解决](https://blog.csdn.net/teisite/article/details/117675403)

由于微软更新了驱动程序签名算法，2019年开始弃用SHA1，改用SHA2。猜测VMware Tools驱动程序使用SHA2，而Windows7只支持SHA1，需要下载安装补丁kb4474419来支持SHA2算法。下载地址：Microsoft Update Catalog

建议主机搭建ftp服务器，虚拟机直接访问ftp服务器来下载。ftp工具推荐3CDaemon，只有200KB+，非常轻量。