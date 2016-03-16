from Tkinter import *
import tkMessageBox
import MySQLdb
import Image
import boto
import boto.s3.connection
from boto.s3.connection import S3Connection
from boto.s3.key import Key
# sudo apt-get install python-pip python-dev build-essential
# sudo pip install --upgrade pip
# sudo pip install --upgrade virtualenv
# sudo pip install boto
# pip install boto3
import pygst
pygst.require("0.10")
import gst
#sudo apt-get install python-gst0.10 gstreamer0.10-plugins-good
#sudo apt-get install python-gst0.10 gstreamer0.10-plugins-ugly 

"""Section to define global variables"""
access_key = ''
secret_key = ''
mysql_pass = ''
##########
"""Section to define frames"""
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
	Button(registerC1, text='Register', command=lambda:register_work(regUserdbNameTF.get(), regPasswordTF.get(), confirmRegPasswordTF.get(), registerC, registerC1)).pack(side=RIGHT,padx=30,pady=10)



def option_frame(dbName):
	"""Section to define OPTION frame"""
	raise_frame(option) 
	Label(option).grid(row=0) # empty row in GUI
	Label(option, text='OPTIONS').grid(row=1, columnspan=4) # empty row in GUI
	Label(option).grid(row=2) # empty row in GUI
	Button(option, text='Song List', command=lambda:songList_frame(dbName), width=36).grid(row=3, column=0, columnspan=4, padx=2)
	Button(option, text='Playlist', command=lambda:playlist_frame(dbName),width=36).grid(row=4, column=0, columnspan=4, padx=2) 
	Label(option, text="Filter:").grid(row=5, column=0, columnspan=4) 
	Label(option, text="Genre:").grid(row=6, column=1) 
	var1 = StringVar(option)
	var2 = StringVar(option)
	menu1= [''] 
	results1 = query_group(dbName, 'genre', 'songs', 'genre', 'genre')
	for row in results1:
		menu1.append(row[0])
	var1.set(menu1[0])
	genre = OptionMenu(option, var1, *menu1)
	genre["width"]=15
	genre.grid(row=6,column=2) 
	Label(option, text="Artist:").grid(row=7, column=1) 
	menu2= [''] 
	results2 = query_group(dbName, 'artist', 'songs', 'artist', 'artist')
	for row in results2:
		menu2.append(row[0])
	var2.set(menu2[0])
	artist = OptionMenu(option, var2, *menu2)
	artist["width"]=15
	artist.grid(row=7,column=2) 
	Button(option, text='Filter', command=lambda:filter_frame(dbName, var1.get(), var2.get())).grid(row=6, column=3, rowspan=2) 
	Button(option, text='Quit', command=lambda:raise_frame(login)).grid(row=10, columnspan=4)

	
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
		results = query_list(dbName, 'songs')
		for row in results:
			myList.insert(END, str(row[1]))
		myList.pack(side = LEFT, fill=BOTH, expand = "true",padx=2,pady=10)
		scrollbar.pack(side = RIGHT, fill=Y, pady=10)
		scrollbar.config(command = myList.yview)
	except:
		tkMessageBox.showinfo("Connection Error", "Cannot query database")
	Button(songListC1, text='Back\nto Lists', command=lambda:raise_and_destroy_frame(dbName, option_frame,songListC, songListC1)).pack(side = LEFT, padx=2)
	Button(songListC1, text='Play', command=lambda:play_song(dbName, myList, songListC, songListC1)).pack(side=LEFT, padx=5)
	Button(songListC1, text='Add to\nPlaylist', command=lambda:add_play_list(dbName, myList)).pack(side = LEFT, padx=5)
	Button(songListC1, text='Add song').pack(side = LEFT)

def playlist_frame(dbName):
	"""Section to define LIST OF SONGS frame"""
	raise_frame(playlist)
	playlistC = Frame(playlist)
	playlistC1 = Frame(playlist)
	playlistC.pack(fill=BOTH, expand="true", padx=10)
	playlistC1.pack(side=BOTTOM)
	scrollbar = Scrollbar(playlistC)
	myList = Listbox(playlistC, yscrollcommand = scrollbar.set)
	try: 
		results = query_list(dbName, 'playlist')
		for row in results:
			myList.insert(END, str(row[1]))
		myList.pack(side = LEFT, fill=BOTH, expand = "true",padx=2,pady=10)
		scrollbar.pack(side = RIGHT, fill=Y, pady=10)
		scrollbar.config(command = myList.yview)
	except:
		tkMessageBox.showinfo("Connection Error", "Cannot query database")
	Button(playlistC1, text='Back\nto Lists', command=lambda:raise_and_destroy_frame(dbName, option_frame,playlistC, playlistC1)).pack(side = LEFT, padx=2)
	Button(playlistC1, text='Play', command=lambda:play_song(dbName, myList, playlistC, playlistC1)).pack(side=LEFT, padx=40)
	Button(playlistC1, text='Delete\nfrom Playlist', command=lambda:delete_playlist(dbName, myList,playlist_frame, playlistC,playlistC1)).pack(side=LEFT, padx=2)

