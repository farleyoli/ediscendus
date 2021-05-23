from PIL import ImageTk, Image, ImageOps
import os

class ImageManager:
    # naming convention: ediscendus_{{book_name}}_{{page_number}}.jpg
    def __init__(self, app):
        self.app = app
        self.added_cards = app.anki.invoke('getMediaFilesNames')
        self.last_loaded_card = self.get_last_loaded()
        #print(self.get_last_loaded())
        #print(self.added_cards)

    def get_last_loaded(self, upperlimit = 10000):
        for i in range(1, upperlimit):
            if "ediscendus_{}_{}.jpg".format(self.app.id, i) not in self.added_cards:
                return i-1
        return upperlimit

    def send_image_to_anki(self, page_number):
        raw_image = self.app.open_image(page_no=page_number)
        filepath = "temp/ediscendus_{}_{}.jpg".format(self.app.id, page_number)
        filename = "ediscendus_{}_{}.jpg".format(self.app.id, page_number)
        raw_image.save(filepath)
        self.app.anki.send_multimedia(filename, filepath)
        os.remove(filepath)

    def sync_images(self, offset = 5):
        # TODO: instead of last page visited, do it based on last card added
        last = self.app.last_visited_page
        print("last = {}".format(last))
        for i in range(1, last+1+offset):
            name = "ediscendus_{}_{}.jpg".format(self.app.id, i)
            if name not in self.added_cards:
                self.send_image_to_anki(i)
                print("Added page #{}".format(i))
                self.added_cards.append(name)
