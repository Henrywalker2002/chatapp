import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
from tkinter import *

def signin(username, password):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        rc = cursor.execute("SELECT * from account WHERE username = %s and pass = %s", (username, password))
        if rc == 0:
            return False
        return True
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

def signup(name, username, password):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        rc = cursor.execute("INSERT INTO account (name, username, pass) values (%s, %s,%s)", (name,username, password))
        if rc == 0:
            return False
        return True
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()
            
def handleButtonLogin(event = None):
    username = USERNAME.get()
    password = PASSWORD.get()
    if signin(username, password):
        HomeWindow()
        USERNAME.set('')
        PASSWORD.set('')
        lbl_text = ""
    else:
        lbl_text.config(text="Invalid username or password", fg="red")
        USERNAME.set("")
        PASSWORD.set("") 

def HomeWindow():
    global Home
    root.withdraw()
    Home = Toplevel()
    Home.title("Python: Simple Login Application")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.resizable(0, 0)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    lbl_home = Label(Home, text="Successfully Login!", font=('times new roman', 20)).pack()

root = Tk()
root.title("Python: Simple Login Application")
width = 400
height = 280
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

USERNAME = StringVar()
PASSWORD = StringVar()
 
#==============================FRAMES=========================================
Top = Frame(root, bd=2,  relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(root, height=200)
Form.pack(side=TOP, pady=20)
 
#==============================LABELS=========================================
lbl_title = Label(Top, text = "Python: Simple Login Application", font=('arial', 15))
lbl_title.pack(fill=X)
lbl_username = Label(Form, text = "Username:", font=('arial', 14), bd=15)
lbl_username.grid(row=0, sticky="e")
lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
lbl_password.grid(row=1, sticky="e")
global lbl_text
lbl_text = Label(Form)
lbl_text.grid(row=2, columnspan=2)
 
#==============================ENTRY WIDGETS==================================
username = Entry(Form, textvariable=USERNAME, font=(14))
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
password.grid(row=1, column=1)
 
#==============================BUTTON WIDGETS=================================
btn_login = Button(Form, text="Login", width=45, command=handleButtonLogin)
btn_login.grid(pady=25, row=3, columnspan=2)
btn_login.bind('<Return>', signin)

root.mainloop()