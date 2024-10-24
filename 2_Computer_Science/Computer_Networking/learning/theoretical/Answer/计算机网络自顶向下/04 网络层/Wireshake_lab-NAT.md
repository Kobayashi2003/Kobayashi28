在这个实验中，我们将探索 NAT 协议的行为。在其他 Wireshake 实验中我们会在单个 Wireshake 上捕获一个分组轨迹文件。这个 NAT 实验将不同于我们的其他 Wireshake Lab 实验。因为我们对 NAT 设备的输入端一边和输出端一边都感兴趣。我们将需要在两个位置捕获分组。同样，因为很多学生没有访问 NAT 设备的简便方式或者没法在两台电脑上进行 Wireshake 分组捕获。因此不是一个可以在真实环境中被学生进行的实验。因此在这个实验中，你将使用我们为你提供已捕获的 Wireshake 分组轨迹文件。在开始这个实验前，你可能想去复习在课本 4.4 节中的 NAT 章节。

* 1、NAT 测量情形
  * 在这个实验中，我们将在家庭网络中捕获一个从 PC 客户端发往 `www.google.com` 服务器的 Web 请求。该家庭网络路由器提供了一个 NAT 设备，正如在第 4 章中讨论的那样。
  * Figure 1 展示了我们使用 Wireshake 轨迹收集分组的情形，和其他 lab 一样，我们在家庭网络中的一台 PC 客户端上收集 Wireshake 轨迹，这个文件被命名为 `NAT_home_side`。因为我们也对被 NAT 发送进 ISP 中的分组感兴趣，所以我们也将在另一台电脑上收集第二份轨迹文件，正如在 Figure 1 中展示的那样（这台电脑通过链路接入并位于 NAT 路由器和 ISP 第一跳路由器之间）。在第二个点上被 Wireshake 捕获的分组已经经历过 NAT 转换。这份 Wireshake 轨迹文件在家庭路由器的 ISP 一侧，被命名为 `NAT_ISP_side`。
  
  * 打开 `NAT_home_side` 文件并回答下列问题。你会发现使用 Wireshake 筛选框过滤出只包含 HTTP 报文的帧会很有帮助。
  
* 回答下列问题:
* 1、客户端的 IP 地址是什么？
  * 192.168.1.100

* 2、该客户端实际上和几个不同的 Google 服务器通信，这是为了实现 "安全浏览" （看该实验末尾的额外段落）Google 主服务器提供 IP 地址为 `64.233.169.104` 的 Web 页面，为了只显示这些包含 HTTP 报文的被 Google 收发的帧，在筛选框中键入 `http && ip.addr == 64.233.169.104`。

* 3、思考在时间 7.109267 被客户端发到 Google 服务器的 HTTP GET 报文（ 目的 IP 地址是 `64.233.169.104`），源和目的 IP 地址是什么？TCP 源和端口号是什么？
  * 源和目的 IP 分别是 `192.168.1.100`、`64.233.169.104`
  * 源和目的端口号分别是 `4335`、`80`

* 4、 在何时 Google 服务器返回了相应的 200 OK HTTP 报文？被 IP 数据报携带的 HTTP 200 OK 报文中的源和目的 IP 地址是什么？TCP 源和目的端口号是什么？ 
  * 从下图可以看出，在 7.427932 时间戳返回了 200 OK HTTP 报文
  * 源和目的 IP 分别是 64.233.169.104、192.168.1.100
  * 源和目的端口分别是 80、4335
 
* 5、回想在 GET 命令发给 HTTP 服务器之前，TCP 必须先通过三次握手建立一个连接。在时间点为 7.109267 的 GET 报文的 TCP 何时发出了 SYN 报文段建立 TCP 连接？这个 SYN 报文段的源和目的 IP 是什么？源和目的端口是什么？作为该 SYN 的响应的 ACK 的源和目的 IP 是什么？源和目的端口是什么？在何时客户端收到了该 ACK？（注意：为了找到这些报文段你将需要清除筛选框表达式并输入上面第 2 步的表达式，如果你输入 `tcp`，那么只有 TCP 报文段会被显示出来）
  * 从下图可以看出，在时间点 7.344792 发出了 SYN 报文段建立 TCP 连接。这个 SYN 报文段的源和目的 IP 分别是 192.168.1.100、64.233.169.104。源和目的端口分别是 4335、80。

