#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define BUFSIZE 128
#define PORT 13 // Daytime service port

int main() {
    int listenfd, connfd;
    struct sockaddr_in serv_addr, cli_addr;
    socklen_t cli_len = sizeof(cli_addr);

    listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd < 0) {
        perror("socket error");
        exit(1);
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(PORT);

    if (bind(listenfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("bind error");
        exit(1);
    }

    if (listen(listenfd, 5) < 0) {
        perror("listen error");
        exit(1);
    }

    printf("Server running on port %d...\n", PORT);

    while (1) {
        connfd = accept(listenfd, (struct sockaddr *)&cli_addr, &cli_len);
        if (connfd < 0) {
            perror("accept error");
            continue;
        }

        time_t ticks = time(NULL);
        char buf[BUFSIZE];
        snprintf(buf, BUFSIZE, "%.24s\r\n", ctime(&ticks));
        write(connfd, buf, strlen(buf));

        close(connfd);
    }

    close(listenfd);
    return 0;
}