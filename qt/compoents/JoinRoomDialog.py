from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QVBoxLayout, QLabel, QWidget
)


class JoinRoomDialog(QDialog):
    """加入聊天室对话框 - 紧凑美化版"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        self.setWindowTitle("加入聊天室")
        self.setFixedSize(360, 170)  # 更紧凑的尺寸

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 标题
        title_label = QLabel("加入已有聊天室")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label = title_label

        # 输入表单
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # 仅保留聊天室ID输入
        self.room_id_input = QLineEdit()
        self.room_id_input.setPlaceholderText("输入聊天室数字ID")
        form_layout.addRow("聊天室ID：", self.room_id_input)

        # 按钮组
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.setCenterButtons(True)

        # 组装布局
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(form_widget)
        main_layout.addWidget(self.button_box)

        # 信号连接
        self.button_box.accepted.connect(self.validate_input)
        self.button_box.rejected.connect(self.reject)

    def setup_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F7FA;
            }
            QLabel#Title {
                font-size: 14px;
                font-weight: 600;
                color: #1F2937;
                padding-bottom: 8px;
            }
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                color: #1F2937;
                min-height: 15px;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
                background-color: #F8FAFC;
            }
            QPushButton {
                background-color: #3B82F6;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
            QDialogButtonBox {
                background: transparent;
            }
        """)

        # 标题样式调整
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #111827;
                padding-bottom: 8px;
            }
        """)

    def validate_input(self):
        """验证输入内容"""
        room_id = self.room_id_input.text().strip()

        if not room_id:
            QMessageBox.warning(self, "提示", "必须填写聊天室ID")
            return

        if not room_id.isdigit():
            QMessageBox.warning(self, "格式错误", "聊天室ID必须为纯数字")
            return

        # 这里可以添加额外的验证逻辑，例如检查ID是否存在
        # if not self.check_room_exists(room_id):
        #     QMessageBox.warning(self, "错误", "聊天室不存在")
        #     return

        self.accept()

    def get_room_id(self):
        """获取输入的房间ID"""
        return self.room_id_input.text().strip()