# https://github.com/JPabloPena/ST0263-Proyecto1/blob/master/server/server.py
import socket
from datetime import date, datetime
from _thread import *

def kernel(client):

    while True:

        try:
            data_user = client.recv(1024).decode()
        except error:
            print('Error de lectura.')
            break


def send(src, dst, msg):

    message = {}
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    message = {'cmd':'send', 'src':src, 'dst':dst, 'msg':'[LOG] ({}): {}'.format(date, msg)}
    print(message)

if __name__ == '__main__':

    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = 'localhost'
        port = 8000
        my_socket.bind( (host, port) ) 
        my_socket.listen(5) 

        print('------ Runnning Kernel Application ------')
        
        while True:
            conn, addr = my_socket.accept()
            print(" [x] Conexión desde: " + str(addr))
            start_new_thread(kernel, (conn, ))

    except Exception as error:
        print(socket.error)