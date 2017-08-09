
# configuration
import configparser


config = configparser.ConfigParser()
config.read('./config.cfg')
cfg_info = config['INFO']

global cfg
cfg = {}


for x in cfg_info:
    cfg[x] = cfg_info[x]


def main():




if __name__ == '__main__':
    main()