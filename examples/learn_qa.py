import requests


payload = {"name": "Mike"}
response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
print(response.text)