class ImageManager:
    # naming convention: ediscendus_{{book_name}}_{{page_number}}.jpg
    def __init__(self, app):
        self.app = app
        self.added_cards = app.anki.invoke('getMediaFilesNames')
        self.last_loaded_card = self.get_last_loaded()
        print(self.get_last_loaded())
        #print(self.added_cards)

    def get_last_loaded(self, upperlimit = 10000):
        for i in range(1, upperlimit):
            if "ediscendus_{}_{}.jpg".format(self.app.id, i) not in self.added_cards:
                return i-1
        return upperlimit

    def add_image(self, page_number):
        pass
