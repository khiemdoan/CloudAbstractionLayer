
from cal import Cal
from auth import Auth
from nova import Nova
from glance import Glance
from config import Config
from network import Network


__author__ = 'Khiem Doan Hoa'


class OpenStack(Cal):

    def __init__(self):
        config = Config('config.ini')

        server = config.get_server()
        domain = config.get_domain()
        username = config.get_username()
        password = config.get_password()

        auth = Auth(server, 5000, username, password, domain)
        auth_token = auth.get_auth_token()
        tenant_id = auth.get_tenant_id()

        self.__nova = Nova(server, 8774, auth_token, tenant_id)
        self.__glance = Glance(server, 9292, auth_token)
        self.__network = Network(server, 9696, auth_token)

    def start(self, name='test'):
        image_ref = self.__glance.get_image_ref()
        network_id = self.__network.get_network_id()
        server_id = self.__nova.create(image_ref, name, network_id=network_id)
        return server_id

    def stop(self):
        ret = self.__nova.delete()
        return ret

    def status(self):
        return self.__nova.show_details()

    def add_floating_ip(self, ip_address):
        return self.__nova.add_floating_ip(ip_address)

    def execute(self, command):
        print 'execute command'

    def put_data(self, source, destination):
        print 'putdata'

    def get_data(self, source, destination):
        print 'getdata'

    def backup(self, name='backup'):
        return self.__nova.backup(name)

    def restore(self):
        return self.__nova.restore()
