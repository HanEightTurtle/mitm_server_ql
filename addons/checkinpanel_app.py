
import mitmproxy.http
from mitmproxy import ctx
from .utils import *

class checkinpanel_app(object):
    def __init__(self,child_conn,temp_folder='temp'):
        self.child_conn = child_conn
        self.toml_path = f'{temp_folder}/checkinpanel_app.toml'
        self.table = {}
        # 签到变量初始化，免得重复工作
        self.unicom = 0
        self.fmapp = 0
        self.heytap = 0
        self.lenovo = 0
        self.weibo = 0
        
    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 联通
        if self.unicom == 0:
            if flow.request.pretty_url.startswith('https://m.client.10010.com/mobileService/log'):
                app = 'UNICOM'
                res = "[{{'app_id':'{0}'}}]"
                dt_key = 'appId'
                data_dict = data_str_to_dict(flow.request.get_text())
                if dt_key in data_dict.keys():
                    self.unicom = res.format(data_dict[dt_key])
                    self.table[app] = eval(self.unicom)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
        # Fa米家
        if self.fmapp == 0:
            if flow.request.pretty_url.startswith('https://fmapp.chinafamilymart.com.cn/'):
                app = 'FMAPP'
                res = "[{{'blackbox':'{0}','cookie':'{1}','device_id':'{2}','fmversion':'{3}','os':'{4}','token':'{5}','useragent':'{6}'}}]"
                hd_keys = ['blackbox','cookie','deviceid','fmversion','os','token','user-agent']
                headers_dict = {k.lower():v for k,v in dict(flow.request.headers).items()}
                if set(hd_keys) < set(headers_dict.keys()):
                    self.fmapp = res.format(*[headers_dict[item] for item in hd_keys])
                    self.table[app] = eval(self.fmapp)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
        # 欢太商城
        if self.heytap == 0:
            if flow.request.pretty_url.startswith('https://store.oppo.com/'): 
                app = 'HEYTAP'
                res = "[{{'cookie':'{0}','draw':False,'useragent':'{1}'}}]"
                hd_keys = ['cookie','user-agent']
                ck_keys = ['source_type','TOKENSID','app_param']
                cookies_dict = dict(flow.request.cookies)
                if  set(ck_keys) < set(cookies_dict.keys()):
                    headers_dict = {k.lower():v for k,v in dict(flow.request.headers).items()}
                    if set(hd_keys) < set(headers_dict.keys()):
                        self.heytap = res.format(*[headers_dict[item] for item in hd_keys])
                        self.table[app] = eval(self.heytap)
                        save_toml(self.table,self.toml_path)
                        sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
        # 联想智选
        if self.lenovo == 0:
            if flow.request.pretty_url.startswith('https://api.club.lenovo.cn/common/'):
                app = 'LENOVO'
                res = "[{{'baseinfo':'{1}'}}]"
                hd_keys = ['baseinfo']
                headers_dict = {k.lower():v for k,v in dict(flow.request.headers).items()}
                if set(hd_keys) < set(headers_dict.keys()):
                    self.lenovo = res.format(*[headers_dict[item] for item in hd_keys])
                    self.table[app] = eval(self.lenovo)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
        # 微博
        if self.weibo == 0:
            if flow.request.pretty_url.startswith('https://api.weibo.cn/2/users/show?'):
                app = 'WEIBO'
                res = "[{{'url':'{0}'}}]"
                if 'launchid' in flow.request.pretty_url:
                    self.weibo = flow.request.pretty_url
                    self.table[app] = eval(self.weibo)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))

