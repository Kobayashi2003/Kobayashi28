#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netinet/in_systm.h>
#include <netinet/udp.h>
#include <errno.h>
#include <sys/un.h>
#include <sys/select.h>
#include "../tool/TimeTool.h"
#include "../tool/FdTransmitTool.h"

#define DEFAULT_PATH "unix_hanson"
#define MAXCLI 60000
extern int log_err;

struct icmp_info {
    int icmp_type;
    int icmp_code;
    int icmp_errno;
};

struct client_info {
    int connfd;
    int sport;
};

int max(int a, int b) { return a > b ? a : b;  }

struct client_info ipc_client[MAXCLI];
fd_set rset, allset;
int icmpfd, unixfd;
int nready;
int maxi;
int maxfd;

int unix_server(const char *path)
{
    unlink(path);
    int unixfd = -1;
    if ((unixfd = socket(AF_LOCAL, SOCK_STREAM, 0)) < 0)
        return -1;

    struct sockaddr_un sun;
    sun.sun_family = AF_LOCAL;
    strcpy(sun.sun_path, path);

    if (bind(unixfd, (struct sockaddr *)&sun, SUN_LEN(&sun)) < 0) 
        return -1;
    
    if (listen(unixfd, 100000) < 0)
        return -1;
    return unixfd;
}

int process_fd(int i)
{
    int udp_client_fd;
    int connfd = ipc_client[i].connfd;
    ssize_t nread;
    char c;
    if ((nread = read_fd(connfd, &c, 1, &udp_client_fd)) < 0) {
        mlogx("read_fd error!");
        goto err;
    }
    
    mlogx("read transmit fd succ! recv_fd=%d", udp_client_fd);
    struct sockaddr_in cliaddr;
    socklen_t clilen = sizeof(cliaddr);
    if (getsockname(udp_client_fd, (struct sockaddr *)&cliaddr, &clilen) < 0) {
        mlogx("getsockname error!");
        goto err;
    }

    ipc_client[i].sport = cliaddr.sin_port; /* 大端 */
err:

    close(udp_client_fd);
    FD_CLR(connfd, &allset);
    return --nready;
}

void pack_info(struct icmp *ptr, struct icmp_info *info)
{
    info->icmp_type = ptr->icmp_type;
    info->icmp_code = ptr->icmp_code;
    info->icmp_errno = EHOSTUNREACH;
    if (ptr->icmp_type == ICMP_UNREACH) {
        if (ptr->icmp_type == ICMP_UNREACH_PORT)
            info->icmp_errno = ECONNREFUSED;
        else if (ptr->icmp_type == ICMP_SOURCEQUENCH)
            info->icmp_errno = EMSGSIZE;
    }
}

