import json
import urllib.request

class Anki:
    def __init__(self):
        """ Initializes Anki object, savind the name of the models and the decks available
        on the current session of Anki, so it doesn't have to be retrieved all the time.
        """
        self.model_names = self.invoke('modelNames')
        self.deck_names = self.invoke('deckNames')

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



    def create_model(self, model_name, model_file_path):
        """ Create new model on Anki, with fields/configuration retrieved from file mode_file_path.
        """
        if model_name in self.model_names:
            return "The model with this name already exists."
        with open(model_file_path, "r") as f:
            model_data = json.load(f)
        return self.invoke('createModel', modelName = model_data[0], inOrderFields = model_data[1],\
               css = model_data[2], cardTemplates = model_data[3])
