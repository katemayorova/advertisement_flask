import requests

response = requests.post('http://127.0.0.1:5000/advertisement',
                             json={'owner': 'Смирнов Михаил', 'header': 'Продам ноутбук', 'description': 'Б/у'},)
print(response.json())

response = requests.get('http://127.0.0.1:5000/advertisement/2')

print(response.status_code)
print(response.json())

response = requests.delete('http://127.0.0.1:5000/advertisement/4')

print(response.status_code)
print(response.json())

