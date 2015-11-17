def hashkey(password):
	key = 0
	for c in password:
		key += ord(c) % 16
	print key

hashkey("root")
