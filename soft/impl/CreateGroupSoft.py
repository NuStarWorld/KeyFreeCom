from typing import override

from soft.AbsSoft import AbsSoft


class CreateGroupSoft(AbsSoft):
    def __init__(self,tcp):
        self.tcp = tcp

    @override
    def run(self,**kwargs):
        group_name = kwargs["group_name"]
        group_number = kwargs["group_number"]
        user_phone = kwargs["user_phone"]
        send_data = {
            "data": {
                "user_phone": user_phone,
                "group_name": group_name,
                "group_number": group_number
            },
            "type": "create_group"
        }
        return send_data