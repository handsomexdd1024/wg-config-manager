# 用户界面-客户端核心接口文档
### Login
client-**login**

以给定username和cleartext发送到服务器

- 返回：认证状态信息

### CliWindow
client-**get_user_info**

获得用户信息，包括其拥有/参与的配置文件id

client-**get_wireguard_network**

根据uuid请求WireguardNetwork object

client-**show_graph**

将json格式的node信息用可视化网状图显示

> 小电动：我觉得client只应当负责返回WireguardNetwork object, 剩下在ui里面展示的细节，比如节点和边的位置和颜色，应该是ui模块自己处理的, 所以这个api是否保留有待商榷~~不要什么东西都塞给客户端后台啊~~

client-**get_node_information**

获得该节点信息

> 其实在get_wireguard_network这里就已经把所有节点以object的形式传递进去了，直接在数组里一个一个处理即可

core-**ConfigParser**

click生成配置文件
