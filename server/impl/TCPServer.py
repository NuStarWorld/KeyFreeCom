import base64
import json
import socket
import struct
import threading
from typing import override

from sympy import content

import managers
from enums.SendMode import SendMode
from managers import SoftManager
from server.Server import Server
from soft import *
from soft.impl.DataHandlingSoft import DataHandlingType

"""
认证类服务器
"""


class TCPServer(Server):
    def __init__(self, user_phone):
        try:

            self.host = '127.0.0.1'
            self.port = 25555
            self.tcp_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_cli.connect((self.host, self.port))
            managers.soft_manager.register(self)
            self.hash_user_phone = None
            self.shared_key = None
            self.user_a_data = run(managers.soft_manager.public_key_send_soft, user_phone=user_phone)
            self.receive_msg()
            #threading.Thread(target=self.receive_msg).start()
        except ConnectionRefusedError as ex:
            print(ex)
            exit()

    @staticmethod
    def get_soft_manager() -> SoftManager:
        return managers.soft_manager

    """
    服务端消息处理
    """

    def recv_bytes(self, target_len):
        data = b''
        while len(data) < target_len:
            chunk = self.tcp_cli.recv(min(4096, target_len - len(data)))
            if not chunk:
                return None  # 连接中断
            data += chunk
        return data
    @override
    def receive_msg(self):
        self.tcp_cli.settimeout(1)
        header = self.recv_bytes(4)
        if not header:
            return None
        data_len = struct.unpack(">I", header)[0]
        response_data = self.recv_bytes(data_len)
        data = response_data.decode('utf-8')
        receive_data = json.loads(data)
        print("收到消息",receive_data)
        if receive_data["type"] == "negotiate_key":
            managers.callback_manager.dispatch(self, receive_data)
        else:
            decrypt_data = json.loads(run(managers.soft_manager.data_handling_soft,
                                          untreated_msg=receive_data["data"],
                                          shared_key=self.shared_key,
                                          mode=DataHandlingType.DECRYPT_DATA))
            receive_data["data"] = decrypt_data
            print("解密收到的消息",receive_data)
            #managers.callback_manager.dispatch(self, receive_data)
            return receive_data

    """
    向服务端发送消息
    """
    @override
    def send_msg(self, dict_data, mode):
        match mode:
            case SendMode.ENCRYPT:
                print(33333)
                encrypt_msg = base64.b64encode(run(managers.soft_manager.data_handling_soft,
                                                   untreated_msg=json.dumps(dict_data["data"], ensure_ascii=False),
                                                   shared_key=self.shared_key,
                                                   mode=DataHandlingType.ENCRYPT_DATA)).decode('utf-8')
                dict_data["data"] = encrypt_msg
                print(encrypt_msg)
                self.tcp_cli.sendall(json.dumps(dict_data).encode("utf-8"))
                # 发送消息后等待消息回复
                return self.receive_msg()
            case SendMode.UN_ENCRYPT:
                self.tcp_cli.sendall(json.dumps(dict_data, ensure_ascii=False).encode("utf-8"))


    @managers.callback_manager.register("negotiate_key")
    def negotiate_key(self, data):
        self.shared_key = run(managers.soft_manager.public_key_receive_soft, user_b_data=data)
        print(self.shared_key)

    @managers.callback_manager.register("send_group_msg")
    def receive_group_msg(self, data):
        run(managers.soft_manager.receive_group_msg_soft, group_number=data["group_number"],
            sender_id=data["sender_id"],
            content=data["content"])

if __name__ == '__main__':
    tcp_server = TCPServer()
    while True:
        msg = input()
        run(managers.soft_manager.send_group_msg_soft, user_phone="15382533273",
            group_number="123456",
            content= msg)
        if msg == "Test":
            run(managers.soft_manager.create_group_soft,
                group_name="测试群组",
                group_number="123456",
                user_phone="15382533273")
