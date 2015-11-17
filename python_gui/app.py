from Tkinter import *
import tkMessageBox
import MySQLdb
"""Section to define global variables"""
##########
"""Section to define functions"""
def login_frame():
	raise_frame(login)
def authenticate():
	username = usernameTF.get()
	password = passwordTF.get()
	hashkey = 0
	for c in password:
		hashkey += ord(c) % 16

	authen = [username, hashkey, password[0]]


	sql = """select * from authentication;"""
	try:
   		db = MySQLdb.connect("localhost", "root", "Phuongngo56", "testing")
		cursor = db.cursor()	
		log = False
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			valid = 0
			for i in range (0,3):
				if (authen[i] == row[i]):
					valid += 1;	
			if (valid == 3):
				log = True
				break
		if (log):
			sql = """use %s""" % authen [0]
			cursor.execute(sql) 
			option_frame()
			db.commit()
		else:
			passwordTF.delete(0,END)
			tkMessageBox.showinfo("Invalid Information","Invalid Username or Password\nPlease try again")
			db.rollback()
	except:
		print "Cannot connect to database"	

def raise_frame(frame):
	frame.tkraise() 

def raise_and_destroy_frame(frame1,*frameL):
	for f in frameL:
		f.destroy()
	frame1()

def play_song(songlist, *frame):
	try:
		playingSong = songlist.get(songlist.curselection())
		test = playingSong
		if (playingSong):
			for f in frame:
				f.destroy()
			playSong_frame(playingSong)
	except:
		tkMessageBox.showinfo("Invalid Selection","Please choose a song from the list")

def option_frame():
	"""Section to define OPTION frame"""
	raise_frame(option)
	Button(option, text='Song List', command=songList_frame).grid(row=1, column=0, padx=20, pady=20)
	Button(option, text='Playlist').grid(row=1, column=1, padx=10) 
	Button(option, text='Quit', command=lambda:raise_frame(login)).grid(row=10)
	
def register_frame():
	"""Section to define REGISTER frame"""
	raise_frame(register)		
	registerC1 = Frame(register)
	registerC1.pack(fill=BOTH, expand="true", padx=10)
	#Button(registerC1, text='Quit', command=lambda:raise_frame(login)).pack()
	Button(registerC1, text='Cancel', command=lambda:raise_and_destroy_frame(login_frame, registerC1)).pack()


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
	Button(songListC1, text='Back', command=lambda:raise_and_destroy_frame(option_frame,songListC, songListC1)).pack(side = LEFT)
	Button(songListC1, text='Play', command=lambda:play_song(myList, songListC, songListC1)).pack(side=LEFT, padx=40)


def playSong_frame(song):
	raise_frame(playSong)
	playSongC = Frame(playSong)
	playSongC.pack(fill=BOTH, expand="true", padx=10)
	Label(playSongC, text=song).pack(side=LEFT)
	Button(playSongC, text='Back', command=lambda:raise_and_destroy_frame(songList_frame,playSongC)).pack(side = LEFT)

#############
""" Section for frames creating"""
root = Tk()
root.title("airSound - The Streaming Speaker")
root.geometry("324x240")

login = Frame(root)
register = Frame(root)
option = Frame(root)
songList = Frame(root)
playSong = Frame(root)

for frame in (login, option, songList, playSong, register):
	frame.grid(row=0, column=0, sticky='news')

login_frame()

"""Section for 'login' frame""" 
Label(login).grid(row=0,rowspan=2)
Label(login, text = "Welcome to airSound - The Streaming Speaker\n\nPlease sign in\n").grid(rowspan=2,columnspan=2, row=2)
Label(login, text="Username:").grid(row=4)
Label(login, text="Password:").grid(row=5)
Label(login).grid(row=6,rowspan=2)

usernameTF = Entry(login)
passwordTF = Entry(login, show="*")

usernameTF.grid(row=4, column=1)
passwordTF.grid(row=5, column=1)

Button(login, text='Sign In', command=authenticate).grid(row=8,column = 0, pady=4)

Button(login, text='Register', command=register_frame).grid(row=8,column = 1, pady=4)


mainloop()
