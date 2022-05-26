import socket
import json
import os
import random
import time
from datetime import datetime
from _thread import *

def file_manager(kernel, addr):

    while True:

        try:
            data_kernel = kernel.recv(1024).decode()
            if data_kernel:
                controller(data_kernel, addr)
            
        except error:
            print(' [FILE] Data reading error!')
            break

def controller(data, addr):

    data = json.loads(data)
    port = addr[1]
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_name = '{}/log.txt'.format(port)

    if not os.path.exists(str(port)):
        os.mkdir(str(port))
    
    if 'msg_user' in data: write_log(log_name, data['msg_user'])
    if 'msg_kernel' in data: write_log(log_name, data['msg_kernel'])
    if 'msg_app' in data: write_log(log_name, data['msg_app'])

    # Comentar este método para quitar la respuesta
    if not 'msg_app' in data:
        response(log_name, date)

    if data['cmd'] == 'create':
        msg_user, msg_log = create_folder(port, data['info'], date)
        write_log(log_name, msg_log)
        conn.send(msg_user.encode())

    elif data['cmd'] == 'delete':
        msg_user, msg_log = delete_folder(port, data['info'], date)
        write_log(log_name, msg_log)
        conn.send(msg_user.encode())

    elif data['cmd'] == 'show':
        msg_user, msg_log = show_folders(port, date)
        write_log(log_name, msg_log)
        conn.send(json.dumps(msg_user).encode())

    elif data['cmd'] == 'exit':
        print(" [FILE] Conneciton finished: " + str(addr))
        msg_log = '[LOG] [FILE] ({}): connection ended with kernel'.format(date)
        write_log(log_name, msg_log)

def create_folder(port, name, date):

    folder_name = '{}/{}'.format(port, name)

    if os.path.exists(folder_name):
        msg_user = 'Folder {} already exists!'.format(name)
        msg_log = '[LOG] [FILE] ({}): folder {} already exists!'.format(date, name)
        return msg_user, msg_log
    else:
        os.mkdir(folder_name)
        msg_user = 'Folder {} has been created!'.format(name)
        msg_log = '[LOG] [FILE] ({}): folder {} has been created!'.format(date, name)
        return msg_user, msg_log

def delete_folder(port, name, date):

    folder_name = '{}/{}'.format(port, name)

    if os.path.exists(folder_name):
        os.rmdir(folder_name)
        msg_user = 'Folder {} has been deleted!'.format(name)
        msg_log = '[LOG] [FILE] ({}): folder {} has been deleted!'.format(date, name)
        return msg_user, msg_log
    else:
        msg_user = 'Folder {} does not exists!'.format(name)
        msg_log = '[LOG] [FILE] ({}): folder {} does not exists!'.format(date, name)
        return msg_user, msg_log

def show_folders(port, date):
    
    folders = []

    if len(os.listdir(str(port))) > 1:
        files = os.listdir(str(port))
        for f in files:
            dir = '{}/{}'.format(port, f)
            if os.path.isdir(dir):
                folders.append(f)
        
        msg_user = folders
        msg_log = '[LOG] [FILE] ({}): sending the following folders {}'.format(date, folders)
        return msg_user, msg_log
    else:
        msg_user = 'No folder has been created'
        msg_log = '[LOG] [FILE] ({}): no folder has been created'.format(date)
        return msg_user, msg_log

def write_log(name, msg):

    if os.path.exists(name):
        file = open(name, 'a')
        file.write('{}\n'.format(msg))
        file.close()
    else:
        file = open(name, 'w')
        file.write('{}\n'.format(msg))
        file.close()

def response(log_name, date):
    # Por ahora lo haremos sin error
    number = random.randint(0, 9)

    if number <= 4:
        msg = '[LOG] [FILE] ({}): OK!'.format(date)
        write_log(log_name, msg)
    elif number > 4:
        msg = '[LOG] [FILE] ({}): SYSTEM BUSY: waiting 3 seconds...'.format(date)
        write_log(log_name, msg)
        time.sleep(3)
    elif number == 10:
        msg = '[LOG] [FILE] ({}): ERROR!'.format(date)
        write_log(log_name, msg)

if __name__ == '__main__':

    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = 'localhost'
        port = 8001
        my_socket.bind( (host, port) ) 
        my_socket.listen(5) 

        print('------ Runnning File Manager Application ------')
        
        while True:
            conn, addr = my_socket.accept()
            print(" [FILE] Connection from: " + str(addr))
            start_new_thread(file_manager, (conn, addr))

    except Exception as error:
        print(socket.error)