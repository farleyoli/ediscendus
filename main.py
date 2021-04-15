import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image, ImageOps

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        #self.pack()
        self.curr_img_path = "test.jpeg"
        self.zoom_rate = 0.9
        self.create_widgets()

    def create_widgets(self):
        zoom_frame = Frame(self.master)
        zoom_out_button = Button(zoom_frame, text="Zoom Out", command=self.zoom_out_image)
        zoom_in_button = Button(zoom_frame, text="Zoom In", command=self.zoom_in_image)
        zoom_out_button.grid(row=0, column=0)
        zoom_in_button.grid(row=0, column=1)
        zoom_frame.pack()
        self.put_image()

    def put_image(self):
        raw_image = self.get_raw_image()
        self.image = ImageTk.PhotoImage(raw_image)

        self.canvas = Canvas(self.master, bg="blue")
        self.canvas.pack(expand='true', fill='both')
        #screen_width = root.winfo_screenwidth()
        #screen_height = root.winfo_screenheight()
        self.canvas.create_image(0, 0, anchor=NW, image=self.image)

        self.bind_keys()

    def zoom_out_image(self):
        if self.zoom_rate >= 0.5:
            self.zoom_rate -= 0.1
        self.canvas.pack_forget()
        self.put_image()

    def zoom_in_image(self):
        if self.zoom_rate <= 1.5:
            self.zoom_rate += 0.1
        self.canvas.pack_forget()
        self.put_image()

    def get_raw_image(self):
        raw_image = Image.open(self.curr_img_path)

        w = raw_image.width
        h = raw_image.height

        if self.zoom_rate:
            w *= self.zoom_rate
            h *= self.zoom_rate
            w, h = int(w), int(h)

        raw_image = ImageOps.fit(raw_image, (w, h))
        return raw_image

    def bind_keys(self):
        self.canvas.bind("<Left>",      lambda event: self.canvas.xview_scroll(-1, "units"))
        self.canvas.bind("<h>",         lambda event: self.canvas.xview_scroll(-1, "units"))
        self.canvas.bind("<Right>",     lambda event: self.canvas.xview_scroll( 1, "units"))
        self.canvas.bind("<l>",         lambda event: self.canvas.xview_scroll( 1, "units"))
        self.canvas.bind("<Up>",        lambda event: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<k>",         lambda event: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Down>",      lambda event: self.canvas.yview_scroll( 1, "units"))
        self.canvas.bind("<j>",         lambda event: self.canvas.yview_scroll( 1, "units"))
        self.canvas.bind("<1>",         lambda event: self.canvas.focus_set())
        self.canvas.bind("<Shift-K>",   lambda event: self.zoom_in_image())
        self.canvas.bind("<Shift-J>",   lambda event: self.zoom_out_image())
        self.canvas.focus_set()
        self.canvas.configure(xscrollincrement='20')
        self.canvas.configure(yscrollincrement='40')


root = tk.Tk()
app = Application(master=root)
app.mainloop()
