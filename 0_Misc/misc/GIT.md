[参考](https://www.runoob.com/git/git-remote-repo.html)

# .gitignore无法忽略文件

清除当前的本地Git缓存
git rm -r --cached .

应用.gitignore等本地配置文件重新建立Git索引
git add .

(可选)提交当前Git版本并备注说明
git commit -m "update .gitignore"

# 如何从仓库中移除LFS

> git lfs uninstall

将lfs删除后，将commit跟add的退回到之前的版本

[参考](https://blog.csdn.net/weixin_39278265/article/details/121103819)


# 误传大文件到本地git仓库导致无法push

> git filter-branch -f --index-filter 'git rm --cached --ignore-unmatch fixtures/11_user_answer.json'

[参考1](https://blog.csdn.net/qq_43827595/article/details/105673569)
[参考2](https://marcosantonocito.medium.com/fixing-the-gh001-large-files-detected-you-may-want-to-try-git-large-file-storage-43336b983272)
[参考3](https://stackoverflow.com/questions/33360043/git-error-need-to-remove-large-file)


# 如何将撤销git commit的提交

- 软撤销:

git commit的记录会被撤销，回到上一次的commit状态，同时保留本地修改，不撤销git add的操作

> git reset --soft HEAD~1

- 硬撤销:

本地代码会回到上一次commit的状态，本地修改不会保留，撤销git add的操作

> git reset --hard HEAD~1

- 混合撤销:

不删除工作空间改动代码，撤销commit，并且撤销git add

> git reset --mixed HEAD~1 (default)

- if you only want to change the commit message, you could use

> git commit --amend

[参考](https://blog.csdn.net/qq_32281471/article/details/95478314)


# git clone的一直是自己的远程仓库

挺有趣的一个问题，由于我平时在进行上传时一般都是用wsl进行，所以一直没有发现这个问题。直到我一次在windows上进行clone时，才发现明明命令里面写的是别人的仓库，但是clone下来的却是自己的仓库。

导致这个问题的原因是我在.gitconfig文件中将remote仓库定死为了自己的仓库，只需要将其注释即可。

随后在之前的项目中添加回自己的远程仓库：

```bash
git remote add origin
```


# Updates were rejected because the tip of your current branch is behind

Accordingly, the solution is to either:

- `git pull`, so that the remote changes are merged on to my local work, or
- `git push -f`, a force push to update the remote (origin) branch


# Large files detected. You may want to try Git Large File Storage.

```bash
git lfs install
git lfs track "*.psd"
git add .gitattributes
git add file.psd
git commit -m "Add design file"
git push origin master
```

[参考](https://git-lfs.github.com/)