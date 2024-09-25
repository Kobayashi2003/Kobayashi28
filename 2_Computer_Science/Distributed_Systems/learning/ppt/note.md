# 分布式系统定义

分布式系统是若干**独立自主计算机**的集合（硬件），这些计算机对于用户来说像是**单个耦合**系统（软件）。

- 自主性：
  - 计算节点硬件或者软件进程是独立的
- 耦合性：
  - 用户或者应用程序感觉系统是一个系统——节点之间需要相互协作


# 分布式系统中的8个谬误

1. The network is reliable : 网络是可靠的
2. Latency is ZERO : 延迟是0
3. Bandwidth is infinite : 带宽是无限的
4. The network is secure : 网络是安全的
5. Topology doesn't change : 拓扑不会改变
6. There is one administrator : 只有一个管理员
7. Transport costs is ZERO : 传输成本是0
8. The network is homogeneous : 网络是同构的