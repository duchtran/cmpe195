from Tkinter import *
import tkMessageBox
import Image
import base64
import boto
import boto.s3.connection
from boto.s3.connection import S3Connection
from boto.s3.connection import Location
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
import os
import re 
try:
    # Python2
    import Tkinter as tk
    from urllib2 import urlopen
except ImportError:
    # Python3
    import tkinter as tk
    from urllib.request import urlopen

"""Section to define global variables"""
access_key = ''
secret_key = ''
image_url = "https://s3-us-west-1.amazonaws.com/sjsudb1/Ambassador-75x75.png"
image_byt = urlopen(image_url).read()
image_b64 = base64.encodestring(image_byt)
#path = "/home/ductran/Dropbox/Ambassador-75x75.png"
#path1= "/home/duc/Dropbox/Ambassador-75x75.png"
sdir = "/home/ductran/Dropbox/songs"
sdir_mac = "/home/duc/Dropbox/songs" 
plist = []

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
	Label(option, text="Filter:").grid(row=5, column=0, columnspan=4) 
	Label(option, text="Genre:").grid(row=6, column=1) 
	var1 = StringVar(option)
	var2 = StringVar(option)
	t = []
	get_list(dbName, t)
	genre = []
	artist = [] 
	for song in t:
		genre_flag = 1
		artist_flag = 1
		for index in range (len(genre)):
			if song[2] == genre[index]:
				genre_flag = 0
		if (genre_flag):
			genre.append(song[2])
		for index in range (len(artist)):
			if song[1] == artist[index]:
				artist_flag = 0
		if (artist_flag):
			artist.append(song[1]) 
	menu1= [''] 
	for row in genre:
		menu1.append(row)
	var1.set(menu1[0])
	genre = OptionMenu(option, var1, *menu1)
	genre["width"]=15
	genre.grid(row=6,column=2) 
	Label(option, text="Artist:").grid(row=7, column=1) 
	menu2= [''] 
	for row in artist:
		menu2.append(row)
	var2.set(menu2[0])
	artist = OptionMenu(option, var2, *menu2)
	artist["width"]=15
	artist.grid(row=7,column=2) 
	Button(option, text='Song List', command=lambda:songList_frame(dbName, t), width=36).grid(row=3, column=0, columnspan=4, padx=2)
	Button(option, text='Playlist', command=lambda:playlist_frame(dbName, t),width=36).grid(row=4, column=0, columnspan=4, padx=2) 
	Button(option, text='Filter', command=lambda:filter_frame(dbName, t, var1.get(), var2.get())).grid(row=6, column=3, rowspan=2) 
	Button(option, text='Quit', command=lambda:raise_frame(login)).grid(row=10, columnspan=4)

	
def songList_frame(dbName, t):
	"""Section to define LIST OF SONGS frame"""
	raise_frame(songList)
	songListC = Frame(songList)
	songListC1 = Frame(songList)
	songListC.pack(fill=BOTH, expand="true", padx=10)
	songListC1.pack(side=BOTTOM)
	scrollbar = Scrollbar(songListC)
	myList = Listbox(songListC, yscrollcommand = scrollbar.set)
	try: 
		for row in t:
			myList.insert(END, str(row[0]))
		myList.pack(side = LEFT, fill=BOTH, expand = "true",padx=1,pady=10)
		scrollbar.pack(side = RIGHT, fill=Y, pady=10)
		scrollbar.config(command = myList.yview)
	except:
		tkMessageBox.showinfo("Connection Error", "Cannot query database")
	Button(songListC1, text='Back\nto Lists', command=lambda:raise_and_destroy_frame(dbName, option_frame,songListC, songListC1)).pack(side = LEFT, padx=1)
	Button(songListC1, text='Play', command=lambda:play_song(dbName, t, myList, songListC, songListC1)).pack(side=LEFT, padx=1)
	Button(songListC1, text='Add to\nPlaylist', command=lambda:add_play_list(dbName, myList)).pack(side = LEFT, padx=1)
	Button(songListC1, text='Add\nsong', command=lambda:raise_and_destroy_frame1(dbName, t, adding_frame,songListC, songListC1)).pack(side = LEFT, padx=1)
	Button(songListC1, text='Delete', command=lambda:delete_songlist(dbName, myList,songList_frame, songListC, songListC1)).pack(side = LEFT)

