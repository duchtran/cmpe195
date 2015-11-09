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

# create a label
label1 = Label(app, text = "This is the label")
label1.grid(row=0,column=0)	# put the label on grid to show it

#the order of the frame will be based on this one
label2 = Label(app)
label2["text"] = "Second label"
label2.grid(row=0,column=1)

# 1st way to create a button with text
button1 = Button(app, text = "First")
button1.grid(row=1, column=0)

# 2nd way to write text in a button 
button2 = Button(app)
button2.configure(text = "Second")
button2.grid(row=1,column=1)

# 3rd way to write text in a button
button3 = Button(app)
button3["text"] = "Third"
button3.grid(row=1,column=2)

#kick of the event loop
#scrollbar = Scale(app,orient=HORIZONTAL, length=320)
#scrollbar.grid(row=2,column=0)
root.mainloop()
