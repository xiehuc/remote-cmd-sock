#!/usr/bin/env python3
from os.path import basename
import socket
import sys
import json

SERVER_PORT = 11450  # client 使用 port 更稳定，避免 socket 文件失效的问题


def send_request(argv=None):
    """发送请求到服务器并获取响应"""
    try:
        # 创建 Unix domain socket 客户端
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", SERVER_PORT))

        client.sendall(json.dumps(argv).encode())

        # 接收响应
        response = client.recv(4096).decode()
        print(response.strip())
        client.close()

    except ConnectionRefusedError:
        print("Error: Server is not running")
    except Exception as e:
        print(f"Error: {str(e)}")


argv = sys.argv
argv[0] = basename(argv[0])

send_request(sys.argv)
