
import tomli
import glob, os
from itertools import chain

import tomli_w

# 读取toml
def get_toml(path):
    '''
    '''
    with open(path,'rb') as f:
        r = tomli.load(f)
    return r

def get_tomls(toml_folder='tomls'):
    '''
    '''
    path_lst = glob.glob(f"{toml_folder}/*.toml")
    f_lst = [open(path,'rb') for path in path_lst]
    toml_lst = [tomli.load(f) for f in f_lst]
    [f.close() for f in f_lst]
    return merge_dicts(toml_lst)

def save_toml(data,path):
    with open(path,'wb') as f:
        w  = tomli_w.dump(data,f)

def clear_path(path):
    for file in glob.glob(f"{path}/*"):
        os.remove(file)

def add_fixdata(fixdata,appdata):
    fixdict = {k:v[0] for k,v in tomli.loads(fixdata).items()}
    apps = fixdict.keys()
    for app in apps:
        if app in appdata.keys():
            for item in appdata[app]:
                item.update(fixdict[app])
    return appdata

def merge_dicts(dicts):
    combined_keys = list(set([key for item in dicts for key in item.keys()]))
    result = {key: list(chain(*[dict.get(key,[]) for dict in dicts])) for key in combined_keys}
    return result