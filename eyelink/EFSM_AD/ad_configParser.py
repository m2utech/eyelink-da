from configparser import ConfigParser


def getConfig():
    config = ConfigParser()
    config.read('./config.cfg', encoding='utf-8')

    cfg = {}

    for section_name in config.sections():
        cfg[section_name] = {}
        for key, val in config.items(section_name):
            cfg[section_name][key] = val

    return cfg
