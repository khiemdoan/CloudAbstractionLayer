
from cal import Cal
from auth import Auth
from nova import Nova
from glance import Glance
from config import Config
from network import Network
import subprocess


__author__ = 'Khiem Doan Hoa'


class OpenStack(Cal):

    def __init__(self):
        self.__config = Config('config.ini')

        server = self.__config.get_server()
        domain = self.__config.get_domain()
        username = self.__config.get_username()
        password = self.__config.get_password()
        self.__network_name = self.__config.get_internal_network()

        auth = Auth(server, 5000, username, password, domain)
        auth_token = auth.get_auth_token()
        tenant_id = auth.get_tenant_id()

        self.__nova = Nova(server, 8774, auth_token, tenant_id)
        self.__glance = Glance(server, 9292, auth_token)
        self.__network = Network(server, 9696, auth_token)

        self.__key_pair = self.__config.get_key_pair()
        self.__user_vm = self.__config.get_user_vm()

    def start(self, name='test'):
        image_name = self.__config.get_image_name()
        key_name = self.__config.get_key_name()
        flavor = self.__config.get_flavor()

        image_ref = self.__glance.get_image_ref(image_name)
        network_id = self.__network.get_network_id(self.__network_name)
        server_id = self.__nova.create(image_ref, name, flavor, network_id=network_id, key_name=key_name)
        return server_id

    def stop(self):
        ret = self.__nova.delete()
        return ret

    def status(self):
        return self.__nova.show_details()

    def associate_floating_ip(self):
        return self.__nova.add_floating_ip()

    def execute(self, command):
        ip = self.__nova.get_floating_ip()
        cmd = 'ssh -i ' + self.__key_pair + ' ' + self.__user_vm + '@' + ip + ' ' + command
        cmd_run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        return cmd_run.communicate()

    def put_data(self, source, destination):
        ip = self.__nova.get_floating_ip()
        cmd = 'ssh-keygen -R ' + ip
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd = 'scp -i ' + self.__key_pair + ' -r ' + source + ' ' + self.__user_vm + '@' + ip + ':' + destination
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()

    def get_data(self, source, destination):
        ip = self.__nova.get_floating_ip()
        cmd = 'ssh-keygen -R ' + ip
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd = 'scp -i ' + self.__key_pair + ' -r ' + self.__user_vm + '@' + ip + ':' + destination + ' ' + source
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()

    def backup(self, name='backup'):
        return self.__nova.backup(name)

    def restore(self):
        return self.__nova.restore()

    def get_system_info(self):
        absolute = self.__nova.get_system_info()
        print
        print 'maxTotalInstances: %d' % absolute['maxTotalInstances']
        print 'totalInstancesUsed: %d' % absolute['maxTotalCores']
        print
        print 'maxTotalRAMSize: %d' % absolute['maxTotalRAMSize']
        print 'totalRAMUsed: %d' % absolute['totalRAMUsed']
        print
        print 'maxTotalCores: %d' % absolute['maxTotalCores']
        print 'totalCoresUsed: %d' % absolute['totalCoresUsed']
        print
        print 'maxTotalFloatingIps: %d' % absolute['maxTotalFloatingIps']
        print 'totalFloatingIpsUsed: %d' % absolute['totalFloatingIpsUsed']
        print
