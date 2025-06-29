import requests


response = requests.get("https://playground.learnqa.ru/api/check_type/", params={"param1": "value1"})
print(response.text)

post_response = requests.post("https://playground.learnqa.ru/api/check_type/", data={"post_param1": "post_value1"})
print(post_response.text)