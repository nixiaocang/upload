#!/usr/bin/env python
# -*- coding:utf-8 -*-

from opends.sdk import Client


class CreateTb(object):
    def __init__(self, token):
        self.opends = Client(token)

    def create_ds(self):
        ds_name = self.opends.create_ds(u'快商通')
        print ds_name

    def create_one(self):
        ds = self.opends.get_ds(u'快商通')
        name = 'kuaishangtong'
        title = '消息记录'
        schema = [
            {"comment": "", "name": "recId", "type": "string", "title": "会话ID"},
            {"comment": "", "name": "visitorId", "type": "string", "title": "访客ID"},
            {"comment": "", "name": "visitorName", "type": "string", "title": "访客名称"},
            {"comment": "", "name": "curEnterTime", "type": "date", "title": "本次访问时间"},
            {"comment": "", "name": "firstVisitTime", "type": "date", "title": "首次访问时间"},
            {"comment": "", "name": "curFirstViewPage", "type": "string", "title": "本次最初访问网页"},
            {"comment": "", "name": "preVisitTime", "type": "date", "title": "上次访问时间"},
            {"comment": "", "name": "totalVisitTime", "type": "number", "title": "累计来访次数"},
            {"comment": "", "name": "firstCsId", "type": "string", "title": "初次接待客服"},
            {"comment": "", "name": "diaPage", "type": "string", "title": "发起对话网址"},
            {"comment": "", "name": "joinCsIds", "type": "string", "title": "参与接待客服"},
            {"comment": "", "name": "curStayTime", "type": "date", "title": "访客停留时间"},
            {"comment": "", "name": "sourceIp", "type": "string", "title": "访客来源IP"},
            {"comment": "", "name": "sourceIpInfo", "type": "string", "title": "网络接入商"},
            {"comment": "", "name": "sourceUrl", "type": "string", "title": "来源网页"},
            {"comment": "", "name": "sourceType", "type": "string", "title": "来源类型"},
            {"comment": "", "name": "searchEngine", "type": "string", "title": "搜索引擎"},
            {"comment": "", "name": "keyword", "type": "string", "title": "搜索关键词"},
            {"comment": "", "name": "requestType", "type": "string", "title": "对话请求方式"},
            {"comment": "", "name": "endType", "type": "string", "title": "对话结束方式"},
            {"comment": "", "name": "diaStartTime", "type": "date", "title": "开始对话时间"},
            {"comment": "", "name": "diaEndTime", "type": "date", "title": "结束对话时间"},
            {"comment": "", "name": "dialogType", "type": "string", "title": "对话类型"},
            {"comment": "", "name": "terminalType", "type": "string", "title": "终端类型"},
            {"comment": "", "name": "visitorSendNum", "type": "number", "title": "访客发送消息数"},
            {"comment": "", "name": "csSendNum", "type": "number", "title": "客服发送消息数"},
            {"comment": "", "name": "ds_channel", "type": "string", "title": "数据源渠道"},
        ]
        uniq_key = ['recId', 'visitorId', 'curEnterTime', 'diaStartTime']
        tbname = ds.create_table(name, schema, uniq_key, title)
        print tbname

    def create_two(self):
        ds = self.opends.get_ds(u'快商通')
        name = 'vcard'
        title = '名片记录'
        schema = [
            {"comment": "", "name": "visitorId", "type": "string", "title": "访客ID"},
            {"comment": "", "name": "linkman", "type": "string", "title": "联系人名称"},
            {"comment": "", "name": "compName", "type": "string", "title": "公司名称"},
            {"comment": "", "name": "webUrl", "type": "string", "title": "网址"},
            {"comment": "", "name": "mobile", "type": "string", "title": "手机"},
            {"comment": "", "name": "phone", "type": "string", "title": "电话"},
            {"comment": "", "name": "qq", "type": "string", "title": "QQ"},
            {"comment": "", "name": "msn", "type": "string", "title": "MSN/微信"},
            {"comment": "", "name": "email", "type": "string", "title": "邮箱"},
            {"comment": "", "name": "address", "type": "string", "title": "地址"},
            {"comment": "", "name": "birthday", "type": "date", "title": "生日"},
            {"comment": "", "name": "remark", "type": "string", "title": "备注说明"},
            {"comment": "", "name": "loginName", "type": "string", "title": "添加客服（登录名）"},
            {"comment": "", "name": "addtime", "type": "date", "title": "添加时间"},
            {"comment": "", "name": "lastChangeTime", "type": "date", "title": "最后修改时间"},
            {"comment": "", "name": "ds_channel", "type": "string", "title": "数据源渠道"},
        ]
        uniq_key = []
        tbname = ds.create_table(name, schema, uniq_key, title)


