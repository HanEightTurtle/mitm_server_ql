
import mitmproxy.http
from mitmproxy import ctx
from .utils import *

class checkinpanel_web(object):
    def __init__(self,child_conn,temp_folder='temp'):
        self.child_conn = child_conn
        self.toml_path = f'{temp_folder}/checkinpanel_web.toml'
        self.table = {}
        # 签到变量初始化，免得重复工作
        self.aqc = 0
        self.iqiyi = 0
        self.vqq = 0
        self.bilibili = 0
        self.smzdm = 0
        self.pojie = 0
        self.v2ex = 0
        self.wps = 0
        self.csdn = 0
        
    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 爱企查
        if self.aqc == 0:
            if flow.request.pretty_url.startswith('https://aiqicha.baidu.com/'):
                app = 'AQC'
                res = "[{{'cookie':'log_guid={0}; BDUSS={1}; BDPPN={2}','exportkey':''}}]"
                ck_keys = ['log_guid','BDUSS','BDPPN']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    self.aqc = res.format(*[cookies_dict[item] for item in ck_keys])
                    self.table[app] = eval(self.aqc)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
        # 爱奇艺
        if self.iqiyi == 0:
            if flow.request.pretty_url.startswith('https://www.iqiyi.com/'):
                app = 'IQIYI'
                res = "[{{'cookie':'{0}'}}]"
                ck_keys = ['__dfp','QYABEX','P00001','P00002','P00007']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    self.iqiyi = res.format(ck_dict_to_str(cookies_dict))
                    self.table[app] = eval(self.iqiyi)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
        # 腾讯视频 
        if self.vqq == 0:
            if flow.request.pretty_url.startswith('https://access.video.qq.com/user/auth_refresh?'):
                app = 'VQQ'
                res = "[{{'auth_refresh':'{0}','cookie':'{1}'}}]"
                ck_keys = ['pgv_pvid','vqq_appid','vqq_openid','vqq_vuserid','vqq_refresh_token']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    self.vqq = res.format(flow.request.pretty_url,ck_dict_to_str(dict(flow.request.cookies)))
                    self.table[app] = eval(self.vqq)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res)) 
        # 哔哩哔哩 
        if self.bilibili == 0:
            if flow.request.pretty_url.startswith('https://api.bilibili.com/'):
                app = 'BILIBILI'
                res = "[{{\"coin_num\":0,\"coin_type\":1,\"cookie\":\"{0}\",\"silver2coin\":True}}]"
                ck_keys = ['fingerprint','bili_jct']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    self.bilibili = res.format(ck_dict_to_str(cookies_dict))
                    self.table[app] = eval(self.bilibili)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
        # 什么值得买
        if self.smzdm == 0:
            if flow.request.pretty_url.startswith('https://www.smzdm.com'):
                app = 'SMZDM'
                res = "[{{'cookie':'sess={0}'}}]"
                ck_keys = ['sess']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    self.smzdm = res.format(cookies_dict['sess'])
                    self.table[app] = eval(self.smzdm)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
        # 吾爱破解
        if self.pojie == 0:
            if flow.request.pretty_url.startswith('https://www.52pojie.cn'):
                app = 'POJIE'
                res = "[{{'cookie':'{0}'}}]"
                ck_keys = ['htVC_2132_saltkey','HMACCOUNT_BFESS']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    self.pojie = res.format(ck_dict_to_str(cookies_dict))
                    self.table[app] = eval(self.pojie)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
        # v2ex
        if self.v2ex == 0:
            if flow.request.pretty_url.startswith('https://www.v2ex.com'):
                app = 'V2EX'
                res = "[{{'cookie':'{0}','proxy':''}}]"
                ck_keys = ['PB3_SESSION','V2EX_TAB']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    self.v2ex = res.format(ck_dict_to_str(cookies_dict))
                    self.table[app] = eval(self.v2ex)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
        # WPS
        if self.wps == 0:
            if flow.request.pretty_url.startswith('https://www.kdocs.cn/'):
                app = 'WPS'
                res = "[{{'cookie':'{0}'}}]"
                ck_keys = ['wpsua','wps_sid']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    self.wps = res.format(ck_dict_to_str(cookies_dict))
                    self.table[app] = eval(self.wps)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res)) 
        # CSDN
        if self.csdn == 0:
            if flow.request.pretty_url.startswith('https://www.csdn.net/'):
                app = 'CSDN'
                res = "[{{'cookie':'{0}'}}]"
                ck_keys = ['uuid_tt_dd','UserToken']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    self.csdn = res.format(ck_dict_to_str(cookies_dict))
                    self.table[app] = eval(self.csdn)
                    save_toml(self.table,self.toml_path)
                    sendlog(self.child_conn,f'{app} success!'+'&&&'+dict2conf(res))