def playlist_frame(dbName, t):
	"""Section to define LIST OF SONGS frame"""
	raise_frame(playlist)
	playlistC = Frame(playlist)
	playlistC1 = Frame(playlist)
	playlistC.pack(fill=BOTH, expand="true", padx=10)
	playlistC1.pack(side=BOTTOM)
	scrollbar = Scrollbar(playlistC)
	myList = Listbox(playlistC, yscrollcommand = scrollbar.set)
	try: 
		plist.sort()
		for row in plist:
			myList.insert(END, row)
		myList.pack(side = LEFT, fill=BOTH, expand = "true",padx=2,pady=10)
		scrollbar.pack(side = RIGHT, fill=Y, pady=10)
		scrollbar.config(command = myList.yview)
	except:
		tkMessageBox.showinfo("Connection Error", "Cannot query database")
	Button(playlistC1, text='Back\nto Lists', command=lambda:raise_and_destroy_frame(dbName, option_frame,playlistC, playlistC1)).pack(side = LEFT, padx=2)
	Button(playlistC1, text='Play', command=lambda:play_song(dbName, t, myList, playlistC, playlistC1)).pack(side=LEFT, padx=40)
	Button(playlistC1, text='Delete\nfrom Playlist', command=lambda:delete_playlist(dbName, t, myList,playlist_frame, playlistC,playlistC1)).pack(side=LEFT, padx=2)

def adding_frame(dbName, t):
	"""Section to define LIST OF SONGS frame"""
	raise_frame(adding)
	addingC = Frame(adding)
	addingC1 = Frame(adding)
	addingC.pack(fill=BOTH, expand="true", padx=10)
	addingC1.pack(side=BOTTOM)
	scrollbar = Scrollbar(addingC)
	myList = Listbox(addingC, yscrollcommand = scrollbar.set)
	try: 
		for file in os.listdir(sdir):
			file = file[:-4]
			myList.insert(END, file)
		myList.pack(side = LEFT, fill=BOTH, expand = "true",padx=2,pady=10)
		scrollbar.pack(side = RIGHT, fill=Y, pady=10)
		scrollbar.config(command = myList.yview)
	except:
		tkMessageBox.showinfo("Connection Error", "Cannot query database")
	Button(addingC1, text='Back', command=lambda:raise_and_destroy_frame1(dbName, t, songList_frame,addingC, addingC1)).pack(side = LEFT, padx=2)
	Button(addingC1, text='Continue', command=lambda:continue_function(dbName, t, myList,addingC,addingC1)).pack(side=LEFT, padx=40)


def addingSong_frame(dbName, t, addSong):
	"""Section to define frame"""
	raise_frame(addingSong)		
	addingSongC = Frame(addingSong)
	addingSongC1 = Frame(addingSong)
	addingSongC.grid() 
	addingSongC1.grid()
	Label(addingSongC, text="Please enter information for the song").grid(row=0, pady=25, columnspan=2)
	Label(addingSongC, text="Song Adding:").grid(row=1,column=0, padx=10) 
	Label(addingSongC, text=addSong).grid(row=1,column=1, padx=10) 
	Label(addingSongC, text="Genre:").grid(row=2,column=0, padx=10)
	Label(addingSongC, text="Artist:").grid(row=3,column=0, padx=10)
	genreTF = Entry(addingSongC)
	artistTF = Entry(addingSongC)
	####
	genreTF.grid(row=2, column=1, padx=10)
	artistTF.grid(row=3,column=1, padx=10)
	####
	Button(addingSongC1, text='Cancel', command=lambda:raise_and_destroy_frame1(dbName,t, adding_frame,addingSongC, addingSongC1)).pack(side = LEFT, padx=2)
	Button(addingSongC1, text='Add', command=lambda:add_function(dbName, addSong,genreTF.get(),artistTF.get(), adding_frame, addingSongC, addingSongC1)).pack(side=RIGHT,padx=30,pady=10)

def filter_frame(dbName, t, var1, var2):
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
		results = []	
		try: 
			if (var1 != '') and (var2 == ''): 
				for row in t:
					if var1 == row[2]:
						results.append(row[0])
			elif (var1 =='') and (var2 != ''):
				for row in t:
					if var2 == row[1]:
						results.append(row[0])
			elif (var1 != '') and (var2 != ''):
				for row in t:
					if var1 == row[2] and var2 == row[1]:
						results.append(row[0])
			results.sort()
			for row in results:
				myList.insert(END,row)
			myList.pack(side = LEFT, fill=BOTH, expand = "true",padx=2,pady=10)
			scrollbar.pack(side = RIGHT, fill=Y, pady=10)
			scrollbar.config(command = myList.yview)
		except:
			tkMessageBox.showinfo("Connection Error", "Cannot query database")
		Button(filteringC1, text='Back\nto Lists', command=lambda:raise_and_destroy_frame(dbName, option_frame,filteringC, filteringC1)).pack(side = LEFT, padx=2)
		Button(filteringC1, text='Play', command=lambda:play_song(dbName, t, myList, filteringC, filteringC1)).pack(side=LEFT, padx=40)


