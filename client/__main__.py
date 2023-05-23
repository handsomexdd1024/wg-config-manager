import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QSplitter, QDialog, QScrollArea
from qt_material import apply_stylesheet


# 创建应用程序对象
def jump_to_forget_password():
    child = ForgetPasswordWindow()
    child.exec_()
    print('跳转到忘记密码界面')


def jump_to_sign_up():
    child = SignUpWindow()
    child.exec_()
    print('跳转到注册界面')


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建一个水平布局
        self.main_window = None
        self.h_layout = QHBoxLayout(self)

        # 创建一个分割窗口，左右各占一半
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.h_layout.addWidget(self.splitter)

        # 创建左侧的背景图片
        self.bg_pic = QLabel(self.splitter)
        self.bg_pic.setScaledContents(True)
        self.splitter.addWidget(self.bg_pic)

        # 创建右侧的登录表单
        self.login_widget = QWidget(self.splitter)
        self.splitter.addWidget(self.login_widget)
        self.login_layout = QGridLayout(self.login_widget)
        self.login_widget.setStyleSheet('background-color: #3c3f41')

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
        # 把按钮加宽一倍
        self.login_button.setStyleSheet('QPushButton{padding: 6px 30px}')
        self.login_layout.addWidget(self.login_button, 3, 0, 1, 2, Qt.AlignCenter)

        '''
        self.check_box = QCheckBox('管理员登陆', self.login_widget)
        self.login_layout.addWidget(self.check_box, 4, 0, 1, 2, Qt.AlignCenter)
        '''

        # 底部的注册和忘记密码(使用另一种样式）
        self.bottom_widget = QWidget(self.login_widget)
        self.bottom_layout = QHBoxLayout(self.bottom_widget)
        self.bottom_widget.setStyleSheet('background-color: #3c3f41')
        self.login_layout.addWidget(self.bottom_widget, 5, 0, 1, 2, Qt.AlignCenter)

        self.register_button = QPushButton('注册', self.bottom_widget)
        self.register_button.setStyleSheet('border: none')
        self.bottom_layout.addWidget(self.register_button, Qt.AlignLeft)
        self.register_button.clicked.connect(jump_to_sign_up)

        self.forget_button = QPushButton('忘记密码', self.bottom_widget)
        self.forget_button.setStyleSheet('border: none')
        self.bottom_layout.addWidget(self.forget_button, Qt.AlignRight)
        self.forget_button.clicked.connect(jump_to_forget_password)

        # 设置窗口属性
        self.setGeometry(745, 445, 800, 500)

        self.setWindowIcon(QIcon('../resource/bupt1.png'))
        self.setWindowTitle('Fast WireGuard Network Manager')
        self.login_button.clicked.connect(self.login)

        # 设置动态背景图片
        # TODO: 换上一个正经的icon
        movie = QMovie('../resource/tunnel.gif')
        self.bg_pic.setMovie(movie)
        movie.start()

    def login(self):
        username = self.user_edit.text()
        password = self.passwd_edit.text()

        # TODO: 在此处编写验证登录信息的代码

        # 登陆成功后跳转到主界面
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()
        print('账号：', username)
        print('密码：', password)

    # 主界面


