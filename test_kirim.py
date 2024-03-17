import requests

url = "http://127.0.0.1:5000/API/get_chat"

data = {}
respon = requests.post(url, data=data)
print(respon.text)