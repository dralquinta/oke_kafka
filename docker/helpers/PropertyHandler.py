import os
from pathlib import Path
import configparser
from helpers.Printer import debug


def get_config_data(section, key):

    path = Path(__file__)    
    ROOT_DIR = str(path.parent.parent.absolute())+"/props"        
    config_path = os.path.join(ROOT_DIR, "config.properties")    
    config = configparser.ConfigParser()
    config.read(config_path)    
    config_property = config.get(section, key)
    
    return config_property