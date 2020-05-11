import requests
import json

BASE_URL = "https://openlibrary.org/api/books"
JAVASCRIPT_FORMAT = 'var'

def get_json_body(url):
    return requests.get(url).json()

def get_text(url):
    return requests.get(url).text