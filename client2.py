#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""UDP client program."""
import socket
import sys


def sendRegister(server, port, sipmsg, my_socket, myaddr, myexp):
    """sendRegister method sends a SIP REGISTER message when called.

    Arguments needed are (serverIP, serverPort, sipMessage,
    clientAddress, clientExpire).

    """
    finalMsg = sipmsg + " " + "sip:" + myaddr + " " + "SIP/2.0\r\n"
    finalMsg = finalMsg + "Expires: " + str(myexp) + "\r\n\r\n"
    my_socket.send(bytes(finalMsg, 'utf-8'))
    try:
        data = my_socket.recv(1024)
    except ConnectionRefusedError:
        sys.exit("Incorrect or not found server tuple")

    print()
    print('Received:', data.decode('utf-8'))


def doClient(server, port, sipmsg, myaddr, myexp):
    """Create an ip address for the client and calls register function too.

    Arguments needed are (serverIP, serverPort, sipMessage,
    clientAddress, clientExpire).

    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        try:
            my_socket.connect((server, port))

        except socket.gaierror:
            sys.exit('Incorrect or not found server tuple')

        sendRegister(server, port, sipmsg, my_socket, myaddr, myexp)
    print("Socket terminado.")


if __name__ == "__main__":
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    try:

        SIPMSG = sys.argv[1]
        SIPMSG = SIPMSG.upper()
        


    except(FileNotFoundError, IndexError, ValueError):
        sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

    doClient(SERVER, PORT, SIPMSG, MYADDR, MYEXP)
