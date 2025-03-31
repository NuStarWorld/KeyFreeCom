import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

from server.impl.TCPServer import TCPServer

verify = ""
tcp_server= None

class ImprovedLoginWindow(QMainWindow):
    send_code_request = pyqtSignal(str)
    verify_request = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("手机登录")
        self.setup_ui()
        self.setFixedSize(300, 350)

        # 初始化提示系统
        self.tip_timer = QTimer()
        self.tip_timer.timeout.connect(self.hide_tip)

    def setup_ui(self):
        # 主界面布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 10)
        main_layout.setSpacing(15)

        # Logo
        logo = QLabel("📱")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size: 32px;")
        main_layout.addWidget(logo)

        # 手机号输入
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("手机号")
        self.phone_input.setStyleSheet("font-size: 13px; padding: 6px;")
        main_layout.addWidget(self.phone_input)

        # 验证码区域
        code_layout = QHBoxLayout()
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("验证码")
        self.code_input.setStyleSheet("font-size: 13px; padding: 6px;")

        self.get_code_btn = QPushButton("获取")
        self.get_code_btn.setFixedWidth(60)
        self.get_code_btn.clicked.connect(self.on_get_code)

        code_layout.addWidget(self.code_input)
        code_layout.addWidget(self.get_code_btn)
        main_layout.addLayout(code_layout)

        # 登录按钮
        self.login_btn = QPushButton("登录")
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #20c997;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #1aa179; }
        """)
        self.login_btn.clicked.connect(self.on_login)
        main_layout.addWidget(self.login_btn)

        # 固定提示栏
        self.tip_label = QLabel()
        self.tip_label.setFixedHeight(30)
        self.tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tip_label.setStyleSheet("""
            QLabel {
                background-color: #ff4444;
                color: white;
                border-radius: 4px;
                font-size: 12px;
                padding: 4px;
            }
        """)
        self.tip_label.hide()
        main_layout.addWidget(self.tip_label)

    def show_tip(self, message, duration=1500):
        """显示固定位置的醒目提示"""
        self.tip_label.setText(message)
        self.tip_label.show()

        # 停止之前的定时器
        if self.tip_timer.isActive():
            self.tip_timer.stop()

        # 启动新定时器
        self.tip_timer.start(duration)

    def hide_tip(self):
        """隐藏提示"""
        self.tip_label.hide()
        self.tip_timer.stop()

    def on_get_code(self):
        phone = self.phone_input.text()
        if len(phone) != 11 or not phone.isdigit():
            self.show_tip("请输入11位有效手机号", 2000)
            return

        self.send_code_request.emit(phone)
        self.start_countdown()

    def start_countdown(self):
        self.get_code_btn.setEnabled(False)
        self.remaining = 30
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_btn_text)
        self.timer.start(1000)

    def update_btn_text(self):
        self.remaining -= 1
        if self.remaining <= 0:
            self.timer.stop()
            self.get_code_btn.setText("获取")
            self.get_code_btn.setEnabled(True)
        else:
            self.get_code_btn.setText(f"{self.remaining}s")

    def on_login(self):
        phone = self.phone_input.text()
        code = self.code_input.text()

        if not phone or not code:
            self.show_tip("请输入手机号和验证码", 2000)
            return

        self.verify_request.emit(phone, code)

class VerifyHandler:
    @staticmethod
    def send_phone_verify_code(phone):
        global verify
        verify = "1111"

    @staticmethod
    def login(phone, box_verify):
        global verify
        print(verify)
        if box_verify == verify:
            global tcp_server
            if tcp_server is None:
                tcp_server = TCPServer(phone)
                print("登录成功")
            else:
                print("请勿重复登录")
        else:
            print("验证码错误")
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = ImprovedLoginWindow()
    verifyHandler = VerifyHandler()
    window.send_code_request.connect(verifyHandler.send_phone_verify_code)
    window.verify_request.connect(verifyHandler.login)
    window.show()
    sys.exit(app.exec())