#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


def composeSipAnswer(method, address):

    sipmsg = method

    return sipmsg


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        LINE = (composeSipAnswer('101 TRYING', self.client_address)+ '\r\n').encode()
        self.wfile.write(LINE)
        LINE = (composeSipAnswer('180 RINGING', self.client_address)+ '\r\n').encode()
        self.wfile.write(LINE)
        LINE = (composeSipAnswer('200 OK', self.client_address)+ '\r\n').encode()
        self.wfile.write(LINE)
        print('Replying to', self.client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if line:
                print("user sent " + line.decode('utf-8'))
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        serv = socketserver.UDPServer(('', 6001), EchoHandler)
        print("Launching UDP echo service..." + '\r\n')
        serv.serve_forever()

    except KeyboardInterrupt:
        sys.exit('Exiting')
