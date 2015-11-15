from Tkinter import *

def authenticate():
   print("Username: %s\nPassword: %s" % (usernameTF.get(), passwordTF.get()))


master = Tk()
master.title("airSound - The Streaming Speaker")
master.geometry("324x240")

Label(master).grid(row=0,rowspan=2)
Label(master, text = "Welcome to airSound - The Streaming Speaker\n\nPlease log in\n").grid(rowspan=2,columnspan=2, row=2)
Label(master, text="Username:").grid(row=4)
Label(master, text="Password:").grid(row=5)
Label(master).grid(row=6,rowspan=2)

usernameTF = Entry(master)
passwordTF = Entry(master, show="*")

usernameTF.grid(row=4, column=1)
passwordTF.grid(row=5, column=1)

#Button(master, text='Quit', command=master.quit).grid(row=4, column=0, sticky=W, pady=4)
Button(master, text='   Login   ', command=authenticate).grid(row=8, column=1,columnspan=2, sticky=W, pady=4)

mainloop()
