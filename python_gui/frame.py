# simple GUI 
# use show the version of Python
# $ python -V

from Tkinter import *




# create the window
root = Tk()

#modify root window
root.title("airSound - The Streaming Speaker")
root.geometry("324x240")

# create the frame
app = Frame(root)
app1 = Frame(root)
app.grid()	# put the frame on to grid to show it, have to put the frame onto grid for all other widgets to show
app1.grid()

# create the welcome label on the login page
loginLabel = Label(app, text = "Welcome to airSound - The Streaming Speaker\nPlease log in\n")
loginLabel.grid(row=0)	# put the label on grid to show it

#username label
usernameLabel = Label(app)
usernameLabel = Label(app, text = "Username:")
usernameLabel.grid(row=1)

#Username text field
usernameTF = Entry(app).grid(row=2)


#password label
passwordLabel = Label(app)
passwordLabel = Label(app, text = "Password:")
passwordLabel.grid(row=3)

#Username text field
passwordTF = Entry(app, show="*").grid(row=4)

###############
# 1st way to create a button with text
loginButton = Button(app, text = "Log In")
loginButton.grid(row=5, column=0)

## 2nd way to write text in a button 
#button2 = Button(app)
#button2.configure(text = "Second")
#button2.grid(row=2,column=1)
#
## 3rd way to write text in a button
#button3 = Button(app)
#button3["text"] = "Third"
#button3.grid(row=2,column=2)
#
##kick of the event loop
##scrollbar = Scale(app,orient=HORIZONTAL, length=320)
##scrollbar.grid(row=2,column=0)
root.mainloop()
