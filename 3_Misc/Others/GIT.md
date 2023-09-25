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

[参考1](https://blog.csdn.net/qq_43827595/article/details/105673569)
[参考2](https://marcosantonocito.medium.com/fixing-the-gh001-large-files-detected-you-may-want-to-try-git-large-file-storage-43336b983272)
[参考3](https://stackoverflow.com/questions/33360043/git-error-need-to-remove-large-file)


# 如何将撤销git commit的提交

> git reset --soft HEAD~1
> git reset --hard HEAD~1
> git reset --mixed HEAD~1 (default)

if you only want to change the commit message, you could use
> git commit --amend

[参考](https://blog.csdn.net/qq_32281471/article/details/95478314)