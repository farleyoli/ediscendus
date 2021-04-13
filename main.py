import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image, ImageOps

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.curr_img_path = "test.jpeg"
        self.create_widgets()

    def create_widgets(self):
        self.put_image()


    def put_image(self, zoom_rate = None):
        raw_image = self.get_raw_image(0.7)
        self.image = ImageTk.PhotoImage(raw_image)

        self.canvas = Canvas(self.master, bg="blue")
        self.canvas.pack(expand='true', fill='both')
        self.canvas.create_image(0, 0, anchor=NW, image=self.image)

        self.bind_keys()

    def get_raw_image(self, zoom_rate):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        raw_image = Image.open(self.curr_img_path)

        w = raw_image.width
        h = raw_image.height

        if zoom_rate:
            w *= zoom_rate
            h *= zoom_rate
            w, h = int(w), int(h)

        raw_image = ImageOps.fit(raw_image, (w, h))
        return raw_image

    def bind_keys(self):
        self.canvas.bind("<Left>",  lambda event: self.canvas.xview_scroll(-1, "units"))
        self.canvas.bind("<h>",  lambda event: self.canvas.xview_scroll(-1, "units"))
        self.canvas.bind("<Right>", lambda event: self.canvas.xview_scroll( 1, "units"))
        self.canvas.bind("<l>", lambda event: self.canvas.xview_scroll( 1, "units"))
        self.canvas.bind("<Up>",    lambda event: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<k>",    lambda event: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Down>",  lambda event: self.canvas.yview_scroll( 1, "units"))
        self.canvas.bind("<j>",  lambda event: self.canvas.yview_scroll( 1, "units"))
        self.canvas.bind("<1>", lambda event: self.canvas.focus_set())
        self.canvas.focus_set()
        self.canvas.configure(xscrollincrement='20')


root = tk.Tk()
app = Application(master=root)
app.mainloop()
