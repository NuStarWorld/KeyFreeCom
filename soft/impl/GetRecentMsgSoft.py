from typing import override

from soft.AbsSoft import AbsSoft


class GetRecentMsgSoft(AbsSoft):

    @override
    def run(self, **kwargs):
        group_number = kwargs.get("group_number")
        send_data = {
            "data": {
                "group_number": group_number
            },
            "type": "get_recent_msg"
        }
        return send_data