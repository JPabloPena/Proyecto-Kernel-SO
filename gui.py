import socket
import json
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

def gui():

    my_socket = socket.socket()
    my_socket.connect( ('localhost', 8000) ) # Se conecta al kernel

    while True:

        command = input(' >').lower().strip()
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if command == 'create folder':
            cmd = 'create'
            src = 'gui'
            dst = 'file manager'
            name = 'folder_test'
            message = '[LOG] [USER] ({}): {}'.format(date, command)
            msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':name, 'msg':message}
            my_socket.send(json.dumps(msg).encode())
            kernel_data = my_socket.recv(1024).decode()
            print(kernel_data)

        elif command == 'delete folder':
            cmd = 'delete'
            src = 'gui'
            dst = 'file manager'
            name = 'folder_test'
            message = '[LOG] [USER] ({}): {}'.format(date, command)
            msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':name, 'msg':message}
            my_socket.send(json.dumps(msg).encode())
            kernel_data = my_socket.recv(1024).decode()
            print(kernel_data)

        elif command == 'exit':
            cmd = 'exit'
            message = '[LOG] [USER] ({}): {}'.format(date, command)
            msg = {'cmd':cmd, 'msg':message}
            my_socket.send(json.dumps(msg).encode())
            kernel_data = my_socket.recv(1024).decode()
            print(kernel_data)
            break

        else:
            print(' [x] Try again!')
    
    my_socket.close() # Se termina la conexión con el servidor

def myInterface():

    my_socket = socket.socket()
    my_socket.connect( ('localhost', 8000) ) # Se conecta al kernel

    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    root = tk.Tk()
    root.config(width=600, height=400)
    root.title("GUI")

    entry_create = ttk.Entry()
    button_create = ttk.Button(text="Create folder", command=lambda: create(my_socket, entry_create, date))
    button_create.bind("<Return>", create)
    button_create.place(x=50, y=50)
    entry_create.place(x=150, y=50)

    entry_delete = ttk.Entry()
    button_delete = ttk.Button(text="Delete folder", command=lambda: delete(my_socket, entry_delete, date))
    button_delete.bind("<Return>", delete)
    button_delete.place(x=50, y=100)  
    entry_delete.place(x=150, y=100)

    button_show = ttk.Button(text='Show folders', command=lambda: show_folders(my_socket, date))
    button_show.bind("<Return>", show_folders)
    button_show.place(x=50, y=150)

    button_exit = ttk.Button(text="Exit", command=lambda: exit(my_socket, date))
    button_exit.bind("<Return>", exit)
    button_exit.place(x=270, y=190)

    root.mainloop()

def create(socket, entry, date):

    command = 'create folder'
    cmd = 'create'
    src = 'gui'
    dst = 'file manager'
    name = entry.get()
    entry.delete(0, tk.END)
    message = '[LOG] [USER] ({}): {}'.format(date, command)
    msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':name, 'msg':message}
    socket.send(json.dumps(msg).encode())
    kernel_data = socket.recv(1024).decode()
    messagebox.showinfo(message=kernel_data, title="created")

def delete(socket, entry, date):

    command = 'delete folder'
    cmd = 'delete'
    src = 'gui'
    dst = 'file manager'
    name = entry.get()
    entry.delete(0, tk.END)
    message = '[LOG] [USER] ({}): {}'.format(date, command)
    msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':name, 'msg':message}
    socket.send(json.dumps(msg).encode())
    kernel_data = socket.recv(1024).decode()
    messagebox.showinfo(message=kernel_data, title="deleted")

def show_folders(socket, date):

    command = 'show folders'
    cmd = 'show'
    src = 'gui'
    dst = 'file manager'
    message = '[LOG] [USER] ({}): {}'.format(date, command)
    msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':'', 'msg':message}
    socket.send(json.dumps(msg).encode())
    kernel_data = socket.recv(1024).decode()
    folder_list = json.loads(kernel_data)
    if isinstance(folder_list, str):
        messagebox.showinfo(message=folder_list, title="show")
    else:
        print(folder_list)
        # mostrar folders en labels

def exit(socket, date):

    cmd = 'exit'
    message = '[LOG] [USER] ({}): {}'.format(date, cmd)
    msg = {'cmd':cmd, 'msg':message}
    socket.send(json.dumps(msg).encode())
    kernel_data = socket.recv(1024).decode()
    messagebox.showinfo(message=kernel_data, title="bye")
    socket.close()
    quit()

if __name__ == '__main__':
    myInterface()