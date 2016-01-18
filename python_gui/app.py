from Tkinter import *
import tkMessageBox
import MySQLdb
import boto
import boto.s3.connection
from boto.s3.connection import S3Connection
from boto.s3.key import Key
"""Section to define global variables"""
access_key = ''
secret_key = ''
##########
"""Section to define functions"""
def connectDB(dbName):
	db = MySQLdb.connect("localhost", "root", "Phuongngo56", dbName)
	return db 

def login_frame():
	raise_frame(login)
def authenticate():
	userdbName = userdbNameTF.get()
	password = passwordTF.get()
	hashkey = 0
	if (len(userdbName) == 0 or len(password) == 0):
		passwordTF.delete(0,END)
		tkMessageBox.showinfo("Invalid Information","Invalid User Name or Password\nPlease try again")
	else:	
		for c in password:
			hashkey += ord(c) % 16
		authen = [userdbName, hashkey, password[0]]
		sql = """select * from authentication;"""
		try:
   			db = connectDB("AUTHENTICATION")
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
				dbName = authen[0]
		#		sql = """use %s""" % dbName  
		#		cursor.execute(sql) 
				option_frame(dbName)
				db.commit()
			else:
				passwordTF.delete(0,END)
				db.rollback()
				tkMessageBox.showinfo("Invalid Information","Invalid User Name or Password\nPlease try again")
		except:
			tkMessageBox.showinfo("Cannot connect to database")
		db.close()
def raise_frame(frame):
	frame.tkraise() 

def raise_and_destroy_frame(dbName,frame,*frameL):
	for f in frameL:
		f.destroy()
	frame(dbName)

def cancel_and_return(frame, *frameL):
	for f in frameL:
		f.destroy()	
	frame()
def register_frame():
	"""Section to define REGISTER frame"""
	raise_frame(register)		
	registerC = Frame(register)
	registerC1 = Frame(register)
	registerC.grid() 
	registerC1.grid()
	Label(registerC, text="Please enter information").grid(row=0, pady=25, columnspan=2)
	Label(registerC, text="UserName:").grid(row=1,column=0, padx=10)
	Label(registerC, text="Password:").grid(row=2,column=0, padx=10)
	Label(registerC, text="Confirm Password:").grid(row=3,column=0, padx=10,pady=15)
	regUserdbNameTF = Entry(registerC)
	regPasswordTF = Entry(registerC, show="*")
	confirmRegPasswordTF = Entry(registerC, show="*")
	####
	regUserdbNameTF.grid(row=1, column=1, padx=10)
	regPasswordTF.grid(row=2,column=1, padx=10)
	confirmRegPasswordTF.grid(row=3,column=1, padx=10,pady=15)
	####
	Button(registerC1, text='Cancel', command=lambda:cancel_and_return(login_frame, registerC, registerC1)).pack(side=LEFT, pady=10)
	Button(registerC1, text='Register', command=lambda:test(regUserdbNameTF.get(), regPasswordTF.get(), confirmRegPasswordTF.get(), registerC, registerC1)).pack(side=RIGHT,padx=30,pady=10)

def test(dbName, password, confirmPassword, *frameL):
	if len(dbName) == 0 or len(password) == 0 or len(confirmPassword) == 0:
		tkMessageBox.showinfo("Invalid Information","Invalid User Name or Password\nPlease try again")
	elif password != confirmPassword:
		tkMessageBox.showinfo("Invalid Information","Invalid User Name or Password\nPlease try again")
		for f in frameL:
			f.destroy()
		register_frame()
	else:
		for f in frameL:
			f.destroy()
		login_frame()	
		tkMessageBox.showinfo("Account created","Successfully create account\nPlease log in ")
		print "testing"	

def option_frame(dbName):
	"""Section to define OPTION frame"""
	raise_frame(option)
	Button(option, text='Song List', command=lambda:songList_frame(dbName)).grid(row=1, column=0, padx=20, pady=20)
	Button(option, text='Playlist').grid(row=1, column=1, padx=10) 
	Button(option, text='Quit', command=lambda:raise_frame(login)).grid(row=10)
	
