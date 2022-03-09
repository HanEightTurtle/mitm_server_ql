
import mitmproxy.http
from .utils import *

class leafxcy_JavaScript_txs(object):
    def __init__(self,child_conn,temp_folder='temp'):
        # app
        self.app = '淘小说'
        # result of capture
        self.res = {
            'txsCookie':''
        }
        # ini
        self.count = 0
        self.table = {}
        self.toml_path = f'{temp_folder}/{self.app}.toml'
        self.child_conn = child_conn

    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 
        if self.count == 0:
            if any( [url in str(flow.request.pretty_url) for url in ['itaoxiaoshuo','taoyuewenhua'] ] ):
                body = data_str_to_dict(flow.request.get_text())
                if set(['token','uid']) < set(body.keys()):
                    self.res['txsCookie'] = f"{body.get('token')}&{body.get('uid')}"
            # check res and save
            if all(self.res.values()):
                self.table[self.app] = [self.res]
                self.count = 1
                sendlog(self.child_conn,f'{self.app} success!'+'&&&'+dict2conf(self.res))
                save_toml(self.table,self.toml_path)
                   