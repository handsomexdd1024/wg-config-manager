# `数据库设计：`
# `一、wireguard.database:`
## 1.schema WireguardNode:

### (1)table NodeType(Enum和三个int之间的转换)：
- PEER = 0（int）
- ROUTER = 1（int）
- ROUTED = 2（int）

### (2)table EndpointType(Enum和三个int之间的转换):
- IPV4 = 0（int）
- IPV6 = 1（int）
- DOMAIN = 2（int）

### (3)table self
- 包含：
- identifier: uuid.UUID **_(PRIMARY KEY)_**
- owner: uuid.UUID,
- name（string）， 
- address_list:(实现list与string之间转换）
list[IPv4Address | IPv4Network | IPv6Address | IPv6Network | None]
- admin_approval: bool
- node_type（PEER与string之间转换）
- private_key: （string） 
- public_key: （string） 
- endpoint: string（两数之间用逗号隔开）（endpoint: (str, int) | None = None）


## 2.schema WireguardObject
### (1)table ObjectType(Enum和四个int之间的转换)：
- UNSPECIFIED = 0 （int）
- NODE = 1 （int）
- CONNECTION = 2 （int）
- NETWORK = 3（int）
### (2)table self
- identifier: uuid.UUID,**_(PRIMARY KEY)_**
- **_object_type_**
## 3.schema WireguardConnection(ABC)
### (1)table WireguardConnection.self
- dentifier:uuid(UUID与string类型的转换)**_(PRIMARY KEY)_**
- peers:uuid,uuid(UUID与string类型的转换：将其转换为一个string，其中以空格隔开)（peers: (uuid.UUID, uuid.UUID),）
- preshared_key: string | None

## 4.schema WireguardNetwork
### (1)table WireguardNetwork.self
- dentifier:uuid(UUID与string类型的转换)**_(PRIMARY KEY)_**
- name: string 
- node_uuid_list:WireguardNode(list与string类型转换)
- connection_uuid_list:WireguardConnection(list与string类型转换)


# `二、user.database`
## 1.schema user_self:
### (1)table user_self
- identifier(uuid与string类型的转换) **_(PRIMARY KEY)_**
- name（string）
- hashed_password（bytes与string转换） 
- salt（bytes与string转换）

# `三、WireguardConfig.database`
## 1.schema WireguardConfig:
- identifier: uuid.UUID **_(PRIMARY KEY)_**
- owner: uuid.UUID,
- name（string）， 
- address_list:(实现list与string之间转换）
- network_uuid: UUID
- 
# `四、massage.database`
## 1.schema StandardResponse:
### (1)table StandardResponse_self
- code: int
- message: string
- content: （bytes与string转换）

## 2.schema NetworkModification
### (1)table NetworkModification_Action:
- CREATE = 0(int)
- DELETE = 1(int)
- UPDATE = 2(int)
### (2)table NetworkModification_self:
- self.action = None(string)
- self.content = None(string)


#数据库与py之间的类型转换
#### 一、Enum和int之间的转换
- 1.将枚举类型转换为整数： 可以使用枚举成员的值（value）属性来获取枚举成员的整数值
```python
NodeType = NodeType.PEER
NodeType_value = NodeType.value  # 获取枚举成员的整数值
```
- 2.将整数转换为枚举类型： 要将整数转换为枚举类型，可以使用枚举类型的类方法——EnumClass(int_value)，其中EnumClass是枚举类型的类名，int_value是要转换的整数值
```python
NodeType = NodeType(int_PEER)  # 将整数转换为枚举类型
```

#### 二、list与string之间转换：
在Python中，可以使用以下方法将列表（list）与字符串（string）之间进行转换：

- 1.将列表转换为字符串：
   使用`join()`方法将列表中的元素连接成一个字符串。`join()`方法接受一个可迭代对象作为参数，并将其中的元素连接成一个字符串。
   ```python
   # 将列表转换为字符串
   address_list = ' '.join(address_list)
   ```

   在这个示例中，使用空格作为分隔符，将列表`my_list`中的元素连接成一个字符串。

- 2.将字符串转换为列表：
   使用`split()`方法将字符串拆分成多个子字符串，并返回一个列表。`split()`方法接受一个分隔符作为参数，用于确定字符串拆分的位置。示例如下：

   ```python
   # 将字符串转换为列表
   address_list = address_list.split()
   ```

  使用空格作为分隔符，将字符串`address_list `拆分成多个子字符串，并返回一个列表。

#### 三、PEER与string之间转换:
用pickle模块将Python对象（包括字符串）与PEER（Python的序列化格式）之间进行相互转换。
- 1.把字符串转化为PEER：
```python
import pickle
node_type = pickle.dumps(node_type_string)# 将字符串转换为PEER
```
- 2.把PEER转化为字符串：
```python
import pickle
node_type_string = pickle.loads(node_type)
```
#### 四、UUID与string之间的转换:
在Python中，可以使用`uuid`模块来进行UUID和字符串类型之间的转换。

1. 将UUID转换为字符串：
   可以使用UUID对象的`str()`函数或`str(uuid_obj)`方法将UUID转换为字符串类型。

   ```python
   import uuid

   # 生成UUID
   uuid_obj = uuid.uuid4()

   # 将UUID转换为字符串
   uuid_str = str(uuid_obj)
   print(uuid_str)
   ```

   在这个示例中，使用`str()`函数将UUID对象`uuid_obj`转换为字符串类型。

2. 将字符串转换为UUID：
   可以使用`uuid.UUID()`函数将字符串转换为UUID对象。

   ```python
   import uuid

   # 将字符串转换为UUID
   uuid_str = 'c8ca1d32-8ee7-4a8b-9d7f-870f813b292a'
   uuid_obj = uuid.UUID(uuid_str)
   print(uuid_obj)  # 输出: UUID('c8ca1d32-8ee7-4a8b-9d7f-870f813b292a')
   ```
注：转换过程中要确保UUID字符串的格式正确，符合UUID的标准格式。否则，在转换过程中可能会引发`ValueError`异常。

#### 五、bytes与string转换之间的转换:
- 方法一：可以使用编码（encoding）和解码（decoding）的方式将字节串（bytes）和字符串（string）类型相互转换。

1. 将字节串转换为字符串：
   使用字节串对象的`decode()`方法将其解码为字符串。需要指定合适的字符编码（如UTF-8）来进行解码。示例代码如下：

   ```python
   # 将字节串转换为字符串
   byte_data = b'Hello, World!'
   str_data = byte_data.decode('utf-8')
   print(str_data)  # 输出: 'Hello, World!'
   ```

   在这个示例中，使用字节串对象`byte_data`的`decode()`方法将其解码为字符串类型。

2. 将字符串转换为字节串：
   使用字符串对象的`encode()`方法将其编码为字节串。同样需要指定字符编码来进行编码。示例代码如下：

   ```python
   # 将字符串转换为字节串
   str_data = 'Hello, World!'
   byte_data = str_data.encode('utf-8')
   print(byte_data)  # 输出: b'Hello, World!'
   ```

   在这个示例中，使用字符串对象`str_data`的`encode()`方法将其编码为字节串类型。

！！！需要注意的是，编码和解码使用相同的字符编码才能保持正确的转换。常见的字符编码包括UTF-8、UTF-16、ASCII等。如果在解码过程中使用了错误的编码，会引发`UnicodeDecodeError`异常。

- 方法二：可以通过字节串的构造函数`bytes()`来创建字节串对象，通过字符串的构造函数`str()`来创建字符串对象。示例代码如下：

```python
# 将字节串转换为字符串
byte_data = b'Hello, World!'
str_data = str(byte_data, 'utf-8')
print(str_data)  # 输出: 'Hello, World!'

# 将字符串转换为字节串
str_data = 'Hello, World!'
byte_data = bytes(str_data, 'utf-8')
print(byte_data)  # 输出: b'Hello, World!'
```

这种方式也可以实现字节串和字符串之间的转换。

综上所述，可以使用`decode()`方法将字节串解码为字符串，使用`encode()`方法将字符串编码为字节串，或使用构造函数`str()`和`bytes()`进行转换。