import json
import urllib.request

def request(action, **params):
    """ Return object used to request something from Anki.
    """
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    """ Perform an action and get response from Anki.
    """
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
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

def create_deck(deck_name, model_file_path):
    """ Create new deck on Anki, with given fields and CSS/HTML configuration.
    """
    # get data object with JSON
    model_data = dict()
    with open(model_file_path, "r") as f:
        model_data = json.load(f)
    return invoke('createModel', modelName = model_data[0], inOrderFields = model_data[1],\
           css = model_data[2], cardTemplates = model_data[3])

    #return invoke('createDeck', deck=deck_name)
#create_deck("test1")
print(create_deck("ediscendus", "data/model.json"))