def songList_frame(dbName):
	"""Section to define LIST OF SONGS frame"""
	raise_frame(songList)
	songListC = Frame(songList)
	songListC1 = Frame(songList)
	songListC.pack(fill=BOTH, expand="true", padx=10)
	songListC1.pack(side=BOTTOM)
	scrollbar = Scrollbar(songListC)
	myList = Listbox(songListC, yscrollcommand = scrollbar.set)
	try: 
		db = connectDB(dbName)
		cursor = db.cursor()
	### query song list	
		sql = "select * from songs order by name;"
		cursor.execute(sql) 
		results = cursor.fetchall()	
		for row in results:
			myList.insert(END, str(row[1]))
		myList.pack(side = LEFT, fill=BOTH, expand = "true",padx=2,pady=10)
		scrollbar.pack(side = RIGHT, fill=Y, pady=10)
		scrollbar.config(command = myList.yview)
		db.commit()
	except:
		db.rollback()
		tkMessageBox.showinfo("Cannot query database")
	db.close()
	Button(songListC1, text='Back', command=lambda:raise_and_destroy_frame(dbName, option_frame,songListC, songListC1)).pack(side = LEFT, padx=2)
	Button(songListC1, text='Play', command=lambda:play_song(dbName, myList, songListC, songListC1)).pack(side=LEFT, padx=40)
	Button(songListC1, text='Add to\nPlaylist', command=lambda:add_play_list(dbName, myList)).pack(side = LEFT)

def check_query(dbName, table, column_number, value):
	db = connectDB(dbName)
	cursor = db.cursor()
	sql = "select * from %s;" % table	
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		if value == str(row[column_number]):
			db.close()
			return False
	db.close()
	return True

def add_play_list(dbName, songlist):
	addSong = songlist.get(songlist.curselection())
	if (addSong):
		if check_query(dbName, "playlist", 1, addSong):
			db = connectDB(dbName)
			cursor = db.cursor()
			sql = "insert into playlist (name) value ('%s');" % addSong
 			cursor.execute(sql)
			db.commit()
			db.close()
			tkMessageBox.showinfo("MySQL Success","Song is successfully added into playlist")
		else:
			tkMessageBox.showinfo("MySQL Error","Selected Song is already in the playlist")
	else:
		tkMessageBox.showinfo("Invalid Selection","Please choose a song to add to playlist") 

def play_song(dbName, songlist, *frame):
	try:
		playingSong = songlist.get(songlist.curselection())
		#test = playingSong
		if (playingSong):
		#	conn = S3Connection(access_key, secret_key)
		#	bucket = conn.get_bucket('sjsu195db1')
		#	key = bucket.get_key(playingSong)
		#	key.get_contents_to_filename('/home/duc/Desktop/test_folder/'+playingSong)
			for f in frame:
				f.destroy()
			playSong_frame(dbName, playingSong)
	except:
		tkMessageBox.showinfo("Invalid Selection","Please choose a song from the list")

def playSong_frame(dbName, song):
	raise_frame(playSong)
	playSongC = Frame(playSong)
	playSongC.pack(fill=BOTH, expand="true", padx=10)
	Label(playSongC, text=song).pack(side=LEFT)
	Button(playSongC, text='Back', command=lambda:raise_and_destroy_frame(dbName,songList_frame,playSongC)).pack(side = LEFT)

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
Label(login).grid(row=0,rowspan=2, pady=10)
Label(login, text = "Welcome to airSound - The Streaming Speaker").grid(row=2,columnspan=2, ipadx=15)
Label(login, text= "Please sign in").grid(row=3,columnspan=2,pady=10)
#Label(login, text = "Welcome to airSound - The Streaming Speaker\n\nPlease sign in\n").grid(rowspan=2,columnspan=2, row=2)
Label(login, text="User Name:").grid(row=4)
Label(login, text="Password:").grid(row=5)
Label(login).grid(row=6,rowspan=2)

userdbNameTF = Entry(login)
passwordTF = Entry(login, show="*")

userdbNameTF.grid(row=4, column=1)
passwordTF.grid(row=5, column=1)

Button(login, text='Sign In', command=authenticate).grid(sticky=E,row=8,column = 0, pady=4)

Button(login, text='Register', command=register_frame).grid(row=8,column = 1, pady=4)


mainloop()
