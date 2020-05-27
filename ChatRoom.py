# Python program to build Chat Room Application.
import requests
import time
from threading import *
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import tkinter as tk

def DestroyLoginWindow():
	signinup_button.destroy()
	username_label.destroy()
	username_textbox.destroy()
	password_label.destroy()
	password_textbox.destroy()
	linkforSignupin.destroy()
	signinup_lbl.destroy()

def GenerateTextboxes():
	global username_label, username_textbox, password_label, password_textbox
	username_label = Label(window, text = "Username: ")
	username_label.pack()
	username_textbox = Entry(window)
	username_textbox.pack()
	password_label = Label(window, text = "Password: ")
	password_label.pack()
	password_textbox = Entry(window)
	password_textbox.pack()

def ShowSignInWindow():
	global login_button, text, linkforSignupin, signinup_button, signinup_lbl
	if signup_window_visible_status:
		signinup_lbl['text'] = 'Login Window'
		signinup_button.configure(text = "Sign In", command=ValidateSignIn)
		linkforSignupin['text'] = 'No Account? Click here to register'
		linkforSignupin.bind("<Button-1>", lambda e: ShowSignUpWindow())
	else:
		signinup_lbl = Label(window, text="Login to Chat Room")
		signinup_lbl.pack()
		GenerateTextboxes()
		signinup_button = Button(window, text="Sign In", command=ValidateSignIn)
		signinup_button.place(x = 210, y = 120)
		linkforSignupin = Label(window, text="No Account? Click here to register", fg="blue", cursor="hand2")
		linkforSignupin.place(x = 160, y = 150)
		linkforSignupin.configure(anchor="center")
		linkforSignupin.bind("<Button-1>", lambda e: ShowSignUpWindow())

def ShowSignUpWindow():
	global signup_window_visible_status
	signup_window_visible_status = 1
	signinup_lbl['text'] = 'Registration Window'
	linkforSignupin['text'] = 'Already registered! Sign In'
	linkforSignupin.bind("<Button-1>", lambda e: ShowSignInWindow())
	signinup_button.configure(text = "Sign Up", command = SignUp)

def ShowChatWindow():
	global chat_lbl, active_users_lbl, active_users_textbox, chatbox_lbl, chatbox, message_box, send_button, signout_button
	DestroyLoginWindow()	

	chat_lbl = Label(window, text="Chat Window")
	chat_lbl.pack()

	active_users_lbl = Label(window, text="Users Online")
	active_users_lbl.pack()

	active_users_textbox = Text(window, height=5, width=40)
	active_users_textbox.pack()

	chatbox_lbl = Label(window, text="Chat Box")
	chatbox_lbl.pack()

	chatbox = Text(window, width = 40, height = 20, wrap = WORD)
	chatbox.config(state = DISABLED) 
	chatbox.pack()

	message_box = Entry(width=40)
	message_box.place(x = 88, y = 510)

	send_button = Button(window, text="Send", command=SendMessage)
	send_button.place(x = 415, y = 505)

	signout_button = Button(window, text="Signout", command=SignOut)
	signout_button.place(x = 210, y = 535)

def SignOut():
	global login_status
	login_status = 0
	chat_lbl.destroy()
	active_users_lbl.destroy()
	chatbox_lbl.destroy()
	chatbox.destroy()
	send_button.destroy()
	signout_button.destroy()
	message_box.destroy()
	active_users_textbox.destroy()
	try:
		ShowSignInWindow()
	except:
		ShowSignInWindow()

def GetUserNameAndPassword():
	global UserName, Password
	UserName = username_textbox.get();
	Password = password_textbox.get();

def GetActiveUsersData():
	try:
		while True:
			response = my_session.get(f'{url}GetActiveUsersData.jsp?UserName={UserName}')
			active_users_textbox.config(state = 'normal')
			active_users_textbox.delete('1.0', END)
			active_users_textbox.insert(1.0, response.text.replace("&#8226;", "-->"))
			active_users_textbox.yview('end')
			active_users_textbox.config(state = DISABLED)
	except:
		print('',end = '')

def GetMessages():
	try:
		while login_status:
			response = my_session.get(f'{url}GetMessage.jsp?UserName={UserName}')
			chatbox.config(state = 'normal')
			chatbox.delete('1.0', END)
			chatbox.insert(1.0, response.text)
			chatbox.yview('end')
			chatbox.config(state = DISABLED)
	except:
		print('',end = '')

def SendMessage():
	Message = message_box.get()
	message_box.delete(0, last=END)
	response = my_session.get(f'{url}SendMessage.jsp?UserName={UserName}&Message={Message}');
	# if(str(response).find("200") >= 0):
	# 	messagebox.showinfo('status', 'Message sent successfully.')

def ValidateSignIn():
	global login_status
	GetUserNameAndPassword()
	if UserName and Password:
		response = my_session.get(f'{url}Login.jsp?UserName={UserName}&Password={Password}');
		# print(str(response.text))
		if (response.text.find("Success") >= 0):
			messagebox.showinfo('Success', 'Login Successful.')
			ShowChatWindow()
			login_status = 1

			Thread(target = GetActiveUsersData).start()
			Thread(target = GetMessages).start()

		elif(response.text.find("Failed") >= 0):
			messagebox.showinfo('Failed', 'Invalid Login Credentials.')
	else:
		messagebox.showinfo('Warning', 'Please fill the required details.')


def SignUp():
	GetUserNameAndPassword()
	if UserName and Password:
		response = my_session.get(f'{url}Register.jsp?UserName={UserName}&Password={Password});');
		if (response.text.find("Registered") >= 0):
			messagebox.showinfo('Success', 'Registered Successfully.')
			ShowSignInWindow()
		elif response.text:
			messagebox.showinfo('Registration Failed', response.text)
	else:
		messagebox.showinfo('Warning', 'Please fill the required details.')

def CreateConnection():
	response = my_session.get(f'{url}Connection.jsp?mode=A')
	# print(str(response.text))

url = 'http://165.22.14.77:8080/Anwesh/Chat/'
my_session = requests.Session()
signup_window_visible_status = 0
login_status = 0
window = Tk()
window.geometry('500x600')
window.resizable(0, 0)
window.title('Chat Room')
ShowSignInWindow()
CreateConnection()
mainloop()