from PyQt5.QtWidgets import QVBoxLayout, QScrollArea


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 窗口居中占满半个屏幕
        self.resize(1680, 1150)
        self.move(400, 250)
        # 设置窗口标题
        self.setWindowTitle('Fast WireGuard Network Manager')
        # 设置窗口图标
        # TODO: 换上一个正经的icon
        # 整体使用水平布局
        self.main_layout = QHBoxLayout(self)
        # 创建一个主分割窗口分割左右两个部分
        self.main_splitter = QSplitter(Qt.Horizontal, self)
        self.main_layout.addWidget(self.main_splitter)

        # 创建左侧的文件栏，用于列出文件
        self.file_widget = QWidget(self.main_splitter)
        self.file_layout = QVBoxLayout(self.file_widget)
        self.file_widget.setStyleSheet('background-color: #3c3f41')

        # 创建一个垂直布局用于容纳文件栏和滚动条
        self.file_layout_with_scroll = QVBoxLayout(self.file_widget)
        self.file_layout_with_scroll.setContentsMargins(0, 0, 0, 0)
        self.file_layout_with_scroll.setSpacing(0)

        # 使用滚动区域包装文件栏部件
        self.file_scroll_area = QScrollArea()
        self.file_scroll_area.setWidgetResizable(True)
        self.file_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.file_scroll_area.setWidget(self.file_widget)

        self.main_splitter.addWidget(self.file_scroll_area)

        # 创建一个右侧的分割窗口用于上下分割
        self.right_splitter = QSplitter(Qt.Vertical, self.main_splitter)

        # 创建右侧上方的主窗口
        self.top_widget = QWidget(self.right_splitter)
        self.top_widget.setStyleSheet('background-color: #3c3f41')

        # 底部创建一个水平分割栏，用于设置三个按钮，分别为更新、添加、删除
        self.bottom_splitter = QSplitter(Qt.Horizontal, self.right_splitter)
        self.bottom_text_widget = QWidget(self.bottom_splitter)
        self.bottom_button_widget = QWidget(self.bottom_splitter)
        self.bottom_splitter.setHandleWidth(6)
        self.bottom_text_widget.setStyleSheet('background-color: #3c3f41')
        self.bottom_button_widget.setStyleSheet('background-color: #3c3f41')

        # 调整伸缩性，使得右上方的主窗口可以伸缩
        self.right_splitter.setStretchFactor(0, 3)
        self.right_splitter.setStretchFactor(1, 1)
        self.main_splitter.setStretchFactor(1, 1)

        # 设置左右splitter初始宽度比例1：3
        self.right_splitter.setSizes([3, 1])
        self.main_splitter.setSizes([self.width() // 4, self.width() * 3 // 4])
        self.right_splitter.setSizes([self.width() * 3 // 4, self.width() // 4])
        self.bottom_splitter.setSizes([self.width() * 3 // 4, self.width() // 4])

        # 设置边框宽度
        self.right_splitter.setHandleWidth(5)

        # 创建底部按钮,用于新建配置文件
        self.file_button = QPushButton("New config", self.file_widget)
        self.file_layout.addStretch()
        self.file_layout.addWidget(self.file_button, alignment=Qt.AlignCenter)
        self.file_button.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"')
        self.file_button.clicked.connect(self.new_config)

    def get_network_info(self):
        # TODO: 在此处编写获取该用户网络信息的代码
        pass

    def show_config(self):
        # TODO: 在此处编写显示获取的配置文件的代码
        pass

    def new_config(self):
        # TODO: 在此处编写新建配置文件的代码
        pass

    def show_graph(self):
        # TODO: 在此处编写显示获取的图表的代码
        pass

    def show_node(self):
        # TODO: 在此处编写显示点击的的节点信息的代码
        pass
    
    def update_wireguard_node(self):
        # TODO: 在此处编写修改节点信息的代码
        pass

    def create_wireguard_node(self):
        # TODO: 在此处编写新建节点信息的代码
        pass
    
    def delete_wireguard_node(self):
        # TODO: 在此处编写删除节点信息的代码
        pass

    def generate_config(self):
        # TODO: 在此处编写生成配置文件的代码
        pass

class ChildDialogUi(QDialog):
    def __init__(self, text):
        super().__init__()

        self.setWindowFlags(self.windowFlags() | Qt.WindowCloseButtonHint)
        layout = QGridLayout(self)
        self.label = QLabel(self)
        self.label.setText(text)
        layout.addWidget(self.label, 0, 0, 1, 0, Qt.AlignCenter)
        self.setLayout(layout)


# 注册窗口继承自ChildDialogUi
class SignUpWindow(ChildDialogUi):
    def __init__(self):
        super().__init__('SIGN UP NOW AND JOIN US')

        self.setWindowTitle('注册')
        self.setGeometry(1100, 750, 800, 500)

        sign_up_layout = self.layout()

        sign_up_label = self.label
        sign_up_label.setStyleSheet('font-size: 30px; font-weight: bold; color: white')
        sign_up_layout.addWidget(sign_up_label, 0, 0, 1, 0, Qt.AlignCenter)
        self.user_label = QLabel('账号:', self)
        # 将控件添加到布局中
        sign_up_layout.addWidget(self.user_label, 1, 2, 1, 1)

        self.sign_up_user_edit = QLineEdit(self)
        sign_up_layout.addWidget(self.sign_up_user_edit, 1, 3, 1, 1)

        self.sign_up_passwd_label = QLabel('密码:', self)
        sign_up_layout.addWidget(self.sign_up_passwd_label, 2, 2, 1, 1)

        self.sign_up_passwd_edit = QLineEdit(self)
        sign_up_layout.addWidget(self.sign_up_passwd_edit, 2, 3, 1, 1)

        self.sign_up_passwd_label = QLabel('确认密码:', self)
        sign_up_layout.addWidget(self.sign_up_passwd_label, 3, 2, 1, 1)

        self.sign_up_passwd_edit = QLineEdit(self)
        sign_up_layout.addWidget(self.sign_up_passwd_edit, 3, 3, 1, 1)

        self.sign_up_button = QPushButton('注册', self)
        sign_up_layout.addWidget(self.sign_up_button, 4, 2, 1, 2)

        self.sign_up_button.clicked.connect(self.sign_up)

    def sign_up(self):
        username = self.sign_up_user_edit.text()
        cleartext_password = self.sign_up_passwd_edit.text()
        # TODO: 在此处编写注册账号的代码（发送usrname和cleartext_password到服务器）


class ForgetPasswordWindow(ChildDialogUi):
    def __init__(self):
        super().__init__('找回密码')

        self.setWindowTitle('Get your password back')
        self.setGeometry(1100, 750, 800, 500)

        passwd_recovery_layout = self.layout()

        sign_up_label = self.label
        sign_up_label.setStyleSheet('font-size: 30px; font-weight: bold; color: white')
        passwd_recovery_layout.addWidget(sign_up_label, 0, 0, 1, 0, Qt.AlignCenter)
        self.user_label = QLabel('账号/用户名:', self)
        # 将控件添加到布局中
        passwd_recovery_layout.addWidget(self.user_label, 1, 2, 1, 1)

        self.user_edit = QLineEdit(self)
        passwd_recovery_layout.addWidget(self.user_edit, 1, 3, 1, 1)

        self.passwd_recovery_bn = QPushButton('认证', self)
        passwd_recovery_layout.addWidget(self.passwd_recovery_bn, 4, 2, 1, 2)

        self.passwd_recovery_bn.clicked.connect(self.passwd_recovery)

    def passwd_recovery(self):
        username = self.user_edit.text()


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