接下来我们将关注两个 HTTP 报文，(GET 和 200 OK) 以及 TCP 的 SYN 和 ACK。我们下面的目标是在轨迹文件 `NAT_ISP_side` 中定位这些分组。因为这些分组已经被 NAT 路由器转发了，所以 IP 地址和端口号已经被修改。
  
打开 `NAT_ISP_side`，注意在这份文件中的时间戳和在 `NAT_home_side` 中的时间戳是不同步的，因为在两个地点的分组捕获没有同时开始（你会发现 ISP 链路上被捕获的分组的时间戳实际上比在客户端 PC 上被捕获分组的时间戳要小）

* 6、在 `NAT_ISP_side` 轨迹文件中，找到在时间点 7.109267 (`NAT_home_side` 中该分组的时间戳) 从客户端发送到 Google 服务器的 HTTP GET 报文。在 `NAT_ISP_side` 文件中，这个分组的时间戳是啥？这个 HTTP GET 分组的源和目的 IP 是什么？源和目的端口是什么？对比 `NAT_home_side`中相应的分组，哪些字段是相同的？哪些是不同的？
  * 在 `NAT_ISP_side` 文件中这个时间戳是 7.800232
  * 源和目的 IP 是 71.192.34.104、64.233.169.104
  * 源和目的端口分别是 4335 和 80

* 7、HTTP GET 报文中的所有字段都被改变了吗？下面列出的哪些字段被改变了？版本号、首部长度、Flags、校验和、如果有任何一个字段被改变，给出一个这些字段被改变的理由。
  * 下图是 ISP 边的分组 
  * ![figure 2](https://github.com/YangXiaoHei/Networking/blob/master/计算机网络自顶向下/04%20网络层/images/wl_nat_3.png)
  * 下图是 home 变的分组
  * ![figure 2](https://github.com/YangXiaoHei/Networking/blob/master/计算机网络自顶向下/04%20网络层/images/wl_nat_4.png)	
  * 下图是网络层和运输层对比字段的改变
  * ![figure 2](https://github.com/YangXiaoHei/Networking/blob/master/计算机网络自顶向下/04%20网络层/images/wl_nat_5.png)	
  * ⚠️为什么 TCP 的 checksum 会改变？	

* 8、在 `NAT_ISP_side` 文件中，第一个来自 Google 服务器的 HTTP 200 OK 报文在何时被收到？源和目的 IP 是什么？源和目的端口是什么？哪些字段是相同的？哪些是不同的？为什么？
  * 在 `NAT_ISP_side` 文件中，第一个来自 Google 的 HTTP 200 OK 在 7.848634。
  * 源和目的 IP 的地址 71.192.34.104、64.233.169.104
  * 不相同的字段见下图所示
  * ![figure 2](https://github.com/YangXiaoHei/Networking/blob/master/计算机网络自顶向下/04%20网络层/images/wl_nat_8.png)	

* 9、在 `NAT_ISP_side` 文件中，什么时候捕获到客户端到服务器的 SYN 以及什么时候捕获到服务器到客户端的 ACK，源和目的 IP 地址是什么？源和目的端口是什么？哪些字段相同，哪些不同？为什么？
  * 在时间点 7.766539 捕获到客户端到服务器的 SYN
  * 在时间点 7.799818 捕获到服务器到客户端的 ACK
  * 源和 IP 地址分别是 71.192.34.104，源和端口分别是 4335、80

* 10、用你对上述 1-8 的回答，填写 NAT 映射表。
  
  |WAN|LAN|
  |:--:|:--:|
  |71.192.34.104/4335|192.168.1.100/4335|

额外关卡 : 上面探索的轨迹文件中对 Google 服务器额外建立的连接超出了我们的学习范围，比如，在 `NAT_home_side` 文件中，考虑客户端到服务器在时间点为 1.572315 的 GET 报文和时间在 7.573305 的 GET 报文，写下对这两个 HTTP 报文意图的探究。
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
