import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QTextBrowser, QTextEdit, QPushButton, QSplitter, QSizePolicy, QApplication, QDialog, QMessageBox
)

from PyQt6.QtCore import Qt, QSize

from qt.compoents.JoinRoomDialog import JoinRoomDialog
from soft import run
from qt.NetworkThread import NetworkThread
from qt.compoents.CreateRoomDialog import CreateRoomDialog
from server.impl.TCPServer import TCPServer


class ChatWindow(QMainWindow):


    def __init__(self, tcp):
        super().__init__()
        self.setWindowTitle("聊天室")
        self.setGeometry(100, 100, 500, 500)
        self.setup_ui()
        self.setup_styles()
        self.tcp = tcp
        self.managers = tcp.get_soft_manager()
        self.setup_network()
        # 用户加入的群组列表
        self.groups = []
        # 用户ID
        self.id = ""
        self.get_groups()

    def setup_network(self):
        self.network_thread = NetworkThread(self.tcp)
        self.network_thread.result_received.connect(self.handle_network_result)
        self.network_thread.error_occurred.connect(self.handle_network_error)



    def handle_network_result(self, result):
        """处理网络响应"""
        self.tcp.debug.debug_info(f"收到界面消息:{result}")
        if result["data"]["result"] == "success":
            match result["type"]:
                case "join_group":
                    self.chatroom_list.clear()
                    self.get_groups()
                case "get_recent_msg":
                    messages = result["data"]["messages"]
                    for key in messages:
                        sender_id = messages[key]["sender_id"]
                        message = messages[key]["content"]
                        from datetime import datetime
                        sent_at = datetime.fromisoformat(messages[key]["sent_at"])
                        formatted_time = sent_at.strftime("%Y-%m-%d %H:%M:%S")
                        if sender_id == self.id:
                            # 如果是自己的id消息就显示在聊天框右边，要包含日期,用户ID,消息内容元素
                            # 自己的消息（右侧）
                            html_content = f"""
                                    <div>{formatted_time}</div>
                                    <div>你:{message}</div>
                                    """
                        else:
                            # 他人的消息（左侧）
                            html_content = f"""
                                    <div>{formatted_time}</div>
                                    <div>用户{sender_id}:{message}</div>
                                    """
                        self.chat_display.append(html_content)
                        # 自动滚动到底部
                    self.chat_display.verticalScrollBar().setValue(
                        self.chat_display.verticalScrollBar().maximum()
                    )
                case "create_group":
                    self.update_chatroom_list({
                        "group_number": result["data"]["group_number"],
                        "group_name": result["data"]["group_name"]
                    })
                    QMessageBox.information(self, "成功", "聊天室创建成功")
                case "get_groups":
                    groups = result["data"]["groups"]
                    self.id = result["sender_id"]
                    for key in groups:
                        self.update_chatroom_list({
                            "group_number": groups[key]["group_number"],
                            "group_name": groups[key]["group_name"]
                        })
                case "send_group_msg":
                    # 获取当前选中的群组项
                    current_item = self.chatroom_list.currentItem()
                    if current_item is None:
                        return  # 没有选中任何群组时忽略消息
                    group_number = result["data"]["group_number"]
                    # 如果消息群组ID是当前聊天室，就显示在聊天框
                    if group_number == self.chatroom_list.currentItem().text().split(":")[1]:
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        sender_id = result["data"]["sender_id"]
                        message = result["data"]["content"]
                        if sender_id == self.id:
                            # 如果是自己的id消息就显示在聊天框右边，要包含日期,用户ID,消息内容元素
                            # 自己的消息（右侧）
                            html_content = f"""
                                    <div>{timestamp}</div>
                                    <div>你:{message}</div>
                                    """
                        else:
                            # 他人的消息（左侧）
                            html_content = f"""
                                    <div>{timestamp}</div>
                                    <div>用户{sender_id}:{message}</div>
                                    """
                        self.chat_display.append(html_content)
                        # 自动滚动到底部
                        self.chat_display.verticalScrollBar().setValue(
                            self.chat_display.verticalScrollBar().maximum()
                        )
        elif result["data"]["result"] == "failed":
            match result["type"]:
                case "join_group":
                    QMessageBox.critical(self, "错误", result["data"]["reason"])
                case "create_group":
                    QMessageBox.critical(self, "错误", "聊天室号码已存在")
                case "get_groups":
                    QMessageBox.critical(self, "错误", "获取聊天室列表失败")
        else:
            QMessageBox.critical(self, "错误", "未知错误")

    def handle_network_error(self, error):
        """处理网络错误"""
        QMessageBox.critical(self, "网络异常", error)
    def setup_ui(self):
        # 主窗口布局
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # 左侧区域（1/3）
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        # 左侧功能按钮
        self.new_button = QPushButton("新建聊天室")
        self.join_button = QPushButton("加入聊天室")
        self.exit_button = QPushButton("退出聊天室")

        # 统一按钮尺寸
        for btn in [self.new_button, self.join_button, self.exit_button]:
            btn.setFixedHeight(40)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # 聊天室列表
        self.chatroom_list = QListWidget()
        self.chatroom_list.itemClicked.connect(self.handle_chatroom_click)
        self.chatroom_list.setSpacing(5)  # 列表项间距

        # 添加组件到左侧布局
        left_layout.addWidget(self.new_button)
        left_layout.addWidget(self.join_button)
        left_layout.addWidget(self.exit_button)
        left_layout.addWidget(self.chatroom_list)

        # 右侧区域（2/3）
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(15, 0, 0, 0)
        right_layout.setSpacing(15)

        # 聊天记录显示区域
        self.chat_display = QTextBrowser()

        # 输入区域
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("输入消息...")
        self.message_input.setFixedHeight(130)

        self.send_button = QPushButton("发送")
        self.send_button.setFixedSize(QSize(80, 50))

        # 添加输入组件
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)

        # 添加右侧组件
        right_layout.addWidget(self.chat_display)
        right_layout.addWidget(input_widget)

        # 设置左右区域比例
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([200, 350])  # 初始宽度

        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)

        # 设置布局比例
        right_layout.setStretch(0, 2)
        right_layout.setStretch(1, 1)
        left_layout.setStretch(3, 1)

        # 连接信号槽（保持不变）
        self.send_button.clicked.connect(self.send_message)
        self.new_button.clicked.connect(self.create_chatroom)
        self.join_button.clicked.connect(self.join_chatroom)
        self.exit_button.clicked.connect(self.leave_chatroom)


    def setup_styles(self):
        # 主样式表
        self.setStyleSheet("""
                QWidget {
                    background-color: #F5F7FA;
                }
                QPushButton {
                    background-color: #FFFFFF;
                    border: 2px solid #D1D5DB;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 14px;
                    color: #374151;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #E5E7EB;
                    border-color: #9CA3AF;
                }
                QPushButton:pressed {
                    background-color: #D1D5DB;
                }
                QListWidget {
                    background-color: #FFFFFF;
                    border: 2px solid #D1D5DB;
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 14px;
                    color: #000000; /* 新增文本颜色设置 */
                }
                QMessageBox QLabel { color: black; }
                QListWidget::item {
                    color: #000000; /* 确保列表项文本颜色 */
                }
                QTextBrowser, QTextEdit {
                    background-color: #FFFFFF;
                    border: 2px solid #D1D5DB;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 14px;
                    color: #374151;
                }
                QScrollBar:vertical {
                    width: 10px;
                    background: transparent;
                }
                QScrollBar::handle:vertical {
                    background: #CBD5E1;
                    border-radius: 4px;
                }
            """)
        # 特殊按钮样式
        self.send_button.setStyleSheet("""
                QPushButton {
                    background-color: #3B82F6;
                    color: #FFFFFF;
                    border-radius: 15px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #2563EB;
                }
                QPushButton:pressed {
                    background-color: #1D4ED8;
                }
            """)
    # 以下为预留接口，需自行实现具体功能
    def handle_chatroom_click(self, item):
        self.chat_display.clear()
        group_name, group_number = item.text().split(":")
        group_number = group_number.strip()
        request = run(self.managers.get_recent_msg_soft, group_number=group_number)
        self.network_thread.set_request_data(request)
        self.network_thread.run()
    def create_chatroom(self):
        """创建聊天室完整流程"""
        dialog = CreateRoomDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            room_data = dialog.get_data()
            # 构造请求协议 该对象是一个字典
            request = run(self.managers.create_group_soft,
                group_name=room_data["group_name"],
                group_number=room_data["group_number"],
                user_phone=self.tcp.hash_user_phone)

            # 发送网络请求
            self.network_thread.set_request_data(request)
            self.network_thread.run()

    def get_groups(self):
        request = run(self.managers.get_group_soft, user_phone=self.tcp.hash_user_phone)
        self.network_thread.set_request_data(request)
        self.network_thread.run()

    def update_chatroom_list(self, room_data):
        """更新左侧聊天室列表"""
        self.tcp.debug.debug_info("添加列表:" + str(room_data))
        item_text = f"{room_data['group_name']} :{room_data['group_number']}"
        self.chatroom_list.addItem(item_text)
    def send_message(self):
        """发送消息接口"""
        message = self.message_input.toPlainText().strip()
        if message:
            # 这里添加实际发送逻辑
            request = run(self.managers.send_group_msg_soft, group_number=self.chatroom_list.currentItem().text().split(":")[1],
                          user_phone=self.tcp.hash_user_phone,
                          content=message)
            self.network_thread.set_request_data(request)
            self.network_thread.run()
            self.message_input.clear()
            self.tcp.debug.debug_info("当前选择群组:" + self.chatroom_list.currentItem().text())
            pass


    def join_chatroom(self):
        """加入聊天室接口"""
        # 添加实际加入逻辑
        dialog = JoinRoomDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            room_id = dialog.get_room_id()
            # 构造请求协议 该对象是一个字典
            request = run(self.managers.join_group_soft, group_number=room_id, user_id=self.id)
            self.network_thread.set_request_data(request)
            self.network_thread.run()

    def leave_chatroom(self):
        """离开聊天室接口"""
        # 添加实际离开逻辑
        pass


if __name__ == "__main__":
    #app = sys.argv.append('--no-sandbox')  # 仅在Linux桌面环境需要
    app = QApplication(sys.argv)
    tcp_server = TCPServer("15167466371")
    window = ChatWindow(tcp_server)
    window.show()
    sys.exit(app.exec())