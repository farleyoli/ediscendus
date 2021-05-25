from collections import defaultdict

class CardManager():
    """ This class contains code to manage cards to be added to Anki and their
    corresponding highlights to be rendered to user.
    """
    def __init__(self, app, pointers = None, highlights = None, ID = None, id_added_cards = None):
        """ Initialize main variables.
        """
        self.app = app
        self.pointers, self.highlights, self.id, self.id_added_cards = pointers, highlights, ID, id_added_cards
        if not pointers:
            self.pointers = defaultdict(set) # self.pointers[i] will contain a list of pointers to highlights in page i
        if not highlights:
            self.highlights = dict()
        if not ID:
            self.id = 0
        if not id_added_cards:
            self.id_added_cards = []

    def add_highlight(self, page_number, y, question = "", comments = "", height = 1000):
        """ Takes coordinates, questions and comments for a card and add them
        to the pointers and highlights data-structures.
        """
        self.id += 1
        last_page_number, max_y = self.get_last_highlight(page_number)
        if last_page_number == page_number:
            if max_y < y:
                self.pointers[page_number].add(self.id)
                self.highlights[self.id] = [last_page_number, max_y+1, page_number, y, question, comments, height]
        else:
            for pn in range(last_page_number, page_number+1):
                self.pointers[pn].add(self.id)
            self.highlights[self.id] = [last_page_number, max_y+1, page_number, y, question, comments, height]

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
        t = [y1 for _, _, _, y1, _, _, _ in t]
        max_y = max(t) if len(t) > 0 else 0
        return last_page_number, max_y

    def add_highlight_to_anki(self, idx):
        if idx not in self.highlights or idx in self.id_added_cards:
            return None
        if len(self.highlights[idx][-3]) == 0:
            return None
        #self.highlights[self.id] = [last_page_number, max_y+1, page_number, y, question, comments, height]
        question = self.highlights[idx][4]
        page_number = str(self.highlights[idx][0])
        x, y = 100*self.highlights[idx][1]/self.highlights[idx][-1], 100*self.highlights[idx][3]/self.highlights[idx][-1]
        xpage, ypage = str(self.highlights[idx][0]), str(self.highlights[idx][2])
        coordinates = "{}@{}#{}@{}".format(xpage, x, ypage, y)
        card_id = str(self.app.id) + "_" + str(idx)
        self.app.anki.add_card(card_id, book_id=self.app.id, question=question, page_number=page_number, coordinates=coordinates)
        self.id_added_cards.append(idx)

    def sync_highlights(self):
        for key in self.highlights:
            self.add_highlight_to_anki(key)
