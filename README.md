# MyBlog
练手续作
### 框架
tornado
### 研发须知
> Python版本：2.7.x

基于conf/offline.conf 文件复制一份以自己的用户名命名的配置放到conf目录下，并修改端口，以防止重复。

**由于该服务用于接收数据，因此测试时需要联系运维人员开放相关端口**

启动服务:


```
source bin/env.sh   
python main.py  
```
新增配置，注意同步到app.conf文件中
依赖的所有第三方包需要添加到requirements.txt中。通过`pip install -r requirements.txt`安装依赖包

### 命名规范
Python代码规范：统一采用PEP8规范，请参考<https://www.python.org/dev/peps/pep-0008/>

统一采用utf-8编码，代码文件头部统一添加：


```
#!/usr/bin/python
# -*- coding: utf-8 -*-
```

### 部署信息

- 线下测试环境：http://127.0.0.1:19930
- 线上环境：暂未上线

### 关键设计

#### 项目结构说明

```
.
├── bin
├── conf
├── env.py
├── __init__.py
├── main.py
├── README.md
├── src
└── supervisord.conf
```
### API接口文档
接口基于http协议，所有的接口均支持GET和POST两种请求
