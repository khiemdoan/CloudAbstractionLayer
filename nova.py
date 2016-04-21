
from http import Http
from config import Config


__author__ = 'Khiem Doan Hoa'


class Nova:

    def __init__(self, server, port, auth_token, tenant_id):
        self.__http = Http(server)
        self.__http.set_port(port)

        self.__auth_token = auth_token
        self.__tenant_id = tenant_id
        self.__server_id = None
        self.__name = None
        self.__floating_ip = None

    def create(self, image_ref, server_name, flavor='m1.tiny', network_id=None, key_name=None):
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
            network = [{'uuid': network_id}]
            data['server']['networks'] += network

        if key_name is not None:
            data['server']['key_name'] = key_name

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
            self.__floating_ip = None
            return True
        else:
            return False

    def show_details(self):
        path = 'v2.1/' + self.__tenant_id + '/servers/' + self.__server_id
        header = {"X-Auth-Token": self.__auth_token}

        data = self.__http.send_get(path, {}, header)
        return data

    def add_floating_ip(self):
        path = 'v2.1/' + self.__tenant_id + '/servers/' + self.__server_id + '/action'
        header = {"X-Auth-Token": self.__auth_token}
        ip_address = self.__get_float_ip_address()
        data = {
            "addFloatingIp": {
                "address": ip_address
            }
        }
        code = self.__http.send_post_get_code(path, data, header)
        if code == 202:
            self.__floating_ip = ip_address
            return ip_address
        else:
            return False

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

    def __get_float_ip_address(self):
        path = 'v2.1/' + self.__tenant_id + '/os-floating-ips'
        header = {"X-Auth-Token": self.__auth_token}

        floating_ips = self.__http.send_get(path, {}, header)
        for floating_ip in floating_ips['floating_ips']:
            if floating_ip['fixed_ip'] is None:
                return floating_ip['ip']

        config = Config()
        public_network_name = config.get_public_network()
        data = {'pool': public_network_name}
        self.__floating_ip = self.__http.send_post(path, data, header)
        return floating_ip['floating_ip']['ip']

    def get_floating_ip(self):
        return self.__floating_ip

    def get_system_info(self):
        path = 'v2.1/' + self.__tenant_id + '/limits'
        header = {"X-Auth-Token": self.__auth_token}
        data = self.__http.send_get(path, {}, header)
        return data['limits']['absolute']
