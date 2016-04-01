
import ConfigParser

__author__ = 'Khiem Doan Hoa'


class Config:

    def __init__(self, file_path='config.ini'):
        self.__config = ConfigParser.SafeConfigParser()
        self.__config.read(file_path)

    def __get(self, option=''):
        section = 'OpenStackConfig'
        try:
            value = self.__config.get(section, option, '')
        except ConfigParser.NoOptionError:
            value = 'No option \'' + option + '\' in section: \'' + section + '\''
        return value

    def get_server(self):
        return self.__get('server')

    def get_domain(self):
        return self.__get('domain')

    def get_username(self):
        return self.__get('username')

    def get_password(self):
        return self.__get('password')

    def get_internal_network(self):
        return self.__get('internal-network')

    def get_public_network(self):
        return self.__get('public-network')

    def get_key_pair(self):
        return self.__get('key_pair')

    def get_user_vm(self):
        return self.__get('user_vm')

    def get_key_name(self):
        return self.__get('key_name')