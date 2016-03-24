
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
    print '1. Start machine'
    print '2. Stop machine'
    print '3. Get status'
    print '4. Add address'
    print '5. Backup'
    print '6. Restore'

    try:
        x = int(raw_input('Enter function number: '))

        if x == 0:
            break;

        if x == 1:
            server_id = machine.start()
            print 'A server has been run with id: ' + server_id

        if x == 2:
            ret = machine.stop()
            if ret:
                print 'Server has been stop!'
            else:
                print 'There is an error when stoping'

        if x == 3:
            print 'Status:'
            dumpclean(machine.status())

        if x == 4:
            ip_address = raw_input('Enter function number: ')
            print 'Add ip address'
            print machine.add_floating_ip(ip_address)

        if x == 5:
            print 'Backup'
            print machine.backup('My backup')

        if x == 6:
            print 'Restore'
            print machine.restore()

    except ValueError:
        print 'Invalid Number'
