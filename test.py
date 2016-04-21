
from openstack import OpenStack


__author__ = 'Khiem Doan Hoa'


def dumpclean(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                dumpclean(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print v
    else:
        print obj

machine = OpenStack()

while True:
    print '\n\n'
    print '0. Exit'
    print '1. System info'
    print '2. Start machine'
    print '3. Stop machine'
    print '4. Get status'
    print '5. Associate floating ip address'
    print '6. Run command'
    print '7. Upload file'
    print '8. Download file'
    print '9. Backup'
    print '10. Restore'

    try:
        x = int(raw_input('Enter function number: '))

        if x == 0:
            break

        if x == 1:
            machine.get_system_info()

        if x == 2:
            server_id = machine.start()
            print 'A server has been run with id: ' + server_id

        if x == 3:
            ret = machine.stop()
            if ret:
                print 'Server has been stop!'
            else:
                print 'There is an error when stopping'

        if x == 4:
            print 'Status:'
            dumpclean(machine.status())

        if x == 5:
            print 'Floating ip address:'
            print machine.associate_floating_ip()

        if x == 6:
            command = raw_input('Enter command: ')
            print machine.execute(command)

        if x == 7:
            print 'Upload file'
            source_path = raw_input('Source path: ')
            destination_path = raw_input('Destination path: ')
            machine.put_data(source_path, destination_path)

        if x == 8:
            print 'Download file'
            source_path = raw_input('Source path: ')
            destination_path = raw_input('Destination path: ')
            machine.put_data(source_path, destination_path)

    except ValueError:
        print 'Invalid Number'
