from collections import defaultdict

class CardManager():
    """ This class contains code to manage cards to be added to Anki and their
    corresponding highlights to be rendered to user.
    """
    def __init__(self, app, pointers = None, highlights = None, ID = None):
        """ Initialize main variables.
        """
        self.app = app
        self.pointers, self.highlights, self.id = pointers, highlights, ID
        if not pointers:
            self.pointers = defaultdict(set) # self.pointers[i] will contain a list of pointers to highlights in page i
        if not highlights:
            self.highlights = dict()
        if not ID:
            self.id = 0

    def add_card(self, page_number, y, question = "", comments = ""):
        """ Takes coordinates, questions and comments for a card and add them
        to the pointers and highlights data-structures.
        """
        self.id += 1
        last_page_number, max_y = self.get_last_highlight(page_number)
        if last_page_number == page_number:
            if max_y < y:
                self.pointers[page_number].add(self.id)
                self.highlights[self.id] = [last_page_number, max_y+1, page_number, y, question, comments]
        else:
            for pn in range(last_page_number, page_number+1):
                self.pointers[pn].add(self.id)
            self.highlights[self.id] = [last_page_number, max_y+1, page_number, y, question, comments]

        self.app.canvas.pack_forget()
        self.app.put_image()

    def get_last_highlight(self, page_number):
        """ Get coordinates of last highlighted part of document, so new
        highlight can continue from there.
        """
        last_page_number = page_number
        while last_page_number >= 2 and len(self.pointers[last_page_number]) == 0:
            last_page_number -= 1

        #t = [y1 for _, _, _, y1 in self.highlights[hln] for hln in self.pointers[last_page_number]]
        t = [self.highlights[hln] for hln in self.pointers[last_page_number]]
        t = [y1 for _, _, _, y1, _, _ in t]
        max_y = max(t) if len(t) > 0 else 0

        return last_page_number, max_y
