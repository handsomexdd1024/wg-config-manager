# 客户端业务逻辑-底层接口
## UI
### Login
- client-main-**login**
  > 包含发送usr_name,usr_pwd,usr_type到服务器
  - client-main-**wait_for_response**
    > 请求server验证usr_name,usr_pwd,usr_type,并且用一个线程等待/接收response
    - client-main-**jump_to_cli_window**
      > 通过response判断是否验证成功，成功则进入CliWindow

- client-main-**jump_to_sign_up**
  > 点击sign_up，进入注册界面
  - ui-jump_to_sign_up
    > 输入usr_name,usr_pwd,usr_type等信息
    > 通过（network-sign_up）发送到服务器
    > 服务器验证成功后，返回response
    > 通过response判断是否注册成功，成功则进入CliWindow
- client-main-**jump_to_forget_password**
  > 点击进入忘记密码界面
  - ui-**forget_pwd**
    > 输入usr_name,usr_type等信息  
    通过（network-forget_pwd）发送到服务器  
    服务器验证成功后，返回response  
    通过response判断是否验证成功，成功则进入CliWindow
### CliWindow
- client-main-**get_network_info**
  > 请求server发送格式化的（json）消息，包含node信息
  > node向json的格式化由服务器完成，先通过数据库（server-database）获取wg_object结点信息
  > 再通过（core-wg_object_parser）解析
- client-main-**show_config**
  > 展示用户的配置文件
- client-main-**new_config**
  > 点击new_config，进入新建配置界面
- client-main-**show_graph**
  > 将json格式的node信息用可视化网状图显示
- client-main-**show_node**
  > 点击某个节点时，显示其信息
- client-main-**update_wireguard_node**
- client-main-**delete_wireguard_node**
- client-main-**create_wireguard_node**
- client-main-**generate_config**
  > click生成配置文件，调用了core-config_parser
- client-main-**logout**
  > 点击logout，退出登录
