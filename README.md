# 1、需求说明
## 1.1、不同FIX协议版本的支持
- 支持不同的FIX协议对FIX消息进行解析。

## 1.2、过滤支持
- 支持根据消息类型进行过滤，如管理类消息、心跳消息。
- 支持对common类的字段进行过滤。

## 1.3、扩展FIX协议的支持
- 支持对FIX协议的扩展，可以自定义字段。

## 1.4、文件上传支持
- 支持上传FIX消息日志文件，并对文件内的FIX消息进行解析。

# 2、模块接口


# 3、使用说明
## 3.1、配置文件说明
```buildoutcfg
[common]
HOST = 0.0.0.0
PORT = 8080

[fix]
FIX_DICT_PATH = FIX_Dict
STANDARD_FIX = FIX40, FIX41, FIX42, FIX43, FIX44, FIX50, FIXT11
CUSTOM_FIX = CICC_FIX42, UBS_FIX42
```
- HOST：服务端的主机IP。
- PORT：服务端的端口号。
- FIX_DICT_PATH：FIX字典的目录。
- STANDARD_FIX：定义支持的标准FIX协议版本，如FIX 4.0定义为FIX40，多个使用逗号分隔。
- CUSTOM_FIX：带自定义字段的扩展FIX协议版本，通常根据broker和FIX协议版本命名，如CICC的FIX 4.2扩展协议命名为CICC_FIX42，
多个使用逗号分隔。


