from typing import override

from soft.AbsSoft import AbsSoft


class ReceiveGroupMsgSoft(AbsSoft):
    def __init__(self, tcp):
        self.tcp = tcp

    @override
    def run(self, **kwargs):
        group_number = kwargs["group_number"]
        content = kwargs["content"]
        sender_id = kwargs["sender_id"]

        print(f"收到群组 {group_number} 的消息：{content}，发送者 ID：{sender_id}")