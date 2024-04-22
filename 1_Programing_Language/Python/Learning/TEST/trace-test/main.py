# https://docs.python.org/zh-cn/3.11/library/trace.html#

# run the command: python -m trace --trace main.py

## 主要的可选参数
# -c --count : 在程序完成时生成一组带有注解的报表文件，显示每个语句被执行的次数。
# -t --trace : 执行时显示每一行
# -l --listfuncs : 显示程序中执行到的函数
# -r --report : 由之前用了 --count 和 --file 运行的程序产生一个带有注解的报表。 不会执行代码。
# -T --trackcalls : 显示程序运行时暴露出来的调用关系。

## 修饰器
# -f --file=<file> : 用于累计多次跟踪运行计数的文件名。应与 --count 一起使用。
# -C --coverdir=<dir> : 报表文件的所在目录，package.module的覆盖率报表将被写入文件 dir/package/module.cover。
# -m --missing : 生成带注解的报表时，用 >>>>>> 标记未执行的行。
# -s --summary : 在用到 --count 或 --report 时，将每个文件的简短摘要输出到 stdout。
# -R --no-report : 不生成带注解的报表。如果打算用 --count 执行多次运行，然后在最后产生一组带注解的报表，该选项就很有用。
# -g --timing : 在每一行前面加上时间，自程序运行算起。只在跟踪时有用。

## 过滤器 （以下参数可重复多次）
# --ignore-moudle=<mod> ： 忽略给出的模块名及其子模块（若为包）。参数可为逗号分隔的名称列表。
# --ignore-dir=<dir> ： 忽略指定目录及其子目录下的所有模块和包。参数可为 os.pathsep 分隔的目录列表。


def say_hello():
    print('Hello, World!')

def main():
    say_hello()

if __name__ == '__main__':
    main()