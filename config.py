import json


def loadConfig(path='config.json'):
    with open(path, 'r') as file:
        return json.load(file)
