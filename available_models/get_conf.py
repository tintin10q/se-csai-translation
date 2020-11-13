import os
import json


def get_conf() -> dict:
    """Function that will read the config file for the translation server and return it as a dict"""
    if conf_exist():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        conf_path = dir_path + "//conf.json"
        with open(conf_path) as config:
            config_data = json.load(config)
        return config_data
    else:
        return {}


def conf_exist() -> bool:
    """Function that will return true if the config file for the translation server exists"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conf_path = dir_path + "//conf.json"
    return os.path.exists(conf_path)
