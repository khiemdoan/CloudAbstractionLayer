
from http import Http


__author__ = 'Khiem Doan Hoa'


class Auth:

    def __init__(self, server, port, username, password, domain='default'):

        self.__http = Http(server)
        self.__http.set_port(port)

        self.__username = username
        self.__password = password

        self.__get_auth_token()
        self.__get_tenant_id()

    def __get_auth_token(self):
        data_request = {
            "auth": {
                "tenantName": self.__username,
                "passwordCredentials": {
                    "username": self.__username,
                    "password": self.__password
                }
            }
        }

        data = self.__http.send_post('v2.0/tokens', data_request)
        self.__auth_token = data['access']['token']['id']

    def __get_tenant_id(self):
        header = {"X-Auth-Token": self.__auth_token}
        data = self.__http.send_get('v2.0/tenants', {}, header)
        tenants = data['tenants']
        for i in range(0, len(tenants), 1):
            if tenants[i]['name'] == self.__username:
                self.__tenant_id = tenants[i]['id']

    def get_auth_token(self):
        return self.__auth_token

    def get_tenant_id(self):
        return self.__tenant_id