int process_icmp(void)
{
    ssize_t nread;
    char buf[512];
    
    if ((nread = read(icmpfd, buf, sizeof(buf))) <= 0) {
        mlogx("read from icmpfd error!");
        goto err;
    } 
    
    mlogx("recv %zd bytes icmpfd", nread);

    /* 从原始套接字中读取到的数据小于IP 首部长度 */
    if (nread < 20) {
        mlogx("read from icmpfd data < 20 bytes %zd bytes", nread);
        goto err;
    }
    struct ip *ip = (struct ip *)buf;

    /* IP 数据报的载荷不是 ICMP */
    if (ip->ip_p != IPPROTO_ICMP) {
        mlogx("ip header protocol field not icmp type! recv_type=%d", ip->ip_p);
        goto err;
    }
    char *ptr = buf;
    int len1 = ip->ip_hl << 2;

    /* IP 首部不足 20 字节 */
    if (len1 < 20) {
        mlogx("ip header must > 20 bytes %zd bytes", len1);
        goto err;
    }

    ip = (struct ip *)(buf + len1 + 8);

    /* 作为 ICMP 载荷的 IP 数据报的载荷必须是 UDP */
    if (ip->ip_p != IPPROTO_UDP) {
        mlogx("payload ip header protocol not udp type! recv_type=%d", ip->ip_p);
        goto err;
    }
    int len2 = ip->ip_hl << 2;

    /* 作为 ICMP 载荷的 IP 数据报的首部长度小于 20 字节 */
    if (len2 < 20) {
        mlogx("payload ip header must > 20 bytes %zd bytes", len2);
        goto err;
    }

    struct udphdr *udp = (struct udphdr*)(buf + len1 + 8 + len2);
    struct icmp *icmp = (struct icmp *)(buf + len1);
    mlogx("icmp packet generated by udp port %d", ntohs(udp->uh_sport));
    int find = 0;
    for (int i = 0; i <= maxi; i++) {
        int connfd = ipc_client[i].connfd;
        if (connfd == -1)
            continue;
        if (ipc_client[i].sport == udp->uh_sport) {
            find = 1;
            struct icmp_info info;
            pack_info(icmp, &info);
            if (write(connfd, &info, sizeof(info)) != sizeof(info)) {
                mlogx("write icmp error to udp socket fd error! sport=%d", ntohs(udp->uh_sport));
                close(connfd);
                ipc_client[i].connfd = -1;
            }
        }
    }    
    if (!find) {
        mlogx("not find matched udp source port for icmp response, sport=%d", ntohs(udp->uh_sport));
        goto err;
    }
 err:
    return --nready;
}

int process_ipc(void)
{
    int connfd = -1;
    if ((connfd = accept(unixfd, NULL, NULL)) < 0) {
        mlogx("accept error!");
        goto ipc_err;
    }

    mlogx("new ipc client connection, connfd = %d", connfd);
    int i = 0;
    for (i = 0; i < MAXCLI; i++)
        if (ipc_client[i].connfd < 0)
            break;
    if (i == MAXCLI) {
        mlogx("service client beyond max limit! reject client connfd=%d", connfd);
        close(connfd);
        goto ipc_err;
    }
    if (i > maxi)
        maxi = i;
    if (connfd > maxfd)
        maxfd = connfd;
    FD_SET(connfd, &allset);
    ipc_client[i].connfd = connfd;
ipc_err:
    return --nready;
}

int main(int argc, char *argv[])
{
    log_err = 1;
    if ((icmpfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)) < 0) {
        mlogx("icmp fd create fail!");
        exit(1);
    }

    if ((unixfd = unix_server(DEFAULT_PATH)) < 0) {
        mlogx("unix_server start fail!");
        exit(1);
    }

    for (int i = 0; i < MAXCLI; i++)
        ipc_client[i].connfd = -1;

    FD_ZERO(&allset);
    FD_SET(unixfd, &allset);
    FD_SET(icmpfd, &allset);

    nready = 0;
    int connfd = -1;
    maxfd = max(icmpfd, unixfd);
    for (;;) {
        rset = allset;
        if ((nready = select(maxfd + 1, &rset, NULL, NULL, NULL)) < 0) {
            if (errno != EINTR)
                mlogx("select error!");
            continue;
        }

        /* 接收 unix 域的连接 */
        if (FD_ISSET(unixfd, &rset)) 
            if (process_ipc() <= 0)
                continue;

        /* 接收 icmp 请求，然后找出引发该 icmp 请求的 udp 客户端, 再将 icmp 信息传递给这个始作俑者 */
        if (FD_ISSET(icmpfd, &rset)) 
            if (process_icmp() <= 0)
                continue;
        
        /*
         * 接收 udp 客户端传递过来的 udp 套接字描述符，
         * 记录该 udp 套接字描述符的源端口
         */
        for (int i = 0; i <= maxi; i++) {
            int connfd = ipc_client[i].connfd;
            if (connfd < 0)
                continue;
            if (FD_ISSET(connfd, &rset)) 
                if (process_fd(i) <= 0)
                    break;
        }
    }
}
