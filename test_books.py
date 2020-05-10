import requests
import json
import pytest
from .api import get_parsed_body

# Тесты на возврат 200:
# *обязательное поле - bibkeys - List of IDs to request the information. The API supports ISBNs, LCCNs, OCLC numbers and OLIDs (Open Library IDs).
# + Проверка разных айдишников (разных библиотечных систем)
# + Тест на проверку пустого поля bibkeys.
# - Проверка, что при запросе разных айдишников, выдаётся разная инфа.
# format - Optional parameter which specifies the response format. Possible values are json and javascript. The default format is javascript.
# callback - Optional parameter which specifies the name of the JavaScript function to call with the result. This is considered only when the format is javascript.
# jscmd - Optional parameter to decide what information to provide for each matched bib_key. Possible values are viewapi and data. The default value is viewapi.
#
# Разбить на разные тесты? Вынести подготовку данных в отдельные файлы?
# Тест отрицательный: с помощью параметризации убедиться, что каждый из запросов выше, если передаёт неверное значение, не возвращает 200. См. пример из статьи по тестированию с данными.


class TestBibkeys():
    def test_get_the_book_with_bibkeys_ISBN(self):
        response = requests.get(
            "https://openlibrary.org/api/books?bibkeys=ISBN:0451526538")
        assert response.status_code == 200, "Status code is wrong, expected 200, got {}".format(
            response.status_code)
# Сделать эти тесты через фикстуру? Параметризацию?

    def test_get_the_book_with_bibkeys_LCCN(self):
        response = requests.get(
            "https://openlibrary.org/api/books?bibkeys=LCCN:96072233")
        assert response.status_code == 200, "Status code is wrong, expected 200, got {}".format(
            response.status_code)

    def test_get_the_book_with_bibkeys_OCLC(self):
        response = requests.get(
            "https://openlibrary.org/api/books?bibkeys=OCLC:36792831")
        assert response.status_code == 200, "Status code is wrong, expected 200, got {}".format(
            response.status_code)

    def test_get_the_book_with_bibkeys_OLIDs(self):
        response = requests.get(
            "https://openlibrary.org/api/books?&bibkeys=OLID:OL123M")
        assert response.status_code == 200, "Status code is wrong, expected 200, got {}".format(
            response.status_code)

    def test_get_the_book_bibkeys_empty(self):
        response = requests.get("https://openlibrary.org/api/books?bibkeys=")
        assert response.status_code == 200, "Status code is wrong, expected 200, got {}".format(
            response.status_code)

    # @pytest.mark.dev
    @pytest.mark.parametrize('search_key1, search_key2', [("ISBN:0451526538", "ISBN:0385472579"), ("LCCN:96072233", "LCCN:86072233"), ("OCLC:36792831", "OCLC:297222669"), ("OLID:OL123M", "OLID:OL124M")])
    def test_get_different_books(self, search_key1, search_key2):
        first_book = get_parsed_body(
            f"https://openlibrary.org/api/books?bibkeys={search_key1}&format=json")
        second_book = get_parsed_body(
            f"https://openlibrary.org/api/books?bibkeys={search_key2}&format=json")
        assert first_book[search_key1]["bib_key"] != second_book[search_key2]["bib_key"], "Books are the same, should be different"

    # @pytest.mark.dev
    @pytest.mark.parametrize('search_key', ["ISBN:0451526538", "LCCN:96072233", "OCLC:36792831", "OLID:OL123M"])
    def test_get_the_right_book(self, search_key):
        book = get_parsed_body(
            f"https://openlibrary.org/api/books?bibkeys={search_key}&format=json")
        assert book[search_key]["bib_key"] == search_key, 'Got the wrong book'


def test_get_the_book_wrong_request():
    response = requests.get(
        "https://openlibrary.org/api/book?bibkeys=ISBN:0451526538")
    assert response.status_code == 404, "Status code is wrong, expected 404, got {}".format(
        response.status_code)


def test_get_the_book_jscmd_data():
    response = requests.get(
        "https://openlibrary.org/api/books?bibkeys=ISBN:0451526538&jscmd=data")
    assert response.status_code == 200, "Status code is wrong, expected 200, got {}".format(
        response.status_code)
