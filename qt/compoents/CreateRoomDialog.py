from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QVBoxLayout, QLabel, QWidget
)


class CreateRoomDialog(QDialog):
    """新建聊天室对话框 - 紧凑美化版"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        self.setWindowTitle("创建新聊天室")
        self.setFixedSize(360, 210)  # 缩小对话框尺寸

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 减小边距
        main_layout.setSpacing(15)  # 缩小间距

        # 标题
        title_label = QLabel("创建新聊天室")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label = title_label

        # 输入表单
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(10)  # 缩小表单间距
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # 输入字段
        self.group_number = QLineEdit()
        self.group_number.setPlaceholderText("数字ID")
        self.group_name = QLineEdit()
        self.group_name.setPlaceholderText("聊天室名称")

        # 添加输入项
        form_layout.addRow("聊天室ID：", self.group_number)
        form_layout.addRow("聊天室名称：", self.group_name)

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
                font-size: 14px;  /* 缩小标题字号 */
                font-weight: 600;
                color: #1F2937;
                padding-bottom: 8px;
            }
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;  /* 减细边框 */
                border-radius: 6px;  /* 减小圆角 */
                padding: 8px 12px;  /* 缩小内边距 */
                font-size: 13px;  /* 缩小字号 */
                color: #1F2937;
                min-height: 15px;  /* 降低最小高度 */
            }
            QLineEdit:focus {
                border-color: #3B82F6;
                background-color: #F8FAFC;
            }
            QPushButton {
                background-color: #3B82F6;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;  /* 减小圆角 */
                padding: 8px 16px;  /* 缩小按钮内边距 */
                font-size: 13px;  /* 缩小按钮字号 */
                min-width: 90px;  /* 减小最小宽度 */
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

        # 标题特殊样式
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;  /* 缩小标题字号 */
                font-weight: 600;
                color: #111827;
                border-bottom: 1px solid #E5E7EB;  /* 减细下划线 */
                padding-bottom: 8px;
            }
        """)

    # 保持原有验证和数据获取方法不变...
    def validate_input(self):
        """验证输入内容"""
        if not self.group_number.text().strip() or not self.group_name.text().strip():
            QMessageBox.warning(self, "提示", "所有字段必须填写")
            return
        # 添加ID必须为数字的验证
        if not self.group_number.text().strip().isdigit():
            QMessageBox.warning(self, "格式错误", "聊天室ID必须为数字")
            return
        self.accept()

    def get_data(self):
        """获取表单数据"""
        return {
            "group_number": self.group_number.text().strip(),
            "group_name": self.group_name.text().strip()
        }