def filter_frame(dbName, var1, var2):
	"""Section to define FILTER frame"""
	if (var1 == '') and (var2 == ''):
		tkMessageBox.showinfo("Invalid Option","Please choose a criteria to filter")
	else:
		raise_frame(filtering)
		filteringC = Frame(filtering)
		filteringC1 = Frame(filtering)
		filteringC.pack(fill=BOTH, expand="true", padx=10)
		filteringC1.pack(side=BOTTOM)
		scrollbar = Scrollbar(filteringC)
		myList = Listbox(filteringC, yscrollcommand = scrollbar.set)
		try: 
			if (var1 != '') and (var2 == ''):
				results = query_list_where(dbName, 'name', 'songs', 'genre', var1)
			elif (var1 =='') and (var2 != ''):
				results = query_list_where(dbName, 'name', 'songs', 'artist', var2) 
			elif (var1 != '') and (var2 != ''):
				results = query_list_where2(dbName, 'name','songs', 'genre', var1, 'artist', var2)	
			for row in results:
				myList.insert(END, str(row[0]))
			myList.pack(side = LEFT, fill=BOTH, expand = "true",padx=2,pady=10)
			scrollbar.pack(side = RIGHT, fill=Y, pady=10)
			scrollbar.config(command = myList.yview)
		except:
			tkMessageBox.showinfo("Connection Error", "Cannot query database")
		Button(filteringC1, text='Back\nto Lists', command=lambda:raise_and_destroy_frame(dbName, option_frame,filteringC, filteringC1)).pack(side = LEFT, padx=2)
		Button(filteringC1, text='Play', command=lambda:play_song(dbName, myList, filteringC, filteringC1)).pack(side=LEFT, padx=40)

path = "/home/ductran/Dropbox/Ambassador-75x75.png"

def playSong_frame(dbName, song):
	raise_frame(playSong)
	playSongC = Frame(playSong)
	playSongC.grid() 
	global img
	vol = [3]
	canvas = Canvas(playSongC, width=50, height=50, bg='blue')
	canvas.grid(row=0, column=0)
	#img = PhotoImage(file = "/home/ductran/Dropbox/Ambassador-75x75.png")
	img = PhotoImage(file = "/home/duc/Dropbox/Fireball_50x50.png")
	canvas.create_image(0,0, anchor=NW, image=img)

	Label(playSongC, text=song).grid(row=0, column=1, columnspan=2)
	title = re.sub(r' ','+',song)	
	uri = 'https://s3-us-west-1.amazonaws.com/sjsu'+dbName+'/'+title
	#creates a playbin (plays media form an uri) 
	player = gst.element_factory_make("playbin", "player")
	#set the properties
	player.set_property('uri', uri)  # songs
	player.set_property('volume', 3.0)  # volume
	player.set_state(gst.STATE_PLAYING)
	Button(playSongC, text='Stop', command=lambda:stop(player)).grid(row=1,column=0)
	Button(playSongC, text='Play', command=lambda:play(player)).grid(row=1,column=1)
	Button(playSongC, text='Pause', command=lambda:pause(player)).grid(row=1,column=2)
	Label(playSongC, text='Volume:').grid(row=3, column=1)
	Button(playSongC, text='-', width=5, command=lambda:decrease_vol(player,vol)).grid(row=3, column=0)
#	volumeTF = Entry(playSongC, width=10)
#	volumeTF.grid(row=3, column=1)
	Button(playSongC, text='+', width=5, command=lambda:increase_vol(player,vol)).grid(row=3, column=2)
	Button(playSongC, text='Song List', width=36, command=lambda:raise_and_destroy_frame_stop(dbName,player, songList_frame,playSongC)).grid(row=4, column=0, columnspan=3, padx=4)
	Button(playSongC, text='Playlist', width=36, command=lambda:raise_and_destroy_frame_stop(dbName,player, playlist_frame,playSongC)).grid(row=5, column=0, columnspan=3, padx=4)

###############
"""Section to define functions"""

def connectDB(dbName):
	db = MySQLdb.connect("localhost", "root", mysql_pass, dbName)
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

def raise_and_destroy_frame_stop(dbName,player,frame,*frameL):
	player.set_state(gst.STATE_NULL)	
	for f in frameL:
		f.destroy()
	frame(dbName)

def cancel_and_return(frame, *frameL):
	for f in frameL:
		f.destroy()	
	frame()
