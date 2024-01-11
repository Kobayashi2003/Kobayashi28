# Shell Tools and Scripting

**Shell脚本**

在bash中为变量赋值的语法是`foo=bar`，访问变量中存储的数值，其语法为 `$foo`。 需要注意的是，`foo = bar` （使用空格隔开）是不能正确工作的，因为解释器会调用程序`foo` 并将 `=` 和 `bar`作为参数。 总的来说，在shell脚本中使用空格会起到分割参数的作用，有时候可能会造成混淆，请务必多加检查。

Bash中的字符串通过`'` 和 `"`分隔符来定义，但是它们的含义并不相同。以`'`定义的字符串为原义字符串，其中的变量不会被转义，而 `"`定义的字符串会将变量值进行替换。

```shell
foo=bar
echo "$foo"
# 打印 bar
echo '$foo'
# 打印 $foo
```

和其他大多数的编程语言一样，bash也支持if, case, while 和 for 这些控制流关键字。同样地， bash 也支持函数，它可以接受参数并基于参数进行操作。下面这个函数是一个例子，它会创建一个文件夹并使用cd进入该文件夹。

```shell
mcd () {
    mkdir -p "$1"
    cd "$1"
}
```

这里 $1 是脚本的第一个参数。与其他脚本语言不同的是，bash使用了很多特殊的变量来表示参数、错误代码和相关变量。下面是列举来其中一些变量，更完整的列表可以参考(这里)[https://www.tldp.org/LDP/abs/html/special-chars.html]。

- `$0` - 当前脚本的名称
- `$1` 到 `$9` - 脚本的第一个到第九个参数
- `$@` - 所有参数
- `$#` - 参数个数
- `$?` - 最后一个命令的退出状态，如果为0则表示没有错误
- `$$` - 当前脚本的进程ID
- `!!` - 完整的上一条命令，包括参数。常见应用：当你因为权限不足执行命令失败时，可以使用`sudo !!`再尝试一次
- `$_` - 上一条命令的最后一个参数。

命令通常使用 `STDOUT`来返回输出值，使用`STDERR` 来返回错误及错误码，便于脚本以更加友好的方式报告错误。 返回码或退出状态是脚本/命令之间交流执行状态的方式。返回值0表示正常执行，其他所有非0的返回值都表示有错误发生。

退出码可以搭配 `&&`（与操作符）和 `||`（或操作符）使用，用来进行条件判断，决定是否执行其他程序。它们都属于短路运算符（short-circuiting） 同一行的多个命令可以用 ; 分隔。程序 true 的返回码永远是0，false 的返回码永远是1。让我们看几个例子

```shell
false || echo "Oops, fail"
# Oops, fail

true || echo "Will not be printed"
#

true && echo "Things went well"
# Things went well

false && echo "Will not be printed"
#

false ; echo "This will always run"
# This will always run
```

另一个常见的模式是以变量的形式获取一个命令的输出，这可以通过 命令替换（command substitution）实现。

当您通过 `$( CMD )` 这样的方式来执行`CMD` 这个命令时，它的输出结果会替换掉 `$( CMD )` 。例如，如果执行 `for file in $(ls)` ，shell首先将调用`ls` ，然后遍历得到的这些返回值。还有一个冷门的类似特性是 进程替换（process substitution）， `<( CMD )` 会执行 `CMD` 并将结果输出到一个临时文件中，并将 `<( CMD )` 替换成临时文件名。这在我们希望返回值通过文件而不是STDIN传递时很有用。例如， `diff <(ls foo) <(ls bar)` 会显示文件夹 `foo` 和 `bar` 中文件的区别。

说了很多，现在该看例子了，下面这个例子展示了一部分上面提到的特性。这段脚本会遍历我们提供的参数，使用grep 搜索字符串 foobar，如果没有找到，则将其作为注释追加到文件中。

```shell
#!/bin/bash

echo "Starting program at $(date)" # date会被替换成日期和时间

echo "Running program $0 with $# arguments with pid $$"

for file in "$@"; do
    grep foobar "$file" > /dev/null 2> /dev/null
    # 如果模式没有找到，则grep退出状态为 1
    # 我们将标准输出流和标准错误流重定向到Null，因为我们并不关心这些信息
    if [[ $? -ne 0 ]]; then
        echo "File $file does not have any foobar, adding one"
        echo "# foobar" >> "$file"
    fi
done
```

在条件语句中，我们比较 $? 是否等于0。 Bash实现了许多类似的比较操作，您可以查看(test手册)[https://man7.org/linux/man-pages/man1/test.1.html]。 在bash中进行比较时，尽量使用双方括号 `[[ ]]` 而不是单方括号 `[ ]`，这样会降低犯错的几率，尽管这样并不能兼容 `sh`。

当执行脚本时，我们经常需要提供形式类似的参数。bash使我们可以轻松的实现这一操作，它可以基于文件扩展名展开表达式。这一技术被称为shell的 通配（globbing）

- 通配符 - 当你想要利用通配符进行匹配时，你可以分别使用 `?` 和 `*` 来匹配一个或任意个字符。例如，对于文件`foo`, `foo1`, `foo2`, `foo10` 和 `bar`, `rm foo?`这条命令会删除`foo1` 和 `foo2` ，而`rm foo*` 则会删除除了`bar`之外的所有文件。
- 花括号`{}` - 当你有一系列的指令，其中包含一段公共子串时，可以用花括号来自动展开这些命令。这在批量移动或转换文件时非常方便。

```shell
convert image.{png,jpg}
# 会展开为
convert image.png image.jpg

cp /path/to/project/{foo,bar,baz}.sh /newpath
# 会展开为
cp /path/to/project/foo.sh /path/to/project/bar.sh /path/to/project/baz.sh /newpath

# 也可以结合通配使用
mv *{.py,.sh} folder
# 会移动所有 *.py 和 *.sh 文件

mkdir foo bar

# 下面命令会创建foo/a, foo/b, ... foo/h, bar/a, bar/b, ... bar/h这些文件
touch {foo,bar}/{a..h}
touch foo/x bar/y
# 比较文件夹 foo 和 bar 中包含文件的不同
diff <(ls foo) <(ls bar)
# 输出
# < x
# ---
# > y
```

编写 `bash` 脚本有时候会很别扭和反直觉。例如 [shellcheck](https://github.com/koalaman/shellcheck) 这样的工具可以帮助你定位sh/bash脚本中的错误。

注意，脚本并不一定只有用 bash 写才能在终端里调用。比如说，这是一段 Python 脚本，作用是将输入的参数倒序输出：

```python
#!/usr/local/bin/python
import sys
for arg in reversed(sys.argv[1:]):
    print(arg)
```

内核知道去用 python 解释器而不是 shell 命令来运行这段脚本，是因为脚本的开头第一行的 [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix))。

在 `shebang` 行中使用 `env` 命令是一种好的实践，它会利用环境变量中的程序来解析该脚本，这样就提高来您的脚本的可移植性。`env` 会利用我们第一节讲座中介绍过的`PATH` 环境变量来进行定位。 例如，使用了`env`的`shebang`看上去时这样的`#!/usr/bin/env python`。

shell函数和脚本有如下一些不同点：

- 函数只能与shell使用相同的语言，脚本可以使用任意语言。因此在脚本中包含 `shebang` 是很重要的。
- 函数仅在定义时被加载，脚本会在每次被执行时加载。这让函数的加载比脚本略快一些，但每次修改函数定义，都要重新加载一次。
- 函数会在当前的shfll环境中执行，脚本会在单独的进程中执行。因此，函数可以对环境变量进行更改，比如改变当前工作目录，脚本则不行。脚本需要使用 `export` 将环境变量导出，并将值传递给环境变量。
- 与其他程序语言一样，函数可以提高代码模块性、代码复用性并创建清晰性的结构。shell脚本中往往也会包含它们自己的函数定义。



**Shell工具**


- 查看命令如何使用

`man`或者`--help`的用户手册太详细不想看？来试试`tldr`吧。它会给出一些简单的例子，让你快速上手。expainshell网站也能帮你快速理解命令的含义。
[TLDR pages](https://tldr.sh/)
[explainshell](https://explainshell.com/)


- 查找文件

`find`的语法难以记忆？试试`fd`吧。它的语法和`find`类似，但是更加简洁易用。
[fd](https://github.com/sharkdp/fd)

example:
查找满足模式`PATTERN`的文件
```shell
> find -name '*PATTERN*'
> fd PATTERN
```

大多数人都认为 `find` 和 `fd` 已经很好用了，但是有的人可能想知道，我们是不是可以有更高效的方法，例如不要每次都搜索文件而是通过编译索引或建立数据库的方式来实现更加快速地搜索。

这就要靠 `locate` 了。 `locate` 使用一个由 `updatedb`负责更新的数据库，在大多数系统中 `updatedb` 都会通过 [cron](https://man7.org/linux/man-pages/man8/cron.8.html) 每日更新。这便需要我们在速度和时效性之间作出权衡。而且，`find` 和类似的工具可以通过别的属性比如文件大小、修改时间或是权限来查找文件，`locate`则只能通过文件名。 这里有一个更详细的对比。

- 查找代码 

查找文件是很有用的技能，但是很多时候您的目标其实是查看文件的内容。一个最常见的场景是您希望查找具有某种模式的全部文件，并找它们的位置。

为了实现这一点，很多类UNIX的系统都提供了`grep`命令，它是用于对输入文本进行匹配的通用工具。它是一个非常重要的shell工具，我们会在后续的数据清理课程中深入的探讨它。

`grep` 有很多选项，这也使它成为一个非常全能的工具。其中我经常使用的有 `-C` ：获取查找结果的上下文（Context）；`-v` 将对结果进行反选（Invert），也就是输出不匹配的结果。举例来说， `grep -C 5` 会输出匹配结果前后五行。当需要搜索大量文件的时候，使用 `-R` 会递归地进入子目录并搜索所有的文本文件。

但是，我们有很多办法可以对 `grep -R` 进行改进，例如使其忽略`.git` 文件夹，使用多CPU等等。

因此也出现了很多它的替代品，包括 [ack](https://beyondgrep.com/), [ag](https://github.com/ggreer/the_silver_searcher) 和 [rg](https://github.com/BurntSushi/ripgrep)。它们都特别好用，但是功能也都差不多，我比较常用的是 ripgrep (rg) ，因为它速度快，而且用法非常符合直觉。例子如下：

```shell
# 查找所有使用了 requests 库的文件
rg -t py 'import requests'
# 查找所有没有写 shebang 的文件（包含隐藏文件）
rg -u --files-without-match "^#!"
# 查找所有的foo字符串，并打印其之后的5行
rg foo -A 5
# 打印匹配的统计信息（匹配的行和文件的数量）
rg --stats PATTERN
```

与 `find/fd` 一样，重要的是你要知道有些问题使用合适的工具就会迎刃而解，而具体选择哪个工具则不是那么重要。


- 查找shell命令

`apropos`命令可以帮助您查找与某个主题相关的命令。例如，如果您想要查找与“压缩”相关的命令，可以使用`apropos compression`。这个命令会返回一系列的命令，包括`bzip2`、`gzip`、`compress`等等。

`history`命令配合`grep`、`fzf`使用可以帮助您快速查找并重复执行之前的命令。[fzf](https://github.com/junegunn/fzf/wiki/Configuring-shell-key-bindings#ctrl-r) 是一个非常好用的命令行模糊查找工具。


- 文件夹导航

[fasd](https://github.com/clvv/fasd)
[autojump](https://github.com/wting/autojump)

[broot](https://github.com/Canop/broot)
[ranger](https://github.com/ranger/ranger)

设置`alias`、使用`ln -s`创建符号连接等也是非常有用的技巧。


**课后练习**

1. 阅读 man ls，然后使用ls命令进行如下操作：
   - 所有文件（包括隐藏文件）
   - 文件打印以人类可以理解的格式输出（例如，使用454M 而不是 454279954）
   - 文件以最近访问顺序排序
   - 以彩色文本显示输出结果

```shell
> ls -a # show all files, including hidden files
> ls -h # print human readable format
> ls -t # sort by time, plus -r for reverse
> ls --color=auto 
```


2. 编写两个bash函数 marco 和 polo 执行下面的操作。 每当你执行 marco 时，当前的工作目录应当以某种形式保存，当执行 polo 时，无论现在处在什么目录下，都应当 cd 回到当时执行 marco 的目录。 为了方便debug，你可以把代码写在单独的文件 marco.sh 中，并通过 source marco.sh命令，（重新）加载函数。通过source 来加载函数，随后可以在 bash 中直接使用。 

```shell
#!/bin/bash
marco() {
    echo "$(pwd)" > $HOME/marco_history.log
    echo "save pwd $(pwd)"
}

polo() {
    cd "$(cat $HOME/marco_history.log)"
}
```

or 

```shell
#!/bin/bash
marco() {
    export MARCO=$(pwd)
}
polo() {
    cd "$MARCO"
}
```

```fish
function marco
    echo (pwd) > $HOME/marco_history.log
    echo "save pwd (pwd)"
end

function polo
    cd (cat $HOME/marco_history.log)
end
```


3. 假设您有一个命令，它很少出错。因此为了在出错时能够对其进行调试，需要花费大量的时间重现错误并捕获输出。 编写一段bash脚本，运行如下的脚本直到它出错，将它的标准输出和标准错误流记录到文件，并在最后输出所有内容。 加分项：报告脚本在失败前共运行了多少次。 

```shell
 #!/usr/bin/env bash

 n=$(( RANDOM % 100 ))

 if [[ n -eq 42 ]]; then
     echo "Something went wrong"
     >&2 echo "The error was using magic numbers"
     exit 1
 fi

 echo "Everything went according to plan"
```

- 使用while循环完成
```shell
#!/usr/bin/env bash
count = 0
echo > out.log

while true
do 
    ./buggy.sh &>> out.log # &>> is equal to >> 2>&1
    if [[ $? -ne 0 ]]; then
        car out.log
        echo "failed after" $count "times"
        break
    fi
    ((count++))
done
```

- 使用for循环完成
```shell
#!/usr/bin/env bash

echo > out.log
for ((count=0;;count++))
do 
    ./buggy.sh &>> out.log
    if [[ $? -ne 0 ]]; then
        echo "failed after" $count "times"
        break
    fi
done
```

- 使用until循环完成
```shell
# !/usr/bin/env bash
count=0
./buggy.sh &>> out.log
until [[ $? -ne 0 ]]; do
    ((count++))
    ./buggy.sh &>> out.log
done

echo "failed after" $count "times"
```

- 执行测试脚本debug.sh并验证脚本结果的正确性
```shell
~$ ./debug.sh
failed after 34 times
~$ cat out.log | grep Everything | wc -l
34
```


4. 本节课我们讲解的 find 命令中的 -exec 参数非常强大，它可以对我们查找的文件进行操作。 如果我们要对所有文件进行操作呢？例如创建一个zip压缩文件？我们已经知道，命令行可以从参数或标准输入接受输入。在用管道连接命令时，我们将标准输出和标准输入连接起来，但是有些命令，例如tar 则需要从参数接受输入。这里我们可以使用[xargs](https://man7.org/linux/man-pages/man1/xargs.1.html) 命令，它可以使用标准输入中的内容作为参数。 例如 ls | xargs rm 会删除当前目录中的所有文件。您的任务是编写一个命令，它可以递归地查找文件夹中所有的HTML文件，并将它们压缩成zip文件。注意，即使文件名中包含空格，您的命令也应该能够正确执行（提示：查看 xargs的参数-d）

- 首先创建所需的文件
```shell
  mkdir html_root
  cd html_root
  touch {1..10}.html
  mkdir html
  cd html
  touch xxxx.html
```

```txt
  ├── html_root
  │   ├── 1.html
  │   ├── 10.html
  │   ├── 2.html
  │   ├── 3.html
  │   ├── 4.html
  │   ├── 5.html
  │   ├── 6.html
  │   ├── 7.html
  │   ├── 8.html
  │   ├── 9.html
  │   └── html
  │       └── xxxx.html
```

- 执行find命令

```shell
# for Linux
find . -type f -name "*.html" | xargs -d '\n' tar -czvf html.zip
```


5. (进阶) 编写一个命令或脚本递归的查找文件夹中最近使用的文件。更通用的做法，你可以按照最近的使用时间列出文件吗？

```shell
find . -type f -mmin -60 -print0 | xargs -0 ls -lt | head -10
```


**关于使用fish的一些补充**

1. 特殊变量

- `$argv` - 所有参数，对应上述的`$@`
- `$argc` - 参数个数，对应上述的`$#`
- `$status` - 最后一个命令的退出状态，如果为0则表示没有错误，对应上述的`$?`
- `$pid` - 当前脚本的进程ID，对应上述的`$$`

此外，特殊语法`!!`在fish是不存在的，如果需要sudo执行上一条指令，可以创建一个函数`sdl.fish`：

```fish
function adl
    eval command sudo $history[1]
end
```

或者：

```fish
function sudo
    if test "argv[1]" = "!!"
        eval command sudo $history[1]
    else
        command sudo $argv
    end 
end
```


2. 命令组合

fish 不使用 `&&` 以及 `||` 语法来组合命令，而是使用 `and` 和 `or` 命令：（后补充：|| && 已在 fish 3.x 中支持）

```shell
missing:~$ echo hello; echo world
hello
world
missing:~$ false; and echo "this is not printed"
missing:~$ true;  or  echo "this is not printed"
```


3. 变量替换

fish脚本在变量替换后不会进一步分裂：

```shell
> set name 'Mister Noodle'
> mkdir $name
> ls
Mister Noodle
```

如果你需要一个变量传递多个参数，可以使用数组：

```shell
> set name Mister Noodle
> mkdir $name
```


4. 变量扩展

为了分离变量和正常文本，fish 支持使用 `{$variable}` 语法，例如：

```shell
> set num 1
> echo The number is {$num}
```

而其它 shell 通常使用 `${variable}` 语法。


5. 命令替换

fish 使用 `(command)` 语法来替换命令，例如：

```shell
> set D (date)
> echo $D
```


6. `touch {foo,bar}/{a..h}`

fish 不支持`{a..h}`这种语法，但是可以使用 `seq` 命令来实现类似的功能：

```shell
> touch {foo,bar}/(seq 0 9)
```


7. `diff <(ls foo) <(ls bar)`

在fish中若要进行进程替换，可以使用 [psub](https://fishshell.com/docs/current/cmds/psub.html) 命令：

```shell
> diff (ls foo | psub) (ls bar | psub)
```

```shell
diff (sort a.txt | psub) (sort b.txt | psub)
# shows the difference between the sorted versions of files ``a.txt`` and ``b.txt``.

source-highlight -f esc (cpp main.c | psub -f -s .c)
# highlights ``main.c`` after preprocessing as a C source.> diff (sort a.txt | psub) (sort b.txt | psub) 
```