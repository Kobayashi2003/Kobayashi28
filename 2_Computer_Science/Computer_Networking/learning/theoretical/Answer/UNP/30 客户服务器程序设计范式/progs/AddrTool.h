#ifndef _ADDR_TOOL_H
#define _ADDR_TOOL_H

#include <stdio.h>
char *getAddrInfo(struct sockaddr *addr);
char *getPeerInfo(int fd);
char *getSockInfo(int fd);

/* 静态内存 */
const char * getMaskInfo(struct sockaddr *sa);

#endif