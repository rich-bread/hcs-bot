import json, requests

url = 'https://script.google.com/macros/s/AKfycbxDLAqusUpAJAn5a1rzuF8QnFIg93eCl017byBb_1H8w6uR8XTtl_LU1WnEBMqxa6_O9w/exec'+'?'

#DBへのPOST処理
async def post_db(param, data):
    uurl = url + f'param={param}'
    output = requests.post(uurl, data=json.dumps(data))
    return output

#DBへのGET処理
async def get_db(param, table, subjectID):
    payload = {'param': param, 'table': table, 'subjectID': subjectID}
    output = requests.get(url, params=payload)
    return output
