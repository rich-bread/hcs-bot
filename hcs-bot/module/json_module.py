import json

def open_json(name):
    #path = ''
    path = './hcs-bot/'
    f = open(path+name, 'r', encoding='utf-8_sig')
    data = json.load(f)
    
    return data