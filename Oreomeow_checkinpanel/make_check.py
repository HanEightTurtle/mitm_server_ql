
from .myfunc import get_toml,save_toml

def make_check(all_data_path,sample_path='Oreomeow_checkinpanel/check.sample.toml',check_path='Oreomeow_checkinpanel/check.toml'):
    data = get_toml(all_data_path)
    sample = get_toml(sample_path)
    check_data = {key:value for key in sample.keys() if (value:=data.get(key))}
    save_toml(check_data,check_path)
    return 'check.toml updated'