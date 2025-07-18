import requests

'''
Cookie - специальные файлы, которые создаёт Клиент (браузер, мобильное приложение и др.) на основе ответа Сервера. Они имеют срок годности, после которого они автоматически удаляются Клиентом.
• У каждого Cookie есть имя, значение и принадлежность к какому-либо домену. И каждый раз, когда К отправляет запрос С, он прикладывает все имеющиеся куки, которые у него есть для этого домена.
• Куки используются для разных целей, одна из главных - авторизация. Когда юзер входит на сайт без имеющихся кук, Сервер видит это и выдаёт в ответ страницу с регистрацией/логином. После ввода верных логина и пароля произойдёт авторизация и от Сервера Клиенту придут нужные куки, которые запомнит К и будет прикладывать их ко всем последующим запросам на данный домен, как карточку-спецпропуск по закрытому объекту. А Сервер на каждый запрос будет видеть этот пропуск и выдавать запрошенные ответы Клиенту

• Также куки нужны для запоминания информации о пользователе, например, проверки того, видел ли какой-либо баннер, страницу (чтобы вновь не показывать ему её), либо определённые интересы именно у этого юзера и т.д. И если очистить куки, то серфинг по сайту будет как с нуля
'''

# Извлекаем и "подкладываем" куки в каждый запрос
payload = {"login": "secret_login", "password": "secret_pass"}
response = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)

print(response.text)
print(response.status_code)
print(response.cookies)

'''
Текст нам не выдало никакой. Но код получили 200, а также видим куки, которые представлены в виде объекта (гугл: объекты python)
Объект похож на словарь, но более гибок. Переведём его в словарь для удобочитаемости в нашем случае с помощью функции dict
'''
print(dict(response.cookies))

# Отправим в теле запроса теперь неверный пароль и увидим, как в ответ придёт сообщение с ошибкой о том, что данные неверны
wrong_pass_payload = {"login": "secret_login", "password": "NO_secret_pass"}
response = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=wrong_pass_payload)

print(response.text)
print(response.status_code)
print(response.cookies)

'''
• Теперь из трёх принтов (print) мы наоборот получили текст с ошибкой, но на этот раз Сервер не выдал нам пропуск, потому что пароль неверный.

• Но статус всё равно 200, то есть обмен запросами с Сервером произошёл успешно
• Вернём правильный пароль и выведем headers. Полученный новый ответ посмотрим через сайт просмотра json и увидим, что в headers теперь есть новый параметр Set-Cookie
'''
payload_with_headers = {"login": "secret_login", "password": "secret_pass"}
response = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload_with_headers)

print(response.text)
print(response.status_code)
print(response.cookies)
print(response.headers)

'''
• Вытаскивать куки из заголовков не совсем удобно (есть более удобный способ), парсить большую строку и вытаскивать их оттуда. Для этого есть отдельный ключ в ответе cookies, где библиотека requests уже всё разложила "по полкам" (как уже мы делали в примерах ранее)
• Мы смогли получить нужную куку (в данном случае авторизационную). Теперь нужно научиться вставлять её в запросы. В тренажёре есть для этого ручка api/check_auth_cookie. В коде к коду с получением данной куки добавим код с отправкой на проверку в данную ручку полученную куку.
'''
payload_using_cookie_for_auth = {"login": "secret_login", "password": "secret_pass"}
response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload_using_cookie_for_auth)

cookie_value = response1.cookies.get("auth_cookie") # из переменной response1 в которую мы подсунули ответ Сервера на запрос по ручке получения куки мы извлекаем куки с ключем "auth_cookie" и вставляем в переменную cookie_value

cookies = {"auth_cookie": cookie_value} # формируем для стандартизированного параметра запросов в http (по библиотеке requests) параметр cookies переменную с аналогичным именем (можно и другое имя, но так удобнее). А именно, добавляем в его словарь #по ключу "auth_cookie" данные из переменной cookie_value

response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies) # формируем запрос на ручку, которая проверяет наличие куки. В параметр cookies отправляем наш словарь с кукой полученной из первого запроса, который мы вставили в переменную cookies

print(response2.text)

'''
• Когда мы отправляем неверные ключи (логин/пароль) для входа, то куки авторизации (пропуск) не приходят (параметр cookies пуст {}). Т.е. None. И дальше передавать его в запросы смысла нет. 
Поэтому добавим немного логики, которая будет проверять, что если кука не пришла, то не будем добавлять её в словарь под именем переменной cookies. Для этого создадим сразу переменную с пустым словарём, добавим логическую конструкцию с оператором if которая перед добавлением в неё имеющейся (полученной ранее) куки, проверит, а точно ли она есть, чтобы её добавлять сюда. Если же кука не пришла и в переменной cookies будет None, то делаем сразу новый запрос с пустой (без обновлений) cookies
'''
payload = {"login": "secret_login", "password": "NO_secret_pass"} # можно проверить и с secret_pass
response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)

cookie_value = response1.cookies.get("auth_cookie")

cookies = {}
if cookie_value is not None:
    cookies.update({"auth_cookie": cookie_value})
response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

print(response2.text)