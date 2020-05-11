import requests
import json
import pytest
from .api import get_parsed_body
from .api import get_text
from .api import base_url
from .api import javascript_format


class TestBasicCases():
    def test_get_the_book_wrong_request(self):
        response = requests.get(
            "https://openlibrary.org/api/book")
        assert response.status_code == 404, f"Expected status code for wrong request is 404, got {response.status_code}."

    def test_get_the_book_with_no_parameters(self):
        response = requests.get(base_url)
        assert response.status_code == 200, f"Status code for request with no parameters is wrong, expected 200, got {response.status_code}."

    def test_get_the_book_with_no_param_returns_default_format(self):
        response = get_text(base_url)
        assert response[0:3] == javascript_format, "Response format is wrong. Expected default response format to be javascript."


class TestBibKeys():
    @pytest.mark.parametrize('bib_key', ["ISBN:0451526538", "LCCN:96072233", "OCLC:36792831", "OLID:OL123M"])
    def test_get_the_book_by_bib_keys(self, bib_key):
        response = requests.get(
            f"{base_url}?bibkeys={bib_key}")
        assert response.status_code == 200, f"Status code for {bib_key} is wrong, expected 200, got {response.status_code}."

    def test_get_the_book_bib_keys_empty(self):
        response = requests.get(f"{base_url}?bibkeys=")
        assert response.status_code == 200, f"Status code is wrong. Empty bib_keys should return 200, got {response.status_code}."

    @pytest.mark.parametrize('bib_key1, bib_key2', [("ISBN:0451526538", "ISBN:0385472579"), ("LCCN:96072233", "LCCN:86072233"), ("OCLC:36792831", "OCLC:297222669"), ("OLID:OL123M", "OLID:OL124M"), ("ISBN:0451526538", "LCCN:86072233")])
    def test_get_different_books(self, bib_key1, bib_key2):
        first_book = get_parsed_body(
            f"{base_url}?bibkeys={bib_key1}&format=json")
        second_book = get_parsed_body(
            f"{base_url}?bibkeys={bib_key2}&format=json")
        assert first_book[bib_key1]["bib_key"] != second_book[bib_key2][
            "bib_key"], "Books in responses are the same, should be different."

    @pytest.mark.parametrize('bib_key', ["ISBN:0451526538", "LCCN:96072233", "OCLC:36792831", "OLID:OL123M"])
    def test_response_has_the_right_book(self, bib_key):
        book = get_parsed_body(
            f"{base_url}?bibkeys={bib_key}&format=json")
        response_bib_key = book[bib_key]["bib_key"]
        assert response_bib_key == bib_key, f'Got the wrong book: should be {bib_key}, got {response_bib_key}.'


class TestResponseFormat():
    @pytest.mark.parametrize('response_format', ['json', 'javascript', 'wrong', ''])
    def test_all_response_format_return_200(self, response_format):
        response = requests.get(
            f"{base_url}?bibkeys=ISBN:0451526538&format={response_format}")
        assert response.status_code == 200, f"Status code for {response_format} is wrong, expected 200, got {response.status_code}."

    @pytest.mark.parametrize('response_format', ['wrong', ''])
    def test_wrong_response_format_returns_default_format(self, response_format):
        response_format = get_text(
            f"{base_url}?bibkeys=ISBN:0451526538&format={response_format}")
        assert response_format[0:3] == javascript_format, "Response format is wrong. Expected default response format to be javascript."


class TestDataFormat():
    @pytest.mark.parametrize('data_format', ['viewapi', 'data', 'details'])
    def test_all_data_formats_return_200(self, data_format):
        response = requests.get(
            f"{base_url}?bibkeys=ISBN:0451526538&jscmd={data_format}")
        assert response.status_code == 200, f"Status code for {data_format} is wrong, expected 200, got {response.status_code}."

    def test_wrong_data_format_returns_200(self):
        response = requests.get(
            f"{base_url}?bibkeys=ISBN:0451526538&jscmd=test")
        assert response.status_code == 200, f"Expected status code for wrong data format is 200, got {response.status_code}."
