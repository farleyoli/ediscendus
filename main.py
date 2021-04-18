import tkinter as tk
import card_manager
from tkinter import *
from PIL import ImageTk, Image, ImageOps
from collections import defaultdict
from tkinter import simpledialog
import pickle

class Application(tk.Frame):
    """ Main class.
    """
    def __init__(self, master=None):
        """ Initialize main variables which will be used throughout the program.
        """
        super().__init__(master)
        self.master = master
        self.load_state()
        #self.id = "test" # ID of the current opened document.
        #self.page_number = 1 # Which page is user reading?
        #self.zoom_rate = 1
        #self.img_x = 0  # Horizontal length of image
        #self.img_y = 0  # Vertical length of image
        #self.cards = card_manager.CardManager(self) # Ancillary class to add cards to document.
        self.create_widgets()

    def get_img_path(self):
        """ Returns path to image file.
        """
        return "{}{}.jpg".format(self.id, self.page_number)

    def create_widgets(self):
        """ Initialize program.
        """
        menu_frame = Frame(self.master)
        zoom_out_button = Button(menu_frame, text="Zoom Out", command=self.zoom_out_image)
        zoom_in_button = Button(menu_frame, text="Zoom In", command=self.zoom_in_image)
        page_back_button = Button(menu_frame, text="<<", command=self.page_back)
        page_fwd_button = Button(menu_frame, text=">>", command=self.page_forward)
        zoom_out_button.grid(row=0, column=2)
        zoom_in_button.grid(row=0, column=3)
        page_back_button.grid(row=0, column=0)
        page_fwd_button.grid(row=0, column=1)
        menu_frame.pack()
        self.put_image()

    def put_image(self):
        """ Load image and card highlights into canvas with correct zoom and
        other configurations.
        """
        raw_image = self.get_raw_image()
        self.image = ImageTk.PhotoImage(raw_image)

        self.canvas = Canvas(self.master, bg="blue")
        self.canvas.pack(expand='true', fill='both')
        self.canvas.create_image(0, 0, anchor=NW, image=self.image)

        self.canvas.configure(xscrollincrement='10')
        self.canvas.configure(yscrollincrement='40')
        self.bind_keys()
        self.render_highlights()
        #screen_width = root.winfo_screenwidth()
        #screen_height = root.winfo_screenheight()

    def zoom_out_image(self):
        """ Decreases zoom rate by 10%.
        """
        if self.zoom_rate >= 0.5:
            self.zoom_rate -= 0.1
            self.canvas.pack_forget()
            self.put_image()

    def zoom_in_image(self):
        """ Increases zoom rate by 10%.
        """
        if self.zoom_rate <= 1.5:
            self.zoom_rate += 0.1
            self.canvas.pack_forget()
            self.put_image()

    def get_raw_image(self):
        """ Gets raw image (before using ImageTk) with correct proportions.
        """
        raw_image = Image.open(self.get_img_path())

        w = raw_image.width
        h = raw_image.height

        if self.zoom_rate:
            w *= self.zoom_rate
            h *= self.zoom_rate
            w, h = int(w), int(h)
        self.img_x, self.img_y = w, h
        raw_image = ImageOps.fit(raw_image, (w, h))
        return raw_image

    def get_img_coordinates(self, event):
        """ Returns _image_ coordinates from mouse event.
        """
        x = int(self.canvas.canvasx(event.x) * (1/self.zoom_rate))
        y = int(self.canvas.canvasy(event.y) * (1/self.zoom_rate))
        return (x, y)

    def print_img_coordinates(self, event):
        """ Prints image coordinates from mouse event.
        """
        print(self.get_img_coordinates(event))

    def bind_keys(self):
        """ Binds keys to allow user commands.
        """
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
        self.canvas.bind("<Control-Button-1>", lambda event: self.cards.add_card(self.page_number, self.get_img_coordinates(event)[1]))
        self.canvas.bind("<Shift-Button-1>", lambda event: self.create_question_card(self.get_img_coordinates(event)[1]))
        self.canvas.bind("<Control-s>", lambda event: self.save_state())
        #self.canvas.bind('<Motion>', lambda event: self.print_img_coordinates(event))
        self.canvas.focus_set()

    def create_question_card(self, y):
        """ Create a card (with corresponding highlight) with a question
        prompted from the user.
        """
        question = simpledialog.askstring("", "Question:")
        self.cards.add_card(self.page_number, y, question)

    def insert_highlight(self, x0, y0, x1, y1):
        """ Takes coordinates of a highlight and loads it over image.
        """
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="black", stipple="gray25")

    def render_highlights(self):
        """ Takes datastructure from card_manager and use it to render
        highlights correctly in current image.
        """
        for hl_id in self.cards.pointers[self.page_number]:
            p0, y0, p1, y1, _, _ = self.cards.highlights[hl_id]
            if self.page_number != p0:
                y0 = 0
            if self.page_number != p1:
                y1 = self.img_y * (1/self.zoom_rate)

            self.insert_highlight(0, int(y0 * self.zoom_rate),
                                  self.img_x, int(y1 * self.zoom_rate))

    def page_forward(self):
        """ Increments page number and rerenders image.
        """
        self.page_number += 1
        self.canvas.pack_forget()
        self.put_image()

    def page_back(self):
        """ Decrements page number and rerenders image.
        """
        if self.page_number >= 2:
            self.page_number -= 1
            self.canvas.pack_forget()
            self.put_image()

    def save_state(self, path = "test.edi"):
        """ Save all relevant data from program to a file so that user can open
        it later.
        """
        with open(path, 'wb') as output:
            program_state = [self.id, self.page_number, self.zoom_rate, self.img_x, self.img_y, self.cards.pointers, self.cards.highlights, self.cards.id]
            pickle.dump(program_state, output, pickle.HIGHEST_PROTOCOL)

    def load_state(self, path = "test.edi"):
        """ Load all relevant data from program saved to a file before.
        """
        with open(path, 'rb') as inpt:
            program_state = pickle.load(inpt)
            self.id, self.page_number, self.zoom_rate, self.img_x, \
                self.img_y, pointers, highlights, cid = program_state
            self.cards = card_manager.CardManager(self, pointers, highlights, cid)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
