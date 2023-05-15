import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from qt_material import apply_stylesheet

# 创建应用程序对象
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建一个水平布局
        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        # 创建左侧的背景图片
        self.bg_pic = QLabel(self)
        self.bg_pic.setPixmap(QPixmap('cloud.jpg').scaledToWidth(400))
        # self.bg_pic.setStyleSheet('background-color: #FAFAFA')
        self.h_layout.addWidget(self.bg_pic)

        # 创建右侧的登录表单
        self.login_widget = QWidget(self)
        self.login_layout = QGridLayout(self.login_widget)
        self.login_widget.setStyleSheet('background-color: #3c3f41')
        self.h_layout.addWidget(self.login_widget)

        # 创建登录表单中的控件
        self.label = QLabel('Central WireGuard Network Manager', self.login_widget)
        self.label.setStyleSheet('font-size: 24px; font-weight: bold')
        self.login_layout.addWidget(self.label, 0, 0, 1, 2, Qt.AlignCenter)

        self.user_label = QLabel('账号:', self.login_widget)
        self.login_layout.addWidget(self.user_label, 1, 0, 1, 1)

        self.user_edit = QLineEdit(self.login_widget)
        self.login_layout.addWidget(self.user_edit, 1, 1, 1, 1)

        self.passwd_label = QLabel('密码:', self.login_widget)
        self.login_layout.addWidget(self.passwd_label, 2, 0, 1, 1)

        self.passwd_edit = QLineEdit(self.login_widget)
        self.login_layout.addWidget(self.passwd_edit, 2, 1, 1, 1)

        self.login_button = QPushButton('登录', self.login_widget)
        self.login_layout.addWidget(self.login_button, 3, 0, 1, 2, Qt.AlignCenter)

        self.check_box = QCheckBox('管理员登陆', self.login_widget)
        self.login_layout.addWidget(self.check_box, 4, 0, 1, 2, Qt.AlignCenter)

        # 设置窗口属性
        self.setGeometry(300, 300, 800, 500)
        self.setWindowIcon(QIcon('vscode.jfif'))
        self.setWindowTitle('Fast WireGuard Network Manager')
        self.login_button.clicked.connect(self.login)

    def login(self):
        username = self.user_edit.text()
        password = self.passwd_edit.text()

        # TODO: 在此处编写验证登录信息的代码

        print('账号：', username)
        print('密码：', password)

if __name__ == '__main__':
    extra = {
        'font_family': '微软雅黑',
        'font_size': '12',
        'font_weight': '100',
        'font_kerning': 'true',
    }

    app = QApplication(sys.argv)
    window = LoginWindow()
    apply_stylesheet(app, theme='dark_teal.xml', invert_secondary=True, extra=extra)
    window.show()
    sys.exit(app.exec_())
