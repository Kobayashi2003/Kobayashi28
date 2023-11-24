# Editors(vim)

## 缓存，标签页，窗口

Vim 会维护一系列打开的文件，称为“缓存”。一个 Vim 会话包含一系列标签页，每个标签页包含 一系列窗口（分隔面板）。每个窗口显示一个缓存。跟网页浏览器等其他你熟悉的程序不一样的是， 缓存和窗口不是一一对应的关系；窗口只是视角。一个缓存可以在多个窗口打开，甚至在同一 个标签页内的多个窗口打开。这个功能其实很好用，比如在查看同一个文件的不同部分的时候。

Vim 默认打开一个标签页，这个标签也包含一个窗口。

## 扩展Vim

通过浏览 [VimAwesome](https://vimawesome.com/) 来了解一些很棒的插件。

- [ctrlp.vim](https://github.com/ctrlpvim/ctrlp.vim)：模糊文件查找
- [ack.vim](https://github.com/mileszs/ack.vim)：代码搜索
- [nerdtree](https://github.com/scrooloose/nerdtree)：文件浏览器
- [vim-easymotion](https://github.com/easymotion/vim-easymotion)：魔术操作

## 其它程序的Vim模式

很多工具提供了 `Vim` 模式。这些 `Vim` 模式的质量参差不齐；取决于具体工具，有的提供了 很多酷炫的 `Vim` 功能，但是大多数对基本功能支持的很好。

**Shell**

如果你是一个 Bash 用户，用 `set -o vi`。如果你用 Zsh：`bindkey -v`。Fish 用 `fish_vi_key_bindings`。另外，不管利用什么 shell，你可以 `export EDITOR=vim`。 这是一个用来决定当一个程序需要启动编辑时启动哪个的环境变量。 例如，`git` 会使用这个编辑器来编辑 `commit` 信息。

**Readline**

很多程序使用 GNU Readline 库来作为 它们的命令控制行界面。Readline 也支持基本的 Vim 模式， 可以通过在 `~/.inputrc` 添加如下行开启：
```shell
set editing-mode vi
```
比如，在这个设置模式下，Python REPL 会支持Vim快捷键


## 其它

甚至有 Vim 的网页浏览快捷键 [browsers](http://vim.wikia.com/wiki/Vim_key_bindings_for_web_browsers), 受欢迎的有 用于 Google Chrome 的 [Vimium](https://chrome.google.com/webstore/detail/vimium/dbepggeogbaibhgnhhndojpepiihcmeb?hl=en) 和用于 Firefox 的 [Tridactyl](https://github.com/tridactyl/tridactyl)。 你甚至可以在 [Jupyter notebooks](https://github.com/lambdalisue/jupyter-vim-binding) 中用 Vim 快捷键。 [这个列表](https://reversed.top/2016-08-13/big-list-of-vim-like-software) 中列举了支持类 vim 键位绑定的软件。