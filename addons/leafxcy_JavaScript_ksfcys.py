
import mitmproxy.http
from .utils import *

class leafxcy_JavaScript_ksfcys(object):
    def __init__(self,child_conn,temp_folder='temp'):
        # app
        self.app = '康师傅畅饮社'
        # result of capture
        self.res = {
            'ksfcysToken':''
        }
        # ini
        self.count = 0
        self.table = {}
        self.toml_path = f'{temp_folder}/{self.app}.toml'
        self.child_conn = child_conn

    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 
        if self.count == 0:
            if flow.request.pretty_url.startswith('https://club.biqr.cn/'):
                headers = {k.lower():v for k,v in dict(flow.request.headers).items()}
                if 'token' in headers.keys():
                    self.res['ksfcysToken'] = headers.get('token')
            # check res and save
            if all(self.res.values()):
                self.table[self.app] = [self.res]
                self.count = 1
                sendlog(self.child_conn,f'{self.app} success!'+'&&&'+dict2conf(self.res))
                save_toml(self.table,self.toml_path)
                   