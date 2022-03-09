
import mitmproxy.http
from .utils import *

class xiecoll_lb_elm(object):
    def __init__(self,child_conn,temp_folder='temp'):
        # app
        self.app = '饿了么'
        # result of capture
        self.res = {
            'elmck':''
        }
        # ini
        self.count = 0
        self.table = {}
        self.toml_path = f'{temp_folder}/{self.app}.toml'
        self.child_conn = child_conn

    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 
        if self.count == 0:
            if any( [flow.request.pretty_url.startswith(item) for item in ['https://h5.ele.me/svip/task-list'] ] ):
                cookies = dict(flow.request.cookies)
                if set(['_tb_token_','cookie2']) < set(cookies.keys()):
                    self.res['elmck'] = ck_dict_to_str(cookies)
            # check res and save
            if all(self.res.values()):
                self.table[self.app] = [self.res]
                self.count = 1
                sendlog(self.child_conn,f'{self.app} success!'+'&&&'+dict2conf(self.res))
                save_toml(self.table,self.toml_path)
                   