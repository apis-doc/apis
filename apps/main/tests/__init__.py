# --*--*--*--*--*--*- Create by bh at 2023/10/4 10:34 -*--*--*--*--*--*--
import requests

res = requests.post('http://127.0.0.1:8000/apis/api/put/',
                    json={'code': '1', 'name': 'text', 'redirect': 'http://127.0.0.1:8000/apis/api'})

print(res.status_code)
