#!/usr/bin/env python
# -*- coding:utf-8 -*-

from handler.base_handler import BaseHandler
from model.blog import Blog
from model.comment import Comment


class ListHandler(BaseHandler):

    def do_action(self):
        args = self.get_args([
            ('user_id', str, None),
        ])
        user_id = args.get('user_id')
        res = Blog().get_list(user_id)
        for item in res:
            if 'ctime' in item:
                ctime = item['ctime']
                item['date']=ctime[:4] + '年' + ctime[5:7] + '月' + ctime[8:10] +'日'
            cres = Comment().get_all(item['text_id'])
            item['ccount'] = len(cres)
        self.result = res
        return True
