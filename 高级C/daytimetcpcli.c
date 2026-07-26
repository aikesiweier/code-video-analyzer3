#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define BUFSIZE 128

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <hostname>\n", argv[0]);
        exit(1);
    }

    struct hostent *host = gethostbyname(argv[1]);
    if (host == NULL) {
        herror("gethostbyname failed");
        exit(1);
    }

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("socket error");
        exit(1);
    }

    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(13); // Daytime service port
    memcpy(&serv_addr.sin_addr, host->h_addr, host->h_length);

    if (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("connect error");
        exit(1);
    }

    char buf[BUFSIZE];
    int n = read(sockfd, buf, BUFSIZE);
    if (n < 0) {
        perror("read error");
        exit(1);
    }
    buf[n] = '\0';
    printf("Server time: %s", buf);

    close(sockfd);
    return 0;
}