from PyQt6.QtCore import QThread, pyqtSignal
from typing import override

from enums.SendMode import SendMode


class NetworkThread(QThread):
    """网络通信线程"""
    result_received = pyqtSignal(dict)  # 成功信号
    error_occurred = pyqtSignal(str)  # 错误信号
    def __init__(self, tcp):
        super().__init__()
        self.server = tcp
        self.request_data = None

    def set_request_data(self, data):
        self.request_data = data

    @override
    def run(self):
        try:
            result = self.server.send_msg(self.request_data, SendMode.ENCRYPT)
            self.result_received.emit(result)
        except Exception as e:
            print(e)
            self.error_occurred.emit(f"网络错误: {str(e)}")