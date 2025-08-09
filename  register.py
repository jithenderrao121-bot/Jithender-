from email_validator import validate_email,EmailNotValidError
from tkinter import *
from tkinter import messagebox,Frame
import sqlite3
from password_strength import PasswordPolicy


con=sqlite3.connect("users.db")
cursor=con.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY
AUTOINCREMENT,
email TEXT UNIQUE NOT NULL,
password TEXT NOT NULL)""")
con.commit()
 
def register():
	login_frame.pack_forget()
	register_frame.pack()
	
def login():
	register_frame.pack_forget()
	login_frame.pack()
	
def check_email(mail):
	try:
		validate_email(mail,check_deliverability=False)
		return True
	except EmailNotValidError:
		return False
		
def check_password(pw):
	policy=PasswordPolicy.from_names(
	length=8,
	numbers=1,
	uppercase=1,
	special=1,
	nonletters=1
	)
	return policy.test(pw)
	
def show_password(entry):
	if entry.cget("show")=='':
		entry.configure(show="*")
	else:
		entry.configure(show="")
def clicked(email,password,password2):
	mail=email.get()
	pw1=password.get()
	pw2=password2.get() if password2 else None
	if not check_email(mail):
	 	messagebox.showerror("in valid gmail","PLEASE ENTER VALID GMAIL")
	 	return 
	 	
	if not mail or not  pw1 or (password2 and not pw2):
		messagebox.showwarning("Empty detail","Please fill the details")
		return
	
	
	if check_password(pw1):
	 	failures=check_password(pw1)
	 	messagebox.showwarning("invalid passward","MUST CONTAIN"+str(failures[0]))
	 	return 
	if password2:
		if pw1!=pw2:
			messagebox.showwarning("password not match","Password doesn't match")
			return 
		try:
			
			cursor.execute("""INSERT INTO users(email,password)VALUES(?,?)""",(mail,pw2))
			con.commit()
			messagebox.showinfo("Registration","Registration Successfull!!")
			login()
		except sqlite3.IntegrityError:
			messagebox.showwarning("EXISTS","Email already Exists")
		
	else:
		cursor.execute("""SELECT*FROM users WHERE (email=? AND password=?)""",(mail,pw1))
		result =cursor.fetchone()
		if result:
			messagebox.showinfo("Login!","Login successfull!!")
		else:
			messagebox.showerror("Error","Invalid Email or Password")




root=Tk()
root.title("login/register")
#root.geometry("850x800")
login_frame=Frame(root)
login_frame.pack()
# _______________login form__________
Label(login_frame,text="LOGIN", bg="blue",fg="white",font=("Arial",20)).pack(pady=10)
Label(login_frame,text="EMAIL:",font=("Arial",16)).pack(pady=10)
login_email=Entry(login_frame,width=30,font=("Arial",10))
login_email.pack()
Label(login_frame,text="PASSWORD",font=("Arial",16)).pack(pady=10)
login_password=Entry(login_frame,width=30,font=("Arial",10),show="*")
login_password.pack()
Checkbutton(login_frame,text="show password",command=lambda:show_password(login_password)).pack()
Button(login_frame,text="login",bg="green",fg="white",command=lambda:clicked(login_email,login_password,None)).pack(pady=50)
Button(login_frame,text="NEW REGISTER",fg="blue",command=register).pack()
##------------register form------------------
register_frame=Frame(root)


Label(register_frame,text="REGISTER", bg="blue",fg="white",font=("Arial",20)).pack(pady=10)
Label(register_frame,text="EMAIL:",font=("Arial",16)).pack(pady=10)
re_email=Entry(register_frame,width=30,font=("Arial",10))
re_email.pack()
Label(register_frame,text="PASSWORD",font=("Arial",16)).pack(pady=10)

re_password=Entry(register_frame,width=30,font=("Arial",10),show="*")
re_password.pack()
Label(register_frame,text="CONFIRM PASSWORD",font=("Arial",16)).pack(pady=10)
re_conformpw=Entry(register_frame,width=30,font=("Arial",10),show="*")
re_conformpw.pack()

Checkbutton(register_frame,text="show password",command=lambda :show_password(re_password)).pack()
Button(register_frame,text="register",bg="green",fg="white",command=lambda:clicked(re_email,re_password,re_conformpw)).pack(pady=50)
Button(register_frame,text="⬅back to login",fg="blue",command=login).pack()


root.mainloop()