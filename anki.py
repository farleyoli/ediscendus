import json, urllib.request, os

class Anki:
    def __init__(self, deck_name = "ediscendus", model_name = "ediscendus_model"):
        """ Initializes Anki object, savind the name of the models and the decks available
        on the current session of Anki, so it doesn't have to be retrieved all the time.
        """
        self.model_names = self.invoke('modelNames')
        self.deck_names = self.invoke('deckNames')
        if model_name not in self.model_names:
            self.create_model(model_name)
        if deck_name not in self.deck_names:
            self.create_deck(deck_name)

    def request(self, action, **params):
        """ Return object used to request something from Anki.
        """
        return {'action': action, 'params': params, 'version': 6}

    def invoke(self, action, **params):
        """ Perform an action and get response from Anki.
        """
        requestJson = json.dumps(self.request(action, **params)).encode('utf-8')
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']

    def create_deck(self, deck_name):
        """ Create new deck on Anki.
        """
        if deck_name in self.deck_names:
            return "The deck with this name already exists."
        return self.invoke('createDeck', deck = deck_name)



    def create_model(self, model_name, model_file_path = "data/model.json"):
        """ Create new model on Anki, with fields/configuration retrieved from file mode_file_path.
        """
        if model_name in self.model_names:
            return "The model with this name already exists."
        with open(model_file_path, "r") as f:
            model_data = json.load(f)
        return self.invoke('createModel', modelName = model_data[0], inOrderFields = model_data[1],\
               css = model_data[2], cardTemplates = model_data[3])

    def add_card(self, model_name, deck_name, question, page_number, coordinates, book_id, extra = ""):
        if model_name not in self.model_names or deck_name not in self.deck_names:
            return "Error"
        note = {
            "deckName": deck_name,
            "modelName": model_name,
            "fields": {
                "question": question,
                "page_number": page_number,
                "coordinate": coordinates,
                "book_id": book_id,
                "extra": extra
            }
        }
        return self.invoke('addNote', note = note)

    def send_multimedia(self, filename, relative_path):
        path = os.path.abspath(relative_path)
        return self.invoke('storeMediaFile', filename=filename, path=path)
#anki = Anki()
#print(anki.send_multimedia('temp/ediscendus_test.jpg'))
#print(anki.add_card('ediscendus_model', 'Default', 'test', 'test', 'test'))
