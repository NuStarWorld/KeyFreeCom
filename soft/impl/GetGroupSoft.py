from typing import override

from soft.AbsSoft import AbsSoft


class GetGroupSoft(AbsSoft):

    @override
    def run(self, **kwargs):
        send_data = {
            "data": {
                "user_phone": kwargs["user_phone"],
            },
            "type": "get_group"
        }
        return send_data