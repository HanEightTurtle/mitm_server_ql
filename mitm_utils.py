
from mitmproxy import proxy, options
from mitmproxy.tools.web.master import WebMaster

import glob
from importlib import import_module
from multiprocessing import Process,Pipe
import asyncio
import threading

def loop_in_thread(loop, m):
    asyncio.set_event_loop(loop)
    m.run()

def start_webmaster(child_conn,username,password,addon_folder='addons',temp_folder='temp'):
    ex_lst = [f'{addon_folder}/__init__.py',f'{addon_folder}/utils.py']
    addonpys = [item[:-3].replace("/",'.') for item in glob.glob(f'{addon_folder}/*.py') if item not in ex_lst]
    addons = []
    for item in addonpys:
        exec(f'addons.append(import_module(item).{item[7:]}(child_conn,temp_folder))')

    ignore_hosts = []
    with open('ignore_hosts.csv','r') as f:
        for item in f.readlines():
            ignore_hosts.append(item.strip('\n'))

    opts = options.Options(
        listen_host='0.0.0.0',
        listen_port=40080,
        confdir='./.mitmproxy',
        ignore_hosts=ignore_hosts,
        ssl_insecure=True,
        add_upstream_certs_to_client_chain=True,
    )
    pconf = proxy.config.ProxyConfig(opts)

    m = WebMaster(options=opts,with_termlog=False)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(*addons)
    m.options.add_option("web_port",int,40081,"")
    m.options.add_option("web_host",str,"0.0.0.0","")
    m.options.update(proxyauth=f"{username}:{password}")

    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop,m))
    t.start()
    while True:
        if child_conn.poll():
            msg = child_conn.recv()
            if msg=='Done':
                child_conn.send('Done')
                break
    m.shutdown()

def mitm_p_start(username,password,addon_folder='addons',temp_folder='temp'):
    parent_conn, child_conn = Pipe()
    p = Process(target=start_webmaster,args=(child_conn,username,password,addon_folder,temp_folder,))
    p.start()
    return p, parent_conn, child_conn

def mitm_p_end(p,parent_conn):
    parent_conn.send('Done')
    p.join()
    p.terminate()
    