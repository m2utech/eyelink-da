import configparser

config = configparser.ConfigParser()
config.read('./config.cfg')

global cfg
cfg = {}

for section in config.sections():
    cfg[section] = {}
    for item in config[section]:
        cfg[section][item] = config[section][item]
