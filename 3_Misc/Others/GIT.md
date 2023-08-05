[参考](https://www.runoob.com/git/git-remote-repo.html)

# .gitignore无法忽略文件

清除当前的本地Git缓存
git rm -r --cached .

应用.gitignore等本地配置文件重新建立Git索引
git add .

(可选)提交当前Git版本并备注说明
git commit -m "update .gitignore"