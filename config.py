
import ConfigParser

__author__ = 'Khiem Doan Hoa'


class Config():

    def __init__(self, file_path):
        config = ConfigParser.ConfigParser()
        config.read(file_path)

        self.__server = config.get('OpenStackConfig', 'server')
        self.__domain = config.get('OpenStackConfig', 'domain')
        self.__username = config.get('OpenStackConfig', 'username')
        self.__password = config.get('OpenStackConfig', 'password')

    def get_server(self):
        return self.__server

    def get_domain(self):
        return self.__domain

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password