def register_work(dbName, password, confirmPassword, *frameL):
	if len(dbName) == 0 or len(password) == 0 or len(confirmPassword) == 0:
		tkMessageBox.showinfo("Invalid Information","Invalid User Name or Password\nPlease try again")
	elif password != confirmPassword:
		tkMessageBox.showinfo("Invalid Information","Invalid User Name or Password\nPlease try again")
		for f in frameL:
			f.destroy()
		register_frame()
	else:
	###register code ###	
		print "testing"	
		try:
			hashkey = 0
			for c in password:
				hashkey += ord(c) % 16
			authen = [dbName, hashkey, password[0]]
			print authen
			db = connectDB("AUTHENTICATION")
			cursor = db.cursor()
			sql_account_authen = "insert into authentication values ('%s',%d,'%s');" % (authen[0], authen[1], authen[2])
			sql_createDB = "create database %s;" %dbName
			sql_useDB = "use %s;" %dbName
			if (cursor.execute(sql_account_authen)):
				cursor.execute(sql_createDB)
				cursor.execute(sql_useDB)
				tkMessageBox.showinfo("Account Created","Successfully create account\nPlease log in ")
			else:
				db.rollback()
				tkMessageBox.showinfo("Account Error","Username is already used.")
		except: 
			tkMessageBox.showinfo("Account Error","Username is already used.")
		for f in frameL:
			f.destroy()
		login_frame()	
			
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
		if (playingSong):
		#	conn = S3Connection(access_key, secret_key)
		#	bucket = conn.get_bucket('sjsu'+dbName)
		#	key = bucket.get_key(playingSong)
		#	key.get_contents_to_filename('/home/duc/Desktop/test_folder/'+playingSong)
			for f in frame:
				f.destroy()
			playSong_frame(dbName, playingSong)
	except:
		tkMessageBox.showinfo("Invalid Selection","Please choose a song from the list")

def stop(player):
	player.set_state(gst.STATE_NULL)	

def play(player):
    player.set_state(gst.STATE_PLAYING)

def pause(player):
    player.set_state(gst.STATE_PAUSED)

def play_next( player, new_uri ):
    player.set_state(gst.STATE_NULL)
    player.set_property('uri', new_uri )
    play()

def increase_vol(player, vol):
	if (vol[0] < 6): 
		vol[0] += 1
    		player.set_property('volume', vol[0])
	else:
		tkMessageBox.showinfo("Invalid Action","Maximum volume reached")
	

def decrease_vol(player, vol):
	if (vol[0] > 0): 
		vol[0] -= 1
    		player.set_property('volume', vol[0])
	else:
		tkMessageBox.showinfo("Invalid Action","Minimum volume reached")

def delete_playlist(dbName, songlist, frame, *frameL):
	deleteSong = songlist.get(songlist.curselection()) 
	if (deleteSong):
		try:
			sql= "delete from playlist where name = '%s';" % deleteSong
			db = connectDB(dbName)
			cursor = db.cursor()	
			cursor.execute(sql)
			db.commit()
			db.close()
			for f in frameL:
				f.destroy()
			frame(dbName)
		except:
			tkMessageBox.showinfo("Invalid Selection","Please choose a song to delete from playlist") 
			
def query_list(dbName, table):		
	sql = "select * from %s order by name;" % table
	db = connectDB(dbName)
	cursor = db.cursor()
	cursor.execute(sql) 
	results = cursor.fetchall()	
	return results

def query_list_where(dbName, column, table, place, condition):		
	sql = "select %s from %s where %s = \"%s\" order by name;" % (column, table, place,condition)
	db = connectDB(dbName)
	cursor = db.cursor()
	cursor.execute(sql) 
	results = cursor.fetchall()	
	return results
	
def query_list_where2(dbName, columns, table, place1, condition1, place2, condition2):		
	sql = "select %s from %s where %s = \"%s\" and %s = \"%s\" order by name;" % (columns, table, place1,condition1, place2, condition2)
	db = connectDB(dbName)
	cursor = db.cursor()
	cursor.execute(sql) 
	results = cursor.fetchall()	
	return results

def query_group(dbName, columns, table, group, order):
	sql = "select %s from %s group by %s order by %s;" % (columns, table, group, order)
	db = connectDB(dbName)
	cursor = db.cursor()
	cursor.execute(sql) 
	results = cursor.fetchall()	
	return results

#############
""" Section for frames creating"""
root = Tk()
root.title("airSound - The Streaming Speaker")
root.geometry("324x240")

login = Frame(root)
register = Frame(root)
option = Frame(root)
songList = Frame(root)
playlist = Frame(root)
playSong = Frame(root)
filtering = Frame(root)
frames = [login, option, songList, playlist, playSong, register, filtering]
for frame in frames:
	frame.grid(row=0, column=0, sticky='news')

login_frame()

"""Section for 'login' frame""" 
Label(login).grid(row=0,rowspan=2, pady=10)
Label(login, text = "Welcome to airSound - The Streaming Speaker").grid(row=2,columnspan=2, ipadx=15)
Label(login, text= "Please sign in").grid(row=3,columnspan=2,pady=10)
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
