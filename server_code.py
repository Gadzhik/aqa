import requests


# 100-199 - информационные
# 200-199 - успех
# 300-399 - перенаправление
# 400-499 - ошибки клиента
# 500-599 - ошибки сервера

'''
Самые популярные из них:
200: успешный запрос
301: перенаправление на другой URL
403: ресурс запрещён для клиента
404: запрос на пустой URL
500: сервер не обработал запрос

В библиотеке requests есть параметр allow_redirects (True/False). Если стоит True, значит наш код будет позволять при тестах (при работе бота) редиректиться под капотом до тех пор, пока не дойдём до конечной точки.
'''
response = requests.get("https://playground.learnqa.ru/api/check_type/")
print(response.status_code)

print("**************500*****************")

get_500 = requests.get("https://playground.learnqa.ru/api/get_500/")
print(get_500.status_code)
print(get_500.text)

print("**************404*****************")

get_404 = requests.get("https://playground.learnqa.ru/api/blablabla/")
print(get_404.status_code)
print(get_404.text)

print("__________________Redirection___________________")

redirect_response = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
print(redirect_response.status_code)
print(redirect_response.text)
'''
Можно увидеть, как запросы пошли в одно место, получили ответ 301, перенаправился и пришёл в конечную точку и получил 200. И все остальные данные по ответу он оставляет и добавляет в переменную по последнему приходу к конечной точке.
'''
print("===================Redirection history====================")

using_history_in_response = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
first_response = using_history_in_response.history[0] # Так вот тут мы обращаемся к элементу массива (гугл: массив) истории под номер 0
second_response = using_history_in_response
print(first_response.url)
print(second_response.url)
