
from http import Http


__author__ = 'Khiem Doan Hoa'


class Glance:

    def __init__(self, server, port, auth_token):
        self.__server = server
        self.__http = Http(server)
        self.__http.set_port(port)
        self.__auth_token = auth_token

    def get_image_ref(self):
        header = {"X-Auth-Token": self.__auth_token}
        data = self.__http.send_get('v2/images', {}, header)
        return self.__server + data['images'][0]['self']