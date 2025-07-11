
'''
* Чтобы запустить работу имеющихся тестов в проекте, пропишем команду запуска тестов в Pytest в терминале -> python -m pytest test_examples.py -k "test_check_math"

* -k -> вызываем по ключу отдельный тест "test_check_math"

* assert -> Оператор, который производит проверку на соответствие. В данном случае стоит проверка того, равно ли a (5) + b (9) четырнадцати ("==" проверка на равность). Выражение за assert должно быть типа boolean как и в проверке условия. То есть в результате должно быть Истина (True) или Ложь (False). Когда в результате истина, то тест считается пройденным успешно

* В одном тесте (который начинается со слова def) может быть и огромное множество проверок на соответствие через команды assert. Но если хоть в одном из них будет False, то и в результате всему тесту выдаст False
 '''
class TestExample:
    def test_check_math(self):
        a = 5
        b = 6
        assert a + b == 11
        assert a == 55, f"Ожидаем увидеть 55, а не {a}" # Когда тестов много, либо на будущее, можно добавить текст ошибки к каждому assert. И в случае, если данный assert вывалится с ошибкой, то любому человеку будет более понятна проблема, если в тексте это будет подробно описано
        assert b == 6 and b - a == 1


    # def test_check_math2(self):
    #     a = 11
    #     b = 6
    #     assert a + b == 8
