# 配置R1端口
Router1(config)#interface gigabitethernet 0/0
Router1(config-if)#ip address 172.16.1.1 255.255.255.0
Router1(config-if)#no shutdown
Router1(config-if)#exit
Router1(config)#interface serial 2/0
Router1(config-if)#ip address 172.16.2.1 255.255.255.0
Router1(config-if)#no shutdown
Router1(config-if)#exit

**截图1：配置R1端口**

# 配置R2端口
Router2(config)#interface serial 2/0
Router2(config-if)#ip address 172.16.2.2 255.255.255.0
Router2(config-if)#no shutdown
Router2(config-if)#exit
Router2(config)#interface gigabitethernet 0/0
Router2(config-if)#ip address 192.168.5.17 255.255.255.240
Router2(config-if)#no shutdown
Router2(config-if)#exit

**截图2：配置R2端口**

# 配置R3端口
Router3(config)#interface gigabitethernet 0/0
Router3(config-if)#ip address 192.168.5.18 255.255.255.240
Router3(config-if)#no shutdown
Router3(config-if)#exit
Router3(config)#interface serial 2/0
Router3(config-if)#ip address 202.103.2.33 255.255.255.240
Router3(config-if)#no shutdown
Router3(config-if)#exit

**截图3：配置R3端口**

# 配置R4端口
Router4(config)#interface serial 2/0
Router4(config-if)#ip address 202.103.2.34 255.255.255.240
Router4(config-if)#no shutdown
Router4(config-if)#exit
Router4(config)#interface gigabitethernet 0/0
Router4(config-if)#ip address 202.103.1.1 255.255.255.0
Router4(config-if)#no shutdown
Router4(config-if)#exit

**截图4：配置R4端口**

# 实验步骤

1. 使用`show ip route`命令，查看**R3与R4在未配置RIP时**的路由表，并记录。

Router3#show ip route
**截图5：R3在未配置RIP时的路由表**

Router4#show ip route
**截图6：R4在未配置RIP时的路由表**

2. 按照实验拓扑图配置所有设备，并在路由器上配置RIP v2协议。

**Router1**:

Router1(config)#router rip
Router1(config-router)#version 2
Router2(config-router)#poison-reverse # 开启毒性反转，保险起见，加上
Router1(config-router)#no auto-summary
Router1(config-router)#network 172.16.1.0 255.255.255.0
Router1(config-router)#network 172.16.2.0 255.255.255.0

**截图7：R1上配置RIPv2协议**

**Router2**:

Router2(config)#router rip
Router2(config-router)#version 2
Router2(config-router)#poison-reverse
Router2(config-router)#no auto-summary
Router2(config-router)#network 172.16.2.0 255.255.255.0
Router2(config-router)#network 192.168.5.16 255.255.255.240

**截图8：R2上配置RIPv2协议**

**Router3**:

Router3(config)#router rip
Router3(config-router)#version 2
Router2(config-router)#poison-reverse
Router3(config-router)#no auto-summary
Router3(config-router)#network 192.168.5.16 255.255.255.240
Router3(config-router)#network 202.103.2.32 255.255.255.240

**截图9：R3上配置RIPv2协议**

**Router4**:

Router4(config)#router rip
Router4(config-router)#version 2
Router2(config-router)#poison-reverse
Router4(config-router)#no auto-summary
Router4(config-router)#network 202.103.2.32 255.255.255.240
Router4(config-router)#network 202.103.1.0 255.255.255.0

**截图10：R4上配置RIPv2协议**

3. 配置RIP后，在路由器上，学会使用`debug ip rip`命令，对该命令的输出信息做分析。

Router#debug ip rip
Router#undebug ip rip    # 关闭调试
Router#debug ip rip events    # 查看RIP事件

**截图11：R2中的debug信息**

4. 查看4台路由器的路由表，验证是否学习到了其他网段的路由信息。

Router1#show ip route
**截图12：R1中的路由表**

Router2#show ip route
**截图13：R2中的路由表**

Router3#show ip route
**截图14：R3中的路由表**

Router4#show ip route
**截图15：R4中的路由表**

5. 对比步骤1中路由器R3和R4的路由表，分析此时路由器R3和R4的路由
表中的R条目是怎样产生的？

6. 测试网络的连通性，分析tracerout PC1（或PC2）的结果。

PC1>traceroute 202.103.1.2    # 追踪到PC2的路由
PC1>ping 202.103.1.2    # 测试与PC2的连通性

**截图16：测试网路的连通性**

7. 捕获数据包，分析RIP封装结构，并给出从捕获的数据包中哪里可以查
看到RIP版本号和发布到的网段？ RIP包在PC1或PC2上能捕获到吗？

**截图17：PC1捕获RIP包**
**截图18：PC2捕获RIP包**
**保存捕获包1、2**

8. 进行拔线实验，拔掉任一根网线，在相关路由器上使用`debug ip rip`命令，查看实验拓扑中链路状态发生改变时，路由表的前后信息对比及debug信息的变化，查看是否出现毒性反转？

Router1#debug ip rip

拔R1与PC1之间的网线
**截图19：毒性反转**

9. RIP v1必须使用自动汇总，不支持不连续网络，请分析若使用RIP v1，路由器R1-R4的路由表最终将会是怎样的？在这种情况下，PC1和PC2是否仍可以联通？

202.103.2.32/28与202.103.1.0/24被汇总，路由失败，PC1和PC2无法联通。