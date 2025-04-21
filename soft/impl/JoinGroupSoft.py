from typing import override

from soft.AbsSoft import AbsSoft


class JoinGroupSoft(AbsSoft):

    @override
    def run(self, **kwargs):
        group_number = kwargs.get("group_number")
        user_id = kwargs.get("user_id")
        send_data = {
            "data": {
                "group_number": group_number,
                "user_id": user_id
            },
            "type": "join_group"
        }
        return send_data