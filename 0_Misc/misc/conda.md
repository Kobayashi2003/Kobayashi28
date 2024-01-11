用终端指令创建一个新的conda环境

> conda create -n [name] python=[python version] # 不指定路径

> conda create -p [the env path] python=[python version] # 指定路径，环境名要直接写在路径名里面，系统会帮你自动创建（权限不够的话管理员开终端，或者直接把对应文件的普通用户权限开了）

查看现有的conda环境

> conda env list

终端中激活一个conda环境

> conda activate [env name]

终端中终止一个conda环境

> conda deactivate

