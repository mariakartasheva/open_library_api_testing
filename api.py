import requests
import json

base_url = "https://openlibrary.org/api/books"
javascript_format = 'var'

def get_parsed_body(url):
    return requests.get(url).json()

def get_text(url):
    return requests.get(url).text