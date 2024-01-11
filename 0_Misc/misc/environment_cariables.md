# 环境变量

## 什么是环境变量

环境变量 英文名为: Environment variables

是在操作系统中一个具有特定名字的对象，它包含了一个或多个应用程序所将使用到的信息, 例如: 如系统临时文件夹位置、系统文件夹位置、某些应用软件文件的路径等等..

例如：

当要求系统运行一个程序但是又没有告诉它这个程序所在的完整路径时，系统默认会在当前目录下面寻找这个程序,如果找不到就会到环境变量中的path中指定的路径去找, 所以我们用户可以通过设置环境变量，来更好的运行程序!

## 读取特殊的环境变量

通过环境变量读取Windows操作系统的安装路径，和默认应用程序的安装路径。

```powershell
PS> $env:windir
C:\Windows
PS> $env:ProgramFiles
C:\Program Files
```

通过$env:，这就提示powershell忽略基本的variable:驱动器，而是去环境变量env:驱动器中寻找变量。为了和其它变量保持一致，powershell环境变量也可以象其它变量那样使用。比如你可以把它插入到文本中。

```powershell
PS> "My computer name $env:COMPUTERNAME"
My computer name MYHome-test-01
```

## 查找环境变量

Powershell把所有环境变量的记录保存在env: 虚拟驱动中，因此可以列出所有环境变量 。一旦查出环境变量的名字就可以使用$env:name 访问了。

```powershell
PS> ls env:
Name                           Value
----                           -----
ALLUSERSPROFILE                C:\ProgramData
APPDATA                        C:\User\sv-test\Home\AppData\Roaming
CommonProgramFiles             C:\Program Files\Common Files
COMPUTERNAME                   MYHome-test-01
ComSpec                        C:\Windows\system32\cmd.exe
FP_NO_HOST_CHECK               NO
HOMEDRIVE                      C:
HOMEPATH                       Users\v-test\Home
```

## 创建新的环境变量

创建新环境变量的方法和创建其它变量一样，只需要指定 `env:` 虚拟驱动器即可

```powershell
PS> $env:TestVar1="This is my environment variable"
PS> $env:TestVar2="Hollow, environment variable"
PS> ls env:Test*

Name                           Value
----                           -----
TestVar1                       This is my environment variable
TestVar2                       Hollow, environment variable
```

## 删除和更新环境变量

在 powershell 删除和更新环境变量和变量一样。例如要删除环境变量的 windir

```powershell
PS> del env:windir
PS> $env:windir
```

可以更新环境变量$env:OS 为linux redhat

```powershell
PS> $env:OS
Windows_NT
PS>  $env:OS="Redhat Linux"
PS> $env:OS
Redhat Linux
```

这样直接操作环境变量，会不会不安全？事实上很安全，因为$env：中的环境变量只是机器环境变量的一个副本，即使你更改了它，下一次重新打开时，又会恢复如初。（.NET方法更新环境变量除外）

我们可以将受信任的文件夹列表追加到环境变量的末尾，这样就可以直接通过相对路径执行这些文件下的文件或者脚本，甚至省略扩展名都可以。

```powershell
PS> md .myscript

    Directory:

Mode                LastWriteTime     Length Name
----                -------------     ------ ----
d----        2011/11/29     18:20            myscript

PS> cd .myscript
PSmyscript> "write-host 'Hollow , Powershell'" > hollow.ps1
PSmyscript> .hollow.ps1
Hollow , Powershell
PSmyscript> cd ..
PS> $env:Path+=";C:PowerShellmyscript"
PS> hollow.ps1
Hollow , Powershell
PS> hollow
Hollow , Powershell
```

## 环境变量更新生效

上述对于环境变量的操作只会影响当前powershell会话，并没有更新在机器上。
.NET方法[environment]::SetEnvironmentvariable操作可以立刻生效。
下面的例子对当前用户设置环境变量，经测试，重新打开powershell仍然存在

```powershell
PS> [environment]::SetEnvironmentvariable("Path", ";c:\powershellscript", "User")
PS> [environment]::GetEnvironmentvariable("Path", "User")
;c:\powershellscript
```


[参考](https://baijiahao.baidu.com/s?id=1739693765201054630&wfr=spider&for=pc)

[参考](https://blog.csdn.net/weixin_51429254/article/details/120394311?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-5-120394311-blog-103857401.t5_layer_eslanding_A_0&spm=1001.2101.3001.4242.4&utm_relevant_index=8)

[参考](https://blog.csdn.net/weixin_33786077/article/details/85081002)