* connect 函数出错的情况

   * TCP 客户端没有收到对 SYN 的响应，则返回 ETIMEDOUT 错误。当调用 connect 时，内核先发送一个 SYN，若 6s 后无响应再发送一个，若 24s 后无响应再发送一个，总共等了 75s 后仍未收到响应则返回 ETIMEDOUT。
   
   * TCP 客户端收到对 SYN 的响应是 RST，这被解释为一种**硬错误**。则一收到就立马返回 ECONNREFUSED 错误。产生 RST 响应有如下情况:
      * 目的主机上的目标端口没有被服务器进程所监听。
      * TCP 发送一个 FIN 到目的主机上时，目的主机上该 TCP 的资源已经被释放。
      * TCP 接收到一个根本不存在于该连接上的分组。
      * ...
   
   * TCP 客户端发出的 SYN 在中间某个路由器引发了一个 "destination unreachable" 的 ICMP 错误。这被解释为一种**软错误**。当收到该 ICMP 错误信息时，不会立马返回并报错，而是由内核保存该消息，然后按照一定时间间隔继续发送 SYN。若某个规定时间内仍然未收到响应，就把保存的 ICMP 消息作为 EHOSTUNREACH 错误返回。 


* bind 函数
   * 如果一个 TCP 客户或服务器未曾调用 bind 绑定一个端口。那么，当调用 connect 或 listen 时，内核就要为相应的套接字选择一个临时端口。
   
   * 进程可以把一个特定的 IP 地址绑定到它的套接字上，这个 IP 地址必须属于其所在主机的网络接口之一。对于 TCP 客户，这就是为该套接字上发送的 IP 数据报指定了源 IP 地址。对于 TCP 服务器，这就限定了该套接字只接收目的是服务器自己特定网络接口上的客户连接。
   
   * 如果 TCP 服务器没有把 IP 地址绑定到它的套接字上，内核就把客户发送的 SYN 的目的 IP 地址作为服务器的源 IP 地址。
   
   * 如果指定端口号为 0，那么内核就在 bind 被调用时选择一个临时端口。然而如果指定 IP 地址为通配地址，那么内核将等到套接字已连接（TCP）或已在套接字上发出数据报（UDP）时才选择一个本地 IP 地址。
   
   * 如果让内核来为套接字选择一个临时端口号，因为 bind 并不返回所选择的值，为了得到内核所选择的临时端口号，必须调用函数 getsockname。
   
* listen 函数

   * listen 函数的第 2 个参数可以理解为已完成连接数的最大值、或者已完成连接队列 + 未完成连接队列的和的最大值，视不同的操作系统而定。
   * ![](https://github.com/YangXiaoHei/Networking/blob/master/UNP/04%20基本%20TCP%20套接字编程/images/tcp_shakehands_queue.png)
   * ![](https://github.com/YangXiaoHei/Networking/blob/master/UNP/04%20基本%20TCP%20套接字编程/images/tcp_shakehands_queue_2.png)
   * 当一个客户 SYN 到达时，若这些队列是满的，TCP 就忽略该分组。
   
* accept 函数
   
   * accpet 函数由 TCP 服务器调用，用于从已完成连接队列头部返回下一个已完成连接，如果已完成连接队列为空，那么进程被投入睡眠 (假定套接字为默认的阻塞方式)。

* getsockname 和 getpeername 的用法和使用场景
 