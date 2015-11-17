#!/usr/bin/python

import MySQLdb
username = "airsound"
password = "pi"

initpw = 0
for c in password:
	initpw += ord(c) % 16
authen = [username, initpw, password[0]]

try:
	db = MySQLdb.connect("localhost", "root", "theking88", "testing")
except:
	print 'Cannot connect to database!'

cursor = db.cursor()
sql = """select * from authentication;"""
try:
	log = False
	database = ""
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		valid = 0
		for i in range (0,3):
			print row[i], 
			if (authen[i] == row[i]):
				valid += 1
		if (valid == 3):
			log = True
			break
	if log:
		sql = """use %s;""" % authen[0]
		cursor.execute(sql)
		print "\nLog in with username: %s" % authen[0]
		db.commit()
	else: 
		print "\nInvalid Username or Password"
except:		
	db.rollback()	
db.close()

