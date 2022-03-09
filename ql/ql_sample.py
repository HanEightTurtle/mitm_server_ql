
from .myfunc import get_toml

def get_conf(all_data_path):
    conf = []
    data = get_toml(all_data_path)

    app,name,lj = ['京东','JD_WSCK','&']
    if data.get(app):
        value ='&'.join([f'pin={account.get("pin")};wskey={account.get("wskey")};' for account in data.get(app)])
        conf.append([name,value,app])

    app,name,lj = ['腾讯自选股','TxStockAppUrl','#']
    if data.get(app):
        value = lj.join([account.get(name) for account in data.get(app)])
        conf.append([name,value,app])
        app,name,lj = ['腾讯自选股','TxStockAppHeader','#']
        value = lj.join([account.get(name) for account in data.get(app)])
        conf.append([name,value,app])
        app,name,lj = ['腾讯自选股','TxStockWxHeader','#']
        value = lj.join([account.get(name) for account in data.get(app)])
        conf.append([name,value,app])

    app,name,lj = ['饿了么','elmck','@']
    if data.get(app):
        value = lj.join([account.get(name) for account in data.get(app)])
        conf.append([name,value,app])

    app,name,lj = ['滴滴果园','ddgyurl','@']
    if data.get(app):
        value = lj.join([account.get(name) for account in data.get(app)])
        conf.append([name,value,app])

    app,name,lj = ['美团','mtTk','@']
    if data.get(app):
        value = lj.join([account.get(name) for account in data.get(app)])
        conf.append([name,value,app])

    app,name,lj = ['快手极速版','kshd','@']
    if data.get(app):
        value = lj.join([account.get(name) for account in data.get(app)])
        conf.append([name,value,app])

    app,name,lj = ['康师傅畅饮社','ksfcysToken','@']
    if data.get(app):
        value = lj.join([account.get(name) for account in data.get(app)])
        conf.append([name,value,app])

    app,name,lj = ['淘小说','txsCookie','@']
    if data.get(app):
        value = lj.join([account.get(name) for account in data.get(app)])
        conf.append([name,value,app])

    app,name,lj = ['快手','ksCookie','@']
    if data.get(app):
        value = lj.join([account.get(name) for account in data.get(app)])
        conf.append([name,value,app])

    return conf
