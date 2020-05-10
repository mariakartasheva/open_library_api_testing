import requests
import json
import pytest
from .api import get_parsed_body

class TestBibkeys():
    @pytest.mark.dev
    @pytest.mark.parametrize('bib_key', ["ISBN:0451526538", "LCCN:96072233", "OCLC:36792831", "OLID:OL123M"])
    def test_get_the_book_by_bibkeys(self, bib_key):
        response = requests.get(
            f"https://openlibrary.org/api/books?bibkeys={bib_key}")
        assert response.status_code == 200, "Status code is wrong, expected 200, got {}".format(
            response.status_code)

    def test_get_the_book_bibkeys_empty(self):
        response = requests.get("https://openlibrary.org/api/books?bibkeys=")
        assert response.status_code == 200, "Status code is wrong, expected 200, got {}".format(
            response.status_code)

    # @pytest.mark.dev
    @pytest.mark.parametrize('bib_key1, bib_key2', [("ISBN:0451526538", "ISBN:0385472579"), ("LCCN:96072233", "LCCN:86072233"), ("OCLC:36792831", "OCLC:297222669"), ("OLID:OL123M", "OLID:OL124M")])
    def test_get_different_books(self, bib_key1, bib_key2):
        first_book = get_parsed_body(
            f"https://openlibrary.org/api/books?bibkeys={bib_key1}&format=json")
        second_book = get_parsed_body(
            f"https://openlibrary.org/api/books?bibkeys={bib_key2}&format=json")
        assert first_book[bib_key1]["bib_key"] != second_book[bib_key2]["bib_key"], "Books are the same, should be different"

    # @pytest.mark.dev
    @pytest.mark.parametrize('bib_key', ["ISBN:0451526538", "LCCN:96072233", "OCLC:36792831", "OLID:OL123M"])
    def test_get_the_right_book(self, bib_key):
        book = get_parsed_body(
            f"https://openlibrary.org/api/books?bibkeys={bib_key}&format=json")
        assert book[bib_key]["bib_key"] == bib_key, 'Got the wrong book'


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
