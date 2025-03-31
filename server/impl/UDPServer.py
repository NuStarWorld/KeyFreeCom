import json
import socket
import threading
import yaml

from soft.impl.PublicKeySoft import PublicKeySendSoft
from soft.AbsSoft import AbsSoft

"""
聊天服务器
"""


class UDPSocketLoad:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 25555
        self.udp_cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_cli.bind(('127.0.0.1', 38801))
        self.ip = None
        # 开一个线程接受服务端消息
        threading.Thread(target=self.recv_msg).start()
        from soft.impl.PublicKeySoft import PublicKeySendSoft
        # 协商密钥
        self.pbs = PublicKeySendSoft(self)

    def get_ip(self):
        return self.ip

    """
    向服务端发送消息
    """
    def send_msg(self, msg):
        self.udp_cli.sendto(msg.encode('gbk'), (self.host, self.port))

    """
    处理服务端的消息
    """
    def recv_msg(self):
        while True:
            data, addr = self.udp_cli.recvfrom(1024)
            mod_msg = json.loads(data.decode('utf-8'))
            match mod_msg:
                case {"method": "negotiate_key"}:
                    print(run_soft(self.pbs, mod_msg))