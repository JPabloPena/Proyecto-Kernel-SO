from cgi import test
import socket
import os

def create_folder(name):

    if os.path.exists(name):
        print('Folder {} already exists!'.format(name))
    else:
        os.mkdir(name)

def delete_folder(name):

    if os.path.exists(name):
        os.rmdir(name)
    else:
        print('Folder {} does not exists!'.format(name))
