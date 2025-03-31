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
        # encrypt_data = self.tcp.get_soft_manager().data_handling_soft.run(json.dumps({
        #         "user_phone": user_phone,
        #         "group_name": group_name,
        #         "group_number": group_number
        #     }, ensure_ascii=False),self.tcp.shared_key,DataHandlingType.ENCRYPT_DATA)
        send_data = {
            "data": {
                "user_phone": user_phone,
                "group_name": group_name,
                "group_number": group_number
            },
            "type": "create_group"
        }
        print(send_data)
        #self.tcp.send_msg(send_data,SendMode.ENCRYPT)
        return send_data