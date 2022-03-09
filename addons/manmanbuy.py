
import mitmproxy.http
from .utils import *

class manmanbuy(object):
    def __init__(self,child_conn,temp_folder='temp'):
        # app
        self.app = '慢慢买'
        # result of capture
        self.res = {
            'cookie':'',
            'user-agent':'',
            'login_body':'',
            'checkin_body':''
        }
        # ini
        self.count = 0
        self.table = {}
        self.toml_path = f'{temp_folder}/{self.app}.toml'
        self.child_conn = child_conn

    def request(self,flow: mitmproxy.http.HTTPFlow):
        # login
        if self.count == 0:
            if flow.request.pretty_url=='https://apph5.manmanbuy.com/taolijin/login.aspx' and flow.request.method=='POST':
                body = data_str_to_dict(flow.request.get_text())
                if body['action']=='newtokenlogin':
                    headers = {k.lower():v for k,v in dict(flow.request.headers).items()}  
                    self.res['cookie'] = headers['cookie']
                    self.res['user-agent'] = headers['user-agent']
                    self.res['login_body'] = flow.request.get_text()
            # checkin
            if flow.request.pretty_url=='https://apph5.manmanbuy.com/renwu/index.aspx' and flow.request.method=='POST':
                body = data_str_to_dict(flow.request.get_text())
                if body['action']=='get_user_info':
                    self.res['checkin_body'] = flow.request.get_text()
            # check res and save
            if all(self.res.values()):
                self.table[self.app] = [self.res]
                self.count = 1
                sendlog(self.child_conn,f'{self.app} success!'+'&&&'+dict2conf(self.res))
                save_toml(self.table,self.toml_path)
                   