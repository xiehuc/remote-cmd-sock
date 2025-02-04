#!/usr/bin/env python3
import os
import socket
import subprocess
import json
import sys

# import shlex

SOCKET_FILE = "/tmp/rcmd.sock"

white = ["macism"]


def handle_client(conn):
    """处理客户端连接"""
    try:
        data = conn.recv(1024)
        argv = json.loads(data.decode())
        if len(argv) == 0:
            return
        if not argv[0] in white:
            return
        result = subprocess.run(argv, capture_output=True, text=True)
        print(argv, result.stdout, file=sys.stderr)
        conn.sendall(result.stdout.encode())
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        conn.close()


def main():
    # 如果 socket 文件已存在则删除
    if os.path.exists(SOCKET_FILE):
        os.remove(SOCKET_FILE)

    # 创建 Unix domain socket
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_FILE)
    server.listen(1)
    print(f"Listening on {SOCKET_FILE}...")

    try:
        while True:
            conn, _ = server.accept()
            handle_client(conn)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.close()
        os.remove(SOCKET_FILE)


if __name__ == "__main__":
    main()
