__author__ = 'jcteng'

import socket
import struct
import binascii
def socket_send(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.1.21', 1080))
    print "connected"
    data = struct.pack("!BBB",05, 01, 00)
    sock.send(data)
    print "sent",binascii.hexlify(data)
    recvdata = sock.recv(2)

    print "recv",binascii.hexlify(recvdata)


socket_send("nothing")