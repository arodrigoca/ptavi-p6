#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


def cropAddr(string):

    IP_start = string.find('@') + 1
    port_start = string.find(':') + 1
    address = [string[IP_start:port_start - 1], int(string[port_start:]),
               string[:IP_start - 1]]
    return address


def composeSipMsg(method, address):

    sipmsg = method + " " + "sip:" + address[2] + '@' + address[0] \
              + ' ' + "SIP/2.0\r\n\r\n"

    return sipmsg


def doClient(server_addr, sipmsg):

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        try:
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.connect((server_addr[0], server_addr[1]))
            LINE = composeSipMsg(sipmsg, server_addr)
            print("Sending: " + LINE)
            my_socket.send(bytes(LINE, 'utf-8'))
            while True:
                data = my_socket.recv(1024)
                if data:
                    print('received -- ', data.decode('utf-8'))
                    okline = 'SIP/2.0 100 Trying\r\n\r\n'
                    okline = okline + 'SIP/2.0 180 Ringing\r\n\r\n'
                    okline = okline + 'SIP/2.0 200 OK\r\n\r\n'
                    if data.decode() == okline:
                        LINE = composeSipMsg('ACK', server_addr)
                        my_socket.send(bytes(LINE, 'utf-8'))
                    break

        except (socket.gaierror, ConnectionRefusedError):
                sys.exit('Error: Server not found')

if __name__ == "__main__":
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    try:

        SIPMSG = sys.argv[1]
        SIPMSG = SIPMSG.upper()
        SERVER_ADDR = cropAddr(sys.argv[2])

    except(FileNotFoundError, IndexError, ValueError):
        sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

    doClient(SERVER_ADDR, SIPMSG)
