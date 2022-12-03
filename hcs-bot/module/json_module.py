import json

def open_json(name):
    path = ''
    f = open(path+name, 'r', encoding='utf-8_sig')
    data = json.load(f)
    
    return data