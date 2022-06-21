import hashlib
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial

import os
from os.path import join
import socket


class MySocket:
    def __init__(self, request):
        PORT = 5055
        SERVER = socket.gethostbyname(socket.gethostname())
        ADDR = (SERVER, PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(ADDR)
        if request == "folders":
            self.request_folder_names()
        elif "files" in request:
            self.request_files(request[5:])

    def request_files(self, folder_name):
        msg = ("getfiles" + folder_name).encode()
        msg += b' ' * (2048 - len(msg))
        self.sock.send(msg)

    def request_folder_names(self):
        msg = "getfolders".encode()
        msg += b' ' * (2048 - len(msg))
        self.sock.send(msg)

    def handle_messages(self):
        msg = self.sock.recv(2048).decode()
        return msg

    def __del__(self):
        # Runs when object destroyed
        print('Closing socket')
        self.sock.close()


sock = MySocket("folders")
folders = sock.handle_messages()
sock.__del__()
print(folders)
folders = folders.replace(" ", "").split("---")




def open_folder(folder_name):
    sock = MySocket(request='files'+folder_name)
    print(1)
    files = sock.handle_messages()
    print(files)
    files = files.replace(" ", "").split("---")
    print(2)
    screen = Tk()
    screen.title(folder_name)
    screen.geometry('600x600+300+200')
    screen.resizable(False, False)
    screen.configure(bg="#F4E9DD")
    frame = Frame(screen, bg="white")
    frame.place(relwidth=0.694, relheight=0.8, relx=0.15, rely=0.02)



    for i in range(len(files)):
        # The partial function enables to functions with args to be used in button.command
        folder_label = Label(frame, text=files[i], bg="grey", width=51, height=1, borderwidth=3,
                             relief="ridge")
        folder_label.grid(row=i, column=0)

        special_function = partial(delete, folder_name + "\\" + files[i])
        delete_folder_button = Button(frame, image=delete_icon, border=0)
        delete_folder_button.grid(row=i, column=1)

        download_folder_button = Button(frame, image=download_icon, border=0)
        download_folder_button.grid(row=i, column=2)

    screen.mainloop()


















root = Tk()
root.title('Data')
root.geometry('600x500+300+200')
root.configure(bg="#F4E9DD")
root.resizable(False, False)
frame = Frame(root, bg="white")
frame.place(relwidth=0.694, relheight=0.8, relx=0.15, rely=0.1)

refresh_icon = Image.open("refresh.png")
refresh_icon.thumbnail((50, 50))
refresh_icon = ImageTk.PhotoImage(refresh_icon)
refresh_button = Button(root, image=refresh_icon, border=0.5)
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

    # special_function = partial(delete, folders[i])
    delete_folder_button = Button(frame, image=delete_icon, border=0)
    delete_folder_button.grid(row=i, column=1)

    download_folder_button = Button(frame, image=download_icon, border=0)
    download_folder_button.grid(row=i, column=2)

root.mainloop()




