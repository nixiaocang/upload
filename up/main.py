# coding:utf-8
import os
import re
import json
from uploader import Uploader
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
static_path = '/Users/jiaoguofu/myproject/upload/file'
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

class UploadHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.upload(args,kwargs)
    
    def get(self, *args, **kwargs):
        self.upload(args,kwargs)

    def upload(self,*args, **kwargs):
        mimetype = 'application/json'
        result = {}
        action = self.get_argument('action')
        path = '/Users/jiaoguofu/Downloads/ueditor-1.4.3.3/dist/utf8-php/php/config.json'
        with open(path) as fp:
            try:
                CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
            except:
                CONFIG = {}
        if action == 'config':
            result = CONFIG
        elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
            if action == 'uploadimage':
                fieldName = CONFIG.get('imageFieldName')
                config = {
                    "pathFormat": CONFIG['imagePathFormat'],
                    "maxSize": CONFIG['imageMaxSize'],
                    "allowFiles": CONFIG['imageAllowFiles']
                }
            elif action == 'uploadvideo':
                fieldName = CONFIG.get('videoFieldName')
                config = {
                    "pathFormat": CONFIG['videoPathFormat'],
                    "maxSize": CONFIG['videoMaxSize'],
                    "allowFiles": CONFIG['videoAllowFiles']
                }
            else:
                fieldName = CONFIG.get('fileFieldName')
                config = {
                    "pathFormat": CONFIG['filePathFormat'],
                    "maxSize": CONFIG['fileMaxSize'],
                    "allowFiles": CONFIG['fileAllowFiles']
                }

            if fieldName in self.request.files:
                field = self.request.files[fieldName]
                for fieldsss in field:
                    uploader = Uploader(fieldsss, config, static_path)
                    result = uploader.getFileInfo()
                    break
            else:
                result['state'] = '上传接口出错'

        elif action in ('uploadscrawl'):
            # 涂鸦上传
            fieldName = CONFIG.get('scrawlFieldName')
            config = {
                "pathFormat": CONFIG.get('scrawlPathFormat'),
                "maxSize": CONFIG.get('scrawlMaxSize'),
                "allowFiles": CONFIG.get('scrawlAllowFiles'),
                "oriName": "scrawl.png"
            }
            if fieldName in self.request.form:
                field = self.request.form[fieldName]
                uploader = Uploader(field, config, static_path, 'base64')
                result = uploader.getFileInfo()
            else:
                result['state'] = '上传接口出错'

        elif action in ('catchimage'):
            config = {
                "pathFormat": CONFIG['catcherPathFormat'],
                "maxSize": CONFIG['catcherMaxSize'],
                "allowFiles": CONFIG['catcherAllowFiles'],
                "oriName": "remote.png"
            }
            fieldName = CONFIG['catcherFieldName']

            if fieldName in self.request.form:
                # 这里比较奇怪，远程抓图提交的表单名称不是这个
                source = []
            elif '%s[]' % fieldName in self.request.form:
                # 而是这个
                source = self.request.form.getlist('%s[]' % fieldName)

            _list = []
            for imgurl in source:
                uploader = Uploader(imgurl, config, static_path, 'remote')
                info = uploader.getFileInfo()
                _list.append({
                    'state': info['state'],
                    'url': info['url'],
                    'original': info['original'],
                    'source': imgurl,
                })

            result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
            result['list'] = _list

        else:
            result['state'] = '请求地址出错'

        result = json.dumps(result)

        if self.request.arguments.has_key("callback"):
            callback = self.get_argument('callback')
            if re.match(r'^[\w_]+$', callback):
                result = '%s(%s)' % (callback, result)
                mimetype = 'application/javascript'
            else:
                result = json.dumps({'state': 'callback参数不合法'})

        self.set_header('Content-Type', mimetype)
        self.set_header('Access-Control-Allow-Origin','*')
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With,X_Requested_With')
        self.write(result)
        self.finish()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler), (r"/ueditor/upload/", UploadHandler)], **{
        "static_path": os.path.join(os.path.dirname(__file__), "static")})
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
