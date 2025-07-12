import pytest
import requests
# Подключим наш новый класс к тестам. В файле с тестом после имени класса с тестом в скобках пропишем имя класса BaseCase, а так как у нас его нет, то сделаем его импорт
from lib.base_case import BaseCase


class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        self.auth_sid - self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_auth_user(self):
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        response2_pars = response2.json()
        assert "user_id" in response2_pars, "There is no user id in the second response"
        user_id_from_check_method = response2_pars["user_id"]
        assert self.user_id_from_auth_method == user_id_from_check_method, "User id from auth method is no equal to user id from check method"

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={"x-csrf-token": self.token}
            )
        else:
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={"auth_sid": self.auth_sid}
            )

        response2_pars = response2.json()
        assert "user_id" in response2_pars, "There is no user id in the the second response"

        user_id_from_check_method = response2.json()["user_id"]

        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"