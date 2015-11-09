from Tkinter import *
from inspect import *

class Application(Frame):
	"""A GUI application with three buttons"""
	
	def __init__(self, master):
		"""The GUI will be create in the init, call functions to add more things"""	
		Frame.__init__(self, master)
		self.grid()
		self.createLabel("This is a label")
		self.clickCount = 0
		self.createButton("This is a lazy button", self.countingEvenly)
		self.createButton("Click: 0", self.increment)

	def createButton (self, buttonStr, command):
		""" Create a button """
		self.button = Button(self, text = buttonStr)
		self.button.grid()
		self.button["command"] = command
	
	def increment(self):
		self.clickCount += 1
		self.button["text"] = "Click: " + str(self.clickCount)
 
	def countingEvenly(self):
		""" Update command in a button """
		self.clickCount += 2
		self.button["text"] = "Click: " + str(self.clickCount)
		

	def createLabel(self, labelStr):
		label = Label(self, text = labelStr)
		label.grid()

root = Tk()
root.title("airSound - The Streaming Speaker")
root.geometry("324x240")
	
app = Application(root)

root.mainloop()	
