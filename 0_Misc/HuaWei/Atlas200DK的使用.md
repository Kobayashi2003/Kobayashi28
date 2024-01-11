# Atlas200DK 连接 Windows PC

**1**. 将200DK上电，并通过网线将200DK与Windows PC机相连

**2**. 在【搜索】中键入【网络连接】，打开【查看网络连接】（或者打开【控制面板】，按照【控制面板】->【网络和Internet】->【查看网络状态和任务】-> 【更改适配器设置】的顺序进入）

![图 1](./images/8ee0dc9875bddba0079f8ceccbfc2b22cc426cf90dae9f559efbeb3abf1fa29f.png)  

![图 2](./images/39623de461124bb69df8cbeefdc65669720124c0f75b082bff5aa6938955884f.png)  

**3**. 右键点击连接了 Atlas200DK 的 NIC网卡（此处为【以太网3】），在【属性】->【网络】中找到【Internet协议版本4（TCP/IPv4）】，双击在【常规】中选择【自动获得 IP 地址】，点击【确定】（可以通过插拔网口的方式查看连接Atlas200DK的是哪一张网卡）

![图 3](./images/92fcb80f17080cd7fe88837ce5b3799ef751b0eec4b1da692cede0c188b599f3.png)  


**4**. 右键点击【WLAN（无线局域网）】依次选择【属性】-> 【共享】，勾选【允许其他网络用户通过此计算机的 Internet 连接来连接到其 Internet 连接】，在【家庭网络连接】中选择 Atlas200DK 的 NIC网卡，点击【确定】

![图 4](./images/6bb8e37a58da5ff5c7d5b2c1dbf392a551e8baf4cd92f81f2b73e5ef3cb05a56.png)  

**5**. 重新进入步骤3中的面板，查看此时自动分配给该网卡的IP地址（一般默认为`192.168.137.1`）

![图 5](./images/426d27303107e1d7395ec5cd73c67d929e8ff3533f94a9bd21252a4a9974e2a4.png)  

**6**. 打开Windows终端，键入

```powershell
PS > arp -a
```

找到步骤5中的IP地址

或者可以通过键入

```powershell
PS > arp -a -N 192.168.137.1
```
快速进行查找


![图 6](./images/84bb726272d558342025ddd4fdecb58528ed04670d00eac92c962f5d6af2f648.png)  

一般Internet下第一条便为Atlas200DK所对应的IP地址，此处为`192.168.137.112`（需要注意：每次计算机所随机分配的IP地址都有可能不相同）

在终端中使用`ping`指令测试与200DK之间的连通性

```powershell
PS > ping 192.168.137.112
```

![图 7](./images/2ab185d2fdc2cf7dd756be5cf553bd6a61c3e4494a1fc019cd59947b26a59e75.png)  


**7**. 在终端中使用`ssh`连接200DK终端

```powershell
PS > ssh HwHiAiUser@192.168.137.112
```

![图 8](./images/527291e92a52537deb225f3a607c1408fcee3ab5e59eb7c23c811a146eb4ec0c.png)  

![图 9](./images/2186837982ce976ca7bd96e0b42b72604c7bee01edeb1656facab1ead2908405.png)  

输入默认密码`Mind@123`，回车就能够进入200DK终端啦！

![图 10](./images/2a48ba05002c2b509c47101114ef08bd1f2f7ea550b894f2769a7339a9972f50.png)  

**8**. 使用`ping`指令测试200DK与外网的连通性

```bash
HwHiAiUser@Atlas200DK:~$ ping www.baidu.com
```

![图 11](./images/a34caadd0afe362e8e69e8ddf87491a183c071104e82cd01905688f7032ac02e.png)  

正常ping通，说明200DK连接成功