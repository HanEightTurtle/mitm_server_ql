


from .ql_sample import get_conf
from .util_ql import *

def qlsend(all_data_path,qlurl,qlid,qlsecret):
    conf = get_conf(all_data_path)
    token = ql_ini(qlurl,qlid,qlsecret)
    envs = ql_envs(qlurl,token)
    msg = []
    for name,value,app in conf:
        msg.append(send2ql(qlurl,token,envs,name,value,app))
    return msg
