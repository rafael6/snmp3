__author__ = 'rafael'

from datetime import timedelta, datetime
from email_helper import send_mail
from snmp_helper import snmp_extract, snmp_get_oid_v3

# Basic varaibles
IP = '50.242.94.227'
a_user = 'pysnmp'
auth_key = 'galileo1'
encrypt_key = 'galileo1'


def notify(subject):
    """Takes a router-ID as argument and notify its config is not saved"""
    recipient = 'rafael.gm01@gmail.com'
    sender = 'ktbyers@twb-tech.com'
    message = '\nWarning, running-config on device %s not saved!!!' % subject
    print message
    print 'Sending notification to %s.' % recipient
    send_mail(recipient, subject, message, sender)


def check_if_saved(start, run):
    """Takes StatupLastChanged and RunningLastChanged as arguments and return
    True if running config is saved"""
    if start == 0:
        return False
    elif start >= run:
        return True
    else:
        return False


def get_oid_val(rtr, oid):
    """Takes a router and an OID object and returns its associated OID value"""
    snmp_user = (a_user, auth_key, encrypt_key)
    return snmp_extract(snmp_get_oid_v3(rtr, snmp_user, oid=oid))


def set_record(name, descr, uptime, start_change, run_change):
    """ Create a dictionary for containing the following items:
    sysName, sysDescr, sysUptime, StartupLastChange, and RunningLastChange."""
    record = {'Hostname': name,
              'Description': descr,
              'Uptime': uptime,
              'Startup-config changed': start_change,
              'Running-config changed': run_change}
    return record


def unpack_dic(dic):
    """Takes a dictionary object and unpack its keys and values"""
    for k, v in dic.items():
        print k + ':', v


def main():
    """Iterate over each router and calls the following functions:
    get_oid_val, get_datetime, timedelta, set_record, and check_if_saved"""
    pynet_rtr1 = (IP, 7961)
    pynet_rtr2 = (IP, 8061)
    oids = {'RunningLastChanged': '1.3.6.1.4.1.9.9.43.1.1.1.0',
            'StartupLastChanged': '1.3.6.1.4.1.9.9.43.1.1.3.0',
            'sysUptime': '1.3.6.1.2.1.1.3.0',
            'sysName': '1.3.6.1.2.1.1.5.0',
            'sysDescr': '1.3.6.1.2.1.1.1.0'}

    for router in pynet_rtr1, pynet_rtr2:
        sys_name = get_oid_val(router, oids['sysName'])
        sys_descr = get_oid_val(router, oids['sysDescr'])

        sys_uptime = int(get_oid_val(router, oids['sysUptime']))
        uptime = sys_uptime/100
        sys_uptime_normal = datetime.now() - timedelta(seconds=(uptime))

        startup_last_change = int(get_oid_val(router, oids['StartupLastChanged']))
        startup_change = datetime.now() - timedelta(seconds=(
            uptime - startup_last_change/100))

        running_last_change = int(get_oid_val(router, oids['RunningLastChanged']))
        running_change = datetime.now() - timedelta(seconds=(
            uptime - running_last_change/100))

        device_id = str(router)
        router = set_record(sys_name, sys_descr, sys_uptime_normal,
                            startup_change, running_change)
        print '\nBELOW ARE THE DETAILS FOR DEVICE %s:' % device_id
        unpack_dic(router)

        if not check_if_saved(startup_last_change, running_last_change):
            notify(device_id)
        else:
            print 'The current running-config on device %s is saved.' % device_id

if __name__ == "__main__":
    main()
