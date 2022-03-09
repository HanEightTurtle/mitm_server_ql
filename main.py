

from pywebio.session import defer_call
from pywebio.input import input,input_group,TEXT,PASSWORD,actions,select
from pywebio.output import put_buttons,put_text,use_scope,put_column
from pywebio.pin import put_textarea,pin
from pywebio import start_server
import re
import csv
import time
from functools import partial
from datetime import datetime
from multiprocessing import Process

from myfunc import get_toml,get_tomls,save_toml,clear_path,add_fixdata
from mitm_utils import mitm_p_start,mitm_p_end
from ql.qlsend import qlsend
from Oreomeow_checkinpanel.make_check import make_check
from notify_mtr import send

# 账号操作
def get_account(path='account.csv'):
    '''
    lock file and read account.csv
    '''
    with open(path,'r+') as f:
        reader = csv.reader(f)
        account = {row[0]:row[1] for row in reader}
        lock = account.get('lock')
        return lock,account
def add_account(username,password,account_path='account.csv',toml_folder='tomls'):
    '''
    '''
    with open(account_path,'a+') as f:
        writer = csv.writer(f)
        w = writer.writerow((username,password))
    with open(f'{toml_folder}/{username}.toml','w') as f:
        f.write('\n')
    with open(f'{toml_folder}/{username}.fixtoml','w') as f:
        f.write('\n')
def add_lock(path='account.csv'):
    '''
    '''
    with open(path,'r+') as f:
        reader = csv.reader(f)
        account = {row[0]:row[1] for row in reader}
        account['lock']='1'
        f.seek(0)
        writer = csv.writer(f)
        for row in account.items():
            w = writer.writerow(row)    
def release_lock(path='account.csv'):
    '''
    '''
    with open(path,'r+') as f:
        reader = csv.reader(f)
        account = {row[0]:row[1] for row in reader}
        account['lock']='0'
        f.seek(0)
        writer = csv.writer(f)
        for row in account.items():
            w = writer.writerow(row)    

# 登录界面
def check_info(info,lock,account):
    '''
    '''
    users = list(account.keys())
    username = info.get('username')
    password = info.get('password')
    is_signup = info.get('action')=='signup'
    is_login = info.get('action')=='login'
    is_login_1 = info.get('action')=='login_1'
    is_edit = info.get('action')=='edit'
    if not lock=='0':
        if any([is_login,is_login_1,is_signup]):
            return ('username','资源已被占用，仅编辑模式')
    if not re.match("^[A-Za-z0-9_-]*$",username):
        return ('username','字母数字下划线')
    if 5>len(username) or len(username)>20:
        return ('username','5-20个字符')
    if is_signup and username in users:
        return ('username','用户已存在')
    if not username in users:
        if any([is_login,is_login_1,is_edit]):
            return ('username','用户不存在')
    if not password==account.get(username):
        if any([is_login,is_login_1,is_edit]):
            return ('password','密码错误')
    if len(password)>20:
        return ('password','error: more than 20 letters')
def login_info(lock,account,qlconf_path):
    '''
    open a web_page
    '''
    if not lock=='0':
        put_text('资源已被占用，can only edit')
    
    if qlconf:=get_toml(qlconf_path).get('青龙'):
        ql_options = [
            {
                'label': ql.get('qlremark'),
                'value': [ql.get('qlurl'),ql.get('qlid'),ql.get('qlsecret')],
                'select': False,
                'disable': False
            } for ql in qlconf]
        ql_options[0]['select'] = True
    else:
        ql_options=[]

    check_info_par = partial(check_info,lock=lock,account=account)
    info = input_group('首页', [
        input('username', type=TEXT, name='username', required=False),
        input('password', type=PASSWORD, name='password', required=False),
        select(label='qinglong',name='qinglong',options=ql_options),
        input('抓包时间(s)', type=TEXT, name='zhua_time', required=False,value=60),
        actions('', [
            {'label': '登录&抓包', 'value': 'login'},
            {'label': '注册&抓包', 'value': 'signup'},
            {'label': '编辑', 'value': 'edit'},
        ], name='action', help_text=''),
    ],validate=check_info_par)
    return info

# 点击抓包button
def start_capture(username,password,qlconf,zhua_time,toml_folder,account_path,addon_folder,temp_folder,all_data_path):
    add_lock(path=account_path)
    toml_path = f'{toml_folder}/{username}.toml'
    appdata = get_toml(toml_path)
    with open(f'{toml_folder}/{username}.fixtoml','r',encoding='utf-8') as f:
        fixdata = f.read()
    tz_lst = appdata.get('通知')
    # 开始抓包
    t1 = datetime.now()
    p, parent_conn, child_conn = mitm_p_start(username,password,addon_folder=addon_folder,temp_folder=temp_folder)
    while True:
        t2 = datetime.now()
        # 时间到了。发出结束指令
        if (t2-t1).seconds>zhua_time:
            mitm_p_end(p,parent_conn)
        if parent_conn.poll():
            # 获取mimtproxy的抓包log:list
            a = parent_conn.recv()
            if not a=='Done':
                title,content = a.split('&&&',1)
                send(tz_lst,'抓取'+title,content)
            # 抓包完成，结束
            else:
                save_newdata(fixdata,appdata,toml_path,temp_folder)
                # 清空temp文件夹
                clear_path(temp_folder)
                # 把所有用户toml合并        
                all_data = get_tomls(toml_folder=toml_folder)
                save_toml(all_data,all_data_path)
                # QL
                qlurl,qlid,qlsecret = qlconf
                msg1 = qlsend(all_data_path,qlurl,qlid,qlsecret)
                # checkinpanel
                msg2 = make_check(all_data_path)
                send(tz_lst,'Capture Finished',f'{msg1}\n{msg2}')
                #
                release_lock(path=account_path)
                break
def user_page(username,password,qlconf,zhua_time,toml_folder,account_path,addon_folder,temp_folder,all_data_path):
    '''
    '''
    p = Process(target=start_capture,args=(username,password,qlconf,zhua_time,toml_folder,account_path,addon_folder,temp_folder,all_data_path,))
    p.start()
# 保存抓到的toml
def save_newdata(fixdata,appdata,toml_path,temp_folder):
    newdata = get_tomls(toml_folder=temp_folder)
    for item in newdata.keys():
        appdata[item] = newdata[item]
    save_toml(add_fixdata(fixdata,appdata),toml_path)

def edit_toml(username,toml_folder):
    '''
    '''
    toml_path = f'{toml_folder}/{username}.toml'
    fixtoml_path = f'{toml_folder}/{username}.fixtoml'
    with open(toml_path,'r',encoding='utf-8') as f:
        appdata = f.read()
    with open(fixtoml_path,'r',encoding='utf-8') as f:
        fixdata = f.read()
    with use_scope('toml_edit',clear=True):
        put_column([
            put_textarea(name='appdata',label='App Data',rows=26,code={'mode':'markdown'},value=appdata),
            put_textarea(name='fixdata',label='Fixed Data',rows=17,code={'mode':'markdown'},value=fixdata),
        ])
    def save_edit():
        with open(toml_path,'w',encoding='utf-8') as f:
            f.write(pin['appdata'])
        with open(fixtoml_path,'w',encoding='utf-8') as f:
            f.write(pin['fixdata'])
        put_text('saved,just close the window')
    put_buttons(['save'],onclick=[save_edit]).show()
# Main
def task(toml_folder,account_path,all_data_path,addon_folder,temp_folder,qlconf_path):
    '''
    '''
    lock,account = get_account(path=account_path)
    @defer_call
    def on_close():
        if lock=='0':
            release_lock(path=account_path)
            clear_path(temp_folder)
    if lock=='0':
        info = login_info(lock,account,qlconf_path)
        username = info.get('username')
        password = info.get('password')
        qlconf = info.get('qinglong')
        zhua_time = int(info.get('zhua_time'))
        # 点击注册
        if info.get('action')=='signup':
            add_account(username,password,account_path,toml_folder)
            user_page(username,password,qlconf,zhua_time,toml_folder,account_path,addon_folder,temp_folder,all_data_path)
            # release_lock(path='account.csv')
        # 转到用户界面    
        if info.get('action')=='login':
            user_page(username,password,qlconf,zhua_time,toml_folder,account_path,addon_folder,temp_folder,all_data_path)
            # release_lock(path='account.csv')
        # edit
        if info.get('action')=='edit':
            edit_toml(username,toml_folder)
    else:
        info = login_info(lock,account,qlconf_path)
        username = info.get('username')
        password = info.get('password')
        # edit
        if info.get('action')=='edit':
            edit_toml(username,toml_folder)
        put_text('资源已被占用')

toml_folder = 'tomls'
account_path = 'account.csv'
all_data_path = 'output/all_data.toml'
addon_folder = 'addons'
temp_folder = 'temp'
qlconf_path = 'ql/qlconf.toml'
task_par = partial(task,toml_folder=toml_folder,account_path=account_path,all_data_path=all_data_path,addon_folder=addon_folder,temp_folder=temp_folder,qlconf_path=qlconf_path)

if __name__ == "__main__":
    start_server(
        task_par,
        port=40082,
        debug=True,
        cdn=False,
        auto_open_webbrowser=False,
        remote_access=False,
    )
