import socket
import json
import tkinter as tk
from tkinter import DISABLED, messagebox, ttk
from datetime import datetime
from tkinter.font import NORMAL

pid_calculator = 0
pid_zoom = 0
pid_spotify = 0

def gui():

    my_socket = socket.socket()
    my_socket.connect( ('localhost', 8000) ) # Se conecta al kernel

    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    root = tk.Tk()
    root.config(width=600, height=400)
    root.title("GUI")

    # File Manager
    label_file = ttk.Label(text='File Manager')
    label_file.place(x=50, y=50)

    entry_create = ttk.Entry()
    button_create = ttk.Button(text="Create folder", command=lambda: create(my_socket, entry_create, date))
    button_create.bind("<Return>", create)
    button_create.place(x=50, y=80)
    entry_create.place(x=150, y=80)

    entry_delete = ttk.Entry()
    button_delete = ttk.Button(text="Delete folder", command=lambda: delete(my_socket, entry_delete, date))
    button_delete.bind("<Return>", delete)
    button_delete.place(x=50, y=110)  
    entry_delete.place(x=150, y=110)

    button_show = ttk.Button(text='Show folders', command=lambda: show_folders(my_socket, date, list))
    button_show.bind("<Return>", show_folders)
    button_show.place(x=50, y=140)

    list = tk.Listbox()
    list.place(x=50, y=170)

    # Applications
    label_app = ttk.Label(text='Applications')
    label_app.place(x=350, y=50)

    button_app1 = ttk.Button(text='Calculator', command=lambda: open_calculator(my_socket, date, button_app1_c))
    button_app1.bind('<Return>', open_calculator)
    button_app1.place(x=350, y=80)

    button_app2 = ttk.Button(text='Zoom', command=lambda: open_zoom(my_socket, date, button_app2_c))
    button_app2.bind('<Return>', open_zoom)
    button_app2.place(x=350, y=110)

    button_app3 = ttk.Button(text='Spotify', command=lambda: open_spotify(my_socket, date, button_app3_c))
    button_app3.bind('<Return>', open_spotify)
    button_app3.place(x=350, y=140)

    # Close Buttons
    button_app1_c = ttk.Button(text='Close', state=DISABLED, command=lambda: close_calculator(my_socket, date, button_app1_c, pid_calculator))
    button_app1_c.bind('<Return>', close_calculator)
    button_app1_c.place(x=450, y=80)

    button_app2_c = ttk.Button(text='Close', state=DISABLED, command=lambda: close_zoom(my_socket, date, button_app2_c, pid_zoom))
    button_app2_c.bind('<Return>', close_zoom)
    button_app2_c.place(x=450, y=110)

    button_app3_c = ttk.Button(text='Close', state=DISABLED, command=lambda: close_spotify(my_socket, date, button_app3_c, pid_spotify))
    button_app3_c.bind('<Return>', close_spotify)
    button_app3_c.place(x=450, y=140)

    # Exit
    button_exit = ttk.Button(text="Exit", command=lambda: exit(my_socket, date))
    button_exit.bind("<Return>", exit)
    button_exit.place(x=260, y=300)

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

def show_folders(socket, date, list):

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
        list.delete(0, tk.END)
        messagebox.showinfo(message=folder_list, title="show")
    else:
        list.delete(0, tk.END)
        i = 0
        for folder in folder_list:
            list.insert(i, folder)
            i += 1

def open_calculator(socket, date, button):

    command = 'open calculator'
    cmd = 'open'
    src = 'gui'
    dst = 'application'
    message = '[LOG] [USER] ({}): {}'.format(date, command)
    app = 'calculator'
    msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':app, 'msg':message, 'pid':''}
    socket.send(json.dumps(msg).encode())
    
    kernel_data = socket.recv(1024).decode()
    kernel_data = json.loads(kernel_data)
    global pid_calculator
    pid_calculator = kernel_data['pid']
    if len(kernel_data['msg_user']) < 1:
        button['state'] = NORMAL

def close_calculator(socket, date, button, pid):

    command = 'close calculator'
    cmd = 'close'
    src = 'gui'
    dst = 'application'
    message = '[LOG] [USER] ({}): {}'.format(date, command)
    app = 'calculator'
    msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':app, 'msg':message, 'pid':pid}
    socket.send(json.dumps(msg).encode())
    
    kernel_data = socket.recv(1024).decode()
    kernel_data = json.loads(kernel_data)
    if len(kernel_data['msg_user']) > 0:
        button['state'] = DISABLED
        messagebox.showinfo(message=kernel_data['msg_user'], title="closed")

def open_zoom(socket, date, button):
    
    command = 'open zoom'
    cmd = 'open'
    src = 'gui'
    dst = 'application'
    message = '[LOG] [USER] ({}): {}'.format(date, command)
    app = 'zoom'
    msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':app, 'msg':message, 'pid':''}
    socket.send(json.dumps(msg).encode())
    
    kernel_data = socket.recv(1024).decode()
    kernel_data = json.loads(kernel_data)
    global pid_zoom
    pid_zoom = kernel_data['pid']
    if len(kernel_data['msg_user']) < 1:
        button['state'] = NORMAL

def close_zoom(socket, date, button, pid):

    command = 'close zoom'
    cmd = 'close'
    src = 'gui'
    dst = 'application'
    message = '[LOG] [USER] ({}): {}'.format(date, command)
    app = 'zoom'
    msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':app, 'msg':message, 'pid':pid}
    socket.send(json.dumps(msg).encode())
    
    kernel_data = socket.recv(1024).decode()
    kernel_data = json.loads(kernel_data)
    if len(kernel_data['msg_user']) > 0:
        button['state'] = DISABLED
        messagebox.showinfo(message=kernel_data['msg_user'], title="closed")

def open_spotify(socket, date, button):

    command = 'open spotify'
    cmd = 'open'
    src = 'gui'
    dst = 'application'
    message = '[LOG] [USER] ({}): {}'.format(date, command)
    app = 'spotify'
    msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':app, 'msg':message, 'pid':''}
    socket.send(json.dumps(msg).encode())
    
    kernel_data = socket.recv(1024).decode()
    kernel_data = json.loads(kernel_data)
    global pid_spotify
    pid_spotify = kernel_data['pid']
    if len(kernel_data['msg_user']) < 1:
        button['state'] = NORMAL

def close_spotify(socket, date, button, pid):

    command = 'close spotify'
    cmd = 'close'
    src = 'gui'
    dst = 'application'
    message = '[LOG] [USER] ({}): {}'.format(date, command)
    app = 'spotify'
    msg = {'cmd':cmd, 'src':src, 'dst':dst, 'info':app, 'msg':message, 'pid':pid}
    socket.send(json.dumps(msg).encode())
    
    kernel_data = socket.recv(1024).decode()
    kernel_data = json.loads(kernel_data)
    if len(kernel_data['msg_user']) > 0:
        button['state'] = DISABLED
        messagebox.showinfo(message=kernel_data['msg_user'], title="closed")

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
    gui()