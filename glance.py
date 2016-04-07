
from http import Http


__author__ = 'Khiem Doan Hoa'


class Glance:

    def __init__(self, server, port, auth_token):
        self.__server = server
        self.__http = Http(server)
        self.__http.set_port(port)
        self.__auth_token = auth_token

    def get_image_ref(self, image_name=None):
        header = {"X-Auth-Token": self.__auth_token}
        data = self.__http.send_get('v2/images', {}, header)
        if image_name is None:
            return self.__server + data['images'][0]['self']
        for i in range(0, len(data['images'])):
            if data['images'][0]['name'] == image_name:
                return self.__server + data['images'][i]['self']