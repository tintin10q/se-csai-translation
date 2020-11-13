import os
import json
from .get_conf import get_conf

def get_valid_model_ids(conf_file=None):
    """Extract ids from conf.json if conf_file = None the default location available_models/conf.json will be tried"""
    if conf_file is None:
        conf_file = get_conf()
    else:
        conf_file = json.loads(conf_file)
    id_list = [model["id"] for model in conf_file["models"]]
    return id_list
