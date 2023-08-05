# 参考https://zhuanlan.zhihu.com/p/59548929
docker --version
docker-compose --version
docker pull ubuntu  # 获取 ubuntu 镜像
docker image ls  # 查看当前安装的Docker镜像

docker run -i -t --name ubuntuTest ubuntu bash  # 创建并运行一个可以使用终端交互的 ubuntu 容器
cat /etc/issue  # 查看ubuntu系统版本
control d  # 退出容器

docker ps  # 查看当前运行的容器
docker ps -a  # 列出所有容器信息，包括已经关闭的。
docker start -i ubuntuTest  # -i启动容器，可以进入终端交互。

apt-get update  # 更新软件源信息
apt-get install vim  # 安装 vim
apt-get install git python3  # 安装 git 和 python3

vim /etc/apt/sources.list  # 更新软件源
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse

apt-get install openssh-server  # 安装 openssh-server,用于开启 ssh 服务供外部连接。
# 安装中途选择的 6-Asia   70-shanghai

vim /etc/ssh/sshd_config  # 更改 sshd 的默认配置 去掉下面3处的注释符#
34行，PermitRootLogin prohibit-password
39行，PubkeyAuthentication yes
42行，AuthorizedKeysFile      .ssh/authorized_keys .ssh/authorized_keys2

/etc/init.d/ssh restart  # 重启sshd
mkdir ~/.ssh
touch ~/.ssh/authorized_keys
# 在本机mac终端，cat ~/.ssh/id_rsa.pub  如果没有该文件，终端输入ssh-keygen，连续回车enter，即生成该文件；
# 将本机id_rsa.pub的一行内容，vim复制到docker容器的 ~/.ssh/authorized_keys中
control d

# 以上完成了ubuntu的基本配置+ssh支持；  以下生成新的镜像版本
docker commit -m 'add ssh' -a 'fxd1991' d4b0fc9b1e81 ubuntu-ssh
# -m，指定提交信息; -a，指定提交者; d4b0fc9b1e81是CONTAINER ID; ubuntu-ssh 是新镜像的名称

docker rm ubuntuTest

docker run -d -p 22222:22 --name ubuntuTest ubuntu-ssh /usr/sbin/sshd -D
# -d 后台运行; -p 绑定宿主机的22222端口到ubuntu容器的22端口; --name 给容器取名为ubuntuTest;
# ubuntu-ssh 使用镜像ubuntu-ssh创建容器; /usr/sbin/sshd -D 指定容器启动使用的应用及参数;
ssh -p 22222 root@localhost  # 不输密码，直接进入容器ubuntuTest；

# 在本机 macOS，vim ~/.ssh/config，添加如下内容：
Host ubuntuTest
    HostName localhost
    User     root
    Port     22222
# 然后可以 ssh ubuntuTest 连接容器。