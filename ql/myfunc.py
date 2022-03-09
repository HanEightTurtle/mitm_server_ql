
import tomli
import glob, os
from collections import ChainMap

import tomli_w

# 读取toml
def get_toml(path):
    '''
    '''
    with open(path,'rb') as f:
        r = tomli.load(f)
    return r

def save_toml(data,path):
    with open(path,'wb') as f:
        w  = tomli_w.dump(data,f)

def clear_path(path):
    for file in glob.glob(f"{path}/*"):
        os.remove(file)

