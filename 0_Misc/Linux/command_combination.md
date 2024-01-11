# 结合使用 find xargs grep locate

```bash
kobayashi@Computer:~$ find ./ -name '*.md' | xargs grep string -n -C5 --color 2>/dev/null  
```

```bash
kobayashi@Computer:~$ locate -i string | xargs grep string -n -C5 --color 2>/dev/null  
```

```bash
fkobayashi@Computer:~$ find ./1_Programing\ Language/Cpp/Practice/HomeWork/ -name "*.cpp" -print0 | xargs -0 grep "Rational" --color -C3 -n -I 2>/dev/null # 当find的搜索路径中带有空格时，需要使用find -print0将IFS设置为'\0'，xargs -0将IFS设置为'\0'  
```

```bash
# change the image path in markdown file
find ./ -type f -name "*.md" | xargs sed -E -i 's@^(!\[(.+)\])\((\.\/)*(.+)\)@![\2](./img/\4)@g'

# you can run a test before you change the file
find ./ -type f -name "*.md" | xargs grep -E "^(!\[.+\])\((.+)\)" -n -C0 --color > buffer.txt && sed -E -i 's@^(!\[(.+)\])\(\.\/(.+)\)@![\2](./img/\3)@g' buffer.txt && cat buffer.txt && rm buffer.txt
```