import configparser

config = configparser.ConfigParser()
config.read('./config.cfg')

cfg = config['INFO']
