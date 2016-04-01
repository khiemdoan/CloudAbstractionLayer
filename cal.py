
class Cal(object):

    def __init__(self, server, user, password):
        print "Please Implement this method"

    def start(self):
        raise NotImplementedError("Please Implement this method")

    def stop(self):
        raise NotImplementedError("Please Implement this method")

    def status(self):
        raise NotImplementedError("Please Implement this method")

    def backup(self):
        raise NotImplementedError("Please Implement this method")

    def restore(self):
        raise NotImplementedError("Please Implement this method")

    def put_data(self, file_path, file_path_remote):
        raise NotImplementedError("Please Implement this method")

    def get_data(self, file_name_remote, file_path):
        raise NotImplementedError("Please Implement this method")