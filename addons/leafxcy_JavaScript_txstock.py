
import mitmproxy.http
from .utils import *

class leafxcy_JavaScript_txstock(object):
    def __init__(self,child_conn,temp_folder='temp'):
        # app
        self.app = '腾讯自选股'
        # result of capture
        self.res = {
            'TxStockAppUrl':'',
            'TxStockAppHeader':'',
            'TxStockWxHeader':''
        }
        # ini
        self.count = 0
        self.table = {}
        self.toml_path = f'{temp_folder}/{self.app}.toml'
        self.child_conn = child_conn

    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 
        if self.count == 0:
            if any( [flow.request.pretty_url.startswith(url) for url in ['https://wzq.tenpay.com/cgi-bin/activity_task_daily.fcgi?'] ] ):
                headers_dict = dict(flow.request.headers)
                cookies_dict = dict(flow.request.cookies)
                if 'qlappid' not in cookies_dict.keys():
                    self.res['TxStockAppUrl'] = flow.request.pretty_url
                    sendlog(self.child_conn,f'{self.app} TxStockAppUrl!'+'&&&'+self.res['TxStockAppUrl'])
                    self.res['TxStockAppHeader'] = str(headers_dict)
                    sendlog(self.child_conn,f'{self.app} TxStockAppHeader!'+'&&&'+self.res['TxStockAppHeader'])
                else:
                    self.res['TxStockWxHeader'] = str(headers_dict)
                    sendlog(self.child_conn,f'{self.app} success!'+'&&&'+self.res['TxStockWxHeader'])
            # check res and save
            if all(self.res.values()):
                self.table[self.app] = [self.res]
                self.count = 1
                sendlog(self.child_conn,f'{self.app} success!'+'&&&'+dict2conf(self.res))
                save_toml(self.table,self.toml_path)
                   