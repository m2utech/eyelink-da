import configparser

config = configparser.RawConfigParser()

config.add_section('Section1')

config.set('Section1', 'an_int', '15')

config.set('Section1', 'a_bool', 'true')

config.set('Section1', 'a_float', '3.141592')

config.set('Section1', 'baz', 'fun')

config.set('Section1', 'bar', 'Python')

config.set('Section1', 'foo', '%(bar)s is %(baz)s!')


with open('config.cfg', 'w') as configfile:

    config.write(configfile)  ##마지막에 꼭 write 해줘야 한다
