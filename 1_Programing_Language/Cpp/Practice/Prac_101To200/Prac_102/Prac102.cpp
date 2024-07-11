#include <unistd.h>
#include <sys/types.h>
#include <cstdio>
#include <cstdlib>

int main() {

    printf("call fork\n");

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork error\n");
        exit(-1);
    }

    printf("fork return\n");

    if (pid) {
        printf("father fork return: %d\n", pid);
    } else {
        printf("child fork return: %d\n", pid);
    }
}
