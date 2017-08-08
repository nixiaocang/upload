#!/usr/bin/env python
# -*- coding:utf-8 -*-

from handler.base_handler import BaseHandler
from model.blog import Blog
from model.comment import Comment


class CommentHandler(BaseHandler):

    def do_action(self):
        args = self.get_args([
            ('text_id', str, None),
            ('email', str, None),
            ('subject', str, None),
            ('comment', str, None),
        ])
        text_id = args.get('text_id')
        chelper = Comment()
        chelper.create(args)
        comments = Comment().get_all(text_id)
        res = Blog().get_one(text_id)
        res['comment'] = comments
        self.result = res
        return True
