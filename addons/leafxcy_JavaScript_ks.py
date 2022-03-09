
import mitmproxy.http
from .utils import *
import re

class leafxcy_JavaScript_ks(object):
    def __init__(self,child_conn,temp_folder='temp'):
        # app
        self.app = '快手'
        # result of capture
        self.res = {
            'ksCookie':''
        }
        # ini
        self.count = 0
        self.table = {}
        self.toml_path = f'{temp_folder}/{self.app}.toml'
        self.child_conn = child_conn

    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 
        if self.count == 0:
            if any( [re.search(pattern,str(flow.request.pretty_url)) for pattern in ['api.kuaisho.*?\.com','open.kuaisho.*?\.com'] ] ):
                params = url2dict(str(flow.request.pretty_url))
                if params:
                    if set(['kuaishou.api_st','did']) < set(params.keys()):
                        self.res['ksCookie'] = f"kuaishou.api_st={params.get('kuaishou.api_st')}; did={params.get('did')};"
                else:
                    body = data_str_to_dict(flow.request.get_text())
                    if set(['kuaishou.api_st','did']) < set(body.keys()):
                        self.res['ksCookie'] = f"kuaishou.api_st={body.get('kuaishou.api_st')}; did={body.get('did')};"
            # check res and save
            if all(self.res.values()):
                self.table[self.app] = [self.res]
                self.count = 1
                sendlog(self.child_conn,f'{self.app} success!'+'&&&'+dict2conf(self.res))
                save_toml(self.table,self.toml_path)
