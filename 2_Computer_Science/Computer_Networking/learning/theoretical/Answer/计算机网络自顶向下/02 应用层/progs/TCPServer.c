#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <errno.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>

int main(int argc, char const *argv[])
{
    if (argc != 2)
    {
        printf("usage : %s <#port>\n", argv[0]);
        exit(1);
    }

    unsigned int port = atoi(argv[1]);

    int listenfd;
    if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("socket error");
        exit(1);
    }
    
    struct sockaddr_in svraddr, cliaddr;
    bzero(&svraddr, sizeof(svraddr));
    svraddr.sin_family = AF_INET;
    svraddr.sin_addr.s_addr = htonl(INADDR_ANY);
    svraddr.sin_port = htons(port);
    
    if (bind(listenfd, (struct sockaddr *)&svraddr, sizeof(svraddr)) < 0)
    {
        perror("bind error");
        exit(1);
    }
    
    if (listen(listenfd, 10) < 0)
    {
        perror("listen error");
        exit(1);
    }
    
    char buf[1 << 20];
    socklen_t len;
    int connfd;
    ssize_t rdlen;
    char cli_ipbuf[128];
    char conn_ipbuf[128];
    while (1)
    {
        len = sizeof(cliaddr);
        printf("wait to accept....\n");
        if ((connfd = accept(listenfd, (struct sockaddr *)&cliaddr, &len)) < 0)
        {
            perror("accpet error");
            exit(1);
        }
        struct sockaddr_in connaddr;
        len = sizeof(connaddr);
        if (getsockname(connfd, (struct sockaddr *)&connaddr, &len) < 0)
        {
            perror("getsockname error!");
            exit(1);
        }
        const char *cli_ip = inet_ntop(AF_INET, &cliaddr.sin_addr, cli_ipbuf, sizeof(cli_ipbuf));
        unsigned short cli_port = ntohs(cliaddr.sin_port);
        const char *svr_ip = inet_ntop(AF_INET, &connaddr.sin_addr, conn_ipbuf, sizeof(conn_ipbuf));
        unsigned short svr_port = ntohs(svraddr.sin_port);
        
        printf("accpet succ! connnection from [%s:%d]\n"
               "OS assign a new connfd for this connection [%s:%d]\n",
               cli_ip, cli_port,
               svr_ip, svr_port);
        
        while (1)
        {
            printf("wait to read data...\n");
            if ((rdlen = read(connfd, buf, sizeof(buf))) < 0)
            {
                printf("read error : already read %zd bytes, error reason: %s\n",rdlen, strerror(errno));
                exit(1);
            }
            else if (rdlen == 0)
            {
                printf("peer close socket, read finished!\n");
                close(connfd);
                break;
            }
            buf[rdlen] = 0; 
            printf("received data from [%s:%d] \n", cli_ip, cli_port);
            printf("*************************************************************\n");
            printf("%s", buf);
            printf("*************************************************************\n");
        }
    }
    
    return 0;
}
