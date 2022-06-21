import hashlib
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial

import os
from os.path import join


def sign_in():

    hashed_username = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
    hashed_password = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
    username = user.get()
    password = code.get()
    if hashlib.sha256(username.encode('utf-8')).hexdigest() == hashed_username and hashlib.sha256(
            password.encode('utf-8')).hexdigest() == hashed_password:
        root.destroy()
        import mainscreen
    else:
        messagebox.showerror(title="ERROR", message="wrong password or username")




root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)


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



