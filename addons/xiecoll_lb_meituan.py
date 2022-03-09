
import mitmproxy.http
from .utils import *

class xiecoll_lb_meituan(object):
    def __init__(self,child_conn,temp_folder='temp'):
        # app
        self.app = '美团'
        # result of capture
        self.res = {
            'mtTk':''
        }
        # ini
        self.count = 0
        self.table = {}
        self.toml_path = f'{temp_folder}/{self.app}.toml'
        self.child_conn = child_conn

    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 
        if self.count == 0:
            if any( [flow.request.pretty_url.startswith(item) for item in ['http://hreport.meituan.com'] ] ):
                cookies = dict(flow.request.cookies)
                if 'mt_c_token' in cookies.keys():
                    self.res['mtTk'] = cookies.get('mt_c_token')
            # check res and save
            if all(self.res.values()):
                self.table[self.app] = [self.res]
                self.count = 1
                sendlog(self.child_conn,f'{self.app} success!'+'&&&'+dict2conf(self.res))
                save_toml(self.table,self.toml_path)
                   