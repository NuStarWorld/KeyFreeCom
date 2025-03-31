from typing import override

from enums.SendMode import SendMode
from soft.AbsSoft import AbsSoft


class SendGroupMsgSoft(AbsSoft):
    def __init__(self, tcp):
        self.tcp = tcp

    @override
    def run(self, **kwargs):
        user_phone = kwargs["user_phone"]
        group_number = kwargs["group_number"]
        content = kwargs["content"]
        send_data = {
            "data": {
                "user_phone": user_phone,
                "group_number": group_number,
                "content": content
            },
            "type": "send_group_msg"
        }
        self.tcp.send_msg(send_data,SendMode.ENCRYPT)