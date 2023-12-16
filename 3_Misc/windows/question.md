# Windows中的硬链接、软链接、符号链接、快捷方式

[参考](https://www.zywvvd.com/notes/system/windows/windows-link/windows-link/)

**shortcut**

- 快捷方式 

**hard link**

- 硬链接

```powershell
New-Item Hardlink.txt -ItemType HardLink -Target C:\...\Demo.txt
```

**symbolic link**

- 符号链接

```powershell
mklink /D to from
New-Item [链接名称] -Itemtype SymbolicLink -Target [目标绝对路径]
```

**junction**

- 软链接

```powershell
mklink /J to from
```