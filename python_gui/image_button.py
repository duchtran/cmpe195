from Tkinter import *
root=Tk()
b=Button(root,justify = LEFT)
photo=PhotoImage(file="/home/duc/Dropbox/cmpe195_repository/python_gui/images/play_button.gif")
b.config(image=photo,width="100",height="100")
b.pack(side=LEFT)
root.mainloop()
