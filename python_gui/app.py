from Tkinter import *
import tkMessageBox

"""Section to define functions"""
def authenticate():
#	print("Username: %s\nPassword: %s" % (usernameTF.get(), passwordTF.get()))
	log = (usernameTF.get() == "a") & (passwordTF.get() == "pi") 
	if (log):
		option_frame()
	else: 
		passwordTF.delete(0,END)
		tkMessageBox.showinfo("Invalid Information","Username or Password incorrect\nPlease try again")

def raise_frame(frame):
	frame.tkraise() 

def raise_and_destroy_frame(frame1,*frameL):
	frame1.tkraise() 
	for f in frameL:
		f.destroy()

def play_song(songlist):
	try:
		print songlist.get(songlist.curselection())
	except:
		print ("Nothing is selected")

def option_frame():
	"""Section to define OPTION frame"""
	raise_frame(option)
	Button(option, text='Song List', command=songList_frame).grid(row=1, column=0, padx=20, pady=20)
	Button(option, text='Playlist').grid(row=1, column=1, padx=10) 
	Button(option, text='Back', command=lambda:raise_frame(login)).grid(row=10)
	
def songList_frame():
	raise_frame(songList)
	songListC = Frame(songList)
	songListC1 = Frame(songList)
	songListC.pack(fill=BOTH, expand="true", padx=10)
	songListC1.pack(side=BOTTOM)
	scrollbar = Scrollbar(songListC)
	myList = Listbox(songListC, yscrollcommand = scrollbar.set)
	for line in range (100):
		myList.insert(END, "This is line number " + str(line))
	myList.pack(side = LEFT, fill=BOTH, expand = "true")
	scrollbar.pack(side = RIGHT, fill=Y)
	scrollbar.config(command = myList.yview)
	Button(songListC1, text='Back', command=lambda:raise_and_destroy_frame(option,songListC, songListC1)).pack(side = LEFT)
	Button(songListC1, text='Play', command=lambda:play_song(myList)).pack(side=LEFT, padx=40)



"""Section for frames creating"""
root = Tk()
root.title("airSound - The Streaming Speaker")
root.geometry("324x240")

login = Frame(root)
option = Frame(root)
songList = Frame(root)

for frame in (login, option, songList):
	frame.grid(row=0, column=0, sticky='news')
raise_frame(login) 


"""Section for 'login' frame""" 
Label(login).grid(row=0,rowspan=2)
Label(login, text = "Welcome to airSound - The Streaming Speaker\n\nPlease log in\n").grid(rowspan=2,columnspan=2, row=2)
Label(login, text="Username:").grid(row=4)
Label(login, text="Password:").grid(row=5)
Label(login).grid(row=6,rowspan=2)

usernameTF = Entry(login)
passwordTF = Entry(login, show="*")

usernameTF.grid(row=4, column=1)
passwordTF.grid(row=5, column=1)

#Button(login, text='Next Frame', command=lambda:raise_frame(option)).grid(row=9, column=1, sticky=W, pady=4)
Button(login, text='Login', command=authenticate).grid(row=8,columnspan=2, pady=4)



mainloop()
