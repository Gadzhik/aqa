import json


string_as_format = '{"answer": "Hello, User"}'
# распарсим в obj строку, которая лежит в переменной string_as_format
obj = json.loads(string_as_format)

key = "answer"

if key in obj:
    # выводим у json-объекта значение ключа answer. Мы обратились к ключу, и код вывел нам значение без самого ключа.
    print(obj[key])
else:
    print(f"Keyy {key} not in JSON")

