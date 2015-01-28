__author__ = 'rafael'

import pygal
from datetime import datetime
from snmp_helper import snmp_extract, snmp_get_oid_v3
from time import sleep

# Variable declaration
IP = '50.242.94.227'
oids = {'ifDescr_fa4': '1.3.6.1.2.1.2.2.1.2.5',
        'ifInOctets_fa4': '1.3.6.1.2.1.2.2.1.10.5',
        'ifInUcastPkts_fa4': '1.3.6.1.2.1.2.2.1.11.5',
        'ifOutOctets_fa4': '1.3.6.1.2.1.2.2.1.16.5',
        'ifOutUcastPkts_fa4': '1.3.6.1.2.1.2.2.1.17.5'}
pynet_rtr1 = (IP, 7961)
in_octects_fa4 = []
out_octects_fa4 = []
in_packets_fa4 = []
out_packets_fa4 = []
counter = 0
timer = 0


def create_chart(title, label1, label2, lst1, lst2):
    """Takes tile, labels and list as arguments and returns a chart object"""
    x_labels = ['0', '5', '10', '15', '20', '25', '30',
                '35', '40', '45', '50', '55', '60']
    line_chart = pygal.Line()
    line_chart.x_labels = x_labels
    line_chart.title = title
    line_chart.add(label1, lst1)
    line_chart.add(label2, lst2)
    line_chart.render_to_file(title)


def get_oid_val(oid, rtr=pynet_rtr1):
    """Takes a router (IP, Port) and an OID and returns corresponding OID value"""
    a_user = 'pysnmp'
    auth_key = 'galileo1'
    encrypt_key = 'galileo1'
    snmp_user = (a_user, auth_key, encrypt_key)
    if oid == '1.3.6.1.2.1.2.2.1.2.5':
        value = snmp_extract(snmp_get_oid_v3(rtr, snmp_user, oid=oid))
    else:
        value = int(snmp_extract(snmp_get_oid_v3(rtr, snmp_user, oid=oid)))
    return value


def set_timer():
    """set timer to 0 seconds for first iteration then to 300 seconds"""
    global timer
    time = 0
    if counter > 0:
        time = 300
    else:
        'There is a logical problem'
    timer = time


def get_counters():
    """Calls get_oid_val and append the return value to the corresponding list"""
    global counter
    set_timer()
    in_octects_fa4.append(get_oid_val(oids['ifInOctets_fa4']))
    out_octects_fa4.append(get_oid_val(oids['ifOutOctets_fa4']))
    in_packets_fa4.append(get_oid_val(oids['ifInUcastPkts_fa4']))
    out_packets_fa4.append(get_oid_val(oids['ifOutUcastPkts_fa4']))
    counter += 1
    sleep(timer)
    return counter


def main():
    """Start and control the sequence of the script"""
    print '''
    Script running...
    It queries every five minutes; about one hour to completion.
    The two graph files will be located in local directory after completion.
    Press Ctrl-C to exit.\n'''
    for i in iter(get_counters, 13):
        print '''Last SNMP query for %s on %s was on %s.
        Waiting for next five-munte interval...'''  % \
              (get_oid_val(oids['ifDescr_fa4']), pynet_rtr1, datetime.now())

    create_chart('IN_OUT_BYTES_RTR-1_INT-F4', 'InBytes', 'OutBytes',
                 in_octects_fa4, out_octects_fa4)

    create_chart('IN_OUT_UNICAST_RTR-1_INT-F4', 'InPackets', 'OutPackets',
                 in_packets_fa4, out_packets_fa4)
    print 'Test complete; the two graph files are located in local directory'


if __name__ == "__main__":
    main()
    
