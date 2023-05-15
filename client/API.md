# 客户端业务逻辑-底层接口
## Initiation部分
- client-network-**configserver**
  > 建立与服务器的连接,ip,port
## UI部分
### Login
- client-main-**login**
  > 包含发送usr_name,usr_pwd,usr_type到服务器
  - client-main-**wait_for_response**
    > 请求server验证usr_name,usr_pwd,usr_type,并且用一个线程等待/接收response
      - ui-**CliWindow** 
        > 通过response判断是否验证成功，成功则进入CliWindow 

- client-main-**sign_up**
  > 点击sign_up，进入注册界面
  - ui-sign_up
    
    > 输入usr_name,usr_pwd,usr_type等信息
    > 通过（network-sign_up）发送到服务器
    > 服务器验证成功后，返回response
    > 通过response判断是否注册成功，成功则进入CliWindow
- client-main-**forget_pwd**
  > 点击forget_pwd，进入忘记密码界面
  - ui-**forget_pwd**
    > 输入usr_name,usr_type等信息  
    通过（network-forget_pwd）发送到服务器  
    服务器验证成功后，返回response  
    通过response判断是否验证成功，成功则进入CliWindow
### CliWindow
- client-network-**get_all_node**
  > 请求server发送格式化的（json）消息，包含node信息
  > node向json的格式化由服务器完成，先通过数据库（server-database）获取wg_object结点信息
  > 再通过（core-wg_object_parser）解析
- client-network-**show_graph**
  > 将json格式的node信息用可视化网状图显示
- client-network-**show_node**
  > 在右侧click任意一个node，显示该node的详细信息（ip,public_key,etc）
  > 以输入框的形式展现，通过判断是否admin，决定是否有权限在输入框直接修改
  > - 通过（network-update_node）将修改后的信息发送到server
- client-network-**generate_config_file**
  > click生成配置文件，调用了core-config_parser
