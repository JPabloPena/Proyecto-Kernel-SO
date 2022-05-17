# https://github.com/JPabloPena/ST0263-Proyecto1/blob/master/server/server.py
import socket
import json
from datetime import datetime
from _thread import *

def kernel(client, addr):

    file_socket = socket.socket()
    file_socket.connect( ('localhost', 8001) ) # Se conecta al file_manager

    while True:

        try:
            data_user = client.recv(1024).decode()
            if data_user:
                controller(data_user, addr, file_socket)
            
        except error:
            print(' [KERNEL] Data reading error!')
            break

def controller(data, addr, file_socket):
    
    data = json.loads(data)
    port = addr[1]

    if data['cmd'] == 'exit':
        # Enviar mensaje al file_manager para el log
        send_to_file(data['cmd'], '', '', '', data['msg'], '', file_socket)
        print(" [KERNEL] Conneciton finished: " + str(addr))
        msg = 'Good bye!'
        conn.send(msg.encode())

    elif data['dst'] == 'file manager':
        send_to_file(data['cmd'], data['src'], data['dst'], data['info'], data['msg'], port, file_socket)

    elif data['dst'] == 'application':
        send_to_application()
    


def send_to_file(cmd, src, dst, info, msg_user, port, file_socket):
    
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if cmd == 'create':
        msg = 'creating folder'
        msg_kernel = '[LOG] [KERNEL] ({}): {} {}'.format(date, msg, info)
        message = {'cmd':cmd, 'src':src, 'dst':dst, 'info':info, 'port':port, 'msg_user':msg_user, 'msg_kernel':msg_kernel}
        file_socket.send(json.dumps(message).encode())
        data_file = file_socket.recv(1024).decode()
        conn.send(data_file.encode())
    
    elif cmd == 'delete':
        msg = 'deleting folder'
        msg_kernel = '[LOG] [KERNEL] ({}): {} {}'.format(date, msg, info)
        message = {'cmd':cmd, 'src':src, 'dst':dst, 'info':info, 'port':port, 'msg_user':msg_user, 'msg_kernel':msg_kernel}
        file_socket.send(json.dumps(message).encode())
        data_file = file_socket.recv(1024).decode()
        conn.send(data_file.encode())

    elif cmd == 'show':
        msg = 'showing folders'
        msg_kernel = '[LOG] [KERNEL] ({}): {}'.format(date, msg)
        message = {'cmd':cmd, 'src':src, 'dst':dst, 'info':info, 'port':port, 'msg_user':msg_user, 'msg_kernel':msg_kernel}
        file_socket.send(json.dumps(message).encode())
        data_file = file_socket.recv(1024).decode()
        conn.send(data_file.encode())

    elif cmd == 'exit':
        msg = 'connection ended with user {}'.format(port)
        msg_kernel = '[LOG] [KERNEL] ({}): {}'.format(date, msg)
        message = {'cmd':cmd, 'msg_user':msg_user, 'msg_kernel':msg_kernel}
        file_socket.send(json.dumps(message).encode())
        file_socket.close()


def send_to_application():
    return 0


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
            print(" [KERNEL] Connection from: " + str(addr))
            start_new_thread(kernel, (conn, addr))

    except Exception as error:
        print(socket.error)


## Application module
# If user sends like a 1, the application module executes the calculator, something like that