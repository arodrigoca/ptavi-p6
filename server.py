#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


def composeSipAnswer(method, address):

    sipmsg = method

    return sipmsg


def sendSong(song):

    command = './mp32rtp -i 127.0.0.1 -p 23032 < ' + song
    print(command)
    os.system(command)

def checkClientMessage(msg):

    sipPart = msg[msg.find(' ')+1:]
    sipPart = [sipPart[:sipPart.find(':')+1], \
    sipPart[sipPart.find(':')+1:sipPart.find('@')], \
    sipPart[sipPart.find('@'):sipPart.find('@')+1], \
    sipPart[sipPart.find('@')+1:sipPart.find(' ')], sipPart[sipPart.find(' ')+1:]]
    msg = msg.split(' ')
    if sipPart[0] == 'sip:' and sipPart[2] == '@' and sipPart[4] == 'SIP/2.0\r\n\r\n':
        if msg[0] == 'INVITE' or msg[0] == 'ACK' or msg[0]== 'BYE':
            return 'OK'
        else:
            return 'METHOD NOT ALLOWED'
    else:
        return 'BAD REQUEST'


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print('Replying to', self.client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if line:
                print("user sent " + line.decode('utf-8'))
                checkClientMessage(line.decode('utf-8'))
                if checkClientMessage(line.decode('utf-8')) == 'OK':
                    print('METHOD ALLOWED')
                    LINE = (composeSipAnswer('100 TRYING', self.client_address)+ '\r\n').encode()
                    self.wfile.write(LINE)
                    LINE = (composeSipAnswer('180 RINGING', self.client_address)+ '\r\n').encode()
                    self.wfile.write(LINE)
                    LINE = (composeSipAnswer('200 OK', self.client_address)+ '\r\n').encode()
                    self.wfile.write(LINE)

                elif checkClientMessage(line.decode('utf-8')) == 'METHOD NOT ALLOWED':
                    print('METHOD NOT ALLOWED')
                    LINE = (composeSipAnswer('405 METHOD NOT ALLOWED', self.client_address)+ '\r\n').encode()
                    self.wfile.write(LINE)

                else:
                    print('BAD REQUEST')
                    LINE = (composeSipAnswer('400 BAD REQUEST', self.client_address)+ '\r\n').encode()
                    self.wfile.write(LINE)
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

        # sendSong(sys.argv[3])

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        serv = socketserver.UDPServer((sys.argv[1], int(sys.argv[2])), EchoHandler)
        print("Listening..." + '\r\n')
        serv.serve_forever()

    except KeyboardInterrupt:
            sys.exit('Exiting')

    except IndexError:
            sys.exit('Usage: python3 server.py IP port audio_file')
