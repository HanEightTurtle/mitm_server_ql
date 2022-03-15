
import mitmproxy.http
from .utils import *
import json

class leafxcy_JavaScript_ddgy(object):
    def __init__(self,child_conn,temp_folder='temp'):
        # app
        self.app = '滴滴果园leafxcy'
        # result of capture
        self.res = {
            'ddgyToken':''
        }
        # ini
        self.count = 0
        self.table = {}
        self.toml_path = f'{temp_folder}/{self.app}.toml'
        self.child_conn = child_conn

    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 
        if self.count == 0:
            if any( [url in flow.request.pretty_host for url in ['game.xiaojukeji.com'] ] ):
                body = json.loads(flow.request.get_text())
                if set(['uid','token']) < set(body.keys()):
                    self.res['ddgyToken'] = f"{body.get('uid')}&{body.get('token')}"
            # check res and save
            if all(self.res.values()):
                self.table[self.app] = [self.res]
                self.count = 1
                sendlog(self.child_conn,f'{self.app} success!'+'&&&'+dict2conf(self.res))
                save_toml(self.table,self.toml_path)
