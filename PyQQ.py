import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from qt_material import apply_stylesheet


# 创建应用程序对象
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 创建一个水平布局
        self.label = None
        self.login_button = None
        self.passwd_edit = None
        self.passwd_label = None
        self.user_edit = None
        self.user_label = None
        self.h_layout = QHBoxLayout()
        # 创建一个垂直布局
        self.v_layout = QVBoxLayout()
        # 设置窗口布局为水平布局

        # self.setLayout(self.h_layout)

    def initUI(self):
        # 设置窗口大小和位置
        self.setGeometry(300, 300, 900, 450)

        # 设置界面标题
        self.setWindowTitle('Central WireGuard Network Manager')
        # 在窗口中居中创建一个标签
        self.label = QLabel('Central WireGuard Network Manager', self)
        self.label.setFont(QFont('微软雅黑', 10))
        self.label.move(200, 100)

        
        # 设置窗口标题
        self.setWindowTitle('登录')
        self.user_label = QLabel('账号:', self)
        self.user_label.move(150, 200)

        self.user_edit = QLineEdit(self)
        self.user_edit.move(220, 200)

        self.passwd_label = QLabel('密码:', self)
        self.passwd_label.move(150, 250)

        self.passwd_edit = QLineEdit(self)
        self.passwd_edit.move(220, 250)
        # self.passwd_edit.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('登录', self)
        self.login_button.move(230, 300)

        # 连接信号和槽函数
        self.login_button.clicked.connect(self.login)

    def login(self):
        # 获取输入框中的文本
        username = self.user_edit.text()
        password = self.passwd_edit.text()

        # TODO: 在此处编写验证登录信息的代码

        # 打印登录信息
        print('账号：', username)
        print('密码：', password)


if __name__ == '__main__':
    extra = {
        # 这个缩放比例apply不了我也不知道咋回事
        'density_scale': '0',

        # Font
        'font_family': '微软雅黑',
        'font_size': '12',
        'font_weight': '100',
        'font_kerning': 'true',

    }
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.initUI()

    # apply_stylesheet(app, theme='light_red.xml', invert_secondary=True)
    apply_stylesheet(app, theme='dark_teal.xml', invert_secondary=True, extra=extra)
    # 这个主题是我找的一个打包使用的主题，https://github.com/UN-GCPDS/qt-material.git

    window.show()
    sys.exit(app.exec_())
