#!/usr/bin/env python

import os
import sys
import time
import socket

import udpsender

def valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

hint = '''\
Usage:  %s [IP]
''' % __file__

if len(sys.argv) == 1:
    ip = '255.255.255.255'
elif len(sys.argv) == 2:
    if sys.argv[1] == '-h':
        print hint
        sys.exit()
    else:
        ip = sys.argv[1]
        print ip
        if not valid_ip(ip):
            print 'Error: invalid ip address'
            sys.exit(1)
else:
    print 'Error: multiple arguments'
    print usage
    sys.exit(2)

path = os.path.split(os.path.realpath(__file__))[0]
senders = {}

try:
    f = open(path + os.path.sep + 'videomap', 'r')
except IOError as e:
    print 'Error:', e
    sys.exit(2)

for line in f.readlines():
    line = line.strip()
    if not len(line) or line.startswith('#'):
        continue

    try:
        fip, fport, fname, fbr = line.split('|')
    except Exception as e:
        print 'Warning:', e
        continue

    if (fip is None) or (fport is None) or (fname is None):
        continue

    fip = fip.strip()
    fport = fport.strip()
    fname = path + os.path.sep + fname.strip()

    if fbr[-1] in ('m', 'M'):
        bitrate = float(fbr[:-1]) * 1024 * 1024
    elif fbr[-1] in ('k', 'K'):
        bitrate = float(fbr[:-1]) * 1024
    elif fbr == '*':
        bitrate = detect_bitrate(fname)
    else:
        bitrate = float(a)

    faddr = (fip, int(fport))
    if faddr not in senders.keys():
        senders[faddr] = udpsender.Sender(
            fname, (ip, int(fport)), True, bitrate=bitrate)
        senders[faddr].start()

f.close()

print 'Vod server is now running.'
print 'Press q to exit.'
try:
    while True:
        i = raw_input('# ').strip()
        if i == 'q':
            break
finally:
    print 'Bye'
    for k in senders.keys():
        senders[k].stop()
        del senders[k]

