import configparser

class cfg_parser:

    config = configparser.ConfigParser()
    config.read('./config.cfg')
    cfg = config['INFO']
    
    def __init__(self):
        self.host = self.cfg['host']
        self.port = self.cfg['PORT']
        self.load_url = self.cfg['data_load_url']
        self.upload_url = self.cfg['result_upload_url']
        #self.s_date = self.cfg['s_date']
        #self.e_date = self.cfg['e_date']
        #self.t_interval = self.cfg['t_interval']


if __name__ == '__main__':
	pass