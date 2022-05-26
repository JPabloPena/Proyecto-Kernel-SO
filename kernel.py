import socket
import json
from datetime import datetime
from _thread import *

def kernel(client, addr):

    file_socket = socket.socket()
    file_socket.connect( ('localhost', 8001) ) # Se conecta al file_manager

    app_socket = socket.socket()
    app_socket.connect( ('localhost', 8002) ) # Se conecta a applications

    while True:

        try:
            data_user = client.recv(1024).decode()
            if data_user:
                controller(data_user, addr, file_socket, app_socket)
            
        except error:
            print(' [KERNEL] Data reading error!')
            break

def controller(data, addr, file_socket, app_socket):
    
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
        send_to_application(data['cmd'], data['src'], data['dst'], data['info'], data['msg'], data['pid'], port, file_socket, app_socket)
    
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

def send_to_application(cmd, src, dst, info, msg_user, pid, port, file_socket, app_socket):

    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    if cmd == 'open':
        msg = 'opening {} app'.format(info)
        msg_kernel = '[LOG] [KERNEL] ({}): {}'.format(date, msg)
        app_message = {'cmd':cmd, 'info':info, 'pid':pid}
        app_socket.send(json.dumps(app_message).encode())

        data_app = app_socket.recv(1024).decode()
        data_app = json.loads(data_app)

        file_message = {'cmd':cmd, 'src':src, 'dst':dst, 'info':info, 'port':port, 'msg_user':msg_user, 'msg_kernel':msg_kernel, 'msg_app':data_app['msg_app']}
        file_socket.send(json.dumps(file_message).encode()) # Escribe en el log lo del usuario       
        conn.send(json.dumps(data_app).encode())

    elif cmd == 'close':
        msg = 'closing {} app'.format(info)
        msg_kernel = '[LOG] [KERNEL] ({}): {}'.format(date, msg)
        app_message = {'cmd':cmd, 'info':info, 'pid':pid}
        app_socket.send(json.dumps(app_message).encode())

        data_app = app_socket.recv(1024).decode()
        data_app = json.loads(data_app)

        file_message = {'cmd':cmd, 'src':src, 'dst':dst, 'info':info, 'port':port, 'msg_user':msg_user, 'msg_kernel':msg_kernel, 'msg_app':data_app['msg_app']}
        file_socket.send(json.dumps(file_message).encode()) # Escribe en el log lo del usuario       
        conn.send(json.dumps(data_app).encode())

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