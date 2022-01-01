import json
import struct
from socket import *

server = socket(AF_INET, SOCK_STREAM)
port = 0  # 端口号
server.bind(('127.0.0.1', port))  # 本地循环地址
server.listen(5)

while True:
    # 链接循环  accept() -> (socket object, address info)
    conn, addr = server.accept()
    try:
        # 先接收报头
        header = conn.recv(4)
        if len(header) != 4:
            print('长度不是4，下次继续')
            continue
        # 解析报头获取字典长度  unpack(fmt, buffer) -> (v1, v2, ...)
        header_len = struct.unpack('i', header)[0]
        # 获取字典
        dic_bytes = conn.recv(header_len)
        dic_json = dic_bytes.decode('utf-8')
        dic = json.loads(dic_json)
        file_size = dic.get('file_size')
        file_name = dic.get('file_name')
        # 接收文件
        recv_size = 0
        print('开始接受文件:', file_size)
        i = 0
        with open(file_name, 'wb') as f:
            # 循环接收文件数据
            while recv_size < file_size:
                data = conn.recv(1024)
                f.write(data)  # 写进文件
                recv_size += len(data)
                if i % (1024 * 1024) == 0:
                    print(recv_size)
                i += 1
        print(dic.get('msg'))
        conn.send('文件传输成功'.encode('utf-8'))
    except ConnectionResetError:
        break
