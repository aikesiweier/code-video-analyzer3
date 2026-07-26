#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

#define BUFFER_SIZE 1024

void error_handling(char *message) {
    fputs(message, stderr);
    fputc('\n', stderr);
    exit(1);
}

int main(int argc, char *argv[]) {
    int sock;
    struct sockaddr_in serv_addr;
    char buffer[BUFFER_SIZE];
    FILE *fp;
    int read_len;

    if (argc != 3) {
        printf("Usage: %s <IP> <filename>\n", argv[0]);
        exit(1);
    }

    // 打开文件
    fp = fopen(argv[2], "r");
    if (fp == NULL) {
        error_handling("fopen() error");
    }

    // 创建套接字
    sock = socket(PF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        error_handling("socket() error");
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(argv[1]);
    serv_addr.sin_port = htons(atoi("12345"));

    // 连接服务器
    if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) == -1) {
        error_handling("connect() error");
    }

    // 发送文件内容
    while ((read_len = fread(buffer, 1, BUFFER_SIZE, fp)) > 0) {
        if (write(sock, buffer, read_len) != read_len) {
            error_handling("write() error");
        }
    }

    // 发送结束标志
    shutdown(sock, SHUT_WR);

    // 接收服务器返回的内容并打印
    printf("Received from server:\n");
    while ((read_len = read(sock, buffer, BUFFER_SIZE)) > 0) {
        fwrite(buffer, 1, read_len, stdout);
    }
    printf("\n");

    fclose(fp);
    close(sock);
    return 0;
}