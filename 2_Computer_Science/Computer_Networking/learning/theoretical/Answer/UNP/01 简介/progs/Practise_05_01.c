#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <fcntl.h>

#define VEASON_IP "119.29.207.157"
// #define DAYTIME_PORT (20013)
#define MAXLINE 1024

int main(int argc, char const *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "usage : ./%s <port>", argv[0]);
        exit(1);
    }

    int fd = -1;
    if ((fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket fd create fail!");
        exit(1);
    }

    struct sockaddr_in svraddr;
    bzero(&svraddr, sizeof(svraddr));
    svraddr.sin_family = AF_INET;
    if (inet_pton(AF_INET, VEASON_IP, &svraddr.sin_addr) < 0) {
        perror("ip formater error");
        exit(1);
    }
    svraddr.sin_port = htons(atoi(argv[1]));

    if (connect(fd, (struct sockaddr *)&svraddr, sizeof(svraddr)) < 0) {
        perror("connect error!");
        exit(1);
    }
    printf("connect succ!\n");

    char buf[MAXLINE];
    ssize_t nread = 0;
    int counter = 0;
    while ((nread = read(fd, buf, MAXLINE)) > 0) {
        buf[nread] = 0;
        counter++;
        if (fputs(buf, stdout) == EOF) {
            fprintf(stderr, "fputs error");
            exit(1);
        }
    }
    if (nread < 0) {
        perror("read error!");
        exit(1);
    }

    printf("MAXLINE = %d, counter = %d\n", MAXLINE, counter);

    return 0;
}