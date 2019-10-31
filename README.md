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

## 1.5、不同分隔符的支持
- 支持不同的分隔符作为FIX消息的分隔符，如逗号、分号、竖线、问号、SOH(0x01)、^A。

# 2、模块接口
## 2.1、config模块
- config模块是程序的配置文件解析模块，用于解析config.ini文件。

## 2.2、model.fix_xml_to_json模块
- fix_xml_to_json模块用于将XML格式的FIX协议字典转换为JSON格式的FIX协议字典。

## 2.3、model.fix_dict模块
- fix_dict模块用于根据FIX协议名称提供响应的FIX协议字典。

## 2.4、model.fix_message模块
- fix_message模块用于解析一条FIX消息。

## 2.5、model.fix_parser模块
- fix_parser模块是FIX协议消息的解析器，将FIX消息文本拆分为多条FIX消息进行解析。

## 2.6、server模块
- server模块是FIX协议消息解析服务的入口文件，基于Flask进行开发。

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


