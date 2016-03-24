
from http import Http


__author__ = 'Khiem Doan Hoa'


class Network:

    def __init__(self, server, port, auth_token):
        self.__http = Http(server)
        self.__http.set_port(port)
        self.__auth_token = auth_token

    def get_network_id(self, network_name=''):
        header = {"X-Auth-Token": self.__auth_token}
        data = self.__http.send_get('v2.0/networks', {}, header)
        networks = data['networks']
        for i in range(0, len(networks)):
            if networks[i]['name'] == network_name:
                return networks[i]['id']

        return 0
