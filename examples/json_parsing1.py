from json import JSONDecodeError
import requests
from pygments.lexers import find_lexer_class_by_name

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)

try:
    parsed_response_text = response.json()
    print(parsed_response_text["answer"])
except JSONDecodeError:
    print("Answer not in JSON format")
finally:
    pass