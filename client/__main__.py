import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QSplitter, QDialog, QScrollArea, \
    QVBoxLayout, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from qt_material import apply_stylesheet
from pyvis.network import Network
import client.network as network
import core.wgconfig as config
import core.wgobject as wgobject
import core.user as user
import networkx as nx


class Session:
    def __init__(self):
        self.user = None
        self.config_server = network.ConfigServer('localhost:8000')
        self.wireguard_object = None

    def get_user_config(self):
        self.config_server.get_config(self.user.uuid)

    def init_config_server(self, url):
        self.config_server = network.ConfigServer(url)

    def get_wg_object(self):
        self.wireguard_object = self.config_server.get_network_object(self.user.uuid, self.user.wg_object_uuid_list)


session = Session()


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

    def login(self) -> [bool, str, user.User]:
        username = self.user_edit.text()
        password = self.passwd_edit.text()
        # 结束这个窗口
        # TODO: 在此处编写验证登录信息的代码
        # auth_response = config_server.user_auth_request(username, password)
        # if not auth_response[0]:
        #     print(auth_response[1])
        #     return
        # else:
        #     session.user = config_server.get_user_profile(auth_response[1])
        #     config_server.get_user_config(session.user.uuid)
        #     print('登录成功')

        # 登陆成功后结束当前窗口，返回一个信息给到主界面
        self.close()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 窗口居中占满半个屏幕
        self.setWindowIcon(QIcon('../resource/bupt1.png'))
        self.conf_line = None
        self.conf_text = None
        self.text_combined_widget = None
        self.resize(1680, 1150)
        self.move(400, 250)

        # 设置窗口标题
        self.setWindowTitle('Fast WireGuard Network Manager')
        # 设置窗口图标

        # 整体使用水平布局
        self.main_layout = QHBoxLayout(self)
        # 创建一个主分割窗口分割左右两个部分
        self.main_splitter = QSplitter(Qt.Horizontal, self)
        self.main_layout.addWidget(self.main_splitter)

        # 创建左侧的文件栏，用于列出文件
        self.file_widget = QWidget(self.main_splitter)
        self.file_layout = QVBoxLayout(self.file_widget)
        self.file_widget.setStyleSheet('background-color: #3c3f41')

        # 创建一个垂直布局用于容纳文件栏
        self.file_layout_with_scroll = QVBoxLayout(self.file_widget)
        self.file_layout_with_scroll.setContentsMargins(0, 0, 0, 0)
        self.file_layout_with_scroll.setSpacing(0)

        # 创建一个右侧的分割窗口用于上下分割
        self.right_splitter = QSplitter(Qt.Vertical, self.main_splitter)

        # 创建一个右上方splitter
        self.right_top_splitter = QSplitter(Qt.Vertical, self.right_splitter)
        self.right_top_splitter.setHandleWidth(1)
        # 创建一个右侧上方的窗口用于存放选项
        self.right_top_widget = QWidget(self.right_top_splitter)
        self.right_top_layout = QHBoxLayout(self.right_top_widget)
        self.right_top_widget.setStyleSheet('background-color: #3c3f41')

        # 创建右侧上方的主窗口
        self.top_widget = QWidget(self.right_splitter)
        self.top_layout = QHBoxLayout(self.top_widget)
        self.top_widget.setStyleSheet('background-color: #3c3f41')

        # 将生成的图加载到top_widget中
        self.graph_view = QWebEngineView(self.top_widget)
        # 设置graph_view占满整个top_widget
        self.top_layout.addWidget(self.graph_view)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(0)

        # 底部创建一个水平分割栏，用于设置三个按钮，分别为更新、添加、删除
        self.bottom_splitter = QSplitter(Qt.Horizontal, self.right_splitter)
        self.bottom_text_widget = QWidget(self.bottom_splitter)
        self.bottom_button_widget = QWidget(self.bottom_splitter)
        self.bottom_splitter.setHandleWidth(6)
        self.bottom_text_widget.setStyleSheet('background-color: #3c3f41')
        self.bottom_button_widget.setStyleSheet('background-color: #3c3f41')

        # 将bottom_text_widget区域全部变成文本区域
        self.bottom_text_layout = QVBoxLayout(self.bottom_text_widget)
        self.bottom_text_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_text_layout.setSpacing(0)

        self.bottom_conf_widget = QWidget(self.bottom_text_widget)
        self.bottom_conf_widget1 = QWidget(self.bottom_text_widget)
        self.bottom_conf_widget2 = QWidget(self.bottom_text_widget)
        self.bottom_conf_widget3 = QWidget(self.bottom_text_widget)
        self.bottom_conf_widget4 = QWidget(self.bottom_text_widget)

        # 全都设置成水平布局
        self.conf_lay = QHBoxLayout(self.bottom_conf_widget)
        self.conf_lay1 = QHBoxLayout(self.bottom_conf_widget1)
        self.conf_lay2 = QHBoxLayout(self.bottom_conf_widget2)
        self.conf_lay3 = QHBoxLayout(self.bottom_conf_widget3)
        self.conf_lay4 = QHBoxLayout(self.bottom_conf_widget4)

        self.bottom_text = QLabel(self.bottom_conf_widget)
        self.bottom_text1 = QLabel(self.bottom_conf_widget1)
        self.bottom_text2 = QLabel(self.bottom_conf_widget2)
        self.bottom_text3 = QLabel(self.bottom_conf_widget3)
        self.bottom_text4 = QLabel(self.bottom_conf_widget4)
        self.bottom_text.setText('UID  :   ')
        self.bottom_text1.setText('Name :')
        self.bottom_text2.setText('Owner:')
        self.bottom_text3.setText('Users:  ')
        self.bottom_text4.setText('NID  :   ')

        self.bottom_line = QLineEdit(self.bottom_conf_widget)
        self.bottom_line1 = QLineEdit(self.bottom_conf_widget1)
        self.bottom_line2 = QLineEdit(self.bottom_conf_widget2)
        self.bottom_line3 = QLineEdit(self.bottom_conf_widget3)
        self.bottom_line4 = QLineEdit(self.bottom_conf_widget4)

        self.conf_lay.addWidget(self.bottom_text)
        self.conf_lay.addWidget(self.bottom_line)
        self.conf_lay1.addWidget(self.bottom_text1)
        self.conf_lay1.addWidget(self.bottom_line1)
        self.conf_lay2.addWidget(self.bottom_text2)
        self.conf_lay2.addWidget(self.bottom_line2)
        self.conf_lay3.addWidget(self.bottom_text3)
        self.conf_lay3.addWidget(self.bottom_line3)
        self.conf_lay4.addWidget(self.bottom_text4)
        self.conf_lay4.addWidget(self.bottom_line4)

        self.bottom_text_layout.addWidget(self.bottom_conf_widget, alignment=Qt.AlignLeft)
        self.bottom_text_layout.addWidget(self.bottom_conf_widget1, alignment=Qt.AlignLeft)
        self.bottom_text_layout.addWidget(self.bottom_conf_widget2, alignment=Qt.AlignLeft)
        self.bottom_text_layout.addWidget(self.bottom_conf_widget3, alignment=Qt.AlignLeft)
        self.bottom_text_layout.addWidget(self.bottom_conf_widget4, alignment=Qt.AlignLeft)

        # 设置底部edit_line区域样式
        self.bottom_line1.setStyleSheet(
            'background-color: #222222; color: white; font-size: 20px; font-family: "Microsoft YaHei"; width: 1100px')
        self.bottom_line2.setStyleSheet(
            'background-color: #222222; color: white; font-size: 20px; font-family: "Microsoft YaHei"; width: 1100px')
        self.bottom_line3.setStyleSheet(
            'background-color: #222222; color: white; font-size: 20px; font-family: "Microsoft YaHei"; width: 1100px')
        self.bottom_line4.setStyleSheet(
            'background-color: #222222; color: white; font-size: 20px; font-family: "Microsoft YaHei"; width: 1100px')

        # 调整伸缩性，使得右上方的主窗口可以伸缩
        self.right_splitter.setStretchFactor(0, 3)
        self.right_splitter.setStretchFactor(1, 1)
        self.main_splitter.setStretchFactor(1, 1)

        # 设置splitter初始宽度比例
        self.right_splitter.setSizes([3, 1])
        self.main_splitter.setSizes([self.width() // 4, self.width() * 3 // 4])
        self.right_splitter.setSizes([self.width() * 1 // 10, self.width() * 7 // 10, self.width() * 1 // 5])
        self.bottom_splitter.setSizes([self.width() * 3 // 4, self.width() // 4])

        # 设置边框宽度
        self.right_splitter.setHandleWidth(5)

        # 创建file区底部按钮,用于新建配置文件
        self.conf_button1 = QPushButton("config file1", self.file_widget)
        self.conf_button1.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"')
        self.conf_button1.setFixedSize(350, 60)
        self.file_layout.addWidget(self.conf_button1, alignment=Qt.AlignCenter)
        self.conf_button1.clicked.connect(self.conf1_button_clicked)

        self.conf_button2 = QPushButton("config file2", self.file_widget)
        self.conf_button2.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"')
        self.conf_button2.setFixedSize(350, 60)
        self.file_layout.addWidget(self.conf_button2, alignment=Qt.AlignCenter)
        self.conf_button2.clicked.connect(self.conf2_button_clicked)

        self.conf_button3 = QPushButton("config file3", self.file_widget)
        self.conf_button3.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"')
        self.conf_button3.setFixedSize(350, 60)
        self.file_layout.addWidget(self.conf_button3, alignment=Qt.AlignCenter)
        self.conf_button3.clicked.connect(self.conf3_button_clicked)

        self.file_layout.addStretch()

        self.file_button = QPushButton("New config", self.file_widget)
        self.file_layout.addWidget(self.file_button, alignment=Qt.AlignCenter)
        self.file_button.setFixedSize(200, 50)
        self.file_button.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"')
        self.file_button.clicked.connect(self.new_config)

        # 按钮区域使用垂直布局
        self.bottom_button_layout = QVBoxLayout(self.bottom_button_widget)
        self.bottom_button_layout.addStretch()

        # 创建右上方filter按钮
        self.filter_button = QPushButton("Filter Mode", self.right_top_widget)
        self.right_top_layout.addWidget(self.filter_button, alignment=Qt.AlignCenter)
        self.filter_button.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"; height: '
                                         '30px; width: 140px')
        self.filter_button.clicked.connect(self.show_filter_menu)

        # 创建右上方select按钮
        self.select_button = QPushButton("Select Mode", self.right_top_widget)
        self.right_top_layout.addWidget(self.select_button, alignment=Qt.AlignCenter)
        self.select_button.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"; height: '
                                         '30px; width: 140px')
        self.select_button.clicked.connect(self.show_select_menu)

        # 创建右上方physics按钮
        self.physics_button = QPushButton("Physics Settings", self.right_top_widget)
        self.right_top_layout.addWidget(self.physics_button, alignment=Qt.AlignCenter)
        self.physics_button.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"; height: '
                                          '30px; width: 190px')
        self.physics_button.clicked.connect(self.show_physics_menu)

        # 创建右上方Nodes UI按钮
        self.nodes_ui_button = QPushButton("Nodes UI", self.right_top_widget)
        self.right_top_layout.addWidget(self.nodes_ui_button, alignment=Qt.AlignCenter)
        self.nodes_ui_button.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"; height: '
                                           '30px; width: 140px')
        self.nodes_ui_button.clicked.connect(self.show_nodes_menu)

        # 创建右上方Edges UI按钮
        self.edges_ui_button = QPushButton("Edges UI", self.right_top_widget)
        self.right_top_layout.addWidget(self.edges_ui_button, alignment=Qt.AlignCenter)
        self.edges_ui_button.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"; height: '
                                           '30px; width: 140px')
        self.edges_ui_button.clicked.connect(self.show_edges_menu)

        # 创建刷新refresh按钮
        self.refresh_button = QPushButton("Refresh", self.right_top_widget)
        self.right_top_layout.addWidget(self.refresh_button, alignment=Qt.AlignCenter)
        self.refresh_button.setStyleSheet('color: white; font-size: 20px; font-family: "Microsoft YaHei"; height: '
                                          '30px; width: 140px')
        self.refresh_button.clicked.connect(self.refresh)

        # 创建底部create按钮,用于新增node
        self.create_node_button = QPushButton("New node", self.bottom_button_widget)
        self.bottom_button_layout.addWidget(self.create_node_button, alignment=Qt.AlignCenter)
        self.create_node_button.setStyleSheet('color: white; font-size: 25px; font-family: "Microsoft YaHei"')
        self.create_node_button.clicked.connect(self.create_wireguard_node)

        # 创建底部update按钮,用于修改node
        self.update_node_button = QPushButton("Update node", self.bottom_button_widget)
        self.bottom_button_layout.addWidget(self.update_node_button, alignment=Qt.AlignCenter)
        self.update_node_button.setStyleSheet('color: white; font-size: 25px; font-family: "Microsoft YaHei"')
        self.update_node_button.clicked.connect(self.update_wireguard_node)

        # 创建底部delete按钮,用于删除node
        self.delete_node_button = QPushButton("Delete node", self.bottom_button_widget)
        self.bottom_button_layout.addWidget(self.delete_node_button, alignment=Qt.AlignCenter)
        self.delete_node_button.setStyleSheet('color: white; font-size: 25px; font-family: "Microsoft YaHei"')
        self.delete_node_button.clicked.connect(self.delete_wireguard_node)

        # 创建底部create_link按钮,用于生成边链接
        self.create_link_button = QPushButton("Generate link", self.bottom_button_widget)
        self.bottom_button_layout.addWidget(self.create_link_button, alignment=Qt.AlignCenter)
        self.create_link_button.setStyleSheet('color: white; font-size: 25px; font-family: "Microsoft YaHei"')
        self.create_link_button.clicked.connect(self.create_link)

        # 创建底部generate config按钮,用于导入导出
        self.gen_conf_button = QPushButton("Generate conf", self.bottom_button_widget)
        self.bottom_button_layout.addWidget(self.gen_conf_button, alignment=Qt.AlignCenter)
        self.gen_conf_button.setStyleSheet('color: white; font-size: 25px; font-family: "Microsoft YaHei"')
        self.gen_conf_button.clicked.connect(self.generate_config)

        # 创建底部logout按钮,用于登出（红色）
        self.logout_button = QPushButton("Logout", self.bottom_button_widget)
        self.bottom_button_layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)
        self.logout_button.setStyleSheet('color: red; font-size: 20px; font-family: "Microsoft YaHei"')
        self.logout_button.clicked.connect(self.logout)

        # 将所有按钮统一设置为圆角，且宽度相同
        self.gen_conf_button.setFixedSize(220, 50)
        self.create_node_button.setFixedSize(220, 50)
        self.update_node_button.setFixedSize(220, 50)
        self.delete_node_button.setFixedSize(220, 50)
        self.create_link_button.setFixedSize(220, 50)
        self.logout_button.setFixedSize(220, 50)
        self.create_node_button.setStyleSheet('border-radius: 10px')
        self.update_node_button.setStyleSheet('border-radius: 10px')
        self.delete_node_button.setStyleSheet('border-radius: 10px')
        self.create_link_button.setStyleSheet('border-radius: 10px')
        self.gen_conf_button.setStyleSheet('border-radius: 10px')
        self.logout_button.setStyleSheet('border-radius: 10px; color:#c75450;border:2px solid #c75450')

        # self.show_config()
        self.init_network()
        self.simple_show_graph()
        self.change_graph_html()
        # self.show_filter_menu()

    def init_network(self):
        # 创建一个network
        self.nt = Network(height="1160px", width="100%", bgcolor="#222222", font_color="white", filter_menu=False)
        nx_graph = nx.florentine_families_graph()
        nx_graph.add_node(1, size=20, label='Jayson', title='罗振声', group=1)
        nx_graph.add_node(2, size=25, label='Billy', title='杨濛', group=1)
        nx_graph.add_node(3, size=15, label='Katherine', title='胡欣扬', group=1)
        nx_graph.add_edge(1, 2, weight=1.5, color='white')
        nx_graph.add_edge(1, 3, weight=1.5, color='green')
        nx_graph.add_edge(2, 3, weight=1.5, color='blue')
        nx_graph.add_node(4, size=10, label='Lonely', title='Lonely', group=2)

        '''此处使用networkx，An easy way to visualize and construct pyvis networks is to use Networkx and use pyvis’s 
        built-in networkx helper method to translate the graph. Note that the Networkx node properties with the same 
        names as those consumed by pyvis (e.g., ) are translated directly to the correspondingly-named pyvis node 
        attributes '''

        # 将pyvis的network转换为networkx的graph
        self.nt.from_nx(nx_graph)

    # 把配置文件以可点击的方式展示在左侧file栏
    def conf1_button_clicked(self):
        self.bottom_line.setText("2021210414")
        self.bottom_line1.setText("Config file 1")
        self.bottom_line2.setText("JaysonLuo")
        self.bottom_line3.setText("JaysonLuo, BillyYang, KatherineHu")
        self.bottom_line4.setText("eaf032g231nh")

    def conf2_button_clicked(self):
        self.bottom_line.setText("2021211329")
        self.bottom_line1.setText("Config file 2")
        self.bottom_line2.setText("BillyYang")
        self.bottom_line3.setText("JaysonLuo, BillyYang, KatherineHu, KayleeWang")
        self.bottom_line4.setText("ure864g458hf")

    def conf3_button_clicked(self):
        self.bottom_line.setText("2021211837")
        self.bottom_line1.setText("Config file 3")
        self.bottom_line2.setText("KatherineHu")
        self.bottom_line3.setText("JaysonLuo, BillyYang, KatherineHu, KayleeWang, Lonely")
        self.bottom_line4.setText("jgk984gjgk4")

    # 保存对图展示模式的修改
    def change_graph_html(self):
        self.nt.write_html("nx.html", open_browser=False)

    def init_show_graph(self):
        """load图的路径，不涉及展示"""
        url = QUrl(QFileInfo("./nx.html").absoluteFilePath())
        self.graph_view.load(url)

    # 最普通的展示图
    def simple_show_graph(self):
        """展示最基础的图，不涉及任何附加功能"""
        self.init_show_graph()
        self.graph_view.show()

    # 可以自定义图的物理属性的展示图
    def phy_changeable_show_graph(self):
        """展示可以自定义物理属性的图，侧边栏可以自定义physics属性"""
        self.init_show_graph()
        # 显示物理栏
        self.show_physics_menu()
        self.graph_view.show()

    # 可以自定义图的节点属性的展示图
    def node_changeable_show_graph(self):
        """展示可以自定义节点属性的图，侧边栏可以自定义nodes属性"""
        self.init_show_graph()
        # 显示节点栏
        self.show_nodes_menu()
        self.graph_view.show()

    # 可以自定义边的属性的展示图
    def edge_changeable_show_graph(self):
        """展示可以自定义边属性的图，侧边栏可以自定义edges属性"""
        self.init_show_graph()
        # 显示边栏
        self.show_edges_menu()
        self.graph_view.show()

    # 展示顶部filter搜索框
    def show_filter_menu(self):
        """展示顶部过滤搜索框，图的一个子功能"""
        self.nt.filter_menu = True
        self.change_graph_html()
        self.graph_view.reload()

    # 展示顶部select搜索框
    def show_select_menu(self):
        """展示顶部select搜索框，图的一个子功能"""
        self.nt.select_menu = True
        self.change_graph_html()
        self.graph_view.reload()

    # 展示侧边物理搜索框
    def show_physics_menu(self):
        """展示侧边physics修改栏，图的一个子功能"""
        # 更改network宽度使得能让侧边栏显示在右侧
        # TODO:需要调整
        self.nt.height = '500px'
        self.nt.show_buttons(filter_=['physics'])
        self.change_graph_html()
        self.graph_view.reload()

    # 展示侧边node自定义框
    def show_nodes_menu(self):
        """展示侧边nodes修改栏，图的一个子功能"""
        # 更改network宽度使得能让侧边栏显示在右侧
        self.nt.height = '500px'
        # 设置网nt的布局为水平
        self.nt.show_buttons(filter_=['nodes'])
        self.change_graph_html()
        self.graph_view.reload()

    # 展示侧边edge自定义框
    def show_edges_menu(self):
        """展示侧边edges修改栏，图的一个子功能"""
        # 更改network宽度使得能让侧边栏显示在右侧
        self.nt.height = '500px'
        self.nt.show_buttons(filter_=['edges'])
        self.change_graph_html()
        self.graph_view.reload()

    def refresh(self):
        # 恢复原始的network
        self.nt.height = '1160px'
        # 隐藏所有的侧边栏
        self.nt.show_buttons(filter_=[' '])
        self.nt.filter_menu = False
        self.change_graph_html()
        self.graph_view.reload()

    def get_network_info(self):
        # TODO: 在此处编写获取该用户网络信息的代码
        session.list = session.config_server.get_network_object(session.user.uuid)
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

    def create_link(self):
        # TODO: 在此处编写生成边链接的代码
        pass

    def logout(self):
        # TODO: 在此处编写登出的代码
        # logout_response = config_server.user_logout_request(session.user.uuid)
        username = session.user
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
        signup_response = session.config_server.user_signup_request(username, cleartext_password)
        if not signup_response[0]:
            print(signup_response[1])
            return
        else:
            print('You have signed up successfully! Now lets get started!')

class ForgetPasswordWindow(ChildDialogUi):
    def __init__(self):
        super().__init__('找回密码')

        self.setWindowTitle('Get your password back')
        self.setGeometry(1100, 750, 800, 500)

        passwd_recovery_layout = self.layout()

        sign_up_label = self.label
        sign_up_label.setStyleSheet('font-size: 30px; font-weight: bold; color: white')
        passwd_recovery_layout.addWidget(sign_up_label, 0, 0, 1, 0)
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
        # 退出登录
        # session.config_server.user_logout_request(username)
        # self.close()


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

    # app1代表登录窗口，app2代表主窗口，当登录窗口关闭时，交接控制权
    if app.exec_() == 0:
        app2 = QApplication(sys.argv)
        window2 = MainWindow()
        apply_stylesheet(app2, theme='dark_teal.xml', invert_secondary=True, extra=extra)
        window2.show()
        sys.exit(app2.exec_())
