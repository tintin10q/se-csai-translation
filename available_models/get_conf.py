import os
import json


def get_conf():
    if conf_exist():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        conf_path = dir_path + "//conf.json"
        with open(conf_path) as config:
            config_data = json.load(config)
        return config_data
    else:
        return {}


def conf_exist():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conf_path = dir_path + "//conf.json"
    return os.path.exists(conf_path)
