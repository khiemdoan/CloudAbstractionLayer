
from http import Http


__author__ = 'Khiem Doan Hoa'


class Nova:

    def __init__(self, server, port, auth_token, tenant_id):
        self.__http = Http(server)
        self.__http.set_port(port)

        self.__auth_token = auth_token
        self.__tenant_id = tenant_id
        self.__server_id = None
        self.__name = None

    def create(self, image_ref, server_name, flavor='m1.tiny', network_id=None):
        if self.__server_id is not None:
            return self.__server_id

        self.__name = server_name
        path = 'v2.1/' + self.__tenant_id + '/servers'
        header = {"X-Auth-Token": self.__auth_token, 'Content-type': 'application/json'}

        flavor_ref = self.__get_flavor_ref(flavor)

        data = {'server': {}}
        data['server']['name'] = server_name
        data['server']['imageRef'] = image_ref
        data['server']['flavorRef'] = flavor_ref

        if network_id is not None:
            data['server']['networks'] = []
            network = [{'uuid': '79351880-ed68-407b-a654-894f60b59dc8'}]
            data['server']['networks'] += network

        data = self.__http.send_post(path, data, header)
        self.__server_id = data['server']['id']
        return self.__server_id

    def delete(self):
        if self.__server_id is None:
            return True

        path = 'v2.1/' + self.__tenant_id + '/servers/' + self.__server_id
        header = {"X-Auth-Token": self.__auth_token}

        response_code = self.__http.send_delete(path, header)
        if response_code == 204:
            self.__server_id = None
            return True
        else:
            return False

    def show_details(self):
        path = 'v2.1/' + self.__tenant_id + '/servers/' + self.__server_id
        header = {"X-Auth-Token": self.__auth_token}

        data = self.__http.send_get(path, {}, header)
        return data

    def add_floating_ip(self, ip_address):
        path = 'v2.1/' + self.__tenant_id + '/servers/' + self.__server_id + '/action'
        header = {"X-Auth-Token": self.__auth_token}
        data = {
            "addFloatingIp": {
                "address": ip_address
            }
        }
        code = self.__http.send_post_get_code(path, data, header)
        return code == 202

    def backup(self, name='backup'):
        path = 'v2.1/' + self.__tenant_id + '/servers/' + self.__server_id + '/action'
        header = {"X-Auth-Token": self.__auth_token}
        data = {
            "createBackup": {
                "name": name,
                "backup_type": "daily",
                "rotation": 1
            }
        }

        code = self.__http.send_post_get_code(path, data, header)
        return code == 202

    def restore(self):
        path = 'v2.1/' + self.__tenant_id + '/servers/' + self.__server_id + '/action'
        header = {"X-Auth-Token": self.__auth_token}
        data = {
            "os-resetState": {
                "state": "active"
            }
        }

        code = self.__http.send_post_get_code(path, data, header)
        return code == 202

    def __get_flavor_ref(self, flavor_name='m1.tiny'):
        path = 'v2.1/' + self.__tenant_id + '/flavors'
        header = {"X-Auth-Token": self.__auth_token}
        flavor_list = self.__http.send_get(path, {}, header)

        flavor_ref = ''

        for flavor in flavor_list['flavors']:
            if flavor['name'] == flavor_name:
                flavor_ref = flavor['id']
                break

        return flavor_ref
