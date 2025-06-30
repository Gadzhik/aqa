import requests
import pytest


class TestUserAuth:
    def test_auth_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        response1_pars = response1.json()

        assert "auth_sid" in response1.cookies, "There is no auth cookies in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF-token header in the response"
        assert "user_id" in response1_pars, "There is no user id in the response"

        auth_sid = response1.cookies.get("auth_sid")
        token = response1.headers.get("x-csrf-token")
        user_id_from_auth_method = response1_pars["user_id"]

        response2 = requests.get("https://playground.learnqa.ru/api/user/auth", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )
        response2_pars = response2.json()
        assert "user_id" in response2_pars, "There is no user id in the second response"
        user_id_from_check_method = response2_pars["user_id"]
        assert user_id_from_auth_method == user_id_from_check_method, "User id from auth method is no equal to user id from check method"

    '''
      Разбор кода запроса:
    • Импортируем requests. Создаём класс и в нём функцию теста. 
    • Создаём словарь data с данными для логина (те, которые бы мы вводили в авторизационные поля на сайте) email и password
    • Делаем запрос на API: /user/login с типом запросов post и отправляем в его теле нашу переменную data с email и password. Ответ сервера на запрос сохраняем в переменной response1
    • Парсим response1
    • Делаем 3 проверки assert-а. 1) наличие в куках ответа поля "auth_sid", 2) наличие в headers ответа поля x-csrf-token, 3) наличие user_id в ответе.
    • Затем, раз если это всё имеется, то сохраняем значения всех этих 3 полей под своими переменными, для того, чтобы подложить их под следующий авторизованный запрос
    # ------------------------------------------------------------------
    • Делаем второй запрос на API: user/auth типа get и отправляем в нём поле "x-csrf-token" в headers и поле "auth_sid" в куках с имеющимся у нас значениями из прошлого запроса. Ответ на данный запрос сохраняем в переменной response2
    • Парсим response2
    • Делаем проверку наличия поля user_id во втором ответе
    • Вынимаем значение данного user_id, пришедшего уже во втором ответе
    • Сравниваем id из первого и второго ответов
    '''

# негативный тест
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        response1_pars = response1.json()

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF-token header in the response"
        assert "user_id" in response1_pars, "There is no user id in the response"

        auth_sid = response1.cookies.get("auth_sid")
        token = response1.headers.get("x-csrf-token")
        if condition == "no_cookie":
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth", headers={"x-csrf-token": token})
        else:
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     cookies={"auth_sid": auth_sid})

        response2_pars = response2.json()
        assert "user_id" in response2_pars, "There is no user id in the second response"

        user_id_from_check_method = response2.json()["user_id"]

        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"




