import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.put_image()


    def put_image(self, path = "test.jpeg"):
        #image = ImageTk.PhotoImage(Image.open(path))
        #label = tk.Label(image=image)
        #label.image = image
        #label.pack(side="bottom")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        pre_image = Image.open(path)
        self.image = ImageTk.PhotoImage(pre_image)

        self.canvas = Canvas(self.master, bg="blue")
        self.canvas.pack(expand='true', fill='both')

        self.canvas.create_image(0, 0, anchor=NW, image=self.image)

        #self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.bind("<Left>",  lambda event: self.canvas.xview_scroll(-1, "units"))
        self.canvas.bind("<Right>", lambda event: self.canvas.xview_scroll( 1, "units"))
        self.canvas.bind("<Up>",    lambda event: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Down>",  lambda event: self.canvas.yview_scroll( 1, "units"))
        self.canvas.focus_set()
        self.canvas.bind("<1>", lambda event: self.canvas.focus_set())
        self.canvas.configure(xscrollincrement='20')


root = tk.Tk()
app = Application(master=root)
app.mainloop()
