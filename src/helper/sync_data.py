#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time
import datetime
from opends.sdk import Client
from pymongo import MongoClient
from util.config import Configuration

req_map = {'rt_v':"访客请求", "rt_c":"客服请求", "rt_ct":"本公司跨站点转接", "rt_ot":"跨公司转接"}
end_map = {"et_v_e":"访客主动结束","et_c_e":"客服主动结束","et_c_r":"客服拒绝对话","et_t_s":"跨站点转接转出","et_t_c":"跨公司转接转出","et_c_o":"客服网络断网","et_c_q":"客服退出系统","et_d_t":"对话状态超时"}
dialog_map = {"dt_v_ov":"仅访问网站","dt_v_nm":"访客无消息","dt_c_na":"客服未接受","dt_c_nm":"客服无消息","dt_d_o":"其他有效对话","dt_d_n":"一般对话","dt_d_g":"较好对话","dt_d_b":"更好/极佳对话"}
terminal_map = {"tt_pc":"电脑","tt_ppc":"平板电脑","tt_mb":"手机"}

class SyncData():
    def __init__(self, user_id, token):
        conf = Configuration()
        self.host = conf.get("mongo", "host")
        self.port = int(conf.get("mongo", "port"))
        self.user_id = user_id
        self.opends = Client(token)
        self.ds = self.opends.get_ds(u'快商通')
        self.tb = self.ds.get_table('kuaishangtong')
        #self.vtb = self.ds.get_table('vcard')
        self.vtb = self.ds.get_table('kst_test')
        self.conn = MongoClient(self.host, self.port)
        self.db = self.conn['jiaogf']
        self.yes = datetime.datetime.today() - datetime.timedelta(days=1)
        self.yesterday = datetime.datetime.strftime(self.yes,'%Y%m%d')

    def push_one(self):
        htable = 'hdata_%s' % self.yesterday
        hdata = self.db[htable]
        content = hdata.find({"user_id":self.user_id})
        fields = ['recId', 'visitorId', 'visitorName', 'curEnterTime', 'firstVisitTime', 'curFirstViewPage', 'preVisitTime', 'totalVisitTime', 'firstCsId',    'diaPage', 'joinCsIds', 'curStayTime', 'sourceIp', 'sourceIpInfo', 'sourceUrl', 'sourceType', 'searchEngine', 'keyword', 'diaStartTime', 'diaEndTime', 'visitorSendNum', 'csSendNum', 'requestType', 'endType', 'dialogType', 'terminalType', 'ds_channel']
        data = []
        count = 0
        for i in content:
            item = []
            data_list = self.deal_map(i)
            item = [i.get(k) for k in fields[:-5]]
            item += data_list
            data.append(item)
        self.tb.insert_data(fields, data)
        self.tb.commit()

    def push_two(self):
        vtable = 'vdata_%s' % self.yesterday
        vdata = self.db[vtable]
        content = vdata.find({"user_id":self.user_id})
        fields = ['visitorId', 'linkman', 'compName', 'webUrl', 'mobile', 'phone', 'qq', 'msn', 'email', 'address', 'birthday', 'remark', 'loginName', 'addtime', 'lastChangeTime', 'ds_channel']
        data = []
        for i in content:
            item = []
            item = [i.get(k) for k in fields[:-1]]
            item.append('快商通')
            data.append(item)
        self.vtb.insert_data(fields, data)
        self.vtb.commit()

    def deal_map(self, i):
        rk = i.get('requestType')
        if rk:
            rk = req_map.get(rk)
        ek = i.get('endType')
        if ek:
            ek = end_map.get(ek)
        dk = i.get('dialogType')
        if dk:
            dk = dialog_map.get(dk)
        tk = i.get('terminalType')
        if tk:
            tk = terminal_map.get(tk)
        data_list = [rk, ek, dk, tk, '快商通']
        return data_list

    def run(self):
        #self.push_one()
        #self.push_two()
        #self.ds.update_all()
        self.yesterday = datetime.datetime.strftime(datetime.datetime.today(),'%Y%m%d')
        vtable = 'vdata_%s' % self.yesterday
        print vtable
        vdata = self.db[vtable]
        content = vdata.find({"user_id":self.user_id})
        data = []
        fields = ['user_id', 'a']
        for i in content:
            print i
            item = []
            item = [i.get(k) for k in fields]
            data.append(item)
        fields = ['recId', 'visitorId']
        self.vtb.insert_data(fields, data)
        self.vtb.commit()

if __name__=='__main__':
    #token = 'd0aac2acfe27607964af34ca136c43eb'
    token = 'b3c8b796823b31f948401c3c07ae17c6'
    #token = '39c7c1007d207c642f32a408cddd61f1'
    client = SyncData(token)
    client.push_one()
    client.push_two()
    client.ds.update_all()
