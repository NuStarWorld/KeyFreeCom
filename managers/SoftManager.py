from soft.impl.ChatSoft import ChatSoft
from soft.impl.CreateGroupSoft import CreateGroupSoft
from soft.impl.DataHandlingSoft import DataHandlingSoft
from soft.impl.GetGroupSoft import GetGroupSoft
from soft.impl.PublicKeySoft import PublicKeySendSoft, PublicKeyReceiveSoft
from soft.impl.ReceiveGroupMsgSoft import ReceiveGroupMsgSoft
from soft.impl.SendGroupMsgSoft import SendGroupMsgSoft


class SoftManager:
    def __init__(self):
        self.chat_soft = None
        self.data_handling_soft = DataHandlingSoft()
        self.public_key_send_soft = None
        self.create_group_soft = None
        self.public_key_receive_soft = None
        self.send_group_msg_soft = None
        self.receive_group_msg_soft = None
        self.get_group_soft = None

    def register(self,tcp):
        self.chat_soft = ChatSoft(tcp)
        self.public_key_send_soft = PublicKeySendSoft(tcp)
        self.create_group_soft = CreateGroupSoft(tcp)
        self.public_key_receive_soft = PublicKeyReceiveSoft(tcp)
        self.send_group_msg_soft = SendGroupMsgSoft(tcp)
        self.receive_group_msg_soft = ReceiveGroupMsgSoft(tcp)
        self.get_group_soft = GetGroupSoft()