def playSong_frame(dbName, t, song, xlist, index, size):
	raise_frame(playSong)
	playSongC = Frame(playSong)
	playSongC.grid() 
	global img
	vol = [10]
	Index = [index]
	nextIndex = [(index + 1 ) % size]
	canvas = Canvas(playSongC, width=50, height=50, bg='blue')
	canvas.grid(row=0, column=0)
	img = PhotoImage(data = image_b64)
	canvas.create_image(0,0, anchor=NW, image=img) 
	m = Label(playSongC, text=song)
	m.grid(row=0, column=1, columnspan=2)
	uri = song_process(dbName, t, song)
	#creates a playbin (plays media form an uri) 
	player = gst.element_factory_make("playbin", "player")
	#set the properties
	player.set_property('uri', uri)  # songs
	player.set_property('volume', 1.0)  # volume
	player.set_state(gst.STATE_PLAYING)
	Button(playSongC, text='Stop', command=lambda:stop(player)).grid(row=1,column=0)
	Button(playSongC, text='Play / Resume', command=lambda:play(player)).grid(row=1,column=1)
	Button(playSongC, text='Pause', command=lambda:pause(player)).grid(row=1,column=2)
	Label(playSongC, text='Volume').grid(row=3, column=0, columnspan=3)
	l = Label(playSongC, text=vol[0])
	l.grid(row=4, column=1)
	Button(playSongC, text='-', width=5, command=lambda:decrease_vol(player,vol, l)).grid(row=4, column=0)
	Button(playSongC, text='+', width=5, command=lambda:increase_vol(player,vol, l)).grid(row=4, column=2) 
	Label(playSongC, text='Next song: ').grid(row=5, column=0)
	n = Label(playSongC, text=xlist[nextIndex[0]])
	n.grid(row=5, column=1)
	Button(playSongC, text='Go', width=5, command=lambda:play_next(dbName, t, player, xlist, Index, size, nextIndex, m, n)).grid(row=5, column=2) 

	Button(playSongC, text='Song List', width=36, command=lambda:raise_and_destroy_frame_stop(dbName, t, player, songList_frame,playSongC)).grid(row=10, column=0, columnspan=3, padx=4)
	Button(playSongC, text='Playlist', width=36, command=lambda:raise_and_destroy_frame_stop(dbName, t, player, playlist_frame,playSongC)).grid(row=11, column=0, columnspan=3, padx=4)

