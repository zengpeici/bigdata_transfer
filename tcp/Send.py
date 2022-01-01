# -*- coding: utf-8 -*-
import socket
import os
import json
import struct

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = 'ip地址'
port = 0  # 端口号
client.connect((ip, port))

file_path = r'文件路径'
file_size = os.path.getsize(file_path)
file_name = '文件名称'
dic = {
    'file_size': file_size,
    'file_name': file_name,
    'msg': '.......'
}
dic_bytes = json.dumps(dic).encode()
# 制作字典报头
dic_header = struct.pack('i', len(dic_bytes))
# 发送报头
client.send(dic_header)
# 发送字典
client.send(dic_bytes)
# 发送文件
with open(file_path, 'rb') as f:
    for line in f:
        client.send(line)

data = client.recv(1024).decode('utf-8')
print(data)
