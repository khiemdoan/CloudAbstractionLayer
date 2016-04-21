
import httplib
import json


__author__ = 'Khiem Doan Hoa'


class Http(object):

    __host = None
    __port = 80
    __https = False

    def __init__(self, host):
        self.__host = host

    def __create_connection(self):
        if self.__https is True:
            conn = httplib.HTTPSConnection(self.__host, self.__port)
        else:
            conn = httplib.HTTPConnection(self.__host, self.__port)
        return conn

    # set use HTTPS
    def use_https(self, flag=True):
        self.__https = flag

    # set port
    def set_port(self, port=80):
        self.__port = port

    # send GET request
    # return data has type is dict
    def send_get(self, path='', data={}, headers={}):
        headers['Content-type'] = 'application/json'
        keys = data.keys()
        values = data.values()

        string = '/' + path

        if len(data) != 0:
            string += "?" + keys[0] + "=" + values[0]
            for i in range(1, len(data), 1):
                string += "&" + keys[i] + "=" + values[i]

        conn = self.__create_connection()
        conn.request("GET", string, '', headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return json.loads(data)

    # send POST request
    # return data has type is dict
    def send_post(self, path, data, headers={}):
        headers['Content-type'] = 'application/json'
        conn = self.__create_connection()
        conn.request("POST", '/' + path, json.dumps(data), headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return json.loads(data)

    def send_post_get_code(self, path, data, headers={}):
        headers['Content-type'] = 'application/json'
        conn = self.__create_connection()
        conn.request("POST", '/' + path, json.dumps(data), headers)
        res = conn.getresponse()
        conn.close()
        return res.status

    # send DELETE request
    # return response code
    def send_delete(self, path, headers={'Accept': 'text/plain'}):
        conn = self.__create_connection()
        conn.request('DELETE', '/' + path, '', headers)
        res = conn.getresponse()
        conn.close()
        return res.status