###############
"""Section to define functions"""
def get_list(bName, t):
	conn = boto.s3.connect_to_region('us-west-1', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
#	conn = S3Connection(access_key, secret_key)
	bucket = conn.get_bucket(bName)
	for key in bucket:
		s = str(key).split(",")[1].split("-")
		s[2] = s[2][:-1]
		t.append(s)

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
                init = password[0]
                try:
                        log = False
                        conn = S3Connection(access_key, secret_key)
                        dbName = userdbName+'-'+str(hashkey)+'-'+init
                        try:
                                bucket = conn.get_bucket(dbName)
                                option_frame(dbName)
                        except:
                                passwordTF.delete(0,END)
                                tkMessageBox.showinfo("Invalid Information","Invalid User Name or Password\nPlease try again")
                except:
                        tkMessageBox.showinfo("Invalid Action","Cannot connect to database")

def raise_frame(frame):
	frame.tkraise() 

def raise_and_destroy_frame(dbName,frame,*frameL):
	for f in frameL:
		f.destroy()
	frame(dbName)

def raise_and_destroy_frame1(dbName,t,frame,*frameL):
	for f in frameL:
		f.destroy()
	frame(dbName, t)

def raise_and_destroy_frame_stop(dbName,t, player,frame,*frameL):
	player.set_state(gst.STATE_NULL)	
	for f in frameL:
		f.destroy()
	frame(dbName, t)

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
		try:
			hashkey = 0
			for c in password:
				hashkey += ord(c) % 16
			init = password[0]
			bName = dbName+'-'+str(hashkey)+'-'+init 
			conn = boto.s3.connect_to_region('us-west-1', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
			try:
				conn.create_bucket(bName, location='us-west-1')	
			except:	
				tkMessageBox.showinfo("Account Error","Username is already used.")
		except: 
			tkMessageBox.showinfo("Account Error","Username is already used.")
		for f in frameL:
			f.destroy()
		login_frame()	
			
def add_play_list(dbName, songlist):
	addSong = songlist.get(songlist.curselection())
	if (addSong):
		if (addSong in plist):
			tkMessageBox.showinfo("MySQL Error","Selected Song is already in the playlist")
		else:
			plist.append(addSong)
			tkMessageBox.showinfo("MySQL Success","Song is successfully added into playlist")
	else:
		tkMessageBox.showinfo("Invalid Selection","Please choose a song to add to playlist") 
			

def continue_function(dbName, t, songlist, *frame):
	try:
		match = False
		addSong = songlist.get(songlist.curselection())
		for row in t:
			if addSong == row[0]: 
				match = True
		if (not (match) and addSong):
			for f in frame:
				f.destroy()
			addingSong_frame(dbName, t, addSong)
		elif (match):
			tkMessageBox.showinfo("Invalid Action","Selected song is already in database") 
	except:
		tkMessageBox.showinfo("Invalid Selection","Please choose a song from the list")

def add_function(dbName, addSong, genre, artist, frame, *frameL):
	try: 
		bName = dbName
		sPath = '/home/ductran/Dropbox/songs/'+addSong+'.mp3'
		conn = boto.s3.connect_to_region('us-west-1', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
		#conn = S3Connection(access_key, secret_key)
		bucket = conn.get_bucket(bName)
		### Upload file ###
		k = Key(bucket)
		song = addSong+'-'+artist+'-'+genre
		k.key = song
		k.set_contents_from_filename(sPath)
		alc = bucket.get_key(song)
		alc.set_canned_acl('public-read') 
		tkMessageBox.showinfo("Successful Action","Song is added to database")
		t = []
		get_list(dbName,t)	
		for f in frameL:
			f.destroy()
		frame(dbName,t)
	except:
		tkMessageBox.showinfo("Invalid Action","Fail to add song")

def play_song(dbName, t, songlist, *frame):
	try:
		playingSong = songlist.get(songlist.curselection())
		index = songlist.curselection()[0]
		size =  songlist.size()
		xlist = list(songlist.get(0,END))
		if (playingSong):
			for f in frame:
				f.destroy()
			playSong_frame(dbName, t, playingSong, xlist, index, size)
	except:
		tkMessageBox.showinfo("Invalid Selection","Please choose a song from the list")

def stop(player):
	player.set_state(gst.STATE_NULL)	

def play(player):
    player.set_state(gst.STATE_PLAYING)

def pause(player):
    player.set_state(gst.STATE_PAUSED)

def play_next(dbName, t, player, xlist, Index, size, nextIndex, label1, label2):
	player.set_state(gst.STATE_NULL)
	uri = song_process(dbName, t, xlist[nextIndex[0]])
	player.set_property('uri', uri)
	label1['text'] = xlist[nextIndex[0]]
	Index[0] = nextIndex[0]
	nextIndex[0] = (nextIndex[0] + 1) % size
	label2['text'] = xlist[nextIndex[0]]
	player.set_state(gst.STATE_PLAYING)

def song_process(dbName, t, song):
	for row in t:
		if song == row[0]:	
			title = re.sub(r' ','+',song)	
			if title: 
				artist = re.sub(r' ','+',row[1])
				genre = re.sub(r' ','+',row[2]) 
	uri = 'https://s3-us-west-1.amazonaws.com/'+dbName+'/'+title+'-'+artist+'-'+genre
	return uri

def increase_vol(player, vol, label):
	if (vol[0] < 20): 
		vol[0] += 1
		player.set_property('volume', vol[0] / 10.0)
		label['text'] = vol[0]
	else:
		tkMessageBox.showinfo("Invalid Action","Maximum volume reached")
	

def decrease_vol(player, vol, label):
	if (vol[0] > 0): 
		vol[0] -= 1
		player.set_property('volume', vol[0] / 10.0)
		label['text'] = vol[0]
	else:
		tkMessageBox.showinfo("Invalid Action","Minimum volume reached")

def delete_playlist(dbName, t, songlist, frame, *frameL):
	deleteSong = songlist.get(songlist.curselection()) 
	if (deleteSong):
		try:
			plist.remove(deleteSong)
			for f in frameL:
				f.destroy()
			frame(dbName, t)
		except:
			tkMessageBox.showinfo("Invalid Selection","Please choose a song to delete from playlist") 
			
def delete_songlist(dbName, songlist, frame, *frameL):
	deleteSong = songlist.get(songlist.curselection()) 
	if (deleteSong):
		try:
			d = []
			get_list(dbName,d)
			for row in d:
				if deleteSong == row[0]:
					dSong = row[0]+'-'+row[1]+'-'+row[2]
					conn = boto.s3.connect_to_region('us-west-1', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
					#conn = S3Connection(access_key, secret_key)
					bucket = conn.get_bucket(dbName)
					bucket.delete_key(dSong)
			n = []
			get_list(dbName,n)
			for f in frameL:
				f.destroy()
			frame(dbName,n)
		except:
			tkMessageBox.showinfo("Invalid Selection","Please choose a song to delete from Song list") 


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
adding = Frame(root)
addingSong = Frame(root)
frames = [login, option, songList, playlist, playSong, register, filtering, adding, addingSong]
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
