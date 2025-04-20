import base64
import json
from typing import override

from enums.SendMode import SendMode
from soft.AbsSoft import AbsSoft
from soft.impl.DataHandlingSoft import DataHandlingType


class ChatSoft(AbsSoft):
    def __init__(self, tcp):
        self.tcp = tcp


    @override
    def run(self,**kwargs):
        user_phone = kwargs["user_phone"]
        destination_ip = kwargs["destination_ip"]
        msg = kwargs["msg"]
        send_data = json.dumps({
            "data": {
                "user_phone": user_phone,
                "destination_ip": destination_ip,
                "msg": msg
            },
            "type": "send_data"
        })
        self.tcp.send_msg(send_data, SendMode.ENCRYPT)