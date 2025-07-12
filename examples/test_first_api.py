import requests
import pytest
from learn_qa import response


class TestFirstApi:
    names = [
        ("Mike"),
        ("Olga"),
        ()
    ] # добавили словарь с кортежами, содержащие имена

    @pytest.mark.parametrize("name", names) # довесили pytest-вое переопределение (как функциональная дообёртка) функции-тесту, которая добавляет новые возможности (прогонка значений указанных переменных). Переменной 'name' в ней будут подставляться значения из нашего словаря names
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        # name = "Mike" # удаляем (закоментируем) прошлое конкретизированное установление имени. Остальное остаётся прежним
        data = {"name": name}

        response = requests.get(url, params=data)
        assert response.status_code == 200, "Wrong response code"

        response_dict = response.json()
        assert "answer" in response_dict, "There is no field 'answer' in response"

        # ///
        if len(name) > 0: # добавили условие на проверку того, что имя имеет длинну > 0, т.е, что в имени имеются символы
            expected_response_text = f"Hello, {name}" # ждем в ответе строку с данным именем
        else:
            expected_response_text = "Hello, someone" # а иначе будем ожидать "someone"
        actual_response_text = response_dict["answer"]
        assert actual_response_text == expected_response_text, "Actual text in the response is not correct"

'''
• Импортируем requests
• Создаём класс в нём определяем тест с именем test_hello_call. self - добавляется как атрибут класса
• Выносим URL в переменную url
• Выносим имя в переменную
• Создаём словарь под именем data, в котором вставим параметр name и добавим ему нашу готовую переменную name ('Mike')
• Выполняем запрос по url и засылаем ему в параметры наш словарь data. Данные ответа сохраняем под именем переменной response
• Дальше создаём 3 проверки. Первый assert на проверку того, что запрос отработал корректно со статусом 200. И добавляем строку, которая появится, если assert отработает в False
• Второй assert проверяет, есть ли в ответе на запрос response поле answer. Делаем распарсивание
• А затем уже сверяем, соответствует ли содержимое данного ответа с нашим ожиданием. Создав перед этим 2 переменные с ожидаемым текстом в ответе и с тем, который пришёл в ответе expected_response_text и actual_response_text

• Запускаем тест с помощью команды python -m pytest test_first_api.py -k "test_hello_call"
'''

'''
Обратите внимание на строки:
1. f"Hello, {name}"
2. "Hello, someone"
В первом с буквой f. Она позволяет совать в строку динамические данные (переменные). Которые в любой момент времени в этом месте могут быть различными. В данном случае это переменная name
Во втором, что бы ни произошло, тут статика, а значит всегда будет именно эта строка символ-в-символ
'''

