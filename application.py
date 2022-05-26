import socket
import json
import os
import random
import psutil
import time
from datetime import datetime
from _thread import *

def application(kernel):

    while True:

        try:
            data_kernel = kernel.recv(1024).decode()
            if data_kernel:
                controller(data_kernel)
            
        except error:
            print(' [APP] Data reading error!')
            break

def controller(data):

    data = json.loads(data)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Comentar este método para quitar la respuesta
    msg_res = response(date)

    if data['info'] == 'calculator':
        msg_app, msg_user, pid = calculator(data['cmd'], date, data['pid'], msg_res)
        msg = {'msg_app':msg_app, 'msg_user':msg_user, 'pid':pid}
        conn.send(json.dumps(msg).encode())

    elif data['info'] == 'zoom':
        msg_app, msg_user, pid = zoom(data['cmd'], date, data['pid'], msg_res)
        msg = {'msg_app':msg_app, 'msg_user':msg_user, 'pid':pid}
        conn.send(json.dumps(msg).encode())

    elif data['info'] == 'spotify':
        msg_app, msg_user, pid = spotify(data['cmd'], date, data['pid'], msg_res)
        msg = {'msg_app':msg_app, 'msg_user':msg_user, 'pid':pid}
        conn.send(json.dumps(msg).encode())

def calculator(cmd, date, pid, response):
    
    if cmd == 'open':
        os.system('calc.exe')
        msg_app = '{}\n[LOG] [APP] ({}): calculator app was opened'.format(response, date)
        msg_user = ''
        pid = get_PID('Calculator')
        return msg_app, msg_user, pid

    elif cmd == 'close':
        os.system('taskkill /PID {} /f'.format(pid))
        msg_app = '{}\n[LOG] [APP] ({}): calculator app was closed'.format(response, date)
        msg_user = 'Calculator closed successfully!'
        pid = 0
        return msg_app, msg_user, pid

def zoom(cmd, date, pid, response):

    if cmd == 'open':
        os.startfile(r'C:\Users\Usuario\AppData\Roaming\Zoom\bin\Zoom.exe')
        msg_app = '{}\n[LOG] [APP] ({}): zoom app was opened'.format(response, date)
        msg_user = ''
        pid = get_PID('Zoom')
        return msg_app, msg_user, pid

    elif cmd == 'close':
        os.system('taskkill /PID {} /f'.format(pid))
        msg_app = '{}\n[LOG] [APP] ({}): zoom app was closed'.format(response, date)
        msg_user = 'Zoom closed successfully!'
        pid = 0
        return msg_app, msg_user, pid

def spotify(cmd, date, pid, response):
    
    if cmd == 'open':
        os.system('Spotify.exe')
        msg_app = '{}\n[LOG] [APP] ({}): spotify app was opened'.format(response, date)
        msg_user = ''
        pid = get_PID('Spotify')
        return msg_app, msg_user, pid

    elif cmd == 'close':
        os.system('taskkill /PID {} /f'.format(pid))
        msg_app = '{}\n[LOG] [APP] ({}): spotify app was closed'.format(response, date)
        msg_user = 'Spotify closed successfully!'
        pid = 0
        return msg_app, msg_user, pid

def response(date):
    # Por ahora lo haremos sin error
    number = random.randint(0, 9)

    if number <= 4:
        msg = '[LOG] [APP] ({}): OK!'.format(date)
    elif number > 4:
        msg = '[LOG] [APP] ({}): SYSTEM BUSY: waiting 3 seconds...'.format(date)
        time.sleep(3)
    elif number == 10:
        msg = '[LOG] [APP] ({}): ERROR!'.format(date)

    return msg

def find_process_by_name(process_name):

    list_of_process = []
    for proc in psutil.process_iter():
        pinfo = proc.as_dict(attrs=['pid', 'name'])
        if process_name.lower() in pinfo['name'].lower() :
            list_of_process.append(pinfo)
    return list_of_process;

def get_PID(app_name):

    list_of_process = find_process_by_name(app_name)
    process = list_of_process[-1]
    pid = process['pid']
    return pid

if __name__ == '__main__':

    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = 'localhost'
        port = 8002
        my_socket.bind( (host, port) ) 
        my_socket.listen(5) 

        print('------ Runnning Application Application ------')
        
        while True:
            conn, addr = my_socket.accept()
            print(" [APP] Connection from: " + str(addr))
            start_new_thread(application, (conn, ))

    except Exception as error:
        print(socket.error)