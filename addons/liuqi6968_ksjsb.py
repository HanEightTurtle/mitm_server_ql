
import mitmproxy.http
from .utils import *

class liuqi6968_ksjsb(object):
    def __init__(self,child_conn,temp_folder='temp'):
        # app
        self.app = '快手极速版'
        # result of capture
        self.res = {
            'kshd':''
        }
        # ini
        self.count = 0
        self.table = {}
        self.toml_path = f'{temp_folder}/{self.app}.toml'
        self.child_conn = child_conn

    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 
        if self.count == 0:
            if flow.request.pretty_url.startswith('https://nebula.kuaishou.com/') and flow.request.method=='GET':
                cookies = dict(flow.request.cookies)
                if 'kuaishou.api_st' in cookies.keys():
                    self.res['kshd'] = ck_dict_to_str(cookies)
            # check res and save
            if all(self.res.values()):
                self.table[self.app] = [self.res]
                self.count = 1
                sendlog(self.child_conn,f'{self.app} success!'+'&&&'+dict2conf(self.res))
                save_toml(self.table,self.toml_path)
                   