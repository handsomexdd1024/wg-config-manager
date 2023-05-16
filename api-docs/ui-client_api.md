# 用户界面-客户端核心接口文档

20230516版本

> 我的想法是，ui不要调用main之外的任何模块，所有功能都由main来包装一次

## Login
#### client-main-`login`

以给定`username`和`cleartext_password`发送到服务器

- 返回值：认证状态信息
- *得到的`session_token`由client-main保存*

#### client-main-`signup`

以给定`username`和`cleartext_password`向服务器发送注册信息

- 返回值：注册状态信息

#### client-main-`passwd_recovery`

以给定username请求找回密码

- *内部实现方式和具体步骤待定*

## CliWindow
#### client-main-`get_user_config_list`

获得用户信息，包括其管理/参与的配置文件名称和uuid等信息

> 预计可以展示在某一侧？比如登录之后一个界面展示配置文件信息，进入之后想要切换配置文件就从左侧点一下别的配置文件条切换什么的

#### client-main-`get_wireguard_object`

根据uuid请求wireguard_object（三种类型）

> 我后面会修改一下类继承关系，让WireguardObject成为WireguardNode, WireguardEdge, WireguardObject的父类，这样可以通过统一接口加载~~, 所以类型判断就留给client-main来做吧~~

#### client-main-`show_graph`

将json格式的node信息用可视化网状图显示

> 按照高内聚低耦合原则，我觉得client只应当负责返回WireguardNetwork object, 剩下在ui里面展示的细节，比如节点和边的位置和颜色，应该是ui模块自己处理的, 所以这个api是否保留有待商榷~~不要什么东西都塞给客户端后台啊~~

#### client-main-`get_node_information`

获得该节点信息

> 其实在get_wireguard_network这里就已经把所有节点以object的形式传递进去了，直接在数组里一个一个处理即可

#### client-main-`gen_wg_config`

根据给定的`format`, `network_uuid`和`node_uuid`生成配置文件信息

- *`format`会有wg格式wg-quick格式，前者适用于unix的wg, 后者适用于wg-quick和wireguard for windows等工具*

