from requests import Response
import json.decoder


class BaseCase:
    # Делаем проверку на наличие запрашиваемых полей, и если проверка-assert проходит успешно, то с помощью оператора return возвращаем данные поля из ответа
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with the name {headers_name} in the last response"
        return response.headers[headers_name]

# Здесь благодаря знакомой конструкции работы с возможными ошибками try-except мы учитываем случай, если вдруг в ответе нам придёт текст не в json-формате (мы уже делали подобное ранее). Если отрабатывает except (т.е. в try-блоке у нас вываливается ошибка декодирования json), то в except мы повесили маяк-ориентировку (исключение JSONDecoderError) для поимки именно подобной ошибки и в assert сразу же вписываем False (т.к. у нас уже всё равно ошибка вывалена и мы её без проверок на условия уже сразу заасертим (т.е. тест упадёт в любом случае в этом assert, если код пойдёт в данной конструкции по дорожке except, после неуспеха в try) с понятной пометкой об ошибке. Без данного отлова ошибок, данный случай бы вылетел у нас без обозначения причины ошибки. А так, слабое место мы укрепили и зафиксировали.

# Дальше, если отработал try (т.е. парсинг прошёл успешно (а значит в ответе пришёл json-format)), то идёт проверка в assert на наличие искомого поля в нём. И если уже проверка проходит также успешно, то с помощью оператора return возвращаем данное искомое поле, которое мы извлекли из ответа
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response in not in JSON-format. Response text is '{response.text}'"

        assert name in response_as_dict, "Response JSON does not have key '{name}'"
        return response_as_dict[name]